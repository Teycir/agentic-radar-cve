# VulDB submission — fast lane

VulDB is a CVE CNA and accepts researcher submissions directly. No maintainer action is
required, which is the whole point: the GitHub CNA route is closed on this repository
(private vulnerability reporting disabled).

**Vendor notice already sent 2026-11-12** by email via Proton Mail to `developers@splx.ai`
(Cc `ante@splx.ai`), 10-business-day deadline `2026-11-26`. No reply at submission time.

Entry point: `https://vuldb.com/?submit` (free account required, confirm the email).

## Step 0 — prerequisites

- Register at `vuldb.com`, confirm the address, log in. Use the Proton address so CNA
  correspondence reaches the same mailbox that holds the vendor email.
- Have these files open locally: `cve-submission/advisory.md`,
  `cve-submission/pocs/exfil_listener.py`, `evidence/listener.log`.
- Do not wait for the vendor. VulDB is the notice-of-record for the CVE, the email is the
  notice-of-record for coordination.

## Step 1 — start the entry

`vuldb.com` → log in → submit/add entry (`vuldb.com/?submit`). Choose a **vulnerability**
entry, not a product or an advisory. If the vendor/product does not exist yet, enter the
names as free text; VulDB creates them and links the entry.

## Step 2 — identity fields

| Field | Value |
|---|---|
| Vendor | `SplxAI` (accept `splx-ai` if it already exists) |
| Product | `agentic-radar` |
| Affected version | `0.9.1` through `0.14.1` |
| Fixed version | none — `0.14.1` is latest and remains affected |
| Platform | Python / PyPI |
| CPE | skip; no CPE applies to a PyPI-only package |

## Step 3 — classification

- Primary CWE: **CWE-15** — External Control of System or Configuration Setting
- Secondary: **CWE-522** — Insufficiently Protected Credentials
- Attack vector: remote, no attacker authentication, victim must run the scanner
- User interaction: yes

## Step 4 — CVSS 3.1

Submit **7.4** with vector `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N`.

If the form only accepts base metrics: `AV:N / AC:L / PR:N / UI:R / S:C / C:H / I:N / A:N`.

Scope is changed because the credential belongs to the victim's OpenAI organisation, not to
the tool. If the CNA re-scores to `S:U` (6.5), accept it without argument.

## Step 5 — title (paste)

```
agentic-radar: OPENAI_BASE_URL injection via repository .env leads to API key exfiltration
```

## Step 6 — description (paste)

```
agentic-radar (PyPI) loads environment variables at import time with load_dotenv()
(agentic_radar/cli.py:37 in 0.14.1). python-dotenv's default search begins at the installed
package directory and walks up the directory tree, so a .env file placed in or above
site-packages is read. When the package is installed inside a checked-out repository - the
layout used by the project's own examples/github_workflow/auto-agentic-radar.yaml - a .env
committed to that repository is loaded into the process environment.

The scan command "agentic-radar scan openai-agents" constructs an OpenAI client and sends
chat.completions requests without validating OPENAI_BASE_URL. A repository author who
controls that .env can set OPENAI_BASE_URL to a host they operate and receive the
"Authorization: Bearer" header containing the victim's OPENAI_API_KEY.

Reproduction (0.14.1, Python 3.12):
1. clone a repository containing .env with OPENAI_API_KEY=sk-DUMMY-DO-NOT-USE and
   OPENAI_BASE_URL=http://127.0.0.1:8899/v1
2. python -m venv .venv && .venv/bin/pip install agentic-radar==0.14.1
3. start a loopback HTTP listener that logs request headers
4. .venv/bin/agentic-radar scan openai-agents

Result: two POST /v1/chat/completions requests arrive carrying the key in the Authorization
header, and the scan exits 0. A control install of the same version in a virtualenv outside
the repository issues no requests to the listener, which bounds exposure to in-tree or
editable installs.

Affected: >=0.9.1, <=0.14.1. 0.9.1 is the first release containing both the import-time
load_dotenv() call and the unconditional OpenAI request in the openai-agents analyzer.
Fixed: none; 0.14.1 is the latest release and remains affected.

Impact: disclosure of the user's OpenAI API key, and any other credential the tool forwards,
to the author of the repository being scanned. Scanning third-party or untrusted code is the
tool's intended use case.

Suggested fix: remove the import-time load_dotenv() call or restrict it to the package
directory; require an explicit opt-in before honouring a non-default OPENAI_BASE_URL; do not
load .env from the scanned tree.
```

## Step 7 — timeline (paste)

```
2026-11-12: reported to the vendor by email (developers@splx.ai, Cc ante@splx.ai). No
private reporting channel exists on the repository: private vulnerability reporting is
disabled and there is no SECURITY.md.
2026-11-12: no reply at time of submission; no fix available.
```

## Step 8 — credit and references

Credit: `Teycir (https://github.com/Teycir)`

```
https://pypi.org/project/agentic-radar/
https://github.com/splx-ai/agentic-radar
https://github.com/splx-ai/agentic-radar/tree/65a7e4bd01e2034c7cb52e9620eeed287688cc53
https://github.com/theskumar/python-dotenv
Reporter bundle (full report, evidence, reproducer): https://github.com/Teycir/agentic-radar-cve
```
The bundle is private; state "available to the CNA on request" if the form rejects the link.

## Step 9 — attachments

Attach, in this order:

1. `cve-submission/advisory.md`
2. `evidence/listener.log` — the captured request showing the Authorization header and UTC
   timestamps
3. `cve-submission/pocs/exfil_listener.py`

Both affected and control runs are in the advisory; attach nothing that contains a real key.
The only credential in the bundle is `sk-DUMMY-DO-NOT-USE`.

## Step 10 — record it

On submit, capture the VDB ID and the confirmation page. Add to `contact-log.md`:

- CNA row 1: UTC time, `VulDB`, tracking number `VDB-xxxxxx`, status `submitted`
- Assigned IDs: nothing yet

## Expectations and handling

- Entry review: roughly 1–3 days. The CVE ID follows acceptance, typically days to ~3 weeks.
  There is no separate CVE request form; the entry is the request.
- VulDB may publish a VDB entry before the CVE record exists. Normal, does not block the CVE.
- They may re-score CVSS. Accept the CNA score.
- If they ask for vendor confirmation, reply with the contact log and the 2026-11-26 deadline.
- If rejected as not-a-vulnerability or duplicate: do not argue more than once. At
  `2026-11-26`, file MITRE per `cna/mitre-submission.md`.
- A VDB ID is not a CVE. Only a `CVE-YYYY-NNNNN` counts.
- Do not file MITRE while VulDB is pending and before 2026-11-26 — two parallel CNAs can
  produce duplicate IDs.
