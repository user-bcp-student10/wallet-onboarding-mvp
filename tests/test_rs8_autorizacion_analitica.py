"""RS-8: la analítica exige un token con rol; registrar gasto solo con rol admin (hallazgo H-SEC-7, issue #53)."""
import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.store import JsonStore

TOKEN_ANALISTA = "token-analista-de-prueba"
TOKEN_ADMIN = "token-admin-de-prueba"
GASTO = {"mes": "2026-10", "canal": "referidos", "monto_pen": 50}
LECTURAS = ["/api/analitica/onboarding", "/api/analitica/mensual", "/api/analitica/eventos"]


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def anonimo(monkeypatch, reloj):
    monkeypatch.setenv("TOKEN_ANALISTA", TOKEN_ANALISTA)
    monkeypatch.setenv("TOKEN_ADMIN", TOKEN_ADMIN)
    return TestClient(create_app(store=JsonStore(), reloj=reloj, cargar_demo=False))


@pytest.mark.parametrize("ruta", LECTURAS)
def test_lectura_anonima_de_analitica_se_rechaza(anonimo, ruta):
    r = anonimo.get(ruta)
    assert r.status_code == 401
    assert r.json()["codigo"] == "NO_AUTENTICADO"


@pytest.mark.parametrize("ruta", LECTURAS)
def test_token_invalido_se_rechaza(anonimo, ruta):
    assert anonimo.get(ruta, headers=bearer("token-falso")).status_code == 401


@pytest.mark.parametrize("token", [TOKEN_ANALISTA, TOKEN_ADMIN])
@pytest.mark.parametrize("ruta", LECTURAS)
def test_analista_y_admin_pueden_leer(anonimo, ruta, token):
    assert anonimo.get(ruta, headers=bearer(token)).status_code == 200


def test_registro_anonimo_de_gasto_se_rechaza_y_no_altera_el_cac(anonimo):
    r = anonimo.post("/api/analitica/gasto", json=GASTO)
    assert r.status_code == 401
    meses = anonimo.get("/api/analitica/mensual", headers=bearer(TOKEN_ADMIN)).json()["meses"]
    assert meses == []


def test_analista_no_puede_registrar_gasto(anonimo):
    r = anonimo.post("/api/analitica/gasto", json=GASTO, headers=bearer(TOKEN_ANALISTA))
    assert r.status_code == 403
    assert r.json()["codigo"] == "SIN_PERMISO"


def test_admin_registra_gasto_con_auditoria(anonimo, reloj):
    r = anonimo.post("/api/analitica/gasto", json=GASTO, headers=bearer(TOKEN_ADMIN))
    assert r.status_code == 201
    assert r.json()["registrado_por"] == "admin"
    assert r.json()["registrado_en"] == reloj().isoformat(timespec="seconds")


def test_el_token_no_aparece_en_las_respuestas(anonimo):
    r = anonimo.post("/api/analitica/gasto", json=GASTO, headers=bearer(TOKEN_ADMIN))
    assert TOKEN_ADMIN not in r.text
