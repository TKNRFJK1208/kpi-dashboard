import os
import pickle
import time
import re
from datetime import date
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests

# 環境変数読み込み
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "ig_metrics"
COOKIES_FILE = "ig_cookies.pkl"

def get_ig_followers(username):
    followers = "取得失敗"
    driver = None

    try:
        options = Options()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")  # デバッグ用にはコメントアウト
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://www.instagram.com/")
        time.sleep(5)

        # Cookieが存在する場合は読み込み
        if os.path.exists(COOKIES_FILE):
            with open(COOKIES_FILE, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    if "sameSite" in cookie:
                        del cookie["sameSite"]
                    driver.add_cookie(cookie)
            print("✅ Cookie読み込み成功")

        # アカウントページへ移動
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(8)

        # フォロワー数の取得
        try:
            followers_elem = driver.find_element(By.XPATH, '//ul/li[2]//span')
            raw_text = followers_elem.get_attribute("title") or followers_elem.text
            followers = re.sub(r"[^\d]", "", raw_text)
            print(f"✅ {username} のフォロワー数: {followers}")
        except Exception as e:
            print("⚠️ フォロワー要素取得エラー:", e)
            driver.save_screenshot("ig_debug.png")

    except Exception as e:
        print("⚠️ フォロワー取得処理エラー:", e)

    finally:
        if driver:
            driver.quit()
        return followers

def send_to_supabase(followers):
    today = date.today().isoformat()

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    payload = {
        "date": today,
        "followers": int(followers)
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=headers,
        json=payload
    )

    if response.status_code in [200, 201]:
        print("✅ Supabase送信成功")
    else:
        print(f"❌ Supabase送信失敗: {response.status_code}, {response.text}")

# --- 実行 ---
if __name__ == "__main__":
    username = "mayu_ann1133"
    followers = get_ig_followers(username)
    if followers != "取得失敗":
        send_to_supabase(followers)
