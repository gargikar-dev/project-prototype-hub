from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        print("Playwright Title:", page.title())
        browser.close()
        print("Playwright works in headless mode!")
except Exception as e:
    print("Playwright Error:", e)
