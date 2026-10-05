from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://shop.petlandoman.com/products', timeout=60000)
    page.wait_for_timeout(3000)
    
    # Check all checkbox inputs on products page
    checkboxes = page.query_selector_all('input[type="checkbox"], button[role="checkbox"]')
    print(f"Found {len(checkboxes)} checkboxes!")
    
    urls_after_click = []
    for cb in checkboxes[:15]:
        try:
            label = cb.evaluate('e => e.closest("label") ? e.closest("label").innerText : e.innerText')
            cb.click()
            page.wait_for_timeout(1000)
            urls_after_click.append({'label': label.strip(), 'url': page.url})
        except Exception as e:
            pass
            
    for u in urls_after_click:
        print(f"Label: '{u['label']}' -> {u['url']}")
        
    browser.close()
