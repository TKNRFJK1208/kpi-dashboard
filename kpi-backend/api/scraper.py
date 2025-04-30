from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from auth import get_current_user
from models import User
import subprocess

router = APIRouter()

@router.post("/scrape-all")
def scrape_all(current_user: User = Depends(get_current_user)):
    try:
        subprocess.run(["python3", "scraper_trigger.py"])
        return JSONResponse(content={"message": "スクレイピング完了"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)