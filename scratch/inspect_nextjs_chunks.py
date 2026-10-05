import urllib.request
import re

# Fetch main-app or layout chunks from shop.petlandoman.com
page_url = "https://shop.petlandoman.com/products"
req = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

js_files = re.findall(r'src="(/_next/static/chunks/[^"]+\.js)"', html)
print(f"Found {len(js_files)} JS files")

categories_found = set()
for js in js_files:
    js_url = "https://shop.petlandoman.com" + js
    try:
        jreq = urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(jreq) as jresp:
            jstext = jresp.read().decode('utf-8', errors='ignore')
            # Look for category names or slugs
            cats = re.findall(r'category[^a-zA-Z0-9]*([a-zA-Z0-9_-]+)', jstext, re.IGNORECASE)
            for c in cats:
                if len(c) > 2 and len(c) < 30:
                    categories_found.add(c)
            # Look for slug or category patterns
            matches = re.findall(r'["\'](/products\?[^"\']+)["\']', jstext)
            for m in matches:
                print("Found product route link:", m)
    except Exception as e:
        pass

print("Sample categories keywords found:", list(categories_found)[:20])
