# agentic-radar — CVE submission pack

**Status:** no CVE assigned yet. Submission prepared for the **GitHub CNA** via a private
security advisory on `github.com/splx-ai/agentic-radar`. When issued it will be
`CVE-2026-XXXXX` (assignment year 2026).

**Package:** `agentic-radar` (PyPI) · **Repo:** `splx-ai/agentic-radar`
**Audited:** 0.14.1, commit `65a7e4bd01e2034c7cb52e9620eeed287688cc53` (2025-11-27)
**Affected range:** `>=0.9.1, <=0.14.1` (per-release wheel inspection; see
`cve-submission/range-verification.txt`)
**Patched versions:** none at time of writing

## What is here

| Path | Purpose |
|---|---|
| `cve-submission/advisory.md` | Ready-to-paste GitHub Security Advisory body (metadata, description, PoC, impact, fix) |
| `cve-submission/attack-path-simple.md` | Plain-language explanation of how the attack works, no jargon |
| `cve-submission/attacker-cost.md` | What the attack costs an attacker: cash, time, infrastructure, economics |
| `cve-submission/pocs/exfil_listener.py` | Capture listener used in the PoC (attach to the advisory) |
| `cve-submission/range-verification.txt` | Per-release derivation of the affected range, including the 0.7.0 negative result |
| `cve-submission/MANIFEST.txt` | sha256 of every file in this pack |
| `20261111/231619/` | Full assessment report, evidence, and PoC (source of truth) |

## Why one CVE, not three

Only RT-01 (credential exfiltration) meets CNA thresholds: working PoC, credential theft,
current release. RT-02 is a local crash on malformed input; RT-03 is a latent library-only
XSS whose CLI path is already escaped. Mention both in the advisory body as secondary notes;
do not request separate IDs.

## Submission steps (GitHub CNA)

1. Open `https://github.com/splx-ai/agentic-radar/security/advisories/new`.
2. Ecosystem `pip`, package `agentic-radar`, affected `>=0.9.1, <=0.14.1`, patched: none.
3. Severity: High, vector `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` (7.4).
4. Paste `cve-submission/advisory.md`, attach the listener and the report.
5. Request a CVE ID in the advisory form. GitHub, as CNA, assigns it.
6. If the maintainer does not respond within 90 days, escalate to MITRE
   (`https://cveform.mitre.org/`), referencing the GitHub advisory URL.

## Scoring caveat

7.4 depends on `S:C` (credential belongs to the victim's OpenAI organisation, not the tool).
If the CNA rejects scope change, the same vector scores **6.5 Medium** with `S:U`.
Submit 7.4 with the rationale; expect 6.5.

**CWE:** primary `CWE-15` (External Control of System or Configuration Setting), secondary
`CWE-522` (Insufficiently Protected Credentials). The earlier report's `CWE-426` is a weaker
fit (that CWE targets executable/library search paths); `CWE-427` is the defensible
search-path alternative if the CNA prefers it.

*Generated 2026-11-11T23:58:35Z. All claims traceable to `20261111/231619/`.*
