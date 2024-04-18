from fastapi import Depends, Header, HTTPException
from typing import List
from api.config.dbConfig import router
from api.model.db import TypeQuery
from api.schemas.schemas import TypeQueryModel

@router.get("/typeQueries", response_model=List[TypeQueryModel], tags=['Type_Queries'])
async def get_TypeQueries():
    try:
        ds_type = TypeQuery.objects().all()
        Types = [
            TypeQueryModel(
                id_type_query=_type.id_type_query,
                ds_type_query=_type.ds_type_query,
            )
            for _type in ds_type
        ]
        return Types
    except Exception as e:
        return {"error", str(e)}

