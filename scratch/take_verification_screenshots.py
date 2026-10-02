from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Desktop screenshot
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://localhost:8080/')
    page.wait_for_timeout(1000)
    page.screenshot(path='c:/Users/SRUTHI/.gemini/antigravity-ide/brain/f4dee9e1-f3c6-422f-be04-76cad195ee13/desktop_cart_final.png')
    print('Saved desktop screenshot')
    
    # Mobile screenshot
    mobile_page = browser.new_page(viewport={'width': 375, 'height': 750})
    mobile_page.goto('http://localhost:8080/')
    mobile_page.wait_for_timeout(1000)
    mobile_page.click('#nav-toggle')
    mobile_page.wait_for_timeout(500)
    mobile_page.screenshot(path='c:/Users/SRUTHI/.gemini/antigravity-ide/brain/f4dee9e1-f3c6-422f-be04-76cad195ee13/mobile_cart_final.png')
    print('Saved mobile screenshot')
    
    browser.close()
