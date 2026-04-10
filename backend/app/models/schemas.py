from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Any


class CaseStatus(str, Enum):
    NEW = "New"
    IN_REVIEW = "In Review"
    DUPLICATE_FOUND = "Duplicate Found"
    DUPLICATE_SENT = "Duplicate Sent to ABG"
    CLARIFICATION_NEEDED = "Clarification Needed"
    CLARIFICATION_RECEIVED = "Clarification Received"
    NEW_RECORD_REQUIRED = "New Record Required"
    IN_PROSOL = "In PROSOL"
    PROSOL_COMPLETED = "PROSOL Completed"
    CREATED_IN_MASTER = "Created in Master"
    CLOSED = "Closed"


class MasterReferenceRecord(BaseModel):
    recordTitle: str | None = None
    sourceRowId: str | None = None
    abgMaterialCode: str
    unspsc: str | None = None
    abgSuffix: str | None = None
    shortDescription: str
    longDescription: str
    isActive: bool = True
    lastUpdatedDate: datetime | None = None
    normalizedMatchKey: str | None = None
    importBatchId: str | None = None
    dataSource: str | None = None
    reviewStatus: str | None = None
    abgCodeKey: str | None = None
    descriptionSearchText: str | None = None
    importStatus: str | None = None
    importNote: str | None = None


class CandidateMatch(BaseModel):
    abgMaterialCode: str
    shortDescription: str
    longDescription: str
    unspsc: str | None = None
    abgSuffix: str | None = None
    reviewStatus: str | None = None
    isActive: bool | None = None
    confidence: float | None = None


class MatchResult(BaseModel):
    interpreted_product: str
    extracted_attributes: dict[str, Any]
    duplicate_found: bool
    duplicate_confidence: float = Field(ge=0, le=100)
    best_match_code: str | None = None
    candidate_matches: list[CandidateMatch] = Field(default_factory=list)
    reasoning: str
    clarification_needed: bool
    likely_new_item: bool


class CaseRecord(BaseModel):
    requestId: str
    title: str
    status: CaseStatus = CaseStatus.NEW
    senderEmail: str
    emailSubject: str
    rawInputText: str
    mdmgptInterpretation: str | None = None
    matchConfidence: float | None = None
    candidateMatches: list[CandidateMatch] = Field(default_factory=list)
    duplicateABGMaterialCode: str | None = None
    clarificationQuestion: str | None = None
    clarificationResponse: str | None = None
    needsPROSOL: bool = False
    unspsc: str | None = None
    finalShortDescription: str | None = None
    finalLongDescription: str | None = None
    newABGMaterialCode: str | None = None
    cataloguerNote: str | None = None
    assignedTo: str | None = None
    createdDate: datetime = Field(default_factory=datetime.utcnow)
    lastUpdatedDate: datetime = Field(default_factory=datetime.utcnow)
    finalEmailSentDate: datetime | None = None
    closedDate: datetime | None = None


class EmailDraft(BaseModel):
    requestId: str
    recipient: str
    subject: str
    body: str


class ProsolReturnInput(BaseModel):
    unspsc: str
    shortDescription: str
    longDescription: str
    internalNote: str | None = None

    @field_validator("unspsc")
    @classmethod
    def validate_unspsc(cls, v: str) -> str:
        if len(v) != 8 or not v.isdigit():
            raise ValueError("UNSPSC must be exactly 8 digits")
        return v


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict[str, Any] | None = None
