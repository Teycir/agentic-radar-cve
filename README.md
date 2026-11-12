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

## Submission plan — do not rely on the GitHub CNA alone

GitHub only assigns a CVE **after the maintainer publishes** the private advisory. A ghosted
maintainer therefore blocks the whole process, which is what happened on previous reports.
The GitHub advisory stays as a courtesy channel; the critical path is a CNA that assigns
unilaterally.

Full procedure: **`cna/playbook.md`**.

| File | Purpose |
|---|---|
| `cna/playbook.md` | Route comparison, sequence, duplicate-ID handling, evidence rules |
| `cna/vendor-notice.md` | Email to `developers@splx.ai` with a 10-business-day deadline |
| `cna/vuldb-submission.md` | Fast-lane CNA submission (assigns without maintainer) |
| `cna/mitre-submission.md` | CNA-of-last-resort form, field by field |
| `cna/certcc-vince.md` | Coordinator route for a vendor that engages and stalls |
| `cna/contact-log.md` | Fill-as-you-go evidence log; MITRE requires it |

Sequence: T0 vendor notice + VulDB submission → T+10 business days MITRE if no VulDB ID →
T+45 days CERT/CC only if the vendor replied but will not fix. Never file two CNAs in
parallel; first assigned ID is canonical.

The GitHub advisory route is **unavailable on this repository**: private vulnerability
reporting is disabled, there is no Security tab, and `security/advisories/new` cannot be
opened. The GitHub CNA is therefore closed until the maintainer enables PVR. The email is the
contact of record.

1. Email `developers@splx.ai`, Cc `ante@splx.ai` — body in `cna/vendor-notice.md`.
2. Same day, submit to VulDB — it assigns without vendor involvement.
3. If the email bounces, open a public issue or discussion **asking only for a security
   contact**, with no technical detail, and log it. Never describe the bug in a public thread.
4. Keep the CVSS/CWE/range text above for the VulDB and MITRE forms.

## Scoring caveat

7.4 depends on `S:C` (credential belongs to the victim's OpenAI organisation, not the tool).
If the CNA rejects scope change, the same vector scores **6.5 Medium** with `S:U`.
Submit 7.4 with the rationale; expect 6.5.

**CWE:** primary `CWE-15` (External Control of System or Configuration Setting), secondary
`CWE-522` (Insufficiently Protected Credentials). The earlier report's `CWE-426` is a weaker
fit (that CWE targets executable/library search paths); `CWE-427` is the defensible
search-path alternative if the CNA prefers it.

*Generated 2026-11-11T23:58:35Z. All claims traceable to `20261111/231619/`.*
