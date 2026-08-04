# Configurar agenda virtual con Calendly — SOLUT

Reemplaza el intento de usar "Programación de citas" de Google Calendar (no disponible con el plan de Workspace actual — ver `configurar-cita-programable-google-calendar.md`, queda como referencia histórica).

## Plan necesario

SOLUT necesita solo **1 tipo de evento** ("Evaluación Técnica SOLUT") — esto funciona con el plan **gratuito** de Calendly.

> Si se junta con GEOSOM en la misma cuenta (2 tipos de evento de GEOSOM + 1 de SOLUT = 3 en total), se necesita el plan Standard igual. Ver `configurar-calendly.md` del repo GEOSOM.

## Pasos

1. Si ya creaste la cuenta de Calendly al configurar GEOSOM, usa la misma cuenta (`fmatamala@solut.cl`) — no hace falta una nueva.
2. Confirma que Google Calendar esté conectado (*Account* → *Connected Calendars*).
3. Crea el tipo de evento **"Evaluación Técnica SOLUT"**:
   - Duración: 30–45 min
   - Disponibilidad: bloques reales del equipo técnico, buffer de 15 min
   - Preguntas del formulario de reserva:
     - Empresa / organización
     - Servicio requerido (Ingeniería geotécnica / Suelos / Hormigón)
     - Sector (privado / público / energético / minero)
   - Notificaciones: email 24h y 1h antes
4. Copia la URL pública generada (ej. `calendly.com/fmatamala-solut/evaluacion-tecnica-solut`).
5. Pásamela para insertarla en `03_Flujo_Conversacional/guion-calificacion-prospectos.md` (sección 4, reemplazando `[Link agenda virtual]`).

## Pendiente

- [ ] Crear el tipo de evento "Evaluación Técnica SOLUT" y devolver el link
- [ ] Confirmar si se usa la misma cuenta Calendly que GEOSOM
