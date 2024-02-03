from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
 
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()
 
app = FastAPI()

#app.mount("/static", StaticFiles(directory="static"), name="static")

 
origins = [    "http://localhost:5173",  "http://127.0.0.1:3000",   "http://127.0.0.1:8000",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from api.views.project import project
from api.views.connection import connection
from api.views.query import query
from api.views.log import log
from api.views.time import time 
from api.views.ds_type_query import _type
from api.views.script import script


app.include_router(project.router)
app.include_router(connection.router)
app.include_router(query.router)
app.include_router(log.router)
app.include_router(time.router)
app.include_router(_type.router)
app.include_router(script.router)
