from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://shop.petlandoman.com/products', timeout=60000)
    page.wait_for_timeout(3000)
    
    # Click Category accordion button if closed
    try:
        cat_btn = page.query_selector('button:has-text("Category")')
        if cat_btn:
            cat_btn.click()
            page.wait_for_timeout(1000)
    except Exception as e:
        print("Category click err:", e)

    # Get all checkbox labels or links under Category filter
    categories = page.evaluate('''() => {
        const labels = document.querySelectorAll('label, button, a');
        const list = [];
        labels.forEach(l => {
            const txt = (l.textContent || '').trim();
            if (txt) list.push(txt);
        });
        return list;
    }''')
    
    print("Labels/Buttons on products page:")
    for c in set(categories):
        if any(k in c.lower() for k in ['food', 'toy', 'hygiene', 'supplement', 'accessories', 'dog', 'cat', 'bird']):
            print(" -", c)
            
    browser.close()
