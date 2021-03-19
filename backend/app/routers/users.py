from fastapi import APIRouter

router = APIRouter(tags=["users"])


@router.get("/users")
async def get_all_users():
    pass


@router.get("/users/{account_id}")
async def get_user():
    pass


@router.delete("/users/{account_id}")
async def remove_user():
    pass
