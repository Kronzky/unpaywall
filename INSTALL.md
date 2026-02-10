# FT Paywall Bypass Skill - Installation Guide

## Quick Start

1. **Download the files:**
   - SKILL.md (main skill file)
   - evals.json (optional - for testing)

2. **Create the skill directory structure:**

```bash
# On macOS/Linux
mkdir -p ~/.claude/skills/user/ft-paywall-bypass/evals

# On Windows (PowerShell)
New-Item -Path "$env:USERPROFILE\.claude\skills\user\ft-paywall-bypass\evals" -ItemType Directory -Force
```

3. **Place the files:**

```bash
# On macOS/Linux
mv SKILL.md ~/.claude/skills/user/ft-paywall-bypass/
mv evals.json ~/.claude/skills/user/ft-paywall-bypass/evals/

# On Windows (PowerShell)
Move-Item SKILL.md "$env:USERPROFILE\.claude\skills\user\ft-paywall-bypass\"
Move-Item evals.json "$env:USERPROFILE\.claude\skills\user\ft-paywall-bypass\evals\"
```

4. **Restart Claude Code** (or it should auto-detect the new skill)

## Dependencies

The skill works in two modes:

**Mode 1: WebFetch (built-in)**
- No dependencies required
- Fast but may not work with JavaScript-heavy bypass sites

**Mode 2: Selenium Script (recommended for reliability)**
- Python 3.7+
- Selenium: `pip install selenium`
- Microsoft Edge browser (usually pre-installed on Windows)

## Usage

Simply give Claude Code an FT article URL:

```
Summarize this FT article: https://www.ft.com/content/9c0d4629-7772-4662-a371-2cba68ac398d
```

Claude will automatically:
1. Detect it's paywalled
2. Try WebFetch with bypass URLs
3. If WebFetch fails, use the Selenium script to render JavaScript content
4. Fetch and summarize the article

## File Structure

Your final structure should look like:

```
~/.claude/skills/paywall/
├── SKILL.md
├── INSTALL.md
├── paywall_reader.py (Selenium script)
└── evals/
    └── evals.json
```

The `paywall_reader.py` script is included with the skill and can be used whenever WebFetch fails to retrieve article content.

## Testing

```bash
cd ~/.claude/skills/user/ft-paywall-bypass
claude skill eval
```

## Supported Sites

- Financial Times (ft.com)
- Wall Street Journal (wsj.com)
- New York Times (nytimes.com)
- The Telegraph (telegraph.co.uk)
- Bloomberg (bloomberg.com)
- Most paywalled news sites

## How It Works

Original URL:
```
https://www.ft.com/content/abc123
```

Transformed to:
```
https://removepaywalls.com/https://www.ft.com/content/abc123
```

## Troubleshooting

**Skill not triggering?**
- Verify files are in `~/.claude/skills/paywall/`
- Check SKILL.md has proper YAML frontmatter (three dashes before and after)
- Restart Claude Code

**WebFetch returning only bypass site interface?**
- This is normal - bypass sites use JavaScript to load content
- Claude will automatically fall back to the Selenium script
- Ensure you have Selenium installed: `pip install selenium`
- Ensure Microsoft Edge browser is installed

**Selenium script errors?**
- Check Python version: `python --version` (need 3.7+)
- Install Selenium: `pip install selenium`
- Verify Edge is installed (usually pre-installed on Windows)
- Try running manually: `python paywall_reader.py <url> --try-all`

**Still getting paywall errors?**
- Ensure Claude Code has network access enabled
- Try manually in browser: https://removepaywalls.com/[your-ft-url]
- Check if bypass services are accessible from your network
- Try a different bypass method (1-6)

**Need explicit triggering?**
```
/paywall https://www.ft.com/content/12345
```

## Legal Note

This tool is for educational/research purposes and for users with legitimate subscriptions facing technical access issues. Support quality journalism by subscribing to publications you read regularly.
