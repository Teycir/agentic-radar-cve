# VulDB "Vulnerability Add" — exact form fill

Form path: `vuldb.com` → **Submits** (left rail) → *Vulnerability Add*
(`https://vuldb.com/?add`), logged in as `teycirb`.

**Copy-paste values below. Field order matches the live form.**
Queue notice on the page says moderation estimate **6 weeks** — see §7 before you plan a
MITRE fallback.

---

## 0. Before you click Add — three gates

The CVE checkbox has hard prerequisites. Do not tick it until all three are true.

- [ ] **Vendor contacted.** Email `developers@splx.ai` (Cc `ante@splx.ai`) using
      `cna/vendor-notice.md`. Then fill row 2 of `cna/contact-log.md` with the UTC time and
      the **Message-ID**. If it was already sent, just record it — do not resend.
- [ ] **No CVE assigned.** Confirmed 2026-11-12 via VulDB API: searches for
      `agentic-radar`, `agentic_radar`, `splx-ai` returned 0 items. NVD keyword search: 0.
      GitHub advisories for the package: 0.
- [ ] **Not submitted to another CNA.** No MITRE, no CERT/CC, no other CNA has been filed.
      Filing two CNAs in parallel produces duplicate IDs and can get the submission rejected.

Correction note: `cna/vuldb-submission.md` step 7 states the vendor notice was "already
sent 2026-11-12", but `cna/contact-log.md` row 2 is empty. Treat the email as **not yet
recorded**. Send or verify first; the checkbox attestation must be true.

---

## 1. Vendor

```
SplxAI
```

GitHub org is `splx-ai`, product site `splx.ai`. If the form autocompletes an existing
vendor entry, pick that one instead of creating a near-duplicate.

## 2. Product

```
agentic-radar
```

PyPI distribution name. Do not use the repo name `agentic_radar` (underscore) — that is the
import package, not the product.

## 3. Version or Commit

```
0.9.1 through 0.14.1
```

Lower bound rationale (wheel inspection, per-release grep) is in
`cve-submission/range-verification.txt`. 0.14.1 is latest and unfixed. If the field rejects a
range, enter `0.14.1` and leave the range in the description.

## 4. Vulnerability Class

```
Insufficiently Protected Credentials (CWE-522)
```

Secondary class, if the form takes a second value: `External Control of System or
Configuration Setting (CWE-15)`. Do not use `CWE-426` — weaker fit for this vector.

## 5. Description (plain text, max 9000 chars, markup disabled)

Paste verbatim. 3126 characters.

```
Affected: agentic-radar (PyPI) 0.9.1 through 0.14.1. No fixed release; 0.14.1 is latest and affected.
CVSS 3.1: 7.4 / AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N
CWE: CWE-15 (External Control of System or Configuration Setting), CWE-522 (Insufficiently Protected Credentials)

SUMMARY
agentic-radar calls load_dotenv() unconditionally at import time (agentic_radar/cli.py:37 in 0.14.1). The package depends on the deprecated "dotenv" 0.9.9 distribution, whose find_dotenv() starts at the calling frame's file - the installed agentic_radar package directory - and walks upward. When the package is installed inside a checked-out repository (an in-repo .venv or an editable install, the layout used by the project's own examples/github_workflow/auto-agentic-radar.yaml), a .env committed to that repository is loaded into the process environment.

The command "agentic-radar scan openai-agents" then constructs openai.OpenAI() and sends chat.completions requests without validating OPENAI_BASE_URL. A repository author who controls that .env file can set OPENAI_BASE_URL to a host they operate and receive the victim's OPENAI_API_KEY in the Authorization: Bearer header. The scan exits 0 and prints no warning.

AFFECTED / NOT AFFECTED
Affected: 0.9.1 through 0.14.1. 0.9.1 is the first release containing both the import-time .env load and an unconditional LLM call in the openai-agents analyzer (per-release wheel inspection).
Not affected: installs outside the scanned repository (pipx, system-wide, standalone venv). The upward search never reaches the repository .env; verified as a negative control with 0 requests received.
Not affected for this command: 0.7.0-0.8.x, whose only chat.completions call is behind the explicit --enhance-prompts flag.

REPRODUCTION (verified 2026-11-11 on 0.14.1, Python 3.12)
1. In an empty directory create .env with:
   OPENAI_API_KEY=sk-DUMMY-DO-NOT-USE
   OPENAI_BASE_URL=http://127.0.0.1:8899/v1
2. python3.12 -m venv .venv && .venv/bin/pip install "agentic-radar[openai-agents]==0.14.1"
3. Start a loopback HTTP listener that logs request headers.
4. cd / && OPENAI_API_KEY=sk-DUMMY-DO-NOT-USE /path/to/.venv/bin/agentic-radar scan openai-agents -i sample
Result: two POST /v1/chat/completions requests arrive at the listener carrying "Authorization: Bearer sk-DUMMY-DO-NOT-USE" and "User-Agent: OpenAI/Python 2.54.0"; the scan exits 0. No flag, prompt or confirmation is involved.

IMPACT
Disclosure of the user's OpenAI API key to the author of the repository being scanned. The key is billable and typically carries access to account-level resources. Scanning third-party or untrusted agent repositories is the tool's documented purpose. A repository can also write the .env during build instead of committing it, so the tree shows nothing unusual.

FIX
- Do not call load_dotenv() at import time. If .env support is kept, require an explicit --env-file and load exactly that path.
- Refuse a non-default OPENAI_BASE_URL unless the user passes an explicit flag, and print the resolved base URL before sending prompts.
- Make LLM-backed analysis opt-in.

Credit: Teycir (github.com/Teycir)
```

## 6. Advisory / Exploit / Proof-of-Concept (URL)

One `https://` URL. It must be reachable by the moderator — a private repo scores nothing.
`Teycir/agentic-radar-cve` currently returns 404, so it cannot be used as-is.

Publish a self-contained gist first (advisory + reproducer + captured header line, no real
key). From `/home/teycir/CVEReports/agentic-radar`:

```bash
printf '# agentic-radar: OPENAI_API_KEY exfiltration via repository .env\n\n' > /tmp/opencode/vuldb/gist.md
sed -n '1,200p' cve-submission/advisory.md >> /tmp/opencode/vuldb/gist.md
printf '\n## Reproducer listener\n\n```python\n' >> /tmp/opencode/vuldb/gist.md
cat cve-submission/pocs/exfil_listener.py >> /tmp/opencode/vuldb/gist.md
printf '\n```\n' >> /tmp/opencode/vuldb/gist.md
printf '\n## Captured request (dummy key)\n\n```\n' >> /tmp/opencode/vuldb/gist.md
grep -m2 'chat/completions' evidence/listener.log >> /tmp/opencode/vuldb/gist.md
printf '```\n' >> /tmp/opencode/vuldb/gist.md
gh gist create --public /tmp/opencode/vuldb/gist.md
```

Paste the returned `https://gist.github.com/...` URL into the field.

Trade-off: a public gist discloses the issue before an ID exists. VulDB publishes accepted
entries anyway, and the entry is the disclosure vehicle here, so this is acceptable. If you
refuse pre-ID disclosure, use any stable public URL you control that the moderator can read;
a link to PyPI or the repo alone is not a PoC and slows or blocks moderation.

## 7. Request a CVE checkbox

Tick **only** after §0 gates pass. This is the CVE request — there is no separate form.

## 8. Add

One vulnerability per submit. RT-02 (LangGraph crash) and RT-03 (library-only XSS) do **not**
go in this entry; they stay as notes in the advisory. Submit them separately if ever wanted.

---

## 9. After submit — record evidence

1. Screenshot the confirmation page; save as `evidence/vuldb_submit_confirmation.png`.
2. Note the VDB tracking number (e.g. `VDB-xxxxxx`) — it is **not** a CVE.
3. Update `cna/contact-log.md`:
   - CNA row 1: UTC time, `VulDB`, `vuldb.com/?add`, `VDB-xxxxxx`, `submitted`
   - Assigned IDs: still empty
4. Do not file MITRE while VulDB is pending. The page now says moderation ≈ 6 weeks, so the
   old T+10-business-day fallback in `cna/playbook.md` is too aggressive: you would be filing
   a second CNA while the first is still open, and the checkbox attests you did not.
   Escalate to MITRE only after a VulDB **reject** or after a written status that no CVE will
   be assigned.
5. If VulDB re-scores: accept 6.5 Medium with `S:U` if they reject the scope change. Do not
   argue.

---

## 10. Likely hiccups

| Symptom | Cause | Action |
|---|---|---|
| "Vendor already exists" | VulDB has `SplxAI` or `splx-ai` | Select the existing entry, do not create a duplicate |
| Entry flagged duplicate | Prior VDB entry | Reply with the product/version difference; if genuinely the same, drop it |
| Asked for vendor confirmation | Normal coordination | Reply with the email timestamp, Message-ID and the 2026-11-26 deadline |
| Asked for 0.9.1 proof | Range derived by inspection | Run the reproducer against 0.9.1 and attach the log |
| Rejected "not a vulnerability" | Reviewer did not accept the in-repo install precondition | Cite `examples/github_workflow/auto-agentic-radar.yaml` creating `.venv` in the checkout, and the negative control that bounds it |
| Cloudflare "Security Check" page | Bot challenge on vuldb.com | Use a normal browser session; API key cannot create entries (`query=submit` → 405) |
