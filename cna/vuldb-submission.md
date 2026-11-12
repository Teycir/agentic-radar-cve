# VulDB submission — fast lane

VulDB is a CVE CNA and accepts submissions from researchers directly. No maintainer action
is required. This is the fastest independent path; file it the same day as the vendor notice.

Entry point: `https://vuldb.com/?submit` (free account required).

## Fields

| Field | Value |
|---|---|
| Product | agentic-radar |
| Vendor | SplxAI |
| Version | 0.9.1 – 0.14.1 |
| Vulnerability class | CWE-15 (external control of configuration) / CWE-522 (credential exposure) |
| Attack vector | Remote, requires the victim to run the scanner on an untrusted repository |
| Authentication | None for the attacker |
| User interaction | Yes — victim runs `agentic-radar scan openai-agents` |
| Impact | Disclosure of the user's OpenAI API key |
| CVSS 3.1 | 7.4 `AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| CVE requested | Yes |
| Disclosure status | Vendor notified, unresponsive → coordinate with submitter |

Title:

```
agentic-radar: OPENAI_BASE_URL injection via repository .env leads to API key exfiltration
```

Description:

```
The PyPI package agentic-radar calls load_dotenv() at import time. python-dotenv's default
search starts at the installed package directory and walks upward, so a .env committed to the
repository in which the package is installed is loaded. The tool does not validate
OPENAI_BASE_URL and sends chat.completions requests, carrying the user's OPENAI_API_KEY, to
whatever host that variable names. A repository author can therefore redirect the key to a
server they control. Reproduced on 0.14.1; a standalone install outside the repository is not
affected.
```

## Attachments

- `advisory.md` (full technical report)
- `pocs/exfil_listener.py`
- Listener log with the captured request and UTC timestamps

## Handling

- VulDB may publish an entry before the CVE record appears. That is expected and does not
  block the CVE.
- They may re-score the CVSS. Accept the CNA score; do not argue about one or two tenths.
- If they ask for vendor confirmation, reply with the contact log showing the deadline passed.
- If VulDB assigns an ID, that ID is canonical. Do **not** then file MITRE.
