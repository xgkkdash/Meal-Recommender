from fastapi import APIRouter


router = APIRouter(tags=["plans"])


@router.get("/plans")
async def get_plans():
    pass


@router.get("/plans/{plan_id}")
async def get_plan():
    pass


@router.post("/plans")
async def generate_plan():
    pass
