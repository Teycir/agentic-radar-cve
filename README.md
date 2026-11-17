# agentic-radar — OpenAI API key exfiltration via repository-controlled `.env`

`agentic-radar`'s `scan openai-agents` command sends the user's OpenAI API key to a host
named in a `.env` file that the scanned repository controls. No flag, prompt or warning.

| | |
|---|---|
| Package | `agentic-radar` (PyPI) |
| Source | `github.com/splx-ai/agentic-radar` |
| Audited | 0.14.1, commit `65a7e4bd01e2034c7cb52e9620eeed287688cc53` (2025-11-27) |
| Affected | `0.9.1` – `0.14.1` |
| Fixed in | RT-01 fixed in `0.14.2` (commit `b99bb14`, PR #134, 2026-11-13); RT-02 (langgraph crash) and RT-03 (report XSS) remain unfixed in `0.14.2` |
| Severity | High — CVSS 3.1 **7.4** `AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| CWE | CWE-15, CWE-522 |
| Reported by | Teycir ([github.com/Teycir](https://github.com/Teycir)) |
| Status | RT-01 fixed by vendor in 0.14.2; RT-02 and RT-03 still open. Submitted to VulDB (CNA), no CVE assigned yet. |

## Issue

`agentic_radar/cli.py:37` calls `load_dotenv()` at import time. The bundled deprecated
`dotenv` 0.9.9 package starts its search at the installed `agentic_radar` package directory
and walks upward, so when the tool is installed inside a checkout (in-repo `.venv`, editable
install — the layout of the project's own `examples/github_workflow/auto-agentic-radar.yaml`)
a `.env` from that repository is loaded. `scan openai-agents` then builds `openai.OpenAI()`
without validating `OPENAI_BASE_URL` and sends `chat.completions` requests, so the key lands
in `Authorization: Bearer` at the attacker's host.

## Reproduce

1. In an empty directory create `.env`:
   ```
   OPENAI_API_KEY=sk-DUMMY-DO-NOT-USE
   OPENAI_BASE_URL=http://localhost:8899/v1
   ```
2. `python3.12 -m venv .venv && .venv/bin/pip install "agentic-radar[openai-agents]==0.14.1"`
3. Start a loopback HTTP listener that logs request headers.
4. `cd / && OPENAI_API_KEY=sk-DUMMY-DO-NOT-USE /path/to/.venv/bin/agentic-radar scan openai-agents -i sample`

Expected: two `POST /v1/chat/completions` requests reach the listener with
`Authorization: Bearer sk-DUMMY-DO-NOT-USE`, and the scan exits 0.

## Scope

- **Affected:** 0.9.1 – 0.14.1 — 0.9.1 is the first release with both the import-time `.env`
  load and an unconditional LLM call in this analyzer.
- **Not affected:** installs outside the scanned repository (pipx, system-wide, standalone
  venv) — the upward search never reaches the repository `.env`. Verified control: 0 requests.
- **Not affected for this command:** 0.7.0 – 0.8.x — the only `chat.completions` call is
  behind the explicit `--enhance-prompts` flag.

## Fix

Vendor shipped (0.14.2, commit `b99bb14`, PR #134, 2026-11-13) — addresses RT-01 only:

- Removed import-time `load_dotenv()`; `.env` files load only via explicit `--env-file` (or `AGENTIC_RADAR_ENV_FILE`) on `scan`/`test`, with `override=False`.
- Added `tests/env_file_test.py` (import no longer calls `find_dotenv()`; cwd/input-dir `.env` is not loaded).

Not yet addressed (still present in 0.14.2):

- RT-02: `extract_imports_with_ast` still raises `UnboundLocalError` on unparsable `.py` (add `return []` after the parse-error branch).
- RT-03: `report.generate()` still emits unescaped graph names (Jinja env has no `autoescape`; library-only XSS). Add escaping / autoescape.

Recommendations not adopted: reject a non-default `OPENAI_BASE_URL` unless explicitly opted in, print the resolved base URL before sending prompts, and make LLM-backed analysis opt-in.

## Evidence

| Path | Contents |
|---|---|
| `cve-submission/advisory.md` | Full advisory: metadata, description, PoC, impact, fix |
| `cve-submission/range-verification.txt` | Per-release derivation of the affected range |
| `evidence/listener.log` | Captured requests with the dummy key |
| `evidence/scan_stdout.txt` | Scan output, exit 0, no warning |
| `evidence/rt01_negative_control_outside_venv.txt` | Negative control: 0 requests |
| `evidence/vendor_notice_20261112.eml` | Sent vendor notice, verbatim |
| `report_20261111_232106.md` | Full assessment report |
| `cve-submission/MANIFEST.txt` | sha256 of the submission pack |

## Disclosure

Vendor notified `2026-11-12T00:26:10Z` at `developers@splx.ai` (Cc `ante@splx.ai`), Message-ID
`<AFRc0PZKfwKA0vhEbrH5s_7PN2phfIT_Npa7V6UOuitZ2oW9wuXIzBpqdLiBiMVyeejORT-XWZPqE8FiPm-r6wiuAbsN720Pw0ISzMPDt6I=@protonmail.com>`,
no reply. Submitted to VulDB (CNA) and VulnCheck (CNA, submission ID `ba40600f-11e9-4afa-a1f0-53475fac6a6b`). No other CNAs. GitHub private
vulnerability reporting is disabled on the upstream repository.
