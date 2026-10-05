from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://shop.petlandoman.com/', timeout=60000)
    page.wait_for_timeout(3000)
    
    # Extract links from home page
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a[href]')).map(e => ({
            text: (e.textContent || '').trim(),
            href: e.getAttribute('href')
        }));
    }''')
    
    print("HOME PAGE LINKS:")
    for l in links:
        if l['href'] and not l['href'].startswith('#') and l['href'] != '/':
            print(f"  '{l['text']}' -> {l['href']}")
            
    # Now go to /products
    page.goto('https://shop.petlandoman.com/products', timeout=60000)
    page.wait_for_timeout(3000)
    
    p_links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a[href]')).map(e => ({
            text: (e.textContent || '').trim(),
            href: e.getAttribute('href')
        }));
    }''')
    
    print("\nPRODUCTS PAGE LINKS:")
    for l in p_links:
        if l['href'] and not l['href'].startswith('#') and l['href'] != '/':
            print(f"  '{l['text']}' -> {l['href']}")
            
    browser.close()
