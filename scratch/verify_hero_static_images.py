from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Desktop viewport screenshot
    page_desk = browser.new_page(viewport={'width': 1280, 'height': 800})
    page_desk.goto('http://localhost:8080/')
    page_desk.wait_for_timeout(1000)
    page_desk.screenshot(path='c:/Users/SRUTHI/.gemini/antigravity-ide/brain/f4dee9e1-f3c6-422f-be04-76cad195ee13/hero_desktop_static.png')
    print('Saved hero_desktop_static.png')
    
    # Mobile viewport screenshot
    page_mob = browser.new_page(viewport={'width': 375, 'height': 750})
    page_mob.goto('http://localhost:8080/')
    page_mob.wait_for_timeout(1000)
    page_mob.screenshot(path='c:/Users/SRUTHI/.gemini/antigravity-ide/brain/f4dee9e1-f3c6-422f-be04-76cad195ee13/hero_mobile_static.png')
    print('Saved hero_mobile_static.png')
    
    browser.close()
