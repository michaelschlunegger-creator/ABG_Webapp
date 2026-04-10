from app.services.material_code_service import MaterialCodeService
from app.utils.validation import validate_abg_material_code, suffix_from_code


def test_generate_unique_material_code():
    existing = {"12345678aaaa"}
    svc = MaterialCodeService(lambda c: c in existing)
    code = svc.generate_unique("12345678")
    assert len(code) == 12
    assert code[:8] == "12345678"
    validate_abg_material_code(code)


def test_suffix_extraction():
    assert suffix_from_code("12345678a1b2") == "a1b2"
