# Salida de ejemplo: PR #54

> Salida real de aplicar esta skill a la issue #53 (`H-SEC-7`): [PR #54](https://github.com/user-bcp-student10/wallet-onboarding-mvp/pull/54).
> Commits en el orden de la skill: skill → spec (RS-8) → prueba de regresión que falla → corrección.

**Título:** Corregir H-SEC-7: autorización por rol de la analítica (RS-8)

**Rama:** `fix/h-sec-7-autorizacion-analitica` → `main`

---

> PR generado aplicando la skill [`sdd-corregir-hallazgo`](.github/skills/sdd-corregir-hallazgo/SKILL.md) a la issue #53.

## 1. Hallazgo

`H-SEC-7` · issue #53 · **RS-8** (nuevo; la issue no citaba ningún ID de spec).

## 2. Validación del hallazgo

Reproducido contra `main` (`cd6d725`) con la app en memoria:

```text
GET anónimo mensual -> 200
POST anónimo gasto  -> 201
```

Cualquier persona podía leer la analítica y registrar un gasto (por ejemplo S/ 99,999) que distorsiona el CAC del reporte mensual. **El hallazgo es real.**

## 3. Cambio en la spec

La issue tenía "Spec: —": era un hueco de la spec. Antes del código:

- `spec.md` v1.1: nuevo **RS-8**. La analítica exige `Authorization: Bearer <token>`; leer requiere el rol `analista` o `admin` y registrar gasto, `admin`. Responde `401 NO_AUTENTICADO` y `403 SIN_PERMISO`, y cada gasto guarda el rol y la fecha de registro. También se agregó un historial de cambios.
- `contracts/openapi.yaml`: esquema `tokenAnalitica`, `security` y respuestas 401 y 403 en las 4 operaciones de analítica, que ahora citan `RS-8` en `x-spec`.

## 4. Prueba de regresión

`tests/test_rs8_autorizacion_analitica.py` (docstring con RS-8, 16 casos), ejecutada **antes** de la corrección (commit 27a98a5):

```text
=========================== short test summary info ============================
FAILED tests/test_rs8_autorizacion_analitica.py::test_lectura_anonima_de_analitica_se_rechaza[/api/analitica/onboarding]
FAILED tests/test_rs8_autorizacion_analitica.py::test_lectura_anonima_de_analitica_se_rechaza[/api/analitica/mensual]
FAILED tests/test_rs8_autorizacion_analitica.py::test_lectura_anonima_de_analitica_se_rechaza[/api/analitica/eventos]
FAILED tests/test_rs8_autorizacion_analitica.py::test_token_invalido_se_rechaza[/api/analitica/onboarding]
FAILED tests/test_rs8_autorizacion_analitica.py::test_token_invalido_se_rechaza[/api/analitica/mensual]
FAILED tests/test_rs8_autorizacion_analitica.py::test_token_invalido_se_rechaza[/api/analitica/eventos]
FAILED tests/test_rs8_autorizacion_analitica.py::test_registro_anonimo_de_gasto_se_rechaza_y_no_altera_el_cac
FAILED tests/test_rs8_autorizacion_analitica.py::test_analista_no_puede_registrar_gasto
FAILED tests/test_rs8_autorizacion_analitica.py::test_admin_registra_gasto_con_auditoria
9 failed, 7 passed in 0.35s
```

Los 7 casos que ya pasaban describen el comportamiento que debe conservarse: los roles válidos pueden leer y el token no aparece en las respuestas.

## 5. Corrección

| Archivo | Cambio |
|---|---|
| `app/main.py` | `requiere_rol()` valida el token con `hmac.compare_digest` y devuelve 401 (con `WWW-Authenticate: Bearer`) o 403. Las 3 lecturas exigen `analista` o `admin`; `POST /api/analitica/gasto` exige `admin` y agrega `registrado_por` y `registrado_en`. Los tokens se leen de `TOKEN_ANALISTA` y `TOKEN_ADMIN`; si falta uno, se genera uno aleatorio por ejecución y se muestra en la consola. |
| `frontend/app.js` | La pestaña Analítica pide el token, lo envía en `Authorization` y lo guarda solo en `sessionStorage`. Con 401 o 403 lo borra y vuelve a pedirlo. Incluye un botón "Salir de la analítica". |
| `tests/conftest.py` | **Cambio en una prueba existente, explicado:** el cliente compartido ahora se autentica como `admin`, porque RS-8 cambió la spec y las pruebas de CA-5 y CA-6 consultan la analítica. Las aserciones de esas pruebas no cambiaron. |
| `tools/check_contrato.py` | Usa tokens fijos al crear la app, para no generar ni mostrar tokens temporales al leer las rutas. |
| `render.yaml` | `TOKEN_ANALISTA` y `TOKEN_ADMIN` con `sync: false`: Render los pide al crear el servicio y no se versionan. |
| Documentación | DEC-10 y limitaciones en `docs/supuestos-y-decisiones.md`, `plan.md`, README (variables, API y skills), guion de la demo y trazabilidad. |

## 6. Verificación

Prueba de regresión después de la corrección:

```text
16 passed in 0.25s
```

`python -m pytest -q`:

```text
70 passed in 3.38s
```

`python tools/check_trazabilidad.py`:

```text
Trazabilidad spec → pruebas
  ✓ CA-1: tests/test_ca1_pasos_visibles.py (5 funciones de prueba)
  ✓ CA-2: tests/test_ca2_validaciones.py (6 funciones de prueba)
  ✓ CA-3: tests/test_ca3_activacion.py (5 funciones de prueba)
  ✓ CA-4: tests/test_ca4_eventos.py (5 funciones de prueba)
  ✓ CA-5: tests/test_ca5_ca6_analitica.py (7 funciones de prueba)
  ✓ CA-6: tests/test_ca5_ca6_analitica.py (7 funciones de prueba)
OK
```

`python tools/check_contrato.py`:

```text
Contrato (13 operaciones) frente a la API real
OK
```

Verificación manual en el servidor real (`TOKEN_ANALISTA=demo-analista TOKEN_ADMIN=demo-admin`):

```text
curl anónimo gasto: 401
{"codigo":"SIN_PERMISO","mensaje":"El rol analista no puede realizar esta operación."}
{"mes":"2026-09","canal":"referidos","monto_pen":10.0,"registrado_por":"admin","registrado_en":"2026-10-30T19:43:47+00:00"}
```

En el navegador (Chromium): sin token se muestra el formulario; un token incorrecto da un mensaje de error; con `demo-analista` se ve el panel; "Salir" vuelve al formulario y el registro sigue abierto sin token. Sin errores de JavaScript.

## 7. Fuera de alcance

- **Iconos de error vacíos en los formularios:** la regla `.error-campo { display: flex }` anula el atributo `hidden` y se ven iconos ⚠ sin texto (4 en el paso 1 del registro). Es un defecto previo de la interfaz, no de este hallazgo: va en un PR aparte.
- **RS-6** sigue pendiente: `/api/onboardings/{id}` y sus eventos no exigen sesión.
- `POST /api/demo/reiniciar` no exige token: está pensado para la demo (`DEMO_ENDPOINTS=true`) y debe desactivarse en cualquier despliegue compartido.
- Los tokens son compartidos por rol, sin expiración ni identidad individual. En producción se reemplazarían por usuarios con SSO.

## 8. Checklist de la issue

- [ ] La corrección está aplicada y revisada por otro integrante. *(pendiente: revisión de este PR)*
- [x] La verificación anterior se ejecutó y su salida está en un comentario. *(sección 6)*
- [x] Si cambia el comportamiento, la spec se actualizó primero. *(commit 86bc568, antes del código)*
- [ ] Una nueva ejecución de `python validar.py` ya no reporta el hallazgo. *(pendiente: ejecutar el crew después del merge)*

Closes #53

