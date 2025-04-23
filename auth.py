# auth.py
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from models import User
from database import fake_users_db

# JWT生成・検証用の設定
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# パスワードハッシュ化の設定（bcrypt）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# tokenの受け取り方法を定義
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# プレーンパスワードとハッシュの照合
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ユーザー認証処理（DB照合）
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return User(username=username)

# JWTトークンの生成
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # 有効期限をトークンに埋め込み
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# トークンからユーザー情報を取得
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return User(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")