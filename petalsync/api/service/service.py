import sys
from io import StringIO
from fastapi import HTTPException

class ScriptRunner:
    def __init__(self, script):
        self.script = script
        self.output_buffer = StringIO()

    def execute_script(self):
        try:
            sys.stdout = self.output_buffer

            local_vars = {}
            global_vars = {}
            exec(self.script, global_vars, local_vars)

            script_output = self.output_buffer.getvalue()
            return script_output

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao executar o script: {str(e)}")

        finally:
            sys.stdout = sys.__stdout__