import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def extract_interactive_elements(url: str):
    print(f"Opening browser to load: {url}...")
    
    async with async_playwright() as p:
        # Launch browser (headless=True runs in background, False opens a real window)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to the target page
        await page.goto(url, wait_until="networkidle")
        html_content = await page.content()
        await browser.close()

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract only actionable elements: buttons, links, inputs
    interactive_items = []
    
    for tag in soup.find_all(['button', 'a', 'input']):
        tag_name = tag.name
        text = tag.get_text(strip=True)
        element_id = tag.get("id", "")
        placeholder = tag.get("placeholder", "")
        href = tag.get("href", "")

        # Only keep elements that actually have some content or ID
        if text or placeholder or element_id:
            interactive_items.append({
                "type": tag_name,
                "id": element_id,
                "text": text if text else placeholder,
                "href": href
            })

    # Save to a clean text file
    with open("page_elements.txt", "w") as f:
        f.write(f"Interactive Elements for: {url}\n")
        f.write("=" * 40 + "\n\n")
        for idx, item in enumerate(interactive_items, 1):
            f.write(f"[{idx}] Type: {item['type']} | ID: '{item['id']}' | Label: '{item['text']}'\n")

    print(f"Done! Extracted {len(interactive_items)} interactive items to 'page_elements.txt'.")

# Let's test with Wikipedia's simple page first
asyncio.run(extract_interactive_elements("https://en.wikipedia.org"))