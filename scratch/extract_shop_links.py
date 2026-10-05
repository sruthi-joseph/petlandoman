import re

content_file = r'C:\Users\SRUTHI\.gemini\antigravity-ide\brain\f4dee9e1-f3c6-422f-be04-76cad195ee13\.system_generated\steps\409\content.md'
with open(content_file, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

hrefs = set(re.findall(r'href=["\']([^"\']+)["\']', text))
print("Found links on shop.petlandoman.com:")
for h in sorted(hrefs):
    if not h.startswith('/_next') and not h.startswith('http') and h != '/':
        print(' - https://shop.petlandoman.com' + h)
