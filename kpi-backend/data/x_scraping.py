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
SUPABASE_TABLE = "x_metrics"
COOKIES_FILE = "x_cookies.pkl"

def get_x_followers(username):
    followers = "取得失敗"
    driver = None

    try:
        options = Options()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")  # 必要に応じてコメントアウト
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # 初回はトップページでCookie読み込み
        driver.get("https://x.com/")
        time.sleep(5)

        if os.path.exists(COOKIES_FILE):
            with open(COOKIES_FILE, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    if "sameSite" in cookie:
                        del cookie["sameSite"]
                    driver.add_cookie(cookie)
            print("✅ Cookie読み込み成功")
        else:
            print("⚠️ Cookieファイルが見つかりません")

        # プロフィールページへ遷移
        driver.get(f"https://x.com/{username}")
        time.sleep(7)

        try:
            followers_elem = driver.find_element(By.XPATH, '//a[contains(@href,"followers")]/span[1]/span')
            raw_text = followers_elem.text.strip()
            followers = re.sub(r"[^\d]", "", raw_text)

            if followers.isdigit():
                print(f"✅ {username} のフォロワー数: {followers}")
            else:
                print("⚠️ 数値変換に失敗しました")
                followers = "取得失敗"

        except Exception as e:
            print(f"⚠️ フォロワー要素取得失敗: {e}")
            driver.save_screenshot("x_debug.png")
            print("📸 スクリーンショットを保存しました → x_debug.png")

    except Exception as e:
        print(f"⚠️ フォロワー取得エラー: {e}")

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

# --- 実行部 ---
if __name__ == "__main__":
    username = "mayu_ann1133"
    followers = get_x_followers(username)

    if followers != "取得失敗":
        send_to_supabase(followers)
