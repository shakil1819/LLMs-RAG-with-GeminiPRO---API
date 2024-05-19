import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse
import os

# Set to keep track of visited URLs to avoid duplicates for each base URL
visited_urls = set()

async def scrape_page(page, url, file):
    await page.goto(url)
    # Extract and write text content of the page
    text_content = await page.evaluate("document.body.innerText")
    file.write(f"URL: {url}\n")
    file.write(text_content)
    file.write("\n" + "="*80 + "\n")
    
    # Extract all links from the page
    links = await page.evaluate('''() => Array.from(document.querySelectorAll('a'))
                                  .map(a => a.href).filter(href => href.startsWith(location.origin) || !href.startsWith('http'))''')
    return links

async def scrape_website(base_url, file_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        global visited_urls
        visited_urls = set()  # Reset visited URLs for each base URL
        with open(file_name, 'w', encoding='utf-8') as file:
            await recursive_scrape(page, base_url, file, base_url)
        await browser.close()

async def recursive_scrape(page, url, file, base_url):
    if url in visited_urls:
        return
    visited_urls.add(url)
    print(f"Scraping: {url}")
    links = await scrape_page(page, url, file)
    for link in links:
        # Resolve relative links
        absolute_link = urljoin(url, link)
        if urlparse(absolute_link).netloc == urlparse(base_url).netloc:
            await recursive_scrape(page, absolute_link, file, base_url)

# List of base URLs and corresponding output files
base_urls = {
    "http://gigalogy.com/": "base_url_1.txt",
    "https://tutorial.gigalogy.com/": "base_url_2.txt",
    "https://api.recommender.gigalogy.com/redoc": "base_url_3.txt"
}

# Run the async function for each base URL
async def main():
    for base_url, file_name in base_urls.items():
        print(f"Starting scraping for {base_url}")
        await scrape_website(base_url, file_name)

# Start the script
asyncio.run(main())