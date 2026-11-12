# CERT/CC VINCE case — use only if the vendor engages and stalls

Open a case at `https://kb.cert.org/vince/` when the vendor replies but will not commit to a
fix, or when a CNA has not acted and you want an independent coordinator. CERT/CC is a CNA
and will assign a CVE if coordination concludes without a vendor fix.

## Case type

Vulnerability report, vendor coordination requested.

## Vendor

```
SplxAI — agentic-radar (PyPI), https://github.com/splx-ai/agentic-radar
Contacts: developers@splx.ai, ante@splx.ai
```

## Narrative

```
agentic-radar (PyPI) versions 0.9.1 through 0.14.1 load .env via python-dotenv at import
time. Because the default search walks up from the installed package directory, a .env file
committed in the repository where the package is installed is trusted. The tool does not
validate OPENAI_BASE_URL and sends chat.completions requests with the user's OPENAI_API_KEY
to whatever host that variable names. A repository author can exfiltrate the key by shipping
a .env in the repository they ask the victim to scan.

Reproduced on 0.14.1: two POST /v1/chat/completions requests bearing the key reached a local
listener; the scan exited 0. Control run from a standalone virtualenv outside the repository
produced no requests.

No SECURITY.md exists. The maintainer was notified privately on <date> and did not respond
within 10 business days. <If applicable: the maintainer replied on <date> but declined to
fix.>
```

## Ask

```
CVE assignment and coordination with the vendor, or assignment as CNA if the vendor remains
inactive. Preferred disclosure date: after a fix ships, or 45 days from vendor notification.
```

## Evidence to attach

- advisory.md
- pocs/exfil_listener.py and the captured log
- contact-log.md
- The private GitHub advisory URL

## Expectation

CERT/CC operates on a 45-day coordination window. If the vendor is silent, they publish and
assign. Slower than VulDB, more authoritative than a bare MITRE form when a vendor is
partially engaging.
