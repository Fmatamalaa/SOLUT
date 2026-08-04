# Configurar "Cita programable" en Google Calendar — SOLUT

Mismo procedimiento que en [GEOSOM](https://github.com/Fmatamalaa/GEOSOM/blob/main/04_Configuracion_Agenda/configurar-cita-programable-google-calendar.md). Requiere cuenta de **Google Workspace** (ej. `@solut.cl`) — no disponible en cuentas Gmail gratuitas.

## Pasos

1. Entra a [calendar.google.com](https://calendar.google.com) con la cuenta que administrará las reuniones (ej. `fmatamala@solut.cl`).
2. (Opcional) Crea un calendario nuevo **"SOLUT - Reuniones"** para separarlo de tu calendario personal y del de GEOSOM.
3. Click en **Crear** → **Programación de citas** (Appointment schedule).
4. Configura la programación **"Evaluación Técnica SOLUT"** (según el guion en `03_Flujo_Conversacional/`):
   - Duración sugerida: 30–45 min
   - Calendario asociado: SOLUT - Reuniones
   - Disponibilidad: bloques reales del equipo técnico, con buffer de 15 min entre reuniones
   - Formulario de reserva — pedir:
     - Nombre y apellido
     - Empresa / organización
     - Email corporativo
     - Teléfono
     - Servicio requerido (Ingeniería geotécnica / Suelos / Hormigón — texto libre o desplegable, viene pre-calificado desde el asistente)
     - Sector (privado / público / energético / minero)
   - Notificaciones: confirmación y recordatorio por email (24h y 1h antes)
5. Al guardar, Google genera una **URL pública de reserva**. Cópiala.
6. Pégamela aquí (o la agrego yo directo) para insertarla en `03_Flujo_Conversacional/guion-calificacion-prospectos.md` (sección 4, reemplazando `[Link agenda virtual]`).

## Nota — reutilizar la misma cuenta que GEOSOM

Si usas la misma cuenta `fmatamala@solut.cl` para ambas agendas (GEOSOM y SOLUT), basta con crear **dos programaciones separadas** dentro del mismo Google Calendar — no hace falta una cuenta distinta. Cada una tiene su propia URL pública y su propio calendario asociado si quieres mantenerlos visualmente separados.

## Pendiente

- [ ] Confirmar que la cuenta usada tiene Google Workspace activo (mismo punto pendiente que en GEOSOM)
- [ ] Crear la programación "Evaluación Técnica SOLUT" y devolver el link
- [ ] Decidir si el equipo que recibe la notificación de agendamiento es el mismo que en GEOSOM o uno distinto por línea de servicio
