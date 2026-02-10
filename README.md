# unpaywall

A Claude Code skill that reads paywalled articles by routing them through bypass services.

## What It Does

When you share a paywalled article URL, Claude will automatically attempt to retrieve the full text using a series of bypass methods — no manual steps required.

**Supported sites include:** Bloomberg, NY Times, Washington Post, Wall Street Journal, Financial Times, The Guardian, Harvard Business Review, LA Times, The Economist, Chicago Tribune, Boston Globe, The Atlantic, The Telegraph, The Sydney Morning Herald, and most other paywalled news sites.

## How It Works

Claude tries two methods in order:

1. **WebFetch** — Fast, no dependencies. Prepends the article URL to bypass services. May fail if the bypass site loads content via JavaScript.
2. **Selenium script** (`paywall_reader.py`) — Launches a headless Edge browser to fully render JavaScript content. Used as a fallback when WebFetch only returns the bypass site's interface.

**Bypass services tried (in order):**
| # | Service |
|---|---------|
| 1 | `removepaywalls.com/[url]` |
| 2 | `archive.today/latest/[url]` |
| 3 | `archive.fo/oldest/[url]` |
| 4 | `removepaywalls.com/3/[url]` |
| 5 | `removepaywalls.com/4/[url]` |
| 6 | `removepaywalls.com/5/[url]` |

## Installation

1. Copy the skill folder to your Claude skills directory:

```bash
# macOS/Linux
cp -r unpaywall/ ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse unpaywall "$env:USERPROFILE\.claude\skills\"
```

2. Restart Claude Code.

Your directory structure should look like:

```
~/.claude/skills/unpaywall/
├── SKILL.md
├── INSTALL.md
├── paywall_reader.py
└── evals/
    └── evals.json
```

## Dependencies

**For WebFetch mode:** None — works out of the box.

**For Selenium mode:**
- Python 3.7+
- Selenium: `pip install selenium`
- Microsoft Edge (pre-installed on Windows; available for macOS/Linux)

## Usage

Just paste a paywalled URL into Claude Code:

```
Summarize this article: https://www.ft.com/content/9c0d4629-7772-4662-a371-2cba68ac398d
```

```
I can't read this — can you? https://www.wsj.com/articles/some-article
```

Claude detects the paywall, runs through the bypass methods, and returns the article content for your requested task (summary, analysis, Q&A, etc.).

### Using the script directly

```bash
# Try all methods automatically (recommended)
python paywall_reader.py https://www.ft.com/content/12345 --try-all

# Use a specific method
python paywall_reader.py https://www.ft.com/content/12345 --method 2

# Save article to file
python paywall_reader.py https://www.ft.com/content/12345 --try-all --save

# Run browser in visible mode (for debugging)
python paywall_reader.py https://www.ft.com/content/12345 --visible
```

## Troubleshooting

**Skill not triggering?**
Verify `SKILL.md` is in `~/.claude/skills/unpaywall/` and restart Claude Code.

**Selenium errors?**
- Check Python version: `python --version` (need 3.7+)
- Install Selenium: `pip install selenium`
- Confirm Edge is installed

**All methods failing?**
- Try manually: `https://removepaywalls.com/[your-article-url]`
- Check if bypass services are accessible from your network
- As a fallback, paste the article text directly into Claude

## Legal Note

For educational and research purposes, and for users with legitimate subscriptions experiencing technical access issues.
