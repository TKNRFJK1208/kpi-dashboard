from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import re
from datetime import date
import os
from dotenv import load_dotenv

# --- Supabase設定 ---
# Load environment variables from a .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "tiktok_metrics"

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("Supabase URL or API Key is missing in the environment variables.")



def get_tiktok_followers(username):
    followers = "取得失敗"
    driver = None

    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")  # 必要ならヘッドレスに

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        url = f"https://www.tiktok.com/@{username}"
        driver.get(url)
        time.sleep(5)

        try:
            followers_elem = driver.find_element(By.XPATH, '//strong[@data-e2e="followers-count"]')
            raw_text = followers_elem.text
            followers = re.sub(r'[^\d]', '', raw_text)
            print(f"✅ {username} のフォロワー数: {followers}")
        except Exception as e:
            print(f"⚠️ フォロワー数取得失敗: {e}")
            driver.save_screenshot("tiktok_debug.png")
            print("📸 スクリーンショット保存: tiktok_debug.png")

    except Exception as e:
        print(f"⚠️ エラー発生: {e}")
    finally:
        if driver:
            driver.quit()
        return followers

def send_to_supabase(followers_count):
    today = date.today().isoformat()

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    payload = {
        "date": today,
        "followers": int(followers_count),
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=headers,
        json=payload
    )

    if response.status_code in [200, 201]:
        print(f"✅ Supabase送信成功！status_code: {response.status_code}")
    else:
        print(f"❌ Supabase送信失敗: {response.status_code}, {response.text}")

# --- テスト実行
if __name__ == "__main__":
    username = "mayu_ann1133"  # ← ここに調べたいTikTokアカウント名
    followers = get_tiktok_followers(username)

    if followers != "取得失敗":
        send_to_supabase(followers)
