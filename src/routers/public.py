from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.dependencies.get_db import get_db
from src.services.venue import VenueService
from src.services.wx_miniprogram import WxMiniprogramService
from src.schemas.wx_miniprogram import VenueStatusResponse, PublicVenuesStatusResponse

router = APIRouter(prefix="/public", tags=["公共看板"])

@router.get("/venues-status", response_model=PublicVenuesStatusResponse)
def get_venues_status(
    db: Session = Depends(get_db)
):
    """获取考场实时状态"""
    try:
        venues_status = WxMiniprogramService.get_all_venues_status(db)
        
        return PublicVenuesStatusResponse(
            timestamp=datetime.now().isoformat(),
            venues=venues_status
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取考场状态失败: {str(e)}")

@router.get("/venues/{venue_id}/status", response_model=VenueStatusResponse)
def get_venue_status(
    venue_id: int,
    db: Session = Depends(get_db)
):
    """获取指定考场状态"""
    try:
        status = WxMiniprogramService.get_venue_status(db, venue_id)
        if not status:
            raise HTTPException(status_code=404, detail="考场不存在")
        
        return VenueStatusResponse(**status)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取考场状态失败: {str(e)}") 