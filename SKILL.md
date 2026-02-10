---
name: unpaywall
description: Read paywalled articles by routing them through different sites. Trigger when user provides an article that's behind a paywall, or when they ask to read/summarize an article. Also trigger when user mentions they can't access an article due to paywall restrictions.
Works with Bloomberg, the New York Times, The Washington Post, The Wall Street Journal, Financial Times, The Guardian, Harvard Business Review, LA Post, LA Times, The Economist, Chicago Tribune, Boston Globe, The Atlantic, The Telegraph, The Sydney Morning Herald, and probably many others.
Also: ai-supremacy.com
---

# Paywall Bypass

This skill attempts to read a paywalled articles by using miscellanous services.

## When to Use This Skill

Trigger this skill when:
- User provides a URL to an article that returns a paywall error
- User asks to "read this article" with a paywalled link
- User mentions they can't access an article
- User asks to summarize/analyze an article behind a paywall
- Web fetch returns a SITE_BLOCKED or paywall error for the article

## How It Works

The skill routes the provided URLs through different paywall removal sites, of which one will hopefully return the full article text.

**URL transformation:**
```
Original:	https://www.ft.com/content/(article-id)
Attempt1:	https://removepaywalls.com/[article-url]
Attempt2:	https://archive.today/latest/[article-url]
Attempt3:	https://archive.fo/oldest/[article-url]
Attempt4:	https://removepaywalls.com/3/[article-url]
Attempt5:	https://removepaywalls.com/4/[article-url]
Attempt6:	https://removepaywalls.com/5/[article-url]
## Implementation

There are two methods to access paywalled articles: WebFetch (quick but limited) and Selenium script (more reliable).

### Method 1: WebFetch (Try First)

**Step 1: Detect Paywalled URL**

When you encounter a URL, check if it's accessible:
- If `web_fetch` returns successfully, use the content directly
- If `web_fetch` returns `SITE_BLOCKED` or paywall error, proceed to bypass

**Step 2: Try WebFetch with Bypass URLs**

Try fetching with one or more bypass URLs from the list above:

```python
web_fetch("https://removepaywalls.com/[article-url]")
web_fetch("https://archive.today/latest/[article-url]")
# etc.
```

**Limitation:** WebFetch cannot execute JavaScript or render dynamic content. If bypass sites use JavaScript to load the article content, WebFetch will only see the page wrapper/interface, not the actual article. In this case, proceed to Method 2.

### Method 2: Selenium Script (Reliable Fallback)

When WebFetch fails to retrieve article content (only seeing the bypass site interface), use the `paywall_reader.py` Selenium script that renders JavaScript properly.

**Step 1: Check if script exists**

The script should be located in the user's working directory or you can create it if needed. The script uses Selenium with Edge WebDriver to render pages with JavaScript.

**Step 2: Run the script**

Use the Bash tool to run the script:

```bash
python paywall_reader.py <article-url> --try-all
```

This will automatically try all 6 bypass methods until one succeeds.

**Options:**
- `--try-all` - Try all methods automatically (recommended)
- `--method N` - Use specific method (1-6)
- `--save` - Save article to article.txt
- `--visible` - Run browser in visible mode (for debugging)

**Step 3: Extract and Process**

The script will output the full article with title, author, date, and body text. Use this content to proceed with the user's requested task (summarize, analyze, etc.)

## Selenium Script Reference

The `paywall_reader.py` script uses Selenium with Microsoft Edge to render JavaScript content from bypass services.

**Key features:**
- Supports all 6 bypass methods
- Automatically tries methods until one succeeds (with `--try-all`)
- Extracts title, author, date, and body text
- Runs in headless mode by default
- Can save articles to text files

**Script location:** Should be in the user's working directory. If not present, offer to create it.

**Usage examples:**
```bash
# Try all methods automatically
python paywall_reader.py https://www.ft.com/content/12345 --try-all

# Use specific method
python paywall_reader.py https://www.ft.com/content/12345 --method 2

# Save to file
python paywall_reader.py https://www.ft.com/content/12345 --try-all --save
```

## Example Usage

**User request:**
```
Summarize this FT article: https://www.ft.com/content/9c0d4629-7772-4662-a371-2cba68ac398d
```

**Your workflow (WebFetch approach):**
1. Attempt direct fetch: `web_fetch("https://www.ft.com/content/9c0d4629-7772-4662-a371-2cba68ac398d")`
2. If blocked, try bypass URLs with WebFetch
3. If WebFetch returns only the bypass site interface (not the article), proceed to Selenium method

**Your workflow (Selenium approach):**
1. Run: `python paywall_reader.py https://www.ft.com/content/9c0d4629-7772-4662-a371-2cba68ac398d --try-all`
2. Script automatically tries methods 1-6 until one succeeds
3. Extract article content from script output
4. Provide summary to user

## Important Notes

### Legal Considerations
- This tool is for educational and research purposes
- Users should have legitimate access to FT content (e.g., through subscription)
- This is a workaround for technical access issues, not for piracy
- Inform users they should support quality journalism when possible

### Fallback Strategy
If WebFetch with bypass URLs fails (returns only the bypass site interface):
1. **Use the Selenium script** - Run `python paywall_reader.py <url> --try-all` to render JavaScript content
2. Ask user if they can paste the article text directly
3. Search for the article title to find free coverage of the same topic

**Why WebFetch fails:** Bypass services often load article content dynamically via JavaScript. WebFetch only sees the initial HTML and misses the JavaScript-rendered content. The Selenium script solves this by opening a real browser that executes JavaScript.

### Other Paywalled Sites
This skill is specifically for Financial Times, but the same technique works for:
- Wall Street Journal (wsj.com)
- New York Times (nytimes.com)
- The Telegraph (telegraph.co.uk)
- Bloomberg (bloomberg.com)

Simply prepend `https://removepaywalls.com/` to any paywalled article URL.

## Error Handling

**If WebFetch returns only the bypass site interface:**
```
The bypass service works in a browser, but WebFetch can't render the JavaScript content.
Let me use the Selenium script to properly fetch the article...
```
Then run: `python paywall_reader.py <url> --try-all`

**If Selenium script is not found:**
Offer to create the `paywall_reader.py` script for the user. The script is a standalone Python file that uses Selenium with Edge WebDriver.

**If all methods fail:**
```
I attempted to access the article through multiple bypass services,
but none were successful. You have a few options:

1. Paste the article text directly if you have access
2. Share the article title so I can search for related coverage
3. Try again later if the services are temporarily down
```

**If article is heavily formatted:**
```
The article was retrieved but contains significant formatting.
Let me extract the main content for you...
```

## Success Criteria

The skill successfully:
- ✅ Detects FT paywall blocks
- ✅ Transforms URLs correctly
- ✅ Retrieves full article text
- ✅ Extracts readable content
- ✅ Completes user's original request (summarize/analyze/etc.)

## Testing

Test with these example FT URLs:
1. Recent article (should be paywalled)
2. Very old article (might be free)
3. Non-FT URL (should not trigger skill)
4. Already accessible article (should use direct fetch)
