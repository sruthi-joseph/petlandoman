import glob
import re

# 1. Update HTML files
cart_li_html = '''<li class="nav-cart-item">
                        <a href="https://shop.petlandoman.com/" aria-label="Shop Now" target="_blank" rel="noopener">
                            <i class="fa-solid fa-cart-shopping"></i>
                            <span class="nav-cart-text">SHOP NOW</span>
                        </a>
                    </li>'''

old_cart_li_pattern = re.compile(
    r'<li class="nav-cart-item">\s*<a href="https://shop\.petlandoman\.com/"[^>]*>.*?</a>\s*</li>',
    re.DOTALL | re.IGNORECASE
)

updated_html_count = 0
for filepath in glob.glob('**/*.html', recursive=True):
    if 'node_modules' in filepath or 'scratch' in filepath or 'studio' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'nav-cart-item' in content:
        new_content = old_cart_li_pattern.sub(cart_li_html, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_html_count += 1
        print(f'Updated HTML: {filepath}')

print(f'Total HTML files updated: {updated_html_count}')


# 2. Update CSS files
desktop_css = '''
/* Nav Cart Item */
.nav-cart-item {
    display: flex;
    align-items: center;
    position: relative;
}

.nav-cart-item::before {
    content: '';
    display: inline-block;
    width: 1px;
    height: 24px;
    background-color: rgba(0, 0, 0, 0.25);
    margin-right: 0.3rem;
}

.nav-cart-item a {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #000000;
    line-height: 1;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    transition: var(--transition-smooth);
}

.nav-cart-item a i {
    color: #000000;
    font-size: 1.05rem;
    margin-bottom: 2px;
}

.nav-cart-text {
    font-size: 0.62rem;
    font-weight: 700;
    color: #000000;
    letter-spacing: 0.4px;
    white-space: nowrap;
    text-transform: uppercase;
}
'''

mobile_css = '''
    .nav-cart-item {
        margin-left: 0;
    }
    .nav-cart-item::before {
        display: none;
    }
    .nav-cart-item a {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
        color: var(--white);
    }
    .nav-cart-item a i {
        color: var(--white);
        font-size: 1.5rem;
    }
    .nav-cart-text {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--white);
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
'''

for filepath in ['style.css', 'petlandoman cms/petland-oman/style.css']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace desktop block
    content = re.sub(r'/\* Nav Cart Item \*/.*?(?=\n/\*|\n@|\n[a-zA-Z\.#]|\Z)', desktop_css.strip(), content, flags=re.DOTALL)
    
    # Replace mobile block inside @media (max-width: 768px)
    content = re.sub(r'\.nav-cart-item\s*\{[^}]*\}\s*\.nav-cart-item::before\s*\{[^}]*\}\s*\.nav-cart-item a\s*\{[^}]*\}(?:\s*\.nav-cart-item a i\s*\{[^}]*\})?(?:\s*\.nav-cart-text\s*\{[^}]*\})?', mobile_css.strip(), content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated CSS: {filepath}')
