import os

import uvicorn
from fastapi import FastAPI

# load environment variables
# port = os.environ["PORT"]

# initialize FastAPI
app = FastAPI()

@app.get("/")
def index():
    return {"data": "Application ran successfully - FastAPI"}
