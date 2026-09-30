#!/usr/bin/env python3
"""
SOLUT - Generador de informes de logueo de sondaje a partir del registro ESKUAD.

Usa la ficha Word vigente de SOLUT como plantilla (se conserva su formato: portada,
antecedentes, control de revisiones, tablas, encabezado/pie, estilos) y reemplaza el
contenido con los datos del Excel exportado desde ESKUAD.

Uso:
  # 1) (opcional) descargar las fotos de cada muestra desde los enlaces de ESKUAD
  python sondajes_eskuad.py fotos --excel registro.xlsx --salida fotos/ [--token XXXX]

  # 2) generar el informe (si no hay fotos, deja un recuadro "FOTO PENDIENTE")
  python sondajes_eskuad.py informe --excel registro.xlsx --plantilla ficha.docx \
        --config config_S1.json --salida informe.docx [--fotos fotos/]

Dependencias:  pip install python-docx openpyxl pillow
"""
import argparse
import copy
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % W_NS
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


# --------------------------------------------------------------------------
# Lectura del registro ESKUAD
# --------------------------------------------------------------------------
def abrir_excel(ruta):
    """Abre el xlsx de ESKUAD. Su styles.xml trae colores no estandar ('white',
    'RRGGBB') que openpyxl rechaza; se normalizan en una copia temporal."""
    import openpyxl
    try:
        return openpyxl.load_workbook(ruta)
    except ValueError:
        pass
    tmp = tempfile.mkdtemp()
    fixed = os.path.join(tmp, "fixed.xlsx")
    with zipfile.ZipFile(ruta) as zi, zipfile.ZipFile(fixed, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in zi.infolist():
            data = zi.read(it.filename)
            if it.filename == "xl/styles.xml":
                s = data.decode("utf8")
                s = s.replace('rgb="white"', 'rgb="FFFFFFFF"')
                s = re.sub(r'rgb="([0-9A-Fa-f]{6})"', r'rgb="FF\1"', s)
                data = s.encode("utf8")
            zo.writestr(it, data)
    return openpyxl.load_workbook(fixed)


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def leer_registro(ruta_excel):
    """Devuelve (meta, muestras). Cada muestra es un dict con:
    n, de, hasta, spt (None | dict(n1,n2,n3,N)), desc, foto_url, avisos."""
    import warnings
    warnings.filterwarnings("ignore")
    ws = abrir_excel(ruta_excel).active
    meta = {"ubicacion_gps": None, "creado": None}
    reps = {}
    orden = []
    for row in ws.iter_rows():
        a, b = row[0], (row[1] if len(row) > 1 else None)
        if a.value is None:
            continue
        lab = str(a.value)
        if lab.strip() == "Fecha de Creación" and b is not None:
            meta["creado"] = str(b.value)
        if lab.strip() == "Ubicación" and b is not None:
            meta["ubicacion_gps"] = str(b.value)
        m = re.match(r"Sondaje / (.+?) \(Repetition (\d+)\)", lab)
        if not m:
            continue
        campo, n = m.group(1).strip(), int(m.group(2))
        if n not in reps:
            reps[n] = []
            orden.append(n)
        link = b.hyperlink.target if (b is not None and b.hyperlink) else None
        reps[n].append((campo, b.value if b is not None else None, link))

    muestras = []
    for n in orden:
        c = reps[n]
        nombres = [x[0] for x in c]
        esperado = ["DE", "HASTA", "MTRA. Nº", "DE", "A", "N1", "N2", "N3", "DE", "HASTA",
                    "Descripción General de la muestra", "Foto de la carrera"]
        if nombres != esperado:
            raise SystemExit("Repetición %d del Excel con campos inesperados: %s" % (n, nombres))
        v = [x[1] for x in c]
        muestras.append({
            "rep": n,
            "de": _num(v[0]), "hasta": _num(v[1]), "n": int(_num(v[2])) or n,
            "spt_de": _num(v[3]), "spt_a": _num(v[4]),
            "n1": int(_num(v[5])), "n2": int(_num(v[6])), "n3": int(_num(v[7])),
            "desc": (v[10] or "").strip(),
            "foto_url": c[11][2],
            "avisos": [],
        })
    _normalizar(muestras)
    return meta, muestras


def _normalizar(ms):
    """Define tramo definitivo y SPT de cada muestra, detectando inconsistencias de digitación."""
    prev_hasta = 0.0
    for i, m in enumerate(ms):
        m["es_spt"] = (m["n2"] + m["n3"]) > 0
        m["N"] = m["n2"] + m["n3"] if m["es_spt"] else None
        sig_de = ms[i + 1]["de"] if i + 1 < len(ms) else None
        cand = [(m["de"], m["hasta"])]
        if m["es_spt"]:
            cand.append((m["spt_de"], m["spt_a"]))

        def ok(c):
            return abs(c[0] - prev_hasta) < 1e-6 and (sig_de is None or abs(c[1] - sig_de) < 1e-6)
        elegido = next((c for c in cand if ok(c)), None)
        if elegido is None:  # sin candidato perfecto: el que empieza donde terminó el anterior
            elegido = next((c for c in cand if abs(c[0] - prev_hasta) < 1e-6), cand[0])
            m["avisos"].append("tramo no cierra con la muestra siguiente")
        if elegido != cand[0]:
            m["avisos"].append("tramo corregido %.2f-%.2f -> %.2f-%.2f (usa intervalo SPT)" % (
                cand[0][0], cand[0][1], elegido[0], elegido[1]))
        elif m["es_spt"] and (m["spt_de"], m["spt_a"]) != cand[0]:
            m["avisos"].append("intervalo SPT %.2f-%.2f no coincide con el tramo; se usa el tramo" % (
                m["spt_de"], m["spt_a"]))
        m["de"], m["hasta"] = elegido
        prev_hasta = m["hasta"]


# --------------------------------------------------------------------------
# Utilidades de formato / texto
# --------------------------------------------------------------------------
def f2(x):
    """1.5 -> '1,50'"""
    return ("%.2f" % x).replace(".", ",")


TIPOS = [  # correcciones ortograficas frecuentes en digitacion de terreno
    (r"compácidad|compasacidad|compásacidad|compacidad", "compacidad"),
    (r"plaasticidad|plasticidad", "plasticidad"),
    (r"humedad mártir al", "humedad natural"),
    (r"\bsi\.? ?[Pp]lasticidad", "sin plasticidad"),
    (r"\bsi plasticidad", "sin plasticidad"),
    (r"matriz final", "matriz fina"),
    (r"grisaceo", "grisáceo"),
    (r"\s+,", ","),
    (r"\s+\.", "."),
    (r"\s{2,}", " "),
]


def limpiar_desc(t):
    t = t.strip()
    for pat, rep in TIPOS:
        t = re.sub(pat, rep, t)
    t = re.sub(r",(?=\S)", ", ", t)
    if t:
        t = t[0].upper() + t[1:]
    if t and t[-1] not in ".":
        t += "."
    return t


def utm(lat, lon, huso=None):
    """WGS84 -> UTM (formulas de Kruger). Devuelve (norte, este, huso)."""
    a, f = 6378137.0, 1 / 298.257223563
    k0 = 0.9996
    if huso is None:
        huso = int((lon + 180) // 6) + 1
    lon0 = math.radians((huso - 1) * 6 - 180 + 3)
    phi, lam = math.radians(lat), math.radians(lon)
    n = f / (2 - f)
    A = a / (1 + n) * (1 + n ** 2 / 4 + n ** 4 / 64)
    alpha = [n / 2 - 2 * n ** 2 / 3 + 5 * n ** 3 / 16,
             13 * n ** 2 / 48 - 3 * n ** 3 / 5,
             61 * n ** 3 / 240]
    e = math.sqrt(f * (2 - f))
    t = math.sinh(math.atanh(math.sin(phi)) - e * math.atanh(e * math.sin(phi)))
    xi = math.atan2(t, math.cos(lam - lon0))
    eta = math.atanh(math.sin(lam - lon0) / math.sqrt(1 + t * t))
    E = 500000 + k0 * A * (eta + sum(alpha[j] * math.cos(2 * (j + 1) * xi) * math.sinh(2 * (j + 1) * eta) for j in range(3)))
    N = k0 * A * (xi + sum(alpha[j] * math.sin(2 * (j + 1) * xi) * math.cosh(2 * (j + 1) * eta) for j in range(3)))
    if lat < 0:
        N += 10000000
    return N, E, huso


# --------------------------------------------------------------------------
# Manipulación del XML de la plantilla
# --------------------------------------------------------------------------
def ptext(p):
    return "".join(t.text or "" for t in p.iter(W + "t"))


def set_ptext(p, text):
    """Reemplaza el texto de un párrafo conservando el formato de su primer run."""
    runs = p.findall(W + "r")
    if not runs:
        r = p.makeelement(W + "r", {})
        ppr = p.find(W + "pPr")
        if ppr is not None and ppr.find(W + "rPr") is not None:
            r.append(copy.deepcopy(ppr.find(W + "rPr")))
        p.append(r)
        runs = [r]
    first = runs[0]
    for r in runs[1:]:
        p.remove(r)
    for ch in list(first):
        if ch.tag not in (W + "rPr",):
            first.remove(ch)
    t = first.makeelement(W + "t", {})
    t.text = text
    t.set(XML_SPACE, "preserve")
    first.append(t)


def set_ptext_all(root, old_startswith, new_text):
    """Reemplaza (en cualquier parte del xml, incl. cuadros de texto y su fallback)
    todos los párrafos cuyo texto empiece por old_startswith."""
    n = 0
    for p in root.iter(W + "p"):
        if ptext(p).startswith(old_startswith):
            set_ptext(p, new_text)
            n += 1
    return n


def set_cell(tc, text):
    ps = tc.findall(W + "p")
    for extra in ps[1:]:
        tc.remove(extra)
    set_ptext(ps[0], text)


def drop_between(body, first_el, last_el_exclusive):
    i, j = list(body).index(first_el), list(body).index(last_el_exclusive)
    for el in list(body)[i:j]:
        body.remove(el)


def find_p(body, startswith, nth=0):
    hits = [p for p in body.iter(W + "p") if ptext(p).startswith(startswith)]
    if len(hits) <= nth:
        raise SystemExit("No se encontró en la plantilla el párrafo: %r" % startswith)
    return hits[nth]


def keep_next(p):
    ppr = p.find(W + "pPr")
    if ppr is None:
        ppr = p.makeelement(W + "pPr", {})
        p.insert(0, ppr)
    if ppr.find(W + "keepNext") is None:
        # keepNext va despues de pStyle
        idx = 1 if (len(ppr) and ppr[0].tag == W + "pStyle") else 0
        ppr.insert(idx, ppr.makeelement(W + "keepNext", {}))


# --------------------------------------------------------------------------
# Fotos
# --------------------------------------------------------------------------
ASPECTO = 4860000 / 3060000.0  # relación de la foto de la ficha (13,5 x 8,5 cm)


def buscar_foto(carpeta, n):
    if not carpeta or not os.path.isdir(carpeta):
        return None
    for fn in sorted(os.listdir(carpeta)):
        stem, ext = os.path.splitext(fn)
        if ext.lower() in (".jpg", ".jpeg", ".png") and re.fullmatch(r"\D*0*%d\D*" % n, stem):
            return os.path.join(carpeta, fn)
    return None


def preparar_imagen(ruta_origen, n, etiqueta, destino):
    """Recorta al formato de la ficha (o genera recuadro pendiente) y guarda JPG."""
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    if ruta_origen:
        im = ImageOps.exif_transpose(Image.open(ruta_origen)).convert("RGB")
        w, h = im.size
        if w / h > ASPECTO:
            nw = int(h * ASPECTO)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / ASPECTO)
            im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im = im.resize((1620, 1020))
    else:
        im = Image.new("RGB", (1620, 1020), (238, 241, 247))
        d = ImageDraw.Draw(im)
        d.rectangle([20, 20, 1600, 1000], outline=(150, 160, 185), width=4)
        try:
            fnt = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
            fnt2 = ImageFont.truetype("DejaVuSans.ttf", 44)
        except OSError:
            fnt = fnt2 = ImageFont.load_default()
        for txt, y, ft in (("FOTO PENDIENTE", 380, fnt), ("Muestra N° %d" % n, 480, fnt2), (etiqueta, 550, fnt2)):
            wt = d.textlength(txt, font=ft)
            d.text(((1620 - wt) / 2, y), txt, fill=(86, 96, 119), font=ft)
    im.save(destino, "JPEG", quality=85)


# --------------------------------------------------------------------------
# Informe
# --------------------------------------------------------------------------
def generar_informe(args):
    from docx import Document
    meta_xl, ms = leer_registro(args.excel)
    cfg = json.load(open(args.config, encoding="utf8"))
    if not ms:
        raise SystemExit("El Excel no trae muestras.")

    prof = ms[-1]["hasta"]
    spts = [m for m in ms if m["es_spt"]]
    # coordenadas
    coord = cfg.get("coordenadas")
    if not coord and meta_xl.get("ubicacion_gps"):
        lat, lon = [float(x) for x in meta_xl["ubicacion_gps"].split(",")]
        N, E, huso = utm(lat, lon, cfg.get("huso"))
        coord = "N %s / E %s" % (("%.2f" % N), ("%.2f" % E))
    else:
        huso = cfg.get("huso", 19)
        coord = coord or "[COMPLETAR]"
    datum = "WGS84 – %dS" % huso

    doc = Document(args.plantilla)
    body = doc.element.body
    sond = cfg["sondaje"]
    sc = cfg.get("sondaje_corto", sond)
    prof_txt = "%s m" % f2(prof)
    rev = cfg.get("revision", "0")
    sistema = (" mediante sistema %s" % cfg["sistema"]) if cfg.get("sistema") else ""

    # ---- portada ----
    set_ptext_all(body, "SONDAJE S-", "SONDAJE " + sond)
    set_ptext_all(body, "Estudio de Ingeniería · Proyecto", "Estudio de Ingeniería · Proyecto " + cfg["proyecto"])
    set_ptext_all(body, "SACYR —", cfg.get("linea_portada", cfg["mandante"].upper()))

    # ---- encabezado ----
    hdr_el = doc.sections[0].header._element
    set_ptext_all(hdr_el, "Informe de", "Informe de Logueo de Terreno — Sondaje " + sond)
    set_ptext_all(hdr_el, "Proyecto ", "Proyecto %s · %s · %s · %s-F 2026 Rev.%s" % (
        cfg["proyecto"], cfg["mandante"], cfg["localidad"], cfg["codigo"].rsplit("-", 1)[0], rev))

    # ---- antecedentes y revisiones ----
    tbls = body.findall(W + "tbl")
    ant, revt = tbls[1], tbls[2]
    celdas = {}
    for tr in ant.findall(W + "tr"):
        tcs = tr.findall(W + "tc")
        for k in range(0, len(tcs) - 1, 2):
            celdas[ptext(tcs[k]).strip()] = tcs[k + 1]
    valores = {
        "Mandante": cfg["mandante"], "Proyecto": cfg["proyecto"], "Cliente": cfg.get("cliente", ""),
        "Sondaje": sond, "Ubicación": cfg["ubicacion"], "Profundidad": prof_txt,
        "Método": cfg["metodo"], "Coordenadas (UTM)": coord, "Datum / Huso": datum,
        "Fechas de terreno": cfg["fechas"], "Código documento": cfg["codigo"],
    }
    for k, v in valores.items():
        set_cell(celdas[k], v)
    filas = revt.findall(W + "tr")
    for tc, v in zip(filas[1].findall(W + "tc"),
                     [rev, cfg["fecha_revision"], cfg["elaboro"], cfg["reviso"], cfg["aprobo"]]):
        set_cell(tc, v)
    for tc in filas[2].findall(W + "tc"):
        set_cell(tc, "–")

    # ---- sección 1 ----
    set_ptext(find_p(body, "El presente informe documenta"),
              "El presente informe documenta el registro de terreno correspondiente a la ejecución del sondaje %s, "
              "desarrollado el %s en el marco del proyecto %s, ubicado en %s. Su propósito es presentar de forma "
              "trazable la caracterización preliminar de los materiales recuperados durante la perforación, junto con "
              "el registro de los tramos muestreados y de los ensayos de penetración estándar (SPT) ejecutados, "
              "alcanzando una profundidad de %s." % (sond, cfg["fechas"], cfg["proyecto"], cfg["ubicacion"], prof_txt))
    set_ptext(find_p(body, "Debido al predominio"),
              "El sondaje se ejecutó alternando ensayos de penetración estándar (SPT) y tramos de recuperación de "
              "muestra, registrándose %d ensayos SPT entre %s y %s m de profundidad." % (
                  len(spts), f2(spts[0]["de"]) if spts else "-", f2(spts[-1]["hasta"]) if spts else "-"))
    # figura 1 (foto del equipo sobre balsa, propia del proyecto anterior)
    fig_cap = find_p(body, "Figura 1.")
    fig_img = fig_cap.getprevious()
    body.remove(fig_img)
    body.remove(fig_cap)

    # ---- sección 2 ----
    set_ptext(find_p(body, "El sondaje S-2 se emplaza"),
              "El sondaje %s se emplaza en las coordenadas UTM %s (%s), %s." % (sond, coord, datum, cfg["ubicacion"]))
    set_ptext(find_p(body, "La perforación se ejecutó"),
              "La perforación se ejecutó mediante sondaje con recuperación de muestras, alternando el ensayo de "
              "penetración estándar (SPT) con el muestreo de cada tramo, registrándose para cada uno su intervalo de "
              "profundidad y su descripción y, en los ensayos SPT, el número de golpes (N1, N2, N3). Las muestras "
              "fueron dispuestas en caja, fotografiadas e identificadas por tramo y almacenadas para su posterior "
              "análisis de laboratorio.")
    set_ptext(find_p(body, "2.3 Criterio de recuperación"), "2.3 Ensayo de penetración estándar (SPT)")
    set_ptext(find_p(body, "El %R se calcula"),
              "El ensayo SPT registra el número de golpes necesarios para hincar el tomamuestras en tres tramos "
              "consecutivos de 15 cm (N1, N2 y N3). El valor N corresponde a la suma de los golpes de los dos últimos "
              "tramos (N = N2 + N3), descartándose el primer tramo por asentamiento del equipo.")
    set_ptext(find_p(body, "El sondaje S-2 alcanzó"),
              "El sondaje %s alcanzó una profundidad de %s%s. El registro estratigráfico comprende los materiales "
              "logueados desde 0,00 m hasta el término de la perforación." % (sond, prof_txt, sistema))

    # ---- sección 3: tabla de registro ----
    set_ptext(find_p(body, "A continuación, se presenta"),
              "A continuación, se presenta el registro de terreno del sondaje %s correspondiente a los tramos "
              "logueados entre 0,00 m y %s de profundidad." % (sond, prof_txt))
    set_ptext(find_p(body, "Tabla 1."),
              "Tabla 1. Registro de sondaje %s (0,00 – %s m). Fuente: elaboración propia." % (sond, f2(prof)))
    rec = {int(k): float(v) for k, v in (cfg.get("recuperacion") or {}).items()}
    pct = {}
    for m in ms:
        if not m["es_spt"] and m["n"] in rec:
            pct[m["n"]] = int(round(rec[m["n"]] / (m["hasta"] - m["de"]) * 100 + 1e-9))
    rec_prom = ("%.1f" % (sum(pct.values()) / len(pct))).replace(".", ",") if pct else None
    t1 = tbls[3]
    rows = t1.findall(W + "tr")
    hdr, modelo, modelo_spt = rows[0], rows[1], rows[4]
    for r in rows[1:]:
        t1.remove(r)
    for m in ms:
        src = modelo_spt if m["es_spt"] else modelo
        tr = copy.deepcopy(src)
        tcs = tr.findall(W + "tc")
        p_len = m["hasta"] - m["de"]
        vals = [str(m["n"]), "%s – %s" % (f2(m["de"]), f2(m["hasta"])),
                "-" if m["es_spt"] else f2(p_len),
                "-" if m["es_spt"] else (f2(rec[m["n"]]) if m["n"] in rec else "s/i"),
                "SPT" if m["es_spt"] else (("%d%%" % pct[m["n"]]) if m["n"] in pct else "s/i"),
                limpiar_desc(m["desc"])]
        for tc, v in zip(tcs, vals):
            set_cell(tc, v)
        t1.append(tr)

    nota_ri = "" if pct else (" Los valores de longitud recuperada (R) y porcentaje de recuperación (%R) no vienen en el "
                              "registro de ESKUAD y se indican como s/i (sin información).")
    resumen = (cfg.get("texto_resumen_tabla") or "").replace("{rec_prom}", rec_prom or "s/i") or (
        "Se registran %d ensayos SPT, con valores de N entre %d y %d." % (
            len(spts), min(m["N"] for m in spts), max(m["N"] for m in spts)) if spts else "")
    set_ptext(find_p(body, "Los tramos recuperados"),
              "Se ejecutaron %d ensayos SPT entre %s y %s m, con valores de N entre %d y %d. %s%s" % (
                  len(spts), f2(spts[0]["de"]), f2(spts[-1]["hasta"]),
                  min(m["N"] for m in spts), max(m["N"] for m in spts), resumen, nota_ri))

    # ---- sección 4: unidades (borrador) ----
    set_ptext(find_p(body, "La agrupación de unidades"),
              "La agrupación de unidades geotécnicas que se presenta a continuación es un borrador preliminar, "
              "elaborado a partir de la descripción de terreno y de los valores N del ensayo SPT. Deberá ser "
              "revisada e integrada con los resultados de los ensayos de laboratorio (granulometría, humedad natural, "
              "límites de consistencia y clasificación USCS/AASHTO) una vez disponibles.")
    t2 = tbls[4]
    rows2 = t2.findall(W + "tr")
    modelo2 = rows2[1]
    for r in rows2[1:]:
        t2.remove(r)
    for u, d0, d1, txt in cfg["unidades"]:
        tr = copy.deepcopy(modelo2)
        for tc, v in zip(tr.findall(W + "tc"), [u, "%s – %s" % (f2(d0), f2(d1)), txt]):
            set_cell(tc, v)
        t2.append(tr)

    # ---- sección 5: registro fotográfico ----
    h_caja = find_p(body, "5.27 Caja de muestras")
    h6 = find_p(body, "6. Observaciones")
    primer_h2 = find_p(body, "5.1 Tramo")
    mod_h = copy.deepcopy(primer_h2)
    mod_img = copy.deepcopy(primer_h2.getnext())
    mod_cap = copy.deepcopy(primer_h2.getnext().getnext())
    # eliminar bloques fotográficos de la plantilla y la sección "Caja de muestras" (sin datos en ESKUAD)
    drop_between(body, primer_h2, h6)

    tmpdir = tempfile.mkdtemp()
    docpr_id = 3100000
    faltan = []
    for k, m in enumerate(ms, 1):
        tramo = "%s a %s m" % (f2(m["de"]), f2(m["hasta"]))
        if m["es_spt"]:
            tit = "5.%d Tramo %s – %s m — Ensayo SPT (N1: %d · N2: %d · N3: %d · N: %d)" % (
                k, f2(m["de"]), f2(m["hasta"]), m["n1"], m["n2"], m["n3"], m["N"])
            cap = "Foto %d. Ensayo SPT — tramo %s, %s." % (k, tramo, sc)
        else:
            tit = "5.%d Tramo %s – %s m (P: %s m)" % (k, f2(m["de"]), f2(m["hasta"]), f2(m["hasta"] - m["de"]))
            cap = "Foto %d. Muestra — tramo %s, %s." % (k, tramo, sc)
        h, im, ca = copy.deepcopy(mod_h), copy.deepcopy(mod_img), copy.deepcopy(mod_cap)
        set_ptext(h, tit)
        set_ptext(ca, cap)
        keep_next(h)
        keep_next(im)
        origen = buscar_foto(args.fotos, m["n"])
        if not origen:
            faltan.append(m["n"])
        jpg = os.path.join(tmpdir, "muestra_%02d.jpg" % m["n"])
        preparar_imagen(origen, m["n"], "%s · tramo %s" % (sc, tramo), jpg)
        rid, _ = doc.part.get_or_add_image(jpg)
        blip = im.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
        blip.set("{%s}embed" % R_NS, rid)
        for src in im.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}srcRect"):
            for a in list(src.attrib):
                del src.attrib[a]
        docpr_id += 1
        for dp in im.iter("{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr"):
            dp.set("id", str(docpr_id))
            dp.set("name", "muestra_%02d.jpg" % m["n"])
        for cn in im.iter("{http://schemas.openxmlformats.org/drawingml/2006/picture}cNvPr"):
            cn.set("name", "muestra_%02d.jpg" % m["n"])
        for el in (h, im, ca):
            h6.addprevious(el)

    # ---- sección 6 ----
    obs = [o.replace("{rec_prom}", rec_prom or "s/i") for o in (cfg.get("observaciones") or [])]
    obs_ps = [p for p in body.iter(W + "p") if p.find(W + "pPr") is not None
              and p.find(W + "pPr").find(W + "numPr") is not None]
    for p, txt in zip(obs_ps, obs):
        set_ptext(p, txt)
    for p in obs_ps[len(obs):]:
        p.getparent().remove(p)

    # ---- índice (estático en la ficha): se actualizan los números de página estimados ----
    paginas = cfg.get("paginas_indice")
    if not paginas:
        n_tabla = len(ms)
        p_fotos = 3 + 1 + math.ceil(max(n_tabla - 14, 0) / 22.0) + 2   # tabla 1 ocupa ~1 pág cada 22 filas
        paginas = [3, 4, 4, 3 + 1 + math.ceil(max(n_tabla - 14, 0) / 22.0), p_fotos,
                   p_fotos + math.ceil((len(ms) - 2) / 2.0)]
    for pref, num in zip(("1.   ", "2.   ", "3.   ", "4.   ", "5.   ", "6.   "), paginas):
        for p in body.iter(W + "p"):
            if ptext(p).startswith(pref) and p.find(W + "pPr") is not None and \
                    p.find(W + "pPr").find(W + "tabs") is not None:
                ts = list(p.iter(W + "t"))
                ts[-1].text = str(num)

    # ---- limpieza de imágenes huérfanas y metadatos ----
    xml = doc.element.xml
    usados = set(re.findall(r'r:(?:embed|id|link)="(rId\d+)"', xml))
    for rid, rel in list(doc.part.rels.items()):
        if rel.reltype.endswith("/image") and rid not in usados:
            doc.part.drop_rel(rid)
    doc.core_properties.title = "Informe de Logueo de Terreno — Sondaje %s — %s" % (sond, cfg["proyecto"])
    doc.save(args.salida)

    print("Informe generado:", args.salida)
    print("  Sondaje %s · %s m · %d muestras · %d ensayos SPT" % (sond, f2(prof), len(ms), len(spts)))
    print("  Coordenadas:", coord, datum)
    for m in ms:
        for a in m["avisos"]:
            print("  AVISO muestra %d: %s" % (m["n"], a))
    if faltan:
        print("  Fotos pendientes: %d de %d (recuadro 'FOTO PENDIENTE')" % (len(faltan), len(ms)))


# --------------------------------------------------------------------------
# Descarga de fotos
# --------------------------------------------------------------------------
def descargar_fotos(args):
    import urllib.request
    _, ms = leer_registro(args.excel)
    os.makedirs(args.salida, exist_ok=True)
    ok = 0
    for m in ms:
        if not m["foto_url"]:
            print("Muestra %d: sin enlace de foto" % m["n"])
            continue
        req = urllib.request.Request(m["foto_url"])
        if args.token:
            req.add_header("Authorization", "Bearer " + args.token)
        if args.cookie:
            req.add_header("Cookie", args.cookie)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            open(os.path.join(args.salida, "muestra_%02d.jpg" % m["n"]), "wb").write(data)
            ok += 1
            print("Muestra %d OK (%d KB)" % (m["n"], len(data) // 1024))
        except Exception as e:  # noqa
            print("Muestra %d ERROR: %s" % (m["n"], e))
    print("Descargadas %d de %d fotos en %s" % (ok, len(ms), args.salida))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("informe")
    a.add_argument("--excel", required=True)
    a.add_argument("--plantilla", required=True)
    a.add_argument("--config", required=True)
    a.add_argument("--salida", required=True)
    a.add_argument("--fotos")
    a.set_defaults(fn=generar_informe)
    b = sub.add_parser("fotos")
    b.add_argument("--excel", required=True)
    b.add_argument("--salida", required=True)
    b.add_argument("--token")
    b.add_argument("--cookie")
    b.set_defaults(fn=descargar_fotos)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
