from __future__ import annotations

from datetime import datetime
from app.models.schemas import CaseRecord, MasterReferenceRecord, CandidateMatch
from app.services.sharepoint_mapping import from_sharepoint_row, to_sharepoint_row
from app.utils.normalization import build_description_search_text, build_normalized_match_key


class SharePointService:
    """Service abstraction; mock storage by default. Live extension should reuse scripts/import_abg_master_live.py auth patterns."""

    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode
        self._master: dict[str, MasterReferenceRecord] = {}
        self._cases: dict[str, CaseRecord] = {}
        self._seed()

    def _seed(self):
        rec = MasterReferenceRecord(
            recordTitle="231215010011",
            abgMaterialCode="231215010011",
            unspsc="23121501",
            abgSuffix="0011",
            shortDescription="HEX BOLT M8",
            longDescription="Hex bolt galvanized m8 x 25",
            isActive=True,
            dataSource="Legacy Import",
            reviewStatus="Approved",
            abgCodeKey="231215010011",
            descriptionSearchText="HEX BOLT GALVANIZED M8 X 25",
            normalizedMatchKey="25 BOLT GALVANIZED HEX M8 X",
            importStatus="Imported",
            importNote="Seed",
            lastUpdatedDate=datetime.utcnow(),
        )
        self._master[rec.abgMaterialCode] = rec

    def list_cases(self) -> list[CaseRecord]:
        return sorted(self._cases.values(), key=lambda x: x.createdDate, reverse=True)

    def get_case(self, request_id: str) -> CaseRecord | None:
        return self._cases.get(request_id)

    def save_case(self, case: CaseRecord) -> CaseRecord:
        case.lastUpdatedDate = datetime.utcnow()
        self._cases[case.requestId] = case
        return case

    def list_master_candidates(self, query: str, limit: int = 15) -> list[CandidateMatch]:
        q = query.upper()
        matches: list[CandidateMatch] = []
        for r in self._master.values():
            text = f"{r.shortDescription} {r.longDescription} {r.normalizedMatchKey or ''} {r.abgCodeKey or ''}".upper()
            if any(token in text for token in q.split() if token):
                matches.append(CandidateMatch(
                    abgMaterialCode=r.abgMaterialCode,
                    shortDescription=r.shortDescription,
                    longDescription=r.longDescription,
                    unspsc=r.unspsc,
                    abgSuffix=r.abgSuffix,
                    reviewStatus=r.reviewStatus,
                    isActive=r.isActive,
                ))
        return matches[:limit]

    def material_code_exists(self, code: str) -> bool:
        return code in self._master

    def create_master_record(self, record: MasterReferenceRecord) -> MasterReferenceRecord:
        row = to_sharepoint_row(record)
        parsed = from_sharepoint_row(row)
        self._master[parsed.abgMaterialCode] = parsed
        return parsed

    def build_new_master_record(self, abg_code: str, unspsc: str, short_desc: str, long_desc: str) -> MasterReferenceRecord:
        now = datetime.utcnow()
        return MasterReferenceRecord(
            recordTitle=abg_code,
            abgMaterialCode=abg_code,
            unspsc=unspsc,
            abgSuffix=abg_code[-4:],
            shortDescription=short_desc,
            longDescription=long_desc,
            isActive=True,
            lastUpdatedDate=now,
            normalizedMatchKey=build_normalized_match_key(short_desc, long_desc),
            dataSource="ABG Web App",
            reviewStatus="Approved",
            abgCodeKey=abg_code,
            descriptionSearchText=build_description_search_text(short_desc, long_desc),
            importStatus="Created",
            importNote="Created by ABG Web App MVP",
        )
