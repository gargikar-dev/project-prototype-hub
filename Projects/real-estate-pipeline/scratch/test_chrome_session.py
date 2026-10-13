import os
import shutil
import tempfile
from playwright.sync_api import sync_playwright

chrome_user_dir = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
temp_dir = os.path.join(tempfile.gettempdir(), "chrome_playwright_test")
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir, ignore_errors=True)

# Copy minimal profile files
os.makedirs(os.path.join(temp_dir, "Default"), exist_ok=True)
for fname in ["Preferences", "Secure Preferences"]:
    src = os.path.join(chrome_user_dir, "Default", fname)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(temp_dir, "Default", fname))
for fname in ["Local State"]:
    src = os.path.join(chrome_user_dir, fname)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(temp_dir, fname))

try:
    src_cookies = os.path.join(chrome_user_dir, "Default", "Network", "Cookies")
    dst_cookies_dir = os.path.join(temp_dir, "Default", "Network")
    os.makedirs(dst_cookies_dir, exist_ok=True)
    if os.path.exists(src_cookies):
        shutil.copy2(src_cookies, os.path.join(dst_cookies_dir, "Cookies"))
        print("Copied Cookies!")
except Exception as e:
    print("Cookie copy error:", e)

with sync_playwright() as p:
    try:
        # Launch persistent context
        context = p.chromium.launch_persistent_context(
            user_data_dir=temp_dir,
            channel="chrome",
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.new_page()
        page.goto("https://docs.google.com/spreadsheets/d/1k8aPzpsR3E-yIGsjEpr87cGrzwhgHqUjw-SSagyxSiQ/edit", timeout=15000)
        print("Sheet Page URL:", page.url)
        print("Sheet Page Title:", page.title())
        context.close()
    except Exception as e:
        print("Error launching persistent context:", e)
