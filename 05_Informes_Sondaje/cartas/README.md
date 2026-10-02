# Cartas conductoras (envío de muestras a laboratorio)

Formato CC-SLAB-01 Rev. 01 de SOLUT Laboratorio. Cada carta se define en un JSON (destinatario, proyecto, muestras,
coordenadas, fechas, ensayos) y se genera con:

    pip install python-docx
    python cartas_conductoras.py carta_lonco_ITT-UDEC.json salida.docx

Pendiente de completar a mano en cada carta: N° correlativo (`CNº __/26`) y datos del destinatario marcados en amarillo.
La selección de muestras y ensayos de los JSON es una propuesta (una a tres muestras por unidad geotécnica) y debe
ser confirmada por el ingeniero responsable.
