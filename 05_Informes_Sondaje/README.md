# Informes de logueo de sondaje desde ESKUAD

Genera la ficha Word **"Informe de Logueo de Terreno"** de SOLUT a partir del Excel exportado desde ESKUAD
(formulario *Registro Sondaje*). Usa la ficha vigente como plantilla, por lo que el formato no cambia.

## Uso

```bash
pip install python-docx openpyxl pillow

# 1) Descargar fotos (desde su PC, con sesión ESKUAD; ver nota)
python sondajes_eskuad.py fotos --excel registro.xlsx --salida fotos/ --token <TOKEN>

# 2) Generar informe
python sondajes_eskuad.py informe --excel registro.xlsx --plantilla ficha_vigente.docx \
    --config config_S1_PEWEN_Paicavi.json --salida informe.docx --fotos fotos/
```

Las fotos se buscan por número de muestra (`muestra_01.jpg`, `foto_1.png`, ...). Sin fotos, el informe queda con
recuadros "FOTO PENDIENTE". Se pueden reemplazar a mano o volver a correr el comando con `--fotos`.

## Qué viene de ESKUAD y qué del `config_*.json`

| ESKUAD (Excel) | config JSON |
|---|---|
| Tramos, N1/N2/N3, descripción, fotos, coordenadas GPS (se convierten a UTM) | Mandante, proyecto, ubicación, nombre del sondaje, fechas, código, responsables, unidades geotécnicas (borrador) y observaciones |

## Notas

- ESKUAD no entrega longitud recuperada (R) ni %R en el Excel. Se leen del pizarrón de cada foto y se cargan en `"recuperacion"` del config (%R se calcula). Si falta, la columna queda `s/i`.
- Las fotos exportadas a Drive tienen nombre UUID: se asignan a las muestras en orden de subida (verificar con el pizarrón de cada foto).
- Intervalos inconsistentes de digitación se corrigen y se informan al ejecutar (avisos).
- El índice de la ficha es texto fijo: los números de página son estimados; revisar al abrir en Word.
- Las URLs de fotos de ESKUAD requieren autenticación; si el token no funciona, descargar las fotos desde ESKUAD.

- Si las fotos exportadas llegan en orden inverso al del registro (caso S-3 Lonco), renombrarlas por número de muestra antes de usar `--fotos`; el pizarrón de cada foto indica la cota.
- Si el Excel no trae GPS, indicar `"coordenadas"` en el config (o queda `[COMPLETAR]`).
- Ensayos con rechazo (50 golpes sin completar penetración) se informan como rechazo, sin valor N.
