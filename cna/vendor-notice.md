# Vendor notice — email to send at T0

Send to `developers@splx.ai`, Cc `ante@splx.ai`. Keep the sent copy and the Message-ID;
MITRE will ask for it.

Subject:

```
Security report: agentic-radar <=0.14.1 exfiltrates OPENAI_API_KEY via repository .env
```

Body:

```
Hello,

I am reporting a security issue in agentic-radar (PyPI), versions 0.9.1 through 0.14.1.
I could not find a SECURITY.md or a private reporting channel, so I am contacting you
directly and have also opened a private security advisory on the GitHub repository.

Summary
-------
agentic-radar calls load_dotenv() at import time (agentic_radar/cli.py). python-dotenv's
default search starts at the installed package directory and walks upward, so a .env file
placed anywhere above site-packages is loaded. When the package is installed inside a
checked-out repository - the layout used by your own auto-agentic-radar workflow example -
a .env committed to that repository is picked up before the user's environment.

The tool then honours OPENAI_BASE_URL with no allow-list and, during
`agentic-radar scan openai-agents`, unconditionally sends chat.completions requests using
the OPENAI_API_KEY. A repository author can therefore set OPENAI_BASE_URL to a server they
control and receive the victim's API key in an Authorization: Bearer header.

Reproduction
------------
Verified against 0.14.1 on 2026-11-11: two POST /v1/chat/completions requests reached a
local listener with the user's key, and the scan completed with exit code 0. A control run
with the package installed in a standalone virtualenv outside the repository produced zero
requests, which bounds the exposure to in-tree or editable installs.

Impact
------
Disclosure of the OpenAI API key (and any other credential present in the environment that
the tool forwards) to whoever authored the repository being scanned. Keys are billable and
often carry access to other data in the same account.

Suggested fix
-------------
- Stop calling load_dotenv() at import time, or call it with an explicit path that cannot
  resolve above the installation directory.
- Treat OPENAI_BASE_URL as untrusted configuration: require an explicit opt-in flag, or
  refuse non-default hosts unless the user confirms.
- Consider preventing the tool from reading any .env that lives in the scanned directory.

I plan to request a CVE for this issue. If I do not hear back by <DATE + 10 business days>,
I will proceed with the CNA process without your input. I am happy to share the full report
and reproducer privately, and to hold publication until a fix ships.

Regards,
Teycir
github.com/Teycir
```

## Logging

After sending, fill the first row of `contact-log.md` with the UTC time, recipient, subject,
and Message-ID. If the mail bounces, keep the bounce — a failed contact attempt is still
evidence and strengthens the "vendor unresponsive" case.
