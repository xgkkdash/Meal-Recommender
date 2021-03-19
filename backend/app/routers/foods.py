from fastapi import APIRouter

router = APIRouter(tags=["foods"])


@router.get("/foods")
async def get_all_foods():
    pass


@router.get("/foods/{name}")
async def get_food():
    pass


@router.post("/foods")
async def create_food():
    pass


@router.put("/foods/{name}")
async def update_food():
    pass


@router.delete("/foods/{name}")
async def remove_food():
    pass
