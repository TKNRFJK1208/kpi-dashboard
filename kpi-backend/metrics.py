from fastapi import APIRouter, Depends
from models import Metric, User
from auth import get_current_user
from supabase_client import supabase

router = APIRouter()

# 📝 SNSまとめ用：KPIデータのPOST
@router.post("/metrics")
def add_metric(metric: Metric, current_user: User = Depends(get_current_user)):
    data = metric.dict()
    data["date"] = data["date"].isoformat()  # 日付をISO8601形式に変換して保存
    supabase.table("metrics").insert(data).execute()
    return {"message": "Metric added", "data": data}

# 📊 SNSまとめ用：KPIデータのGET
@router.get("/metrics")
def get_metrics(current_user: User = Depends(get_current_user)):
    res = supabase.table("metrics").select("*").order("date").execute()
    return res.data

# 📈 TikTokフォロワー推移のGET
@router.get("/tiktok_metrics")
def get_tiktok_metrics(current_user: User = Depends(get_current_user)):
    res = supabase.table("tiktok_metrics").select("*").order("date").execute()
    return res.data

# 📷 Instagramフォロワー推移のGET
@router.get("/ig_metrics")
def get_ig_metrics(current_user: User = Depends(get_current_user)):
    res = supabase.table("ig_metrics").select("*").order("date").execute()
    return res.data

# 🐦 Xフォロワー推移のGET
@router.get("/x_metrics")
def get_x_metrics(current_user: User = Depends(get_current_user)):
    res = supabase.table("x_metrics").select("*").order("date").execute()
    return res.data
