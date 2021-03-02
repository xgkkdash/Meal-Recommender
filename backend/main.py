import codecs
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    with codecs.open("hello_world.html", "r", "utf-8") as f:
        html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("main:app", host='0.0.0.0', port=port, reload=True)
