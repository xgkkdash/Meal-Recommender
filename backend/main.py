import codecs
import os

import motor.motor_asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


def init_db():
    db_name = os.environ.get('DB_NAME', 'MR_DEV')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '27017')
    db_url = "mongodb://" + db_host + ":" + str(db_port) + "/"
    db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    return db_client[db_name]


db = init_db()

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    with codecs.open("hello_world.html", "r", "utf-8") as f:
        html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("main:app", host='0.0.0.0', port=port, reload=True)
