from app.utils.normalization import normalize_text, build_normalized_match_key, build_description_search_text


def test_normalization_helpers():
    assert normalize_text("Bolt, m8!!") == "BOLT M8"
    assert build_normalized_match_key("M8 Bolt", "Galvanized") == "BOLT GALVANIZED M8"
    assert "HEX" in build_description_search_text("Hex", "Bolt")
