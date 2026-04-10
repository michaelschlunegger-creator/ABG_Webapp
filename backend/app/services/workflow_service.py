from datetime import datetime
from app.models.schemas import CaseRecord, CaseStatus, MatchResult, ProsolReturnInput
from app.utils.validation import enforce_duplicate_rule, validate_long_description


class WorkflowService:
    def __init__(self, sharepoint, mdm_gpt, gmail, material_codes):
        self.sharepoint = sharepoint
        self.mdm_gpt = mdm_gpt
        self.gmail = gmail
        self.material_codes = material_codes

    def run_match(self, request_id: str) -> MatchResult:
        case = self._must_case(request_id)
        candidates = self.sharepoint.list_master_candidates(case.rawInputText)
        result = self.mdm_gpt.analyze(case.requestId, case.rawInputText, candidates)
        case.status = CaseStatus.IN_REVIEW
        case.mdmgptInterpretation = result.interpreted_product
        case.matchConfidence = result.duplicate_confidence
        case.candidateMatches = result.candidate_matches
        if result.duplicate_found and result.duplicate_confidence == 100 and result.best_match_code:
            case.status = CaseStatus.DUPLICATE_FOUND
            case.duplicateABGMaterialCode = result.best_match_code
        self.sharepoint.save_case(case)
        return result

    def send_duplicate(self, request_id: str):
        case = self._must_case(request_id)
        if not enforce_duplicate_rule(case.matchConfidence or 0):
            raise ValueError("Only 100% duplicate confidence can be closed as duplicate")
        match = next((m for m in case.candidateMatches if m.abgMaterialCode == case.duplicateABGMaterialCode), None)
        if not match:
            raise ValueError("Duplicate match details unavailable")
        draft = self.gmail.draft_duplicate(case.requestId, case.senderEmail, match.abgMaterialCode, match.shortDescription, match.longDescription)
        sent = self.gmail.send_email(draft)
        case.status = CaseStatus.DUPLICATE_SENT
        case.finalEmailSentDate = datetime.utcnow()
        case.status = CaseStatus.CLOSED
        case.closedDate = datetime.utcnow()
        self.sharepoint.save_case(case)
        return sent

    def send_clarification(self, request_id: str, question: str):
        case = self._must_case(request_id)
        case.clarificationQuestion = question
        draft = self.gmail.draft_clarification(case.requestId, case.senderEmail, question)
        sent = self.gmail.send_email(draft)
        case.status = CaseStatus.CLARIFICATION_NEEDED
        self.sharepoint.save_case(case)
        return sent

    def mark_new_item_required(self, request_id: str):
        case = self._must_case(request_id)
        case.status = CaseStatus.NEW_RECORD_REQUIRED
        case.needsPROSOL = True
        self.sharepoint.save_case(case)
        return case

    def submit_prosol(self, request_id: str, payload: ProsolReturnInput):
        case = self._must_case(request_id)
        validate_long_description(payload.longDescription)
        case.unspsc = payload.unspsc
        case.finalShortDescription = payload.shortDescription
        case.finalLongDescription = payload.longDescription
        case.cataloguerNote = payload.internalNote
        case.status = CaseStatus.PROSOL_COMPLETED
        self.sharepoint.save_case(case)
        return case

    def create_master_and_send(self, request_id: str):
        case = self._must_case(request_id)
        if not all([case.unspsc, case.finalShortDescription, case.finalLongDescription]):
            raise ValueError("PROSOL result incomplete")
        code = self.material_codes.generate_unique(case.unspsc)
        record = self.sharepoint.build_new_master_record(code, case.unspsc, case.finalShortDescription, case.finalLongDescription)
        self.sharepoint.create_master_record(record)
        case.newABGMaterialCode = code
        case.status = CaseStatus.CREATED_IN_MASTER
        draft = self.gmail.draft_final(case.requestId, case.senderEmail, code, case.finalShortDescription, case.finalLongDescription)
        sent = self.gmail.send_email(draft)
        case.finalEmailSentDate = datetime.utcnow()
        case.status = CaseStatus.CLOSED
        case.closedDate = datetime.utcnow()
        self.sharepoint.save_case(case)
        return {"record": record, "email": sent, "case": case}

    def _must_case(self, request_id: str) -> CaseRecord:
        case = self.sharepoint.get_case(request_id)
        if not case:
            raise ValueError("Case not found")
        return case
