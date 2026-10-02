import glob
import re

cart_li = '''
                    <li class="nav-cart-item">
                        <a href="https://shop.petlandoman.com/" aria-label="Shopping Cart" target="_blank" rel="noopener">
                            <i class="fa-solid fa-cart-shopping"></i><span class="nav-cart-text">Shopping Cart</span>
                        </a>
                    </li>'''

updated_files = []
for filepath in glob.glob('**/*.html', recursive=True):
    if 'node_modules' in filepath or 'scratch' in filepath or 'studio' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'nav-menu' in content and 'nav-cart-item' not in content:
        pattern = re.compile(r'(<li><a href="[^"]*"[^>]*>Contact Us</a></li>)', re.IGNORECASE)
        match = pattern.search(content)
        if match:
            new_content = pattern.sub(r'\1' + cart_li, content, count=1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files.append(filepath)
            print(f'Updated {filepath}')
        else:
            print(f'WARNING: Could not find Contact Us tag in {filepath}')

print(f'\nTotal files updated: {len(updated_files)}')
