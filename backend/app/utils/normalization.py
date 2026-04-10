import re


def normalize_text(value: str) -> str:
    value = value.upper()
    value = re.sub(r"[^A-Z0-9\s-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def build_description_search_text(short_description: str, long_description: str) -> str:
    return normalize_text(f"{short_description} {long_description}")


def build_normalized_match_key(*parts: str) -> str:
    tokens: list[str] = []
    for part in parts:
        tokens.extend(normalize_text(part).split())
    tokens = sorted([t for t in tokens if t])
    return " ".join(tokens)


def extract_suffix(abg_material_code: str) -> str:
    return abg_material_code[-4:]
