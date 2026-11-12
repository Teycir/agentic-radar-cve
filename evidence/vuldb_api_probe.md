# VulDB API pre-check — 2026-11-12

Purpose: confirm the licence, prove the entry does not already exist, and determine whether
the key can submit. No writes were attempted beyond an operation-name probe that returns
"Unknown request" and has no side effects.

## Licence

| Field | Value |
|---|---|
| Endpoint | `POST https://vuldb.com/?api` (API v3.87) |
| API key | valid (32 hex chars, supplied by the reporter; stored at `~/.config/vuldb.env`, mode 600, never in this repo) |
| User ID | `102943` (account `teycirb`) |
| Plan | free — 50 queries per period |
| Remaining after checks | 42 |

Correct request shape: `apikey=…&query=search&search=<term>`.
`query=product:…` returns `405 Unknown request`; `query=submit` returns the same, which
confirms the API is read-only — an entry cannot be created through the key.

## Duplicate checks

| Search term | Items | Remaining |
|---|---|---|
| `agentic-radar` | 0 | 44 |
| `agentic_radar` | 0 | 43 |
| `splx-ai` | 0 | 42 |

Raw responses: `evidence/vuldb_api_search_*.json`

- `agentic-radar` — sha256 `be725836e0e05ae4978765fcadf8ee6ac03aab62b804c6b819e7cdb5e494e06f`
- `agentic_radar` — sha256 `498e68024adb7a78796f8cf81a511ab1b6c26262252a1576f0f32390a88f35a4`
- `splx-ai` — sha256 `cf8e888a8cd5eee39c7e687b7f3c63d058ef10ba52fb7d936d45cb05c81399d7`

No API key appears in any evidence file (verified with grep).

## Conclusion

- No prior VulDB entry for the package or the vendor as of 2026-11-12: the submission is not
  a duplicate.
- The key cannot create the entry. Submission must go through the web form at
  `https://vuldb.com/?submit` while logged in as `teycirb`.
- Field values, paste blocks and attachment order: `cna/vuldb-submission.md`.
