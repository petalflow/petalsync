from mongoengine import Document, StringField, DateTimeField, IntField, connect
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

import os


load_dotenv()

connection_string = os.getenv("MONGODB_CONNECTION_STRING")
connection_string_db  = os.getenv("MONGODB_CONNECTION_STRING_DB")
# Registrar a conexão com o MongoDB
db = connect(connection_string_db, host=connection_string)

templates = Jinja2Templates(directory="templates")


router = APIRouter()