# models.py
from pydantic import BaseModel
from typing import Optional

# ユーザーモデル
class User(BaseModel):
    username: str

# 商品モデル
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None