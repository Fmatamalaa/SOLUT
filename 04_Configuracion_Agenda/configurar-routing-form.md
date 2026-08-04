# Automatizar la calificación con Calendly Routing Forms — SOLUT

Esto reemplaza el trabajo manual de calificar prospectos por chat/DM (lo que hiciste la primera noche): el prospecto responde un formulario corto y Calendly lo redirige **solo**, sin intervención humana, al link correcto — replicando la lógica de `03_Flujo_Conversacional/guion-calificacion-prospectos.md` sección 3.

Requiere el plan **Standard** de Calendly (el mismo que ya se activó para tener varios tipos de evento).

## Pasos para crearlo

1. En Calendly, ve a **Routing** en el menú lateral izquierdo → **Create routing form**.
2. Nombra el formulario: **"Calificación de proyecto - SOLUT"**.
3. Agrega las preguntas (tipo *Multiple choice* salvo donde se indique):

   **P1 — ¿Qué tipo de servicio buscas?**
   - Ingeniería geotécnica (estabilidad de taludes, túneles, fundaciones)
   - Exploración de suelos (sondajes, calicatas, geofísica)
   - Ensayos y auscultación de hormigón
   - Energía geotérmica / climatización
   - No estoy seguro, necesito orientación

   **P2 — ¿En qué etapa está tu proyecto?**
   - Estudio de factibilidad / diseño inicial, sin fecha definida
   - En diseño de ingeniería (falta exploración/laboratorio)
   - En construcción (control de obra o auscultación)
   - Estructura existente con problema (falla, asentamiento, agrietamiento)

   **P3 — ¿Para cuándo necesitas avanzar?**
   - Urgente (próximas semanas)
   - Este trimestre
   - Este año
   - Aún explorando, sin fecha

   **P4 — Datos de contacto** (tipo *Short answer* / *Email* / *Phone*)
   - Nombre y apellido
   - Empresa / organización
   - Email
   - Teléfono
   - Región/comuna del proyecto

4. Configura las **reglas de enrutamiento** (sección *Routing logic* del editor), en este orden de prioridad:

   | Regla | Condición | Acción |
   |---|---|---|
   | 1 | P1 = "Energía geotérmica / climatización" | Redirigir a sitio externo: `https://calendly.com/fmatamala-solut/new-meeting` (link de GEOSOM — reunión técnica) |
   | 2 | P2 = "Estudio de factibilidad... sin fecha definida" **Y** P3 = "Aún explorando, sin fecha" | Mostrar **mensaje personalizado** (no agenda): ver texto abajo |
   | 3 | Cualquier otra combinación | Redirigir al tipo de evento: **Evaluación Técnica SOLUT** (`evaluacion-tecnica-solut`) |

5. Texto del mensaje personalizado para la regla 2 (pantalla final, sin botón de agenda):

   > ¡Gracias por contarnos sobre tu proyecto! Por ahora está en una etapa temprana, así que te dejamos un recurso útil: descarga nuestro ebook y descubre cómo la geotecnia aporta seguridad y precisión a cada proyecto → https://drive.google.com/drive/folders/11fBvMaf0CcrwwCzKLfWTLzkaEWptCy4B?usp=sharing
   >
   > Trabajamos con clientes como Ausenco, Icafal, IDOM, Pan American Silver, Colbún y SQM, en proyectos mineros, energéticos, de infraestructura pública y privados.
   >
   > Cuando tengas más definido el proyecto, contáctanos directo: +56 9 3006 2244 / contacto@solut.cl

6. **Publica** el formulario y copia su link (algo como `calendly.com/fmatamala-solut/calificacion-proyecto-solut`).

## Dónde usar el link del formulario a partir de mañana

- Reemplaza el link directo de Calendly en la sección **Featured/Destacado** de tu perfil de LinkedIn por este link del formulario.
- En el próximo post de LinkedIn, el CTA "Agenda tu evaluación" debe apuntar a este link (no directo al evento) — así el formulario filtra antes de que la persona vea el calendario.
- Actualiza también `03_Flujo_Conversacional/guion-calificacion-prospectos.md` sección 4 con este link como el CTA principal (dejando el link directo del evento como respaldo si alguien ya sabe que califica).

## Pendiente

- [ ] Crear el formulario en Calendly con las reglas de arriba
- [x] Link de descarga del ebook — carpeta de Google Drive compartida (ver regla 2)
- [ ] Reemplazar los links en LinkedIn (Featured) y en el guion
- [ ] Repetir este mismo proceso para GEOSOM (`guion-calificacion-prospectos.md` sección 3 de ese repo ya tiene la lógica de calificación equivalente)
