from app.models.schemas import MatchResult, CandidateMatch


class MDMGPTService:
    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode

    def analyze(self, case_id: str, raw_dirty_text: str, candidate_reference_data: list[CandidateMatch], optional_context: str | None = None) -> MatchResult:
        text = raw_dirty_text.lower()
        if "hex bolt" in text and candidate_reference_data:
            best = candidate_reference_data[0]
            return MatchResult(
                interpreted_product="Hex bolt",
                extracted_attributes={"family": "Bolt"},
                duplicate_found=True,
                duplicate_confidence=100,
                best_match_code=best.abgMaterialCode,
                candidate_matches=candidate_reference_data,
                reasoning="Exact match on core product tokens and dimensions.",
                clarification_needed=False,
                likely_new_item=False,
            )
        if "unknown" in text or "?" in text:
            return MatchResult(
                interpreted_product="Ambiguous industrial component",
                extracted_attributes={"requires": "clarification"},
                duplicate_found=False,
                duplicate_confidence=62,
                best_match_code=None,
                candidate_matches=candidate_reference_data,
                reasoning="Insufficient precision in input details.",
                clarification_needed=True,
                likely_new_item=False,
            )
        return MatchResult(
            interpreted_product="Potential new catalog item",
            extracted_attributes={"signal": "new"},
            duplicate_found=False,
            duplicate_confidence=24,
            best_match_code=None,
            candidate_matches=candidate_reference_data,
            reasoning="No high-confidence duplicate candidate.",
            clarification_needed=False,
            likely_new_item=True,
        )
