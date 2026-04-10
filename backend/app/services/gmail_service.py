from datetime import datetime
from app.models.schemas import EmailDraft


class GmailService:
    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode
        self.sent_log: list[dict] = []

    def send_email(self, draft: EmailDraft) -> dict:
        entry = {
            "requestId": draft.requestId,
            "recipient": draft.recipient,
            "subject": draft.subject,
            "body": draft.body,
            "sentAt": datetime.utcnow().isoformat(),
        }
        self.sent_log.append(entry)
        return entry

    def draft_duplicate(self, request_id: str, recipient: str, code: str, short_desc: str, long_desc: str) -> EmailDraft:
        return EmailDraft(
            requestId=request_id,
            recipient=recipient,
            subject=f"ABG Duplicate Confirmation - {request_id}",
            body=f"Item already exists. ABG Material Number: {code}\nShort: {short_desc}\nLong: {long_desc}",
        )

    def draft_clarification(self, request_id: str, recipient: str, question: str) -> EmailDraft:
        return EmailDraft(
            requestId=request_id,
            recipient=recipient,
            subject=f"ABG Clarification Needed - {request_id}",
            body=question,
        )

    def draft_final(self, request_id: str, recipient: str, code: str, short_desc: str, long_desc: str) -> EmailDraft:
        return EmailDraft(
            requestId=request_id,
            recipient=recipient,
            subject=f"ABG Catalogued Result - {request_id}",
            body=f"Created ABG Material Number: {code}\nShort: {short_desc}\nLong: {long_desc}",
        )
