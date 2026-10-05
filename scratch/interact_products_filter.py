from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://shop.petlandoman.com/products', timeout=60000)
    page.wait_for_timeout(3000)
    
    # Take screenshot of /products to inspect filter UI
    page.screenshot(path='c:/Users/SRUTHI/.gemini/antigravity-ide/brain/f4dee9e1-f3c6-422f-be04-76cad195ee13/shop_products_page.png')
    
    # Get HTML content of the filter section / sidebar
    filters = page.evaluate('''() => {
        const elements = document.querySelectorAll('button, div, a, span, label');
        const items = [];
        elements.forEach(e => {
            const text = (e.textContent || '').strip ? e.textContent.strip() : (e.textContent || '').trim();
            if (text && text.length > 2 && text.length < 50) {
                if (['Food', 'Pet Food', 'Toys', 'Toys & Fun', 'Hygiene', 'Supplements', 'Accessories', 'Category', 'Categories', 'Dog', 'Cat'].some(k => text.toLowerCase().includes(k.toLowerCase()))) {
                    items.push({text: text, tag: e.tagName, className: e.className, href: e.getAttribute('href')});
                }
            }
        });
        return items;
    }''')
    
    print("MATCHED CATEGORY/FILTER ITEMS ON PRODUCTS PAGE:")
    for item in filters[:30]:
        print(item)
        
    browser.close()
