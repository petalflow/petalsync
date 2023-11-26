from fastapi import Depends, Header, HTTPException
from typing import List
from datetime import datetime
from api.config.dbConfig import db, router
from api.model.db import Project
from api.schemas.schemas import ProjectModel, ProjectSaveModel, ProjectEditModel
from api.controller.deleteall import ProjectDeleter

 
@router.get("/GetAllProjects", response_model=List[ProjectModel], tags=['Project'])
def get_projects():
    projects = Project.objects().all()
    projects_data = [
        ProjectModel(   
            id_project=project.id_project,
            name_project=project.name_project,
            dt_last_run=project.dt_last_run,
            fl_active=project.fl_active,
            in_execution=project.in_execution,
            type_project=project.type_project,
            connection_origin1=project.connection_origin1,
            connection_origin2=project.connection_origin2,
        )
        for project in projects
    ]
    return projects_data

@router.get("/GetProjectsId/{id_project}", response_model=ProjectModel, tags=['Project'])
def get_project(id_project: int):
    try:
        project = Project.objects(id_project=id_project).first()
        if project:
            project_data = ProjectModel(
                id_project=project.id_project,
                name_project=project.name_project,
                dt_last_run=project.dt_last_run,
                fl_active=project.fl_active,
                in_execution=project.in_execution,
                type_project=project.type_project,
                connection_origin1=project.connection_origin1,
                connection_origin2=project.connection_origin2,
            )
            return project_data
        else:
            return {"message": "Não possui projeto com esse id_project"}
    except Exception as e:
        return {"error": str(e)}

@router.post("/CreateProjects/{type_project}", response_model=ProjectSaveModel, tags=['Project'])
def create_project(type_project: int, project: ProjectSaveModel):
    type_project = 1 if type_project != 0 else 0
    new_project = Project(
        name_project=project.name_project,
        dt_last_run=datetime.combine(project.dt_last_run, datetime.min.time()).isoformat(),
        fl_active=project.fl_active,
        type_project=type_project,
        connection_origin1=project.connection_origin1,
        connection_origin2=project.connection_origin2
    )
    new_project.save()
    return project

@router.put("/GetProjectsId/{id_project}", response_model=ProjectEditModel, tags=['Project'])
def update_project(id_project: int, project: ProjectEditModel):
    try:
        existing_project = Project.objects(id_project=id_project).first()
        if existing_project:
            existing_project.name_project = project.name_project
            existing_project.fl_active = project.fl_active
            existing_project.connection_origin1 = project.connection_origin1
            existing_project.connection_origin2 = project.connection_origin2
            existing_project.save()
            return project
        else:
            return {"message": "Projeto não encontrado"}
    except Exception as e:
        return {"error": str(e)}
 

@router.delete("/DeleteProjects/{id_project}", tags=['Project'])
def delete_project(id_project: int):
    deleted_project = Project.objects(id_project=id_project).first()
    if deleted_project:
        ProjectDeleter().delete_project_and_related_objects(id_project)
        return {"message": "Projeto excluído com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Project not found")