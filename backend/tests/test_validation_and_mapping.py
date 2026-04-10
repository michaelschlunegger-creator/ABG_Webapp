import pytest
from app.utils.validation import enforce_duplicate_rule, validate_long_description
from app.services.sharepoint_mapping import from_sharepoint_row, to_sharepoint_row
from app.models.schemas import MasterReferenceRecord


def test_duplicate_rule():
    assert enforce_duplicate_rule(100)
    assert not enforce_duplicate_rule(99.9)


def test_long_description_limit():
    with pytest.raises(ValueError):
        validate_long_description("x" * 3000, max_len=1000)


def test_parse_master_row_with_blanks_and_legacy_unspsc():
    row = {
        "ABGMaterialcode": "231215010011",
        "UNSPSC": "",
        "ABGSuffix": "0011",
        "ShortDescription": "HEX BOLT",
        "LongDescription": "HEX BOLT M8",
        "IsActive": "Yes",
    }
    rec = from_sharepoint_row(row)
    assert rec.unspsc is None
    assert rec.abgMaterialCode == "231215010011"
    assert rec.isActive is True


def test_to_sharepoint_row_schema_generation():
    rec = MasterReferenceRecord(
        abgMaterialCode="12345678a1b2",
        unspsc="12345678",
        abgSuffix="a1b2",
        shortDescription="SHORT",
        longDescription="LONG",
    )
    row = to_sharepoint_row(rec)
    assert row["ABGMaterialcode"] == "12345678a1b2"
    assert row["RecordTitle"] == "12345678a1b2"
