# Guion del Asistente Virtual SOLUT — Calificación y Agendamiento

Basado en `01_Documentacion_Tecnica/resumen-ebook-solut.md` y `02_Marketing/resumen-carrusel-solut.md`.

Objetivo del flujo: captar el prospecto → identificar qué servicio necesita → calificarlo con datos de su proyecto → si califica, agendarlo directo a una **evaluación técnica**. Si pide específicamente climatización/geotermia, derivar al flujo de [GEOSOM](https://github.com/Fmatamalaa/GEOSOM) en vez de este.

Contacto vigente (confirmado en ebook 2026): **+56 9 3006 2244** o **+56 9 7586 1050** / contacto@solut.cl / www.solut.cl. Oficinas en Concepción (Aníbal Pinto 340 y Maipú 1623).

---

## 1. Mensaje de bienvenida

> ¡Hola! 👋 Soy el asistente virtual de **SOLUT Ingeniería**.
> Somos especialistas en geociencias: ingeniería geotécnica, laboratorio y exploración de suelos/hormigón, y energía geotérmica — trabajando con el sector privado, público, energético y minero en todo Chile.
>
> "Lo que no ves bajo el suelo puede definir todo un proyecto" — por eso reducimos sobrecostos, riesgos estructurales y retrasos con datos de terreno confiables.
>
> Para ayudarte, cuéntame de tu proyecto. Son solo unas preguntas rápidas y al final coordinamos tu **evaluación técnica**. ¿Partimos?

Botones: `Sí, partamos` / `Solo quiero información`

Si elige "Solo quiero información" → ofrecer el ebook/contenido educativo (ver sección 5) y dejar abierta la opción de calificar después.

---

## 2. Preguntas de calificación

**P1 — Servicio que necesita**
> ¿Qué tipo de servicio buscas?
- Ingeniería geotécnica (estabilidad de taludes, túneles, fundaciones)
- Exploración de suelos (sondajes, calicatas, geofísica)
- Ensayos y auscultación de hormigón
- Energía geotérmica / climatización *(→ si elige esta opción, derivar al flujo de GEOSOM)*
- No estoy seguro, necesito orientación

**P2 — Sector**
> ¿En qué sector se enmarca tu proyecto?
- Privado (inmobiliario/industrial)
- Público (MOP u otro organismo del Estado)
- Energético
- Minero
- Otro

**P3 — Etapa del proyecto**
> ¿En qué etapa está tu proyecto?
- Estudio de factibilidad / diseño inicial
- En diseño de ingeniería (falta exploración/laboratorio)
- En construcción (requiere control de obra o auscultación)
- Estructura existente con problema (ej. falla, asentamiento, agrietamiento) — requiere diagnóstico

**P4 — Qué problema quiere resolver**
> ¿Qué es lo que más te preocupa del proyecto?
- Falta de información confiable del subsuelo antes de diseñar
- Validar estabilidad (taludes, fundaciones, estructuras)
- Control de calidad en obra
- Diagnóstico de una estructura existente (grietas, asentamientos, deterioro)
- Cumplir exigencias normativas/ambientales de un mandante o del Estado

**P5 — Ubicación**
> ¿En qué región/comuna se ubica el proyecto? (relevante para logística de equipos de terreno)

**P6 — Plazo**
> ¿Para cuándo necesitas avanzar?
- Urgente (próximas semanas)
- Este trimestre
- Este año
- Aún explorando, sin fecha

---

## 3. Lógica de calificación

**Califica para evaluación técnica** si cumple:
- P1 tiene una respuesta concreta (no "no estoy seguro" sin resolver — en ese caso, primero orientar con 1-2 preguntas de contexto y volver a clasificar)
- P3 no es solo "estudio de factibilidad sin fecha" **O** P4 indica una necesidad concreta (validar estabilidad, control de calidad, diagnóstico, exigencia normativa)
- P6 no es "Aún explorando, sin fecha"
- Dio ubicación en P5

**No califica aún (nutrir)** si:
- P3 = factibilidad muy temprana **y** P6 = sin fecha **y** P4 = nada concreto todavía
- → Ofrecer el ebook ("Descarga nuestro ebook y descubre cómo la geotecnia aporta seguridad y precisión a cada proyecto") y dejar la puerta abierta para retomar cuando el proyecto avance.

**Deriva a flujo GEOSOM** si P1 = "Energía geotérmica / climatización" — no seguir con estas preguntas, usar el guion del repo GEOSOM.

---

## 4. Mensaje de cierre — Calificado

> ¡Gracias, {{nombre}}! Con esto ya tenemos claridad de tu proyecto. 🎯
>
> Agendemos tu **evaluación técnica** con nuestro equipo de ingeniería geotécnica — revisamos tu caso y definimos el alcance (sondajes, ensayos, laboratorio, etc.) según lo que necesitas.
>
> 👉 https://calendly.com/fmatamala-solut/evaluacion-tecnica-solut
>
> También puedes escribirnos directo al +56 9 3006 2244 / +56 9 7586 1050 o contacto@solut.cl.

## 5. Mensaje de cierre — No calificado aún / solo información

> ¡Gracias por contarme! Por ahora tu proyecto está en una etapa temprana, así que te dejo un recurso útil:
>
> 📘 Descarga nuestro ebook y descubre cómo la geotecnia aporta seguridad y precisión a cada proyecto: https://drive.google.com/drive/folders/11fBvMaf0CcrwwCzKLfWTLzkaEWptCy4B?usp=sharing
>
> Trabajamos con clientes como Ausenco, Icafal, IDOM, Pan American Silver, Colbún y SQM, en proyectos mineros, energéticos, de infraestructura pública (MOP) y privados.
>
> Cuando tengas más definido el proyecto, escríbeme de nuevo o contáctanos directo: +56 9 3006 2244 / contacto@solut.cl / www.solut.cl.

---

## 6. Preguntas frecuentes que el asistente debería poder responder

- **¿Qué servicios ofrece SOLUT?** Ingeniería geotécnica, exploración de suelos (sondajes, calicatas, geofísica), ensayos y auscultación de hormigón, y energía geotérmica.
- **¿Tienen experiencia en mi sector?** Sí — proyectos mineros (Pan American Silver, Colbún, SQM), energéticos (parques eólicos con Esteyco/Engie), de infraestructura pública (puentes MOP con IDOM y GS Ingeniería) y privados (Icafal, Ausenco).
- **¿Qué equipos usan?** Sondas de perforación propias (MWDL-450, RL-48), equipos de geofísica (MASW, REMI, Downhole, Crosshole), escáner electromagnético y equipo Hilti PS300 para hormigón.
- **¿Están certificados?** El laboratorio de suelos está en proceso de certificación INN.
- **¿Dónde están ubicados?** Concepción (dos oficinas), con proyectos ejecutados en todo el territorio nacional.

---

## 7. Pendientes antes de implementar en una herramienta

- [ ] Definir link de agenda virtual (mismo criterio que GEOSOM — ver `04_Configuracion_Agenda/`)
- [ ] Confirmar link de descarga del ebook para usarlo como recurso de nutrición
- [ ] Validar con Felipe/equipo los criterios exactos de calificación por línea de servicio
- [ ] Definir a quién se notifica internamente cuando un prospecto califica y agenda (¿mismo equipo que GEOSOM o distinto según servicio?)
- [ ] Elegir herramienta de implementación del bot (WhatsApp Business + Manychat, n8n, etc.)
