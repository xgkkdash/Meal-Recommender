import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.routers import items, users

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=settings.PORT, reload=True)
