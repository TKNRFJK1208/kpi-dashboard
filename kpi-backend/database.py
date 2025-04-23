from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 商品DB（UUIDで管理）
fake_items_db = {}

# ユーザーデータ
fake_users_db = {
    "taka": {
        "username": "taka",
        "hashed_password": pwd_context.hash("password123")
    }
}