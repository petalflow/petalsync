
from fastapi import Depends, Header, HTTPException
from typing import Dict
from typing import List
from config.dbConfig import router
from config.db import Time
from schemas.schemas import TimeModel, TimeSaveModel
from datetime import datetime, time


@router.get("/times", response_model=List[TimeModel], tags=['Time'])
def get_times():
    times = Time.objects().all()
    return [TimeModel.from_orm(time) for time in times]

@router.get("/times/{id_project}", response_model=TimeModel, tags=['Time'])
def get_time(id_project: int):
    time = Time.objects(id_project=id_project).first()
    if time:
        return TimeModel.from_orm(time)
    else:
        raise HTTPException(status_code=404, detail="Time not found")

@router.post("/times", response_model=TimeModel, tags=['Time'])
def create_time(time: TimeSaveModel):
    new_time = Time(
        id_project=time.id_project,
        time=time.time
    )
    new_time.validate()  # Executa a validação antes de salvar
    new_time.save()
    return TimeModel.from_orm(new_time)



@router.put("/times/{id_time}", response_model=TimeModel, tags=['Time'])
def update_time(id_time: int, time: TimeModel):
    updated_time = Time.objects(id_time=id_time).first()
    if updated_time:
        updated_time.id_project = time.id_project
        updated_time.time = time.time
        updated_time.save()
        return TimeModel.from_orm(updated_time)
    else:
        raise HTTPException(status_code=404, detail="Time not found")

@router.delete("/times/{id_time}", response_model=TimeModel, tags=['Time'])
def delete_time(id_time: int):
    deleted_time = Time.objects(id_time=id_time).first()
    if deleted_time:
        deleted_time.delete()
        return TimeModel.from_orm(deleted_time)
    else:
        raise HTTPException(status_code=404, detail="Time not found")