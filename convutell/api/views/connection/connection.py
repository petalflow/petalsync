from fastapi import APIRouter
from fastapi import Depends, Header, HTTPException
from typing import List
from api.config.dbConfig import db, router
from api.model.db import ConnectionDestination
from api.schemas.schemas import ConnectionDestinationModel, ConnectionDestinationSaveModel
from api.controller.deleteall import ConnectionDestinationDeleter

router = APIRouter()

@router.get("/connections", response_model=List[ConnectionDestinationModel], tags=['Connection'])
def get_connections():
    connections = ConnectionDestination.objects().all()
    connections_data = [
        ConnectionDestinationModel(
            id_connection=connection.id_connection,
            ds_name_connection=connection.ds_name_connection,
            ds_user=connection.ds_user,
            ds_connection=connection.ds_connection,
            ds_password=connection.ds_password,
            ds_port=connection.ds_port,
            ds_database=connection.ds_database,
            ds_connector=connection.ds_connector
        )
        for connection in connections
    ]
    return connections_data

@router.get("/connections/{id_connection}", response_model=ConnectionDestinationModel, tags=['Connection'])
def get_connection(id_connection: int):
    try:
        connection = ConnectionDestination.objects(id_connection=id_connection).first()
        if connection:
            connection_data = ConnectionDestinationModel(
                id_connection=connection.id_connection,
                ds_name_connection=connection.ds_name_connection,
                ds_user=connection.ds_user,
                ds_connection=connection.ds_connection,
                ds_password=connection.ds_password,
                ds_port=connection.ds_port,
                ds_database=connection.ds_database,
                ds_connector=connection.ds_connector
            )
            return connection_data
        else:
            return {"message": "No connection found with this id_connection"}
    except Exception as e:
        return {"error": str(e)}

@router.post("/connections", response_model=ConnectionDestinationSaveModel, tags=['Connection'])
def create_connection(connection: ConnectionDestinationSaveModel):
    new_connection = ConnectionDestination(
        ds_name_connection=connection.ds_name_connection,
        ds_user=connection.ds_user,
        ds_connection=connection.ds_connection,
        ds_password=connection.ds_password,
        ds_port=connection.ds_port,
        ds_database=connection.ds_database,
        ds_connector=connection.ds_connector
    )
    new_connection.save()
    return connection

@router.put("/connections/{id_connection}", response_model=ConnectionDestinationSaveModel, tags=['Connection'])
def update_connection(id_connection: int, connection: ConnectionDestinationSaveModel):
    updated_connection = ConnectionDestination.objects(id_connection=id_connection).first()
    if updated_connection:
        updated_connection.update(
            ds_name_connection=connection.ds_name_connection,
            ds_user=connection.ds_user,
            ds_connection=connection.ds_connection,
            ds_password=connection.ds_password,
            ds_port=connection.ds_port,
            ds_database=connection.ds_database,
            ds_connector=connection.ds_connector
        )
        return connection
    else:
        return {"message": "No connection found with this id_connection"}

@router.delete("/connections/{id_connection}", tags=['Connection'])
def delete_connection(id_connection: int):
    deleted_connection = ConnectionDestination.objects(id_connection=id_connection).first()
    if deleted_connection:
        ConnectionDestinationDeleter().delete_connection_destination(id_connection)
        return {"message": "Connection deleted successfully"}
    else:
        return {"message": "No connection found with this id_connection"}
