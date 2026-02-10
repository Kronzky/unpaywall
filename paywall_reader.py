"""
Paywall Article Reader
Uses Selenium with Edge to fetch articles through paywall bypass services.
"""

import sys
import time
import io

# Set UTF-8 encoding for stdout to handle Unicode characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def construct_bypass_url(article_url, method=1):
    """
    Construct bypass URL based on method number.

    Args:
        article_url: The original paywalled article URL
        method: Which bypass method to use (1-6)

    Returns:
        Bypass URL string
    """
    bypass_methods = {
        1: f"https://removepaywalls.com/{article_url}",
        2: f"https://archive.today/latest/{article_url}",
        3: f"https://archive.fo/oldest/{article_url}",
        4: f"https://removepaywalls.com/3/{article_url}",
        5: f"https://removepaywalls.com/4/{article_url}",
        6: f"https://removepaywalls.com/5/{article_url}",
    }

    return bypass_methods.get(method, bypass_methods[1])


def read_paywalled_article(article_url, method=1, headless=True):
    """
    Fetch a paywalled article using various bypass services.

    Args:
        article_url: The original paywalled article URL
        method: Which bypass method to use (1-6), default is 1
        headless: Run browser in headless mode (default True)

    Returns:
        Dictionary with article content: {title, author, date, body}
    """

    bypass_url = construct_bypass_url(article_url, method)

    method_names = {
        1: "removepaywalls.com",
        2: "archive.today",
        3: "archive.fo",
        4: "removepaywalls.com method 3",
        5: "removepaywalls.com method 4",
        6: "removepaywalls.com method 5"
    }

    print(f"Fetching article via method {method} ({method_names.get(method, 'unknown')})...")
    print(f"Bypass URL: {bypass_url}")

    # Set up Edge options
    edge_options = Options()
    if headless:
        edge_options.add_argument('--headless')
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    driver = None
    try:
        # Initialize Edge driver
        driver = webdriver.Edge(options=edge_options)
        driver.get(bypass_url)

        # Wait for content to load (adjust timeout as needed)
        print("Waiting for content to load...")
        time.sleep(5)  # Give JavaScript time to execute

        # Try to find article content using common selectors
        article_data = {
            'title': '',
            'author': '',
            'date': '',
            'body': '',
            'url': article_url,
            'method': method
        }

        # Extract title - try multiple selectors
        title_selectors = ['h1', 'article h1', '.article-title', 'header h1', '[data-test="headline"]', '.article__headline']
        for selector in title_selectors:
            try:
                title_elem = driver.find_element(By.CSS_SELECTOR, selector)
                if title_elem.text.strip():
                    article_data['title'] = title_elem.text.strip()
                    break
            except:
                continue

        # Extract author
        author_selectors = ['.author', '[rel="author"]', '.article-author', '[data-test="author-name"]', '.article__byline']
        for selector in author_selectors:
            try:
                author_elem = driver.find_element(By.CSS_SELECTOR, selector)
                if author_elem.text.strip():
                    article_data['author'] = author_elem.text.strip()
                    break
            except:
                continue

        # Extract date
        date_selectors = ['time', '.date', '.article-date', '[data-test="timestamp"]', '.article__timestamp']
        for selector in date_selectors:
            try:
                date_elem = driver.find_element(By.CSS_SELECTOR, selector)
                date_text = date_elem.get_attribute('datetime') or date_elem.text.strip()
                if date_text:
                    article_data['date'] = date_text
                    break
            except:
                continue

        # Extract body - try to get main article content
        body_selectors = [
            'article',
            '.article-body',
            '[data-test="article-body"]',
            '.content',
            'main article',
            '#article-body',
            '.article__content'
        ]

        for selector in body_selectors:
            try:
                body_elem = driver.find_element(By.CSS_SELECTOR, selector)
                # Get all paragraphs within the article body
                paragraphs = body_elem.find_elements(By.TAG_NAME, 'p')
                if paragraphs:
                    article_data['body'] = '\n\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
                    if article_data['body']:
                        break
            except:
                continue

        # If no structured content found, get all text from body
        if not article_data['body']:
            article_data['body'] = driver.find_element(By.TAG_NAME, 'body').text

        return article_data

    except Exception as e:
        print(f"Error fetching article: {e}")
        return None

    finally:
        if driver:
            driver.quit()


def format_article_output(article_data):
    """Format article data for display."""
    if not article_data:
        return "Failed to fetch article."

    output = []
    output.append("=" * 80)

    if article_data['title']:
        output.append(f"TITLE: {article_data['title']}")
        output.append("-" * 80)

    if article_data['author']:
        output.append(f"AUTHOR: {article_data['author']}")

    if article_data['date']:
        output.append(f"DATE: {article_data['date']}")

    if article_data['author'] or article_data['date']:
        output.append("-" * 80)

    if article_data['body']:
        output.append("\nARTICLE CONTENT:")
        output.append(article_data['body'])

    output.append("\n" + "=" * 80)
    output.append(f"Fetched via method {article_data.get('method', 'unknown')}")

    return "\n".join(output)


def save_article_to_file(article_data, filename="article.txt"):
    """Save article content to a text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(format_article_output(article_data))
    print(f"\nArticle saved to: {filename}")


def try_all_methods(article_url, headless=True):
    """
    Try all 6 bypass methods until one succeeds.

    Args:
        article_url: The original paywalled article URL
        headless: Run browser in headless mode (default True)

    Returns:
        Article data from first successful method, or None
    """
    print(f"Trying all bypass methods for: {article_url}\n")

    for method in range(1, 7):
        print(f"\n{'='*80}")
        print(f"Attempting method {method}...")
        print(f"{'='*80}")

        article_data = read_paywalled_article(article_url, method=method, headless=headless)

        if article_data and (article_data['title'] or len(article_data['body']) > 500):
            print(f"\n[SUCCESS] Method {method} worked!")
            return article_data
        else:
            print(f"[FAILED] Method {method} failed or returned insufficient content")

    return None


def main():
    """Main function to run from command line."""
    if len(sys.argv) < 2:
        print("Paywall Article Reader - Uses Selenium to fetch paywalled articles")
        print("\nUsage: python paywall_reader.py <article_url> [options]")
        print("\nOptions:")
        print("  --method N    Use specific bypass method (1-6)")
        print("  --try-all     Try all methods until one succeeds")
        print("  --save        Save article to article.txt")
        print("  --visible     Run browser in visible mode (not headless)")
        print("\nBypass Methods:")
        print("  1 - removepaywalls.com/[url]")
        print("  2 - archive.today/latest/[url]")
        print("  3 - archive.fo/oldest/[url]")
        print("  4 - removepaywalls.com/3/[url]")
        print("  5 - removepaywalls.com/4/[url]")
        print("  6 - removepaywalls.com/5/[url]")
        print("\nExamples:")
        print("  python paywall_reader.py https://www.ft.com/content/12345")
        print("  python paywall_reader.py https://www.ft.com/content/12345 --method 4")
        print("  python paywall_reader.py https://www.ft.com/content/12345 --try-all --save")
        sys.exit(1)

    article_url = sys.argv[1]
    method = 1
    save_to_file = False
    headless = True
    try_all = False

    # Parse additional arguments
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--save':
            save_to_file = True
        elif arg == '--visible':
            headless = False
        elif arg == '--try-all':
            try_all = True
        elif arg == '--method' and i + 1 < len(sys.argv):
            try:
                method = int(sys.argv[i + 1])
                if not 1 <= method <= 6:
                    print(f"Error: Method must be between 1 and 6")
                    sys.exit(1)
                i += 1
            except ValueError:
                print(f"Error: Method must be a number (1-6)")
                sys.exit(1)
        i += 1

    # Fetch article
    if try_all:
        article_data = try_all_methods(article_url, headless=headless)
    else:
        article_data = read_paywalled_article(article_url, method=method, headless=headless)

    if article_data:
        # Display article
        print("\n" + format_article_output(article_data))

        # Save if requested
        if save_to_file:
            save_article_to_file(article_data)
    else:
        print("\nFailed to fetch article with the selected method(s).")
        if not try_all:
            print("Try using --try-all to attempt all bypass methods.")
        sys.exit(1)


if __name__ == "__main__":
    main()
