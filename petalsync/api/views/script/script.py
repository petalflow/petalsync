from fastapi import Depends, Header, HTTPException
from typing import Dict
from typing import List
from fastapi import HTTPException
from api.config.dbConfig import router
from api.model.db import Scripts
from api.schemas.schemas import ScriptModel, ScriptModelExecute, ScriptSaveModel, ScriptEditModel
from api.service.service import ScriptRunner

@router.get("/GetScriptsId/{id_script}", response_model=List[ScriptModel], tags=['Script'])
def get_script(id_script: int):
    try:
        scripts = Scripts.objects(id_script=id_script).all()
        if scripts:
            script_data = [ScriptModel(
                id_script=script.id_script,
                id_project=script.id_project,
                script_name=script.script_name,
                ds_script=script.ds_script, 
                nr_execution_order=script.nr_execution_order
            )for script in scripts]
            return script_data
        else:
            return {"message": "No script found with this id_script"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/GetScriptsIdprojects/{id_project}/", response_model=List[ScriptModel], tags=['Script'])
def get_scripts(id_project: int):
    try:
        scripts = Scripts.objects(id_project=id_project).all()
        if scripts:
            script_data = [ScriptModel(
                id_script=script.id_script,
                id_project=script.id_project,
                script_name=script.script_name,
                ds_script=script.ds_script,
                nr_execution_order=script.nr_execution_order
            ) for script in scripts]
            return script_data
        else:
            return {"message": "No scripts found with this id_project"}
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/CreateScripts", response_model=ScriptSaveModel, tags=['Script'])
def create_script(script: ScriptSaveModel):
    #ds_script_data = ds_script
    new_script = Scripts(
        id_project=script.id_project,
        script_name=script.script_name,
        ds_script=script.ds_script,
        nr_execution_order=script.nr_execution_order
    )
    new_script.save()
    return script
 
@router.put("/UpdateScripts/{id_script}", response_model=ScriptEditModel, tags=['Script'])
def update_script(id_script: int, new_script: ScriptEditModel):
    try:
        script = Scripts.objects(id_script=id_script).first()
        if script:
            script.ds_script = new_script.ds_script
            script.script_name = new_script.script_name
            script.nr_execution_order = new_script.nr_execution_order
            script.save()
        return new_script
    except Exception as e:
        return {"error": str(e)}

@router.delete("/DeleteScripts/{id_script}",response_model=Dict[str, str], tags=['Script'])
def delete_script(id_script: int):
    try:
        script = Scripts.objects(id_script=id_script).first()
        if script:
            script.delete()
            return {"message": "Script deleted successfully"}
    except Exception as e: 
        return {"error": str(e)}


@router.post("/ExecScript/{id_script}", tags=['Script'])
def exec_script(id_script: int):
    try:
        script_obj = Scripts.objects(id_script=id_script).first()

        if not script_obj:
            raise HTTPException(status_code=404, detail="Script não encontrado")

        script_runner = ScriptRunner(script_obj.ds_script)

        script_output = script_runner.execute_script()

        return {"output": script_output}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        return {"error": str(e)}


# executar um script sem salvar no banco
@router.post("/ExecScript", tags=['Script'])
def exec_script(script: ScriptModelExecute):
    try:
        script_runner = ScriptRunner(script.ds_script)

        script_output = script_runner.execute_script()

        return {"output": script_output}

    except Exception as e:
        return {"error": str(e)}