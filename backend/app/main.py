import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.database import connect_db
from app.routers import users, profile

app = FastAPI()
app.include_router(users.router)
app.include_router(profile.router)
app.add_event_handler("startup", connect_db)


@app.get("/")
def root():
    return "Welcome to Meal_Recommender!"


if __name__ == '__main__':
    uvicorn.run("app.main:app", host='0.0.0.0', port=settings.PORT, reload=True)
