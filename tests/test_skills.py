"""Estructura de las skills de .github/skills (formato del curso: metadata, entradas, salida, restricciones,
reglas de validación, evidencia y ejemplos)."""
import re
from pathlib import Path

import pytest
import yaml

SKILLS = sorted((Path(__file__).resolve().parent.parent / ".github" / "skills").glob("*/SKILL.md"))
SECCIONES = ["Metadata", "Inputs", "Output", "Constraints", "Validation Rules", "Evidence"]


def test_hay_skills():
    assert SKILLS


@pytest.mark.parametrize("ruta", SKILLS, ids=lambda r: r.parent.name)
def test_skill_tiene_frontmatter_secciones_y_ejemplos(ruta):
    texto = ruta.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.DOTALL)
    assert m, "falta el frontmatter"
    meta = yaml.safe_load(m.group(1))
    assert meta["name"] == ruta.parent.name
    assert len(meta["description"]) >= 80, "la descripción decide cuándo se activa: debe ser explícita"
    titulos = re.findall(r"^## \d+\) (.+)$", texto, re.MULTILINE)
    for seccion in SECCIONES:
        assert seccion in titulos, f"falta la sección {seccion}"
    assert re.search(r"\*\*Version:\*\* \d+\.\d+\.\d+", texto)
    for ejemplo in ("input.sample.md", "output.sample.md"):
        assert (ruta.parent / "examples" / ejemplo).is_file(), f"falta examples/{ejemplo}"
