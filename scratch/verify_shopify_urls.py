import urllib.request

urls = [
    "https://shop.petlandoman.com/products?category=food",
    "https://shop.petlandoman.com/products?category=toys",
    "https://shop.petlandoman.com/products?category=hygiene",
    "https://shop.petlandoman.com/products?category=accessories",
    "https://shop.petlandoman.com/products",
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[{resp.status}] OK: {url}")
    except Exception as e:
        print(f"FAILED: {url} -> {e}")
