import glob
import re

old_cart_li = re.compile(
    r'<li class="nav-cart-item">\s*<a href="https://shop\.petlandoman\.com/" aria-label="Shopping Cart"[^>]*>\s*<i class="fa-solid fa-cart-shopping"></i>(?:<span class="nav-cart-text">[^<]*</span>)?\s*</a>\s*</li>',
    re.IGNORECASE
)

new_cart_li = '''<li class="nav-cart-item">
                        <a href="https://shop.petlandoman.com/" aria-label="Shopping Cart" target="_blank" rel="noopener">
                            <i class="fa-solid fa-cart-shopping"></i>
                        </a>
                    </li>'''

updated_files = []
for filepath in glob.glob('**/*.html', recursive=True):
    if 'node_modules' in filepath or 'scratch' in filepath or 'studio' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'nav-cart-item' in content:
        new_content = old_cart_li.sub(new_cart_li, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_files.append(filepath)
        print(f'Updated {filepath}')

print(f'\nTotal HTML files updated: {len(updated_files)}')
