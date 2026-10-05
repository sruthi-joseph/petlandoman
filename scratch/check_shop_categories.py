import urllib.request
import json

urls_to_test = [
    "https://shop.petlandoman.com/products",
    "https://shop.petlandoman.com/products?category=food",
    "https://shop.petlandoman.com/products?category=toys",
    "https://shop.petlandoman.com/products?category=hygiene",
    "https://shop.petlandoman.com/products?category=accessories",
    "https://shop.petlandoman.com/products?category=pet-food",
    "https://shop.petlandoman.com/products?category=toys-and-fun",
    "https://shop.petlandoman.com/products?category=hygiene-and-supplements",
]

for url in urls_to_test:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Status {resp.status} for {url}")
    except Exception as e:
        print(f"Error for {url}: {e}")
