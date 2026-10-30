---
name: sdd-corregir-hallazgo
description: Corrige una issue de GitHub con la etiqueta `hallazgo` creada por la validación SDD (títulos como "[H-SEC-7] ..."). Úsala cuando te pidan resolver, corregir o trabajar un hallazgo H-XXX-n o una issue que cite un ID de la spec (CA-n, RN-n, RS-n, RNF-n). Valida el hallazgo, actualiza la spec si cambia el comportamiento, escribe primero una prueba de regresión que falle, aplica la corrección mínima, ejecuta las verificaciones y entrega un PR trazable.
---

# Skill: SDD · Corregir un hallazgo

## 1) Metadata
- **Skill ID:** sdd-corregir-hallazgo
- **Version:** 0.1.0
- **Purpose:** Convertir un hallazgo de la validación SDD en una corrección verificable que mantenga la spec como fuente de verdad.
- **Audience (roles):** Backend, Frontend, QA, Cyber, Tech Lead (revisión del PR)
- **When to use:** Al trabajar una issue con la etiqueta `hallazgo` (creada por `crew-validacion-sdd` o por una persona con el mismo formato).
- **When NOT to use:** Funcionalidades nuevas sin hallazgo previo (usa `feature-intake-spec-checklist`), incidentes P1 en producción, o cambios triviales sin impacto en la spec.
- **Sensitive inputs:** No incluyas datos reales de clientes, credenciales, tokens ni secretos en la issue, el código, las pruebas ni el PR. Usa solo datos ficticios.
- **Expected output:** Una rama con commits, un PR con la estructura de la sección Output y un comentario en la issue.

## 2) Inputs
- **Issue:** número y cuerpo completo. Campos esperados: ID (`H-XXX-n`), Rol, Severidad, Spec, Ubicación (`archivo:línea`), Evidencia, Corrección propuesta y Cómo verificar.
- **Spec:** `specs/001-registro-activacion/spec.md` (y `plan.md` y `contracts/openapi.yaml`).
- **Código y pruebas** de la ubicación citada.
- **Comandos de verificación del repo:**
  - `python -m pytest -q`
  - `python tools/check_trazabilidad.py`
  - `python tools/check_contrato.py`

## 3) Procedure
Sigue los pasos en orden. No avances si un paso falla.

1. **Validar el hallazgo.** Abre la ubicación citada y reproduce el problema con una prueba o un comando.
   - Si el hallazgo **no es real** o ya está resuelto: no cambies código. Comenta en la issue con la evidencia (salida del comando) y propone cerrarla como "no planificada".
   - Si la ubicación cambió desde el commit validado, búscala por el código citado en la evidencia.
2. **Ubicar el hallazgo en la spec.**
   - Si cita un ID existente (CA, RN, RS, RNF): la corrección debe cumplir ese ID tal como está escrito.
   - Si el campo Spec es "—" o el comportamiento correcto no está especificado: es un **hueco de la spec**. Agrega o ajusta el requisito en `spec.md` **antes** del código (nuevo ID consecutivo, por ejemplo RS-8), y el contrato `openapi.yaml` si cambian rutas, respuestas o seguridad.
3. **Escribir la prueba de regresión primero.** Crea o amplía un archivo `tests/test_*.py` cuyo docstring cite el ID de la spec. Ejecútala y **confirma que falla** con el código actual. Guarda esa salida.
4. **Aplicar la corrección mínima.** Cambia solo lo necesario para cumplir la spec. No refactorices ni corrijas otros hallazgos en el mismo PR; si encuentras otros problemas, anótalos en el PR.
5. **Verificar.** Ejecuta la prueba de regresión (debe pasar) y los tres comandos de verificación del repo (deben pasar). Guarda las salidas reales.
6. **Actualizar la documentación** afectada: decisiones (`docs/supuestos-y-decisiones.md`), README o guion de la demo si cambia el uso.
7. **Entregar.** Commits en una rama `fix/<id-hallazgo>-<tema>`, PR hacia `main` con `Closes #<issue>` y un comentario en la issue con el enlace al PR.

## 4) Output
El PR debe tener exactamente estas secciones:

1. **Hallazgo:** `H-XXX-n` · issue `#n` · ID de spec afectado.
2. **Validación del hallazgo:** cómo se reprodujo y su salida (antes de la corrección).
3. **Cambio en la spec:** IDs agregados o modificados, o "Sin cambios" con la razón.
4. **Prueba de regresión:** archivo, nombres de las pruebas y salida **fallando** antes de la corrección.
5. **Corrección:** archivos cambiados y qué hace cada cambio.
6. **Verificación:** salida real de la prueba de regresión y de los tres comandos del repo.
7. **Fuera de alcance:** problemas detectados que no se corrigen en este PR.
8. **Checklist de la issue:** los cuatro puntos de "Para cerrar esta issue", marcados solo si se cumplen.

## 5) Constraints
- No inventes ejecuciones ni resultados: cada salida del PR debe venir de un comando ejecutado.
- No modifiques ni borres pruebas existentes para que pasen. Si una prueba existente debe cambiar porque la spec cambió, explícalo en el PR.
- No cambies el comportamiento sin cambiar antes la spec.
- No mezcles varios hallazgos en un PR.
- No guardes secretos en el repositorio: credenciales por variables de entorno y valores de ejemplo claramente ficticios.
- No cierres la issue tú mismo: se cierra al fusionar el PR, después de la revisión de otro integrante.

## 6) Validation Rules
La salida es válida si:
- El PR tiene las 8 secciones de Output.
- Existe al menos una prueba nueva que cita el ID de spec en su docstring, con evidencia de que falló antes y pasa después.
- Si el campo Spec de la issue era "—", el PR agrega un requisito nuevo en `spec.md`.
- `pytest`, `check_trazabilidad.py` y `check_contrato.py` terminan sin errores, con su salida en el PR.
- El PR contiene `Closes #<issue>` y no contiene datos sensibles.

## 7) Evidence
- `SKILL.md` versionado.
- `examples/input.sample.md`: la issue #53 (`H-SEC-7`) como entrada real.
- `examples/output.sample.md`: el PR que corrigió la #53 siguiendo esta skill.
- Tag de versión: `skill-sdd-corregir-hallazgo-v0.1.0`.
