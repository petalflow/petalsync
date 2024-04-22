
from pydantic import BaseModel
from datetime import datetime, date, time
from typing import List


class TagModel(BaseModel):
    id_tag: int
    name: str

class TagSaveModel(BaseModel):
    name: str
    
class ProjectModel(BaseModel):
    id_project: int
    name_project: str
    dt_last_run: datetime
    fl_active: int
    in_execution: int
    type_project: int
    connection_origin1: int
    connection_origin2: int
    

class ProjectSaveModel(BaseModel):
    name_project: str
    dt_last_run: datetime
    fl_active: int
    type_project: int
    connection_origin1: int
    connection_origin2: int
  

class ProjectEditModel(BaseModel):
    name_project: str
    fl_active: int
    connection_origin1: int
    connection_origin2: int

class ConnectionDestinationModel(BaseModel):
    id_connection: int
    ds_name_connection: str
    ds_user: str
    ds_connection: str
    ds_password: str
    ds_port: str
    ds_database: str
    ds_connector: str

    class Config:
        orm_mode = True

class ConnectionDestinationSaveModel(BaseModel):
    ds_name_connection: str
    ds_user: str
    ds_connection: str
    ds_password: str
    ds_port: str
    ds_database: str
    ds_connector: str

    class Config:
        orm_mode = True

 
class QueryModel(BaseModel):
    id_query: int
    id_project: int
    name_query: str
    origin_query: str
    query_destination: str
    id_type_query: int
    nr_execution_order: int

class QuerySaveModel(BaseModel):
    id_project: int
    origin_query: str
    name_query: str
    query_destination: str
    id_type_query: int
    nr_execution_order: int

class ScriptModel(BaseModel):
    id_script: int
    id_project: int 
    script_name: str
    ds_script: str
    nr_execution_order: int

class ScriptSaveModel(BaseModel):
    id_project: int
    script_name: str
    ds_script: str
    nr_execution_order: int

class ScriptEditModel(BaseModel):
    script_name: str
    ds_script: str
    nr_execution_order: int

class ScriptModelExecute(BaseModel):
    ds_script: str

class LogModel(BaseModel):
    id_log: int
    id_project: int
    dt_execution: datetime
    ds_log: str
    fl_error: int

class LogSaveModel(BaseModel):
    id_project: int
    dt_execution: datetime
    ds_log: str
    fl_error: int


class TimeModel(BaseModel):
    id_time: int
    id_project: int
    time: str

    class Config:
        orm_mode = True
        from_attributes = True


class TimeSaveModel(BaseModel):
    id_project: int
    time: str

    class Config:
        orm_mode = True
        from_attributes = True
     

class TypeQueryModel(BaseModel):
    id_type_query: int
    ds_type_query: str

    class Config:
        orm_mode = True

class UserModel(BaseModel):
    ds_first_name: str
    ds_last_name: str
    ds_email: str
    ds_password: str
    roles: list

class UserResponseModel(BaseModel):
    ds_first_name: str
    ds_last_name: str
    ds_email: str
    ds_password: str
    roles: list

    class Config:
        orm_mode = True
   