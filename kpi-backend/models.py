# models.py
from pydantic import BaseModel # Pydanticモジュール: データバリデーションと設定管理を行うためのライブラリ
from datetime import date # datetimeモジュール: 日付や時間を扱うためのモジュール
from typing import Optional # Optionalモジュール: 型ヒントでオプションの値を指定するためのモジュール

class Metric(BaseModel):
    date: date
    instagram: Optional[int] = None
    tiktok: Optional[int] = None
    x: Optional[int] = None  # Twitter (旧X)

class User(BaseModel):
    username: str