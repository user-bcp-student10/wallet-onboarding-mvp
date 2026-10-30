"""RS-2: el hash de la clave usa un pepper externo; una copia del almacén no permite probar candidatos (hallazgo H-SEC-4, issue #50)."""
import hashlib

from app.onboarding import hash_clave, verificar_clave

CLAVE = "482915"
ITERACIONES = 200_000


def _partes(almacenado):
    _, sal_hex, digest_hex = almacenado.split("$")
    return bytes.fromhex(sal_hex), digest_hex


def test_atacante_con_copia_del_almacen_no_reproduce_el_hash(monkeypatch):
    monkeypatch.setenv("PEPPER_CLAVE", "pepper-de-prueba-no-versionado")
    almacenado = hash_clave(CLAVE)
    sal, digest = _partes(almacenado)

    intento_sin_pepper = hashlib.pbkdf2_hmac("sha256", CLAVE.encode(), sal, ITERACIONES).hex()

    assert intento_sin_pepper != digest


def test_verificador_acepta_la_clave_correcta_y_rechaza_otra(monkeypatch):
    monkeypatch.setenv("PEPPER_CLAVE", "pepper-de-prueba-no-versionado")
    almacenado = hash_clave(CLAVE)

    assert verificar_clave(CLAVE, almacenado)
    assert not verificar_clave("482916", almacenado)


def test_pepper_distinto_no_verifica_la_clave(monkeypatch):
    monkeypatch.setenv("PEPPER_CLAVE", "pepper-original")
    almacenado = hash_clave(CLAVE)

    monkeypatch.setenv("PEPPER_CLAVE", "pepper-rotado")

    assert not verificar_clave(CLAVE, almacenado)
