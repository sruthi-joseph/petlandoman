from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Listen to network responses to capture backend API category endpoint
    categories_api_resp = []
    
    def handle_response(response):
        if 'cat' in response.url.lower() or 'product' in response.url.lower() or 'api' in response.url.lower():
            try:
                if 'json' in response.headers.get('content-type', ''):
                    data = response.json()
                    categories_api_resp.append({'url': response.url, 'data': data})
            except:
                pass
                
    page.on('response', handle_response)
    
    page.goto('https://shop.petlandoman.com/products', timeout=60000)
    page.wait_for_timeout(5000)
    
    print(f"Captured {len(categories_api_resp)} API responses!")
    for item in categories_api_resp:
        print("API URL:", item['url'])
        print("DATA KEYS:", list(item['data'].keys()) if isinstance(item['data'], dict) else type(item['data']))
        print("SAMPLE DATA:", str(item['data'])[:300])
        print("-" * 50)
        
    browser.close()
