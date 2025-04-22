from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import uuid

app = FastAPI()

# 🔹 モデル定義（Item）
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# 🔹 データ保存場所（辞書型に変更 → UUIDがキー）
fake_items_db: Dict[str, Item] = {}

# 🔸 POST: 新規商品をUUID付きで登録
@app.post("/items/")
def create_item(item: Item):
    item_id = str(uuid.uuid4())  # UUIDを文字列にして作成
    fake_items_db[item_id] = item
    return {"item_id": item_id, "item": item}

# 🔸 GET: 全商品を返す
@app.get("/items/")
def read_all_items():
    return fake_items_db

# 🔸 GET: UUID指定で商品を取得
@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

# 🔸 PUT: 商品の更新
@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_items_db[item_id] = item
    return {"message": "Item updated", "item": item}

# 🔸 DELETE: 商品の削除
@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_items_db[item_id]
    return {"message": "Item deleted"}
