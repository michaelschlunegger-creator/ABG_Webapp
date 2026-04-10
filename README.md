# ABG Web App (MVP)

ABG Web App is an internal AI-assisted cataloguing workflow system where the cataloguer remains the final decision maker.

## Architecture overview
- **Frontend (React + Tailwind):** workflow-first UI, dark mode toggle, changelog modal.
- **Backend (FastAPI):** orchestrates case workflow, MDM-GPT matching, Gmail draft/send, SharePoint read/write abstractions.
- **Source of truth:** SharePoint lists `ABG_Master_Reference` and `ABG_Cataloguing_Request_Log`.
- **PROSOL:** manual-only process; no direct integration.

## Project structure
- `backend/` FastAPI app, domain models, services, routers, tests
- `frontend/` React + Tailwind app
- `shared/` shared contract documentation
- `docs/` architecture notes
- `scripts/` SharePoint foundation scripts

## Setup instructions
1. Copy `.env.example` to `.env` and fill values.
2. Backend:
   - `cd backend`
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -e .[test]`
   - `uvicorn app.main:app --reload --port 8000`
3. Frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## Local development
- Backend health: `GET http://localhost:8000/health` with header `x-internal-key`.
- Frontend: `http://localhost:5173`.
- In mock mode (`MOCK_MODE=true`), SharePoint/Gmail/MDM-GPT are simulated for end-to-end demos.

## SharePoint integration
- Typed mapping layer in `backend/app/services/sharepoint_mapping.py` decouples internal models from SharePoint columns.
- Handles blank/missing values, Yes/No normalization, date parsing, schema drift safety.
- New master records follow required field population defaults and preserve legacy compatibility.

## Gmail integration
- Backend service `gmail_service.py` supports draft generation for duplicate/clarification/final-result emails.
- Sending is explicit user action via workflow routes; no automatic uncontrolled sends.
- Sent email log captures recipient, subject, body, sent date, and request ID.

## MDM-GPT integration
- Backend service `mdm_gpt_service.py` receives case input and candidate context.
- Returns structured output contract for interpreted product, confidence, candidates, reasoning, and branch indicators.
- Failures are surfaced to UI and route responses for retry.

## Implementation assumptions
- Live SharePoint/Gmail/MDM-GPT integrations are environment-dependent; mock mode is default for reliable local demo.
- Existing SharePoint auth foundation is represented by `scripts/import_abg_master_live.py` and aligned field contracts.
- Internal auth uses a simple header key pattern (`x-internal-key`) for MVP internal usage.
- Case IDs are provided by user/UI at intake in MVP (instead of automated mailbox ingestion IDs).
- Long description maximum validation defaults to 2048 chars unless configured.

## Known limitations
- Live SharePoint/Gmail connectors are abstracted but not fully wired to production SDK endpoints in this MVP.
- Incoming Gmail polling/webhook intake is not implemented; intake currently manual through UI/API.
- No persistent local database; mock state is in-memory and resets on backend restart.

## Deployment notes
- Deploy backend and frontend separately (container or internal VM).
- Provide env vars via secret manager.
- Set `MOCK_MODE=false` and implement concrete adapters in service layer for production credentials.


## Preview
- See `docs/preview.md` for a walkthrough and sample API calls.
