import pickle
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

COOKIES_FILE = "x_cookies.pkl"

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Xのトップページへ
driver.get("https://x.com/login")

print("🔐 手動でログインしてください...")
input("✅ ログインが完了したら、Enterキーを押してください")

# Cookieを保存
with open(COOKIES_FILE, "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print(f"✅ Cookieを {COOKIES_FILE} に保存しました")

driver.quit()
