from fastapi import Depends, Header, HTTPException
from typing import Dict
from typing import List
from config.dbConfig import router
from model.db import Query
from schemas.schemas import QuerySaveModel, QueryModel


@router.post("/CreateQueries", response_model=QuerySaveModel, tags=['Query'])
def create_query(query: QuerySaveModel):
    new_query = Query(
        id_project=query.id_project,
        origin_query=query.origin_query,
        query_destination=query.query_destination,
        id_type_query=query.id_type_query,
        nr_execution_order=query.nr_execution_order
    )
    new_query.save()
    return query

@router.get("/GetQueriesId/{id_query}", response_model=QueryModel, tags=['Query'])
def get_query(id_query: int):
    try:
        query = Query.objects(id_query=id_query).first()
        if query:
            query_data = QueryModel(
                id_query=query.id_query,
                id_project=query.id_project,
                origin_query=query.origin_query,
                query_destination=query.query_destination,
                id_type_query=query.id_type_query,
                nr_execution_order=query.nr_execution_order
            )
            return query_data
        else:
            return {"message": "No query found with this id_query"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/GetqueriesIdprojects/{id_project}/", response_model=QueryModel, tags=['Query'])
def get_query(id_project: int):
    try:
        query = Query.objects(id_project=id_project).first()
        if query:
            query_data = QueryModel(
                id_query=query.id_query,
                id_project=query.id_project,
                origin_query=query.origin_query,
                query_destination=query.query_destination,
                id_type_query=query.id_type_query,
                nr_execution_order=query.nr_execution_order
            )
            return query_data
        else:
            return {"message": "No query found with this id_project and id_query"}
    except Exception as e:
        return {"error": str(e)}


@router.put("/UpdateQueries/{id_query}", response_model=QueryModel, tags=['Query'])
def update_query(id_query: int, query: QuerySaveModel):
    try:
        existing_query = Query.objects(id_query=id_query).first()
        if existing_query:
            existing_query.id_project = query.id_project
            existing_query.origin_query = query.origin_query
            existing_query.query_destination = query.query_destination
            existing_query.id_type_query = query.id_type_query
            existing_query.nr_execution_order = query.nr_execution_order
            existing_query.save()
            return query
        else:
            return {"message": "No query found with this id_query"}
    except Exception as e:
        return {"error": str(e)}
    
@router.delete("/DeleteQueries/{id_query}", response_model=Dict[str, str], tags=['Query'])
def delete_query(id_query: int):
    deleted_query = Query.objects(id_query=id_query).first()
    if deleted_query:
        deleted_query.delete()
        return {"message": "Query deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Query not found")
