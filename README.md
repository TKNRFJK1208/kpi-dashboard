# kpi-dashboard
# 📊 SNS KPI ダッシュボード - Vue × FastAPI × Supabase

日々のInstagram / TikTok / X（旧Twitter）のフォロワー数を自動取得し、ダッシュボードに可視化するアプリです。

---

## 🏗️ アーキテクチャ概要
+----------------+ +----------------------+ +------------------+ | | | | | | | Vue + ChartJS | <--> | FastAPI (REST API) | <--> | Supabase (DB) | | Frontend | | JWT認証付き | | RLS + Row Insert | +----------------+ +----------------------+ +------------------+

                    ↑
                    │
          +---------------------+
          |  Python (Selenium)  |
          |  各SNSをスクレイピング  |
          +---------------------+

---

## 🔄 処理の流れ

1. **SNSごとのPythonスクリプト（例: `tiktok_scraping.py`）**
    - Seleniumでログイン or Cookie読み込み
    - フォロワー数取得
    - Supabaseへ`POST`で送信

2. **FastAPI (`/metrics`, `/tiktok_metrics` など)**
    - Supabaseからデータを取得
    - JWT認証で保護

3. **フロントエンド（Vue + Chart.js）**
    - トークンを使ってAPIにアクセス
    - 折れ線グラフで推移を表示
    - 「全期間 / 直近7日」切り替え対応
    - SNS種別セレクトボックスあり

---

## 📦 使用技術

| 種類        | 技術・ライブラリ        |
|-------------|--------------------------|
| フロント     | Vue 3, Chart.js, Tailwind |
| バックエンド | FastAPI, JWT             |
| DB          | Supabase (PostgreSQL)    |
| スクレイピング | Python + Selenium       |

---

## ✨ 今後追加予定の機能

- [ ] フォロワー以外の指標（投稿数、いいね等）も可視化
- [ ] データエクスポート（CSV）
- [ ] ABテスト付きLPとの連動
- [ ] Supabase Auth連携（複数ユーザー対応）

---

## 📸 スクリーンショット

（ここにダッシュボード画面やスピナーなどの画像を貼ると見栄えが良くなります）

---

## 📁 ディレクトリ構成（一部）
kpi-dashboard/ ├── backend/ │ ├── main.py │ ├── metrics.py │ ├── scraping/ │ ├── tiktok_scraping.py │ ├── ig_scraping.py │ └── x_scraping.py ├── frontend/ │ ├── src/components/ │ ├── ChartComponent.vue │ ├── Login.vue │ ├── App.vue ├── .env


---

## 🧪 起動方法

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev

```env
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=your-api-key


---