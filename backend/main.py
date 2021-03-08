import codecs
import os
from datetime import datetime, timedelta

import jwt
import motor.motor_asyncio
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import models
from database import find_user, insert_user
from schemas import UserCreate, User


SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
ALGORITHM = os.environ.get('ALGORITHM', "HS256")
TOKEN_EXPIRE_MINUTES = os.environ.get("TOKEN_EXPIRE_MINUTES", 30)


def init_db():
    db_name = os.environ.get('DB_NAME', 'MR_DEV')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '27017')
    db_url = "mongodb://" + db_host + ":" + str(db_port) + "/"
    db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    return db_client[db_name]


db = init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    with codecs.open("hello_world.html", "r", "utf-8") as f:
        html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)


@app.post("/signup")
async def user_sign_up(user: UserCreate):
    exist_user = await find_user(db, user.account_id)
    if exist_user:
        raise HTTPException(status_code=400, detail="user id already existed")
    else:
        result = await insert_user(db, models.User.from_user_base(user))
        if result and result.acknowledged:
            return User(**vars(user))
        else:
            raise HTTPException(status_code=400, detail="insert new user failed")


@app.post("/login")
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user(db, form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = _generate_token(user.account_id)
    return {"access_token": access_token}


async def _generate_token(username):
    to_encode = {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def _get_user_by_token(token: str = Depends(oauth2_scheme)):
    pass


@app.get("/users/me/", response_model=User)
async def get_self_data(current_user: User = Depends(_get_user_by_token)):
    pass


@app.get("/users/me/plan/")
async def get_self_plan(current_user: User = Depends(_get_user_by_token)):
    pass


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("main:app", host='0.0.0.0', port=port, reload=True)
