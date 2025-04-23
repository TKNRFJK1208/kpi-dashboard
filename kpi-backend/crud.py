# crud.py
from fastapi import APIRouter, HTTPException, Depends
from models import Item, User
from database import fake_items_db
from auth import get_current_user
import uuid

router = APIRouter()

# 全件取得（認証あり）
@router.get("/items/")
def read_all_items(current_user: User = Depends(get_current_user)):
    return fake_items_db

# 新規作成（UUIDで一意に管理）
@router.post("/items/")
def create_item(item: Item, current_user: User = Depends(get_current_user)):
    item_id = str(uuid.uuid4())
    fake_items_db[item_id] = item
    return {"item_id": item_id, "item": item}

# 個別取得
@router.get("/items/{item_id}")
def read_item(item_id: str, current_user: User = Depends(get_current_user)):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

# 更新処理
@router.put("/items/{item_id}")
def update_item(item_id: str, item: Item, current_user: User = Depends(get_current_user)):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_items_db[item_id] = item
    return {"message": "Item updated", "item": item}

# 削除処理
@router.delete("/items/{item_id}")
def delete_item(item_id: str, current_user: User = Depends(get_current_user)):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_items_db[item_id]
    return {"message": "Item deleted"}