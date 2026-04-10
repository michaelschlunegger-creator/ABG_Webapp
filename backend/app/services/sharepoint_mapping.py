from datetime import datetime
from app.models.schemas import MasterReferenceRecord


TRUE_VALUES = {"yes", "true", "1", True}


def parse_bool(v):
    if v is None:
        return False
    return str(v).strip().lower() in TRUE_VALUES


def parse_dt(v):
    if not v:
        return None
    try:
        return datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except Exception:
        return None


def from_sharepoint_row(row: dict) -> MasterReferenceRecord:
    return MasterReferenceRecord(
        recordTitle=row.get("RecordTitle"),
        sourceRowId=row.get("SourceRowID"),
        abgMaterialCode=row.get("ABGMaterialcode", ""),
        unspsc=row.get("UNSPSC") or None,
        abgSuffix=row.get("ABGSuffix") or None,
        shortDescription=row.get("ShortDescription", ""),
        longDescription=row.get("LongDescription", ""),
        isActive=parse_bool(row.get("IsActive")),
        lastUpdatedDate=parse_dt(row.get("LastUpdatedDate")),
        normalizedMatchKey=row.get("NormalizedMatchKey") or None,
        importBatchId=row.get("ImportBatchID") or None,
        dataSource=row.get("DataSource") or None,
        reviewStatus=row.get("ReviewStatus") or None,
        abgCodeKey=row.get("ABGCodeKey") or None,
        descriptionSearchText=row.get("DescriptionSearchText") or None,
        importStatus=row.get("ImportStatus") or None,
        importNote=row.get("ImportNote") or None,
    )


def to_sharepoint_row(record: MasterReferenceRecord) -> dict:
    return {
        "RecordTitle": record.recordTitle or record.abgMaterialCode,
        "SourceRowID": record.sourceRowId,
        "ABGMaterialcode": record.abgMaterialCode,
        "UNSPSC": record.unspsc,
        "ABGSuffix": record.abgSuffix,
        "ShortDescription": record.shortDescription,
        "LongDescription": record.longDescription,
        "IsActive": "Yes" if record.isActive else "No",
        "LastUpdatedDate": (record.lastUpdatedDate or datetime.utcnow()).isoformat(),
        "NormalizedMatchKey": record.normalizedMatchKey,
        "ImportBatchID": record.importBatchId,
        "DataSource": record.dataSource,
        "ReviewStatus": record.reviewStatus,
        "ABGCodeKey": record.abgCodeKey,
        "DescriptionSearchText": record.descriptionSearchText,
        "ImportStatus": record.importStatus,
        "ImportNote": record.importNote,
    }
