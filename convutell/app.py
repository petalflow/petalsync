from fastapi import FastAPI



app = FastAPI()

from views.project import project
from views.connection import connection
from views.query import query
from views.log import log
from views.time import time 
from views.ds_type_query import _type

app.include_router(project.router)
app.include_router(connection.router)
app.include_router(query.router)
app.include_router(log.router)
app.include_router(time.router)
app.include_router(_type.router)



