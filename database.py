# database.py
from models import Item

# アイテムDB（UUIDで管理）
fake_items_db = {}

# ユーザーデータ（実務ではDBに接続）
fake_users_db = {
    "taka": {
        "username": "taka",
        "hashed_password": "$2b$12$abc..."  # 実際はハッシュ済み
    }
}