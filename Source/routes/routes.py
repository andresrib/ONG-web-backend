from fastapi import FastAPI
import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from routes.user import user_router
from routes.login import login_router
from routes.ong import ong_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(os.getcwd())

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user_router, tags=["user"])
app.include_router(login_router, tags=["login"])
app.include_router(ong_router, tags=["ong"])

