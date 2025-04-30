import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 保存先
COOKIES_FILE = "ig_cookies.pkl"

def save_instagram_cookies():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("🌐 Instagramを開きます。ログインしてください。")
        driver.get("https://www.instagram.com/")
        time.sleep(10)  # ページが読み込まれるまで少し待つ

        input("🔐 Instagramにログイン後、Enterキーを押してください...")

        # Cookie保存
        cookies = driver.get_cookies()
        with open(COOKIES_FILE, "wb") as f:
            pickle.dump(cookies, f)
        print("✅ Cookie保存完了！ファイル名: ig_cookies.pkl")

    except Exception as e:
        print("❌ エラー:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    save_instagram_cookies()
