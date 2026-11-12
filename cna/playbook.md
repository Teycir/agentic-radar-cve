# CNA Playbook — getting a CVE without maintainer cooperation

## Why the last attempts produced nothing

GitHub's CNA only assigns a CVE when the **maintainer publishes** the private advisory. File
a private advisory at a ghosted repo and it sits unpublished forever: no GHSA, no CVE, no
record. The maintainer therefore holds a veto over the whole process.

Rule for this and every future case:

> Never make maintainer action the critical path. Always pair the vendor notice with at least
> one CNA that assigns unilaterally.

## Route comparison

| Route | CNA assigns unilaterally | P(CVE) with unresponsive vendor | Typical time | Cost |
|---|---|---|---|---|
| **VulDB** (`vuldb.com/?submit`) | Yes — VulDB is a CVE CNA | ~0.85 | 3 days – 3 weeks | free |
| **MITRE** (`cveform.mitre.org`) | Yes — CNA of last resort | ~0.90 with contact evidence | 3 weeks – 4 months | free |
| **CERT/CC** (`kb.cert.org/vince`) | Yes — coordinator + CNA | ~0.80 | 45 days + | free |
| **GitHub CNA** (private advisory) | No — needs maintainer publish | ~0.30 given ghosting | indefinite | free |

VulDB is the fast lane. MITRE is the guaranteed lane. CERT/CC is for when the vendor
engages and negotiations drag. GitHub stays as a courtesy channel, never the plan.

## Sequence (do not run two CNAs in parallel)

**T0 — vendor notice, and VulDB submission.**

1. File the private advisory on `splx-ai/agentic-radar`. This is the contact of record and
   the URL you cite later. Log it.
2. Email `developers@splx.ai` (Cc `ante@splx.ai`) using `vendor-notice.md`. State a
   10-business-day deadline. Keep the SMTP copy / sent folder entry and the Message-ID.
3. Submit to VulDB the same day using `cna/vuldb-submission.md`. Do not wait for the vendor.

**T+10 business days — no vendor reply.**

4. Nothing to chase. VulDB is already working. If VulDB has assigned an ID, stop: that is
   your CVE. Do not file MITRE as well.
5. If VulDB has not assigned and has not replied, file MITRE (`cna/mitre-submission.md`)
   with the contact log. MITRE will assign as CNA of last resort once it sees the vendor was
   notified and did not respond.

**T+45 days — vendor responded but will not fix.**

6. Keep the vendor thread. If they dispute or stall, open a CERT/CC VINCE case
   (`cna/certcc-vince.md`); they will run coordination and assign if the vendor remains
   inactive.

## Duplicate-ID handling

Two CNAs assigning one issue is the main self-inflicted risk.

- Whichever CNA assigns **first** is canonical. Record it.
- If a second CNA assigns later, reply immediately asking them to reject or mark duplicate,
  citing the first ID.
- Never cite two IDs for the same issue in a report, résumé, or advisory.

## Evidence MITRE and CERT/CC will demand

- Product, vendor, affected versions, and how the range was derived.
- Root cause with file/line references.
- Working reproducer and observed proof (request/response, timestamps).
- Every contact attempt: address, UTC timestamp, body, Message-ID, reply or silence.
- A statement that the vendor was given reasonable time and did not respond.
- CVSS vector and CWE.

Everything except the contact log already exists in this repo. `contact-log.md` is the only
file you fill in by hand.

## Do not

- Do not publish the PoC or the advisory body publicly before an ID is assigned or a fix
  ships. Public disclosure first gives a CNA a reason to treat the case as uncoordinated.
- Do not file MITRE and VulDB simultaneously.
- Do not send the vendor a second "reminder" that resets the deadline. One notice, one
  deadline, then escalate.
