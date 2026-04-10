from .normalization import extract_suffix


def validate_long_description(value: str, max_len: int = 2048) -> None:
    if len(value) > max_len:
        raise ValueError(f"LongDescription exceeds limit ({max_len})")


def validate_abg_material_code(code: str) -> None:
    if len(code) != 12:
        raise ValueError("ABG material code must be 12 characters")
    if not code[:8].isdigit():
        raise ValueError("ABG material code must start with 8 digit UNSPSC")
    if not code[-4:].isalnum():
        raise ValueError("ABG suffix must be 4 alphanumeric chars")


def enforce_duplicate_rule(confidence: float) -> bool:
    return confidence == 100


def suffix_from_code(code: str) -> str:
    validate_abg_material_code(code)
    return extract_suffix(code)
