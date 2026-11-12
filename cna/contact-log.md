# Contact log — fill as you go, UTC only

Every row is evidence. MITRE and CERT/CC both ask for this, and a complete log is the
difference between "researcher with a complaint" and "researcher with a case".

## Vendor

| # | UTC timestamp | Channel | From → To | Subject / summary | Message-ID or URL | Reply |
|---|---|---|---|---|---|---|
| 1 |  | GitHub private advisory | — | **Unavailable**: private vulnerability reporting disabled, no Security tab, `advisories/new` cannot be opened | — | n/a |
| 2 | 2026-11-12T00:26:10Z | Email | teycir@protonmail.com → developers@splx.ai (Cc ante@splx.ai) | Security report: agentic-radar reads repo .env and redirects your OpenAI key | `<AFRc0PZKfwKA0vhEbrH5s_7PN2phfIT_Npa7V6UOuitZ2oW9wuXIzBpqdLiBiMVyeejORT-XWZPqE8FiPm-r6wiuAbsN720Pw0ISzMPDt6I=@protonmail.com>` | no reply |
| 3 |  | Email |  | Deadline reminder / bounce note |  |  |

Rules:

- One row per message, including bounces and auto-replies.
- Record the Message-ID header, not just the timestamp. Gmail: "Show original".
- If there is no reply, write `no reply` in the Reply column. Silence is the finding.

## CNA submissions

| # | UTC timestamp | CNA | Channel | Tracking number | Status |
|---|---|---|---|---|---|
| 1 |  | VulDB | vuldb.com/?submit |  |  |
| 2 |  | MITRE | cveform.mitre.org |  |  |
| 3 |  | CERT/CC | kb.cert.org/vince |  |  |
| 4 | — | GitHub | N/A — PVR disabled, no advisory possible, GitHub CNA cannot assign | — | not applicable |

## Assigned IDs

| ID | CNA | Assigned at (UTC) | Canonical | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Deadline arithmetic

- Vendor notice: **sent** `2026-11-12T00:26:10Z` (Thu). Message-ID
  `<AFRc0PZKfwKA0vhEbrH5s_7PN2phfIT_Npa7V6UOuitZ2oW9wuXIzBpqdLiBiMVyeejORT-XWZPqE8FiPm-r6wiuAbsN720Pw0ISzMPDt6I=@protonmail.com>`,
  carried in `Security report_ agentic-radar reads repo .env and redirects your OpenAI key
  2026-11-12T01_26_10+01_00.eml`. HTML-only body, no attachments, no bounce observed.
- 10 business days: `2026-11-26 (Thu)` — **do not** file MITRE on this date. VulDB's form
  states moderation ≈ 6 weeks, and the CVE checkbox attests the issue was not submitted to
  another CNA. Parallel filing breaks that attestation and risks duplicate IDs. MITRE is a
  fallback only after a VulDB reject or a written refusal.
- 45 days: `2026-12-27 (Sun)` — CERT/CC window, public disclosure eligible
- 90 days: `2027-02-10 (Wed)` — hard limit; publish regardless of vendor

## VulDB API pre-check (2026-11-12)

- Key valid, userid `102943`, free plan, 42/50 queries left.
- `query=search` for `agentic-radar`, `agentic_radar`, `splx-ai`: 0 items each — not a duplicate.
- `query=submit`: `405 Unknown request` — API is read-only, entry needs the web form.
- Evidence: `evidence/vuldb_api_probe.md`, `evidence/vuldb_api_search_*.json`.

## Evidence: outbound notice

- `evidence/vendor_notice_20261112.eml` — verbatim copy of the sent message, 5278 bytes,
  sha256 `c00af2a647c7961d716a0e7704af2b1ee4b7d484ab656175bfd7ed574ccfc149`.
- Headers of record: `Date: Thu, 12 Nov 2026 00:26:10 +0000`,
  `From: teycir <teycir@protonmail.com>`, `To: developers@splx.ai`, `Cc: ante@splx.ai`,
  subject `Security report: agentic-radar reads repo .env and redirects your OpenAI key`.
- Proton transport headers present (`X-Pm-Origin: internal`,
  `X-Pm-Recipient-Authentication: developers%40splx.ai=none; ante%40splx.ai=none`) — confirms
  outbound delivery by the provider, not a draft. No originating-IP or DKIM header in the copy.
- Body is HTML-only (2989 bytes), no attachments. No bounce observed.
