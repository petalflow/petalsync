from fastapi import Depends, Header, HTTPException
from typing import List
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from config.dbConfig import db, router, templates
from model.db import Project
from schemas.schemas import ProjectModel, ProjectSaveModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Defina o diretório dos templates HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/")
def get_projects(request: Request):
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
    return templates.TemplateResponse("project/project.html", {"request": request, "projects": projects_data})

