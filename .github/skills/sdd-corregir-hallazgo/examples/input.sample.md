# Entrada de ejemplo: issue #53

> Issue real de `user-bcp-student10/wallet-onboarding-mvp`, creada por `crew-validacion-sdd` (`python validar.py --crear-issues`).
> Petición al agente: **"Resuelve la issue #53"**.

**Título:** [H-SEC-7] · Analítica expuesta y gastos modificables sin autorización

**Etiquetas:** `hallazgo`, `sdd:security`, `severidad:media`

---

## Hallazgo de la validación SDD

| Campo | Valor |
|---|---|
| ID | `H-SEC-7` |
| Rol | Security |
| Severidad | **MEDIA** |
| Spec | — |
| Ubicación | `app/main.py:133-154` |
| Commit validado | `cd6d7253bf3ed565daee07fb83b64277227340fd` |

**Problema:** Analítica expuesta y gastos modificables sin autorización

**Evidencia:** Las rutas de analítica no muestran controles de autorización; `registrar_gasto` agrega datos directamente al almacén, alterando reportes y CAC.

## Corrección propuesta

Restringir la lectura a roles autorizados y el registro de gastos a un rol administrativo; auditar cambios.

## Cómo verificar la corrección

Probar las rutas anónimamente y con un usuario autorizado: las primeras deben denegarse y el rol autorizado debe poder registrar gastos.

## Para cerrar esta issue

- [ ] La corrección está aplicada y revisada por otro integrante.
- [ ] La verificación anterior se ejecutó y su salida está en un comentario.
- [ ] Si cambia el comportamiento, la spec se actualizó primero.
- [ ] Una nueva ejecución de `python validar.py` ya no reporta el hallazgo.

---
Generado por `crew-validacion-sdd` desde `security_review.md`. El informe fue aprobado por una persona y esta
issue se creó con su confirmación. Un hallazgo de un modelo puede estar equivocado: valídalo antes de corregir.
<!-- sdd-hallazgo: H-SEC-7 commit: cd6d7253bf3ed565daee07fb83b64277227340fd -->

