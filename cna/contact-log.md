# Contact log — fill as you go, UTC only

Every row is evidence. MITRE and CERT/CC both ask for this, and a complete log is the
difference between "researcher with a complaint" and "researcher with a case".

## Vendor

| # | UTC timestamp | Channel | From → To | Subject / summary | Message-ID or URL | Reply |
|---|---|---|---|---|---|---|
| 1 |  | GitHub private advisory | — | **Unavailable**: private vulnerability reporting disabled, no Security tab, `advisories/new` cannot be opened | — | n/a |
| 2 |  | Email | teycir@gmail.com → developers@splx.ai (Cc ante@splx.ai) | Security report: agentic-radar <=0.14.1 |  |  |
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

- Vendor notice sent: `2026-11-12 (Thu)`
- 10 business days: `2026-11-26 (Thu)` — file MITRE if VulDB has not assigned
- 45 days: `2026-12-27 (Sun)` — CERT/CC window, public disclosure eligible
- 90 days: `2027-02-10 (Wed)` — hard limit; publish regardless of vendor
