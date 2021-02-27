import codecs

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    with codecs.open("hello_world.html", "r", "utf-8") as f:
        html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
