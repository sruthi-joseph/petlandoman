from playwright.sync_api import sync_playwright

test_urls = [
    "https://shop.petlandoman.com/products?advance_search=Food",
    "https://shop.petlandoman.com/products?advance_search=Toy",
    "https://shop.petlandoman.com/products?advance_search=Hygiene",
    "https://shop.petlandoman.com/products?advance_search=Accessories",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for u in test_urls:
        page.goto(u, timeout=60000)
        page.wait_for_timeout(2000)
        titles = page.evaluate('''() => {
            const els = document.querySelectorAll('h3, h4, .product-title, .font-poppins');
            return Array.from(els).map(e => e.innerText.strip ? e.innerText.strip() : e.innerText.trim()).filter(t => t.length > 3).slice(0, 5);
        }''')
        print(f"URL: {u}")
        print("  Sample titles:", titles[:3])
        print("-" * 50)
        
    browser.close()
