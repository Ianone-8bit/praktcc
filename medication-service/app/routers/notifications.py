# ============ FILE: medication-service/app/routers/notifications.py ============
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.db import get_db
from app.routers.auth_middleware import get_current_user
from app.models.device_token import DeviceToken

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def success_response(data=None, message="Success", meta=None):
    return {"success": True, "message": message, "data": data, "meta": meta}


@router.post("/token")
async def register_token(payload: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    token = payload.get("token")
    platform = payload.get("platform", "unknown")

    if not token:
        raise HTTPException(status_code=400, detail={"success": False, "message": "Token is required", "data": None, "meta": None})

    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail={"success": False, "message": "Invalid user", "data": None, "meta": None})

    existing = db.query(DeviceToken).filter(DeviceToken.token == token).first()
    if existing:
        existing.user_id = user_id
        existing.platform = platform
    else:
        db.add(DeviceToken(user_id=user_id, token=token, platform=platform))

    db.commit()
    return success_response(data={"token": token, "platform": platform}, message="Token registered")


@router.delete("/token")
async def delete_token(payload: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    token = payload.get("token")
    if not token:
        raise HTTPException(status_code=400, detail={"success": False, "message": "Token is required", "data": None, "meta": None})

    db.query(DeviceToken).filter(DeviceToken.token == token).delete(synchronize_session=False)
    db.commit()
    return success_response(data={"token": token}, message="Token removed")
