from fastapi import APIRouter, Depends
from models import Metric, User
from auth import get_current_user
from supabase_client import supabase

router = APIRouter()

@router.post("/metrics")
def add_metric(metric: Metric, current_user: User = Depends(get_current_user)):
    data = metric.dict()
    data["date"] = data["date"].isoformat()  # ←ここが重要！
    supabase.table("metrics").insert(data).execute()
    return {"message": "Metric added", "data": data}


@router.get("/metrics")
def get_metrics(current_user: User = Depends(get_current_user)):
    res = supabase.table("metrics").select("*").order("date").execute()
    return res.data