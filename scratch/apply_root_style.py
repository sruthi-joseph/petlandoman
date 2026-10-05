import os
import re

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
    color: #000000 !important;
    line-height: 1;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    transition: var(--transition-smooth);
    text-decoration: none;
}

.nav-cart-item a i {
    color: #000000 !important;
    font-size: 1.1rem;
    margin-bottom: 2px;
}

.nav-cart-text {
    font-size: 0.6rem;
    font-weight: 800;
    color: #000000 !important;
    letter-spacing: 0.5px;
    white-space: nowrap;
    text-transform: uppercase;
    font-family: var(--font-primary);
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
        color: var(--white) !important;
    }
    .nav-cart-item a i {
        color: var(--white) !important;
        font-size: 1.5rem;
    }
    .nav-cart-text {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--white) !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
'''

# Update root style.css
filepath = 'style.css'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove old nav-cart-item blocks if any
content = re.sub(r'/\* Nav Cart Item \*/.*?(?=\n/\*|\n@|\n[a-zA-Z\.#]|\Z)', '', content, flags=re.DOTALL)
content = re.sub(r'\.nav-cart-item\s*\{[^}]*\}', '', content)
content = re.sub(r'\.nav-cart-item::before\s*\{[^}]*\}', '', content)
content = re.sub(r'\.nav-cart-item a\s*\{[^}]*\}', '', content)
content = re.sub(r'\.nav-cart-item a i\s*\{[^}]*\}', '', content)
content = re.sub(r'\.nav-cart-text\s*\{[^}]*\}', '', content)

# Insert Desktop CSS after nav ul li a.active { ... }
target_desk = 'nav ul li a.active {\n    background-color: rgba(0, 0, 0, 0.08);\n    color: var(--black);\n}'
if target_desk in content:
    content = content.replace(target_desk, target_desk + '\n' + desktop_css)
else:
    print('Warning: target_desk not found')

# Insert Mobile CSS after nav ul li a.active { color: #FCC203 !important; background-color: transparent !important; }
target_mob = 'nav ul li a.active {\n        color: #FCC203 !important;\n        background-color: transparent !important;\n    }'
if target_mob in content:
    content = content.replace(target_mob, target_mob + '\n' + mobile_css)
else:
    print('Warning: target_mob not found')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Root style.css successfully updated!')
