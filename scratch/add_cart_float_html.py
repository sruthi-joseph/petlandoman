import glob
import re

cart_html = '''    <!-- Floating Shopping Cart Button -->
    <a href="https://shop.petlandoman.com/" class="cart-float" target="_blank" aria-label="Shop Petland Oman">
        <i class="fa-solid fa-cart-shopping"></i>
    </a>
'''

updated_files = []
for filepath in glob.glob('**/*.html', recursive=True):
    if 'node_modules' in filepath or 'scratch' in filepath or 'studio' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'whatsapp-float' in content and 'cart-float' not in content:
        # Match the floating whatsapp anchor block
        pattern = re.compile(r'(<a href="https://wa\.me/[^"]*" class="whatsapp-float"[^>]*>.*?</a>)', re.DOTALL)
        match = pattern.search(content)
        if match:
            new_content = pattern.sub(cart_html + r'\1', content, count=1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files.append(filepath)
            print(f'Updated {filepath}')
        else:
            print(f'WARNING: whatsapp-float match failed in {filepath}')

print(f'\nTotal files updated with cart-float HTML: {len(updated_files)}')
