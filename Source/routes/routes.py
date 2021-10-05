from fastapi import FastAPI
import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from routes.user import user_router
from routes.login import login_router

app = FastAPI()

print(os.getcwd())

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user_router, tags=["user"])
app.include_router(login_router, tags=["login"])

