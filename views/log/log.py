from fastapi import Depends, Header, HTTPException
from typing import List
from config.dbConfig import db, router
from model.db import Log
from schemas.schemas import LogModel, LogSaveModel


@router.get("/GetlogId/{id_project}", response_model=LogModel, tags=['Log'])
def get_log(id_project: int):
    try:
        log = Log.objects(id_project=id_project).first()
        if log:
            log_data = LogModel(
                id_log=log.id_log,
                id_project=log.id_project,
                dt_execution=log.dt_execution,
                ds_log=log.ds_log,
                fl_error=log.fl_error
            )
            return log_data
        else:
            raise HTTPException(status_code=404, detail="Log not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/GetAlllog", response_model=List[LogModel], tags=['Log'])
def get_all_logs():
    logs = Log.objects().all()
    log_list = []
    for log in logs:
        log_data = LogModel(
            id_log=log.id_log,
            id_project=log.id_project,
            dt_execution=log.dt_execution,
            ds_log=log.ds_log,
            fl_error=log.fl_error
        )
        log_list.append(log_data)
    return log_list


@router.post("/Createlog", response_model=LogModel, tags=['Log'])
def create_log(log: LogSaveModel):
    new_log = Log(
        id_project=log.id_project,
        dt_execution=log.dt_execution,
        ds_log=log.ds_log,
        fl_error=log.fl_error
    )
    new_log.save()
    return LogModel(
        id_log=new_log.id_log,
        id_project=new_log.id_project,
        dt_execution=new_log.dt_execution,
        ds_log=new_log.ds_log,
        fl_error=new_log.fl_error
    )


@router.put("/logs/{id_log}", response_model=LogModel, tags=['Log'])
def update_log(id_log: int, log: LogSaveModel):
    updated_log = Log.objects(id_log=id_log).first()
    if updated_log:
        updated_log.id_project = log.id_project
        updated_log.dt_execution = log.dt_execution
        updated_log.ds_log = log.ds_log
        updated_log.fl_error = log.fl_error
        updated_log.save()
        return LogModel(
            id_log=updated_log.id_log,
            id_project=updated_log.id_project,
            dt_execution=updated_log.dt_execution,
            ds_log=updated_log.ds_log,
            fl_error=updated_log.fl_error
        )
    else:
        raise HTTPException(status_code=404, detail="Log not found")


@router.delete("/logs/{id_log}", response_model=LogModel, tags=['Log'])
def delete_log(id_log: int):
    deleted_log = Log.objects(id_log=id_log).first()
    if deleted_log:
        deleted_log.delete()
        return LogModel(
            id_log=deleted_log.id_log,
            id_project=deleted_log.id_project,
            dt_execution=deleted_log.dt_execution,
            ds_log=deleted_log.ds_log,
            fl_error=deleted_log.fl_error
        )
    else:
        raise HTTPException(status_code=404, detail="Log not found")