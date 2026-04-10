# ABG Web App MVP Preview

## UI flow preview

1. **Dashboard / Queue**
   - View active/completed request cases.
   - Open a case for review.

2. **Request Intake / Case Detail**
   - Create case with sender, subject, and raw dirty input.
   - Save and route to MDM-GPT analysis.

3. **MDM-GPT Match Results**
   - Inspect interpreted product, confidence, and candidate matches.
   - Branch actions:
     - Send duplicate response
     - Send clarification
     - Mark new-item required

4. **PROSOL Return + Finalization**
   - Enter manual PROSOL output (UNSPSC + descriptions).
   - Create master record, send final email, close case.

5. **Top-right controls**
   - Dark/Light mode toggle
   - Changelog modal (latest 5 entries + Show More)

## Quick API preview (mock mode)

```bash
# health
curl -s http://localhost:8000/health

# create case
curl -s -X POST http://localhost:8000/api/cases \
  -H 'Content-Type: application/json' \
  -H 'x-internal-key: dev-internal-key' \
  -d '{
    "requestId":"REQ-1001",
    "title":"ABG request",
    "senderEmail":"buyer@abg.example",
    "emailSubject":"Need hex bolt",
    "rawInputText":"Need hex bolt m8",
    "status":"New"
  }'

# run match
curl -s -X POST http://localhost:8000/api/cases/REQ-1001/match \
  -H 'x-internal-key: dev-internal-key'
```

## Notes
- This preview is optimized for local mock-mode demonstration.
- Live SharePoint/Gmail/MDM-GPT adapters remain behind backend service abstractions.
