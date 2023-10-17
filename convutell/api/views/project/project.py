from fastapi import Depends, Header, HTTPException
from typing import List
from datetime import datetime
from api.config.dbConfig import db, router
from api.model.db import Project
from api.schemas.schemas import ProjectModel, ProjectSaveModel, ProjectEditModel

 
@router.get("/GetAllProjects", response_model=List[ProjectModel], tags=['Project'])
def get_projects():
    projects = Project.objects().all()
    projects_data = [
        ProjectModel(
            id_project=project.id_project,
            name_project=project.name_project,
            dt_last_run=project.dt_last_run,
            fl_active=project.fl_active,
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
                connection_origin1=project.connection_origin1,
                connection_origin2=project.connection_origin2,
            )
            return project_data
        else:
            return {"message": "Não possui projeto com esse id_project"}
    except Exception as e:
        return {"error": str(e)}

@router.post("/CreateProjects", response_model=ProjectSaveModel, tags=['Project'])
def create_project(project: ProjectSaveModel):
    new_project = Project(
        name_project=project.name_project,
        dt_last_run=datetime.combine(project.dt_last_run, datetime.min.time()).isoformat(),
        fl_active=project.fl_active,
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
            #existing_project.dt_last_run = project.dt_last_run
            existing_project.fl_active = project.fl_active
            existing_project.connection_origin1 = project.connection_origin1
            existing_project.connection_origin2 = project.connection_origin2
            existing_project.save()
            return project
        else:
            return {"message": "Projeto não encontrado"}
    except Exception as e:
        return {"error": str(e)}


@router.delete("/DeleteProjects/{project_id}", response_model=ProjectModel, tags=['Project'])
def delete_project(project_id: int):
    deleted_project = Project.objects(id_project=project_id).first()
    if deleted_project:
        deleted_project.delete()
        return deleted_project
    else:
        raise HTTPException(status_code=404, detail="Project not found")