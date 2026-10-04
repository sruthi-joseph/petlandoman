import re

cart_css = '''

/* --- FLOATING SHOPPING CART BUTTON --- */
.cart-float {
    position: fixed;
    width: 60px;
    height: 60px;
    bottom: 96px;
    right: 24px;
    background-color: #000000;
    color: #FCC203 !important;
    border-radius: 50%;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    z-index: 99999;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: cartPulse 2.2s infinite;
}

.cart-float:hover {
    transform: scale(1.1) translateY(-3px);
    background-color: #FCC203;
    color: #000000 !important;
    box-shadow: 0 8px 24px rgba(252, 194, 3, 0.55);
}

.cart-float i {
    color: inherit !important;
}

@keyframes cartPulse {
    0% {
        box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.4);
    }
    70% {
        box-shadow: 0 0 0 15px rgba(0, 0, 0, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
    }
}

@media (max-width: 480px) {
    .cart-float {
        width: 52px;
        height: 52px;
        bottom: 82px;
        right: 20px;
        font-size: 23px;
    }
}
'''

for filepath in ['style.css', 'petlandoman cms/petland-oman/style.css']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '.cart-float' not in content:
        content += cart_css
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Appended .cart-float CSS to {filepath}')
    else:
        print(f'.cart-float CSS already present in {filepath}')
