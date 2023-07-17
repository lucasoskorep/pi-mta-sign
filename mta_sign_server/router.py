from datetime import datetime

from fastapi import APIRouter, status

router = APIRouter(
    tags=["start"],
)

start_time = datetime.now()
@router.post("/api/start_time", status_code=status.HTTP_200_OK)
def get_start_time():
    return start_time.isoformat()
