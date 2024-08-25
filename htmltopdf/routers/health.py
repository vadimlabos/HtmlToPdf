from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def healthcheck():
    return {"message": "Healthy"}
