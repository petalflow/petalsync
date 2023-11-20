from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sys
from io import StringIO
from time import sleep
import time
from datetime import datetime
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert
from api.model.db import ConnectionDestination, Project, Time, Query, Scripts, Log
from mysql.connector import connect

class ConexaoBancoDados:
    def __init__(self, ds_conexao):
        self.ds_conexao = ds_conexao
        self.engine = None

    def conectar(self):
        if self.ds_conexao.startswith('mysql'):
            self.engine = create_engine(self.ds_conexao)
        elif self.ds_conexao.startswith('postgresql'):
            self.engine = create_engine(self.ds_conexao)
        elif self.ds_conexao.startswith('sqlite'):
            self.engine = create_engine(self.ds_conexao)
        else:
            raise ValueError("Tipo de conexão não suportado")

    def executar_query(self, query):
        with self.engine.connect() as connection:
            stmt = text(query)
            result = connection.execute(stmt)
            return result.fetchall()

class ProjectUpdater:
    @staticmethod
    def update_last_run(id_project):
        project = Project.objects(id_project=id_project).first()
        if project:
            project.dt_last_run = datetime.now()
            project.save()

class Logger:
    def log_entry(self, project_id, log_message, error=False):
        log = Log(
            id_project=project_id,
            dt_execution=datetime.now(),
            ds_log=log_message,
            fl_error=int(error)
        )
        log.save()

class ScritpExecPy:
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
            raise ValueError(f"Erro ao executar o script: {str(e)}")

        finally:
            sys.stdout = sys.__stdout__

class Connection:
    def __init__(self, project_id):
        self.project_id = project_id
        self.connection = None

    def get_connection(self):
        project = Project.objects(id_project=self.project_id).first()
        if project:
            connection_origin1 = project.connection_origin1
            connection_origin2 = project.connection_origin2

            connections = ConnectionDestination.objects(id_connection__in=[connection_origin1, connection_origin2])

            for connection in connections:
                connection_info = {
                    "ID Project": self.project_id,
                    "ID Connection": connection.id_connection,
                    "nameConnection": connection.ds_name_connection,
                    "User": connection.ds_user,
                    "IP": connection.ds_connection,
                    "Password": connection.ds_password,
                    "Port": connection.ds_port,
                    "Database": connection.ds_database,
                    "Connector": connection.ds_connector
                }
                return connection_info

class DataMigration:
    def __init__(self):
        self.metadata = sqlalchemy.MetaData()

    def migrate_data(self):
        current_time = datetime.now().time()
        current_time_str = current_time.strftime("%H:%M:%S")
        times = Time.objects(time=current_time_str)

        connections_list = []

        for time_obj in times:
            project = Project.objects(id_project=time_obj.id_project, fl_active=1,
                                 connection_origin1__ne=0, connection_origin2__ne=0).first()
            
            if project.type_project == 1:
                pyscript = Scripts.objects(id_project=project.id_project).order_by('nr_execution_order').all()

                if pyscript:
                    for script in pyscript:
                        id_project = script.id_project
                        script_name = script.script_name
                        ds_script = script.ds_script
                        nr_execution_order = script.nr_execution_order

                        logger = Logger()

                        print(f"Script: {script_name}")
                        print(f"Script: {ds_script}")
                        print(f"Script: {nr_execution_order}")

                        logger.log_entry(id_project, "Início da ETL", error=False)
                        script_runner = ScritpExecPy(ds_script)
                        script_runner.execute_script()

                        print(f"Script: {script_runner}")
                        
                        logger.log_entry(id_project, "Finalizando ETL", error=False)      

            else:
                if project:
                    project_id = project.id_project
                    connection_origin1 = project.connection_origin1
                    connection_origin2 = project.connection_origin2

                    connections = ConnectionDestination.objects(id_connection__in=[connection_origin1, connection_origin2])

                    for connection in connections:
                        connection_info = {
                            "ID Project": project_id,
                            "ID Connection": connection.id_connection,
                            "nameConnection": connection.ds_name_connection,
                            "User": connection.ds_user,
                            "IP": connection.ds_connection,
                            "Password": connection.ds_password,
                            "Port": connection.ds_port,
                            "Database": connection.ds_database,
                            "Connector": connection.ds_connector
                        }
                        connections_list.append(connection_info)

        if connections_list:
            connection_info_origin1 = connections_list[0]
            connection_info_origin2 = connections_list[1]

            ds_user_origin1 = connection_info_origin1["User"]
            ds_connection_origin1 = connection_info_origin1["IP"]
            ds_password_origin1 = connection_info_origin1["Password"]
            ds_database_origin1 = connection_info_origin1["Database"]
            ds_charset_origin1 = "utf8"
            ds_connector_origin1 = connection_info_origin1["Connector"]
            ds_name_connection1   =  connection_info_origin1["nameConnection"]

            ds_user_origin2 = connection_info_origin2["User"]
            ds_connection_origin2 = connection_info_origin2["IP"]
            ds_password_origin2 = connection_info_origin2["Password"]
            ds_database_origin2 = connection_info_origin2["Database"]
            ds_charset_origin2 = "utf8"
            ds_connector_origin2 = connection_info_origin2["Connector"]
            ds_name_connection2 = connection_info_origin2["nameConnection"]

            if ds_connector_origin1 and ds_connector_origin2 is not None:
                ds_conexao_origin1 = f"{ds_connector_origin1}://{ds_user_origin1}:{ds_password_origin1}@{ds_connection_origin1}/{ds_database_origin1}?charset={ds_charset_origin1}"
                ds_conexao_origin2 = f"{ds_connector_origin2}://{ds_user_origin2}:{ds_password_origin2}@{ds_connection_origin2}/{ds_database_origin2}?charset={ds_charset_origin2}"

            conexao_origin1 = ConexaoBancoDados(ds_conexao_origin1)
            conexao_origin2 = ConexaoBancoDados(ds_conexao_origin2)

            conexao_origin1.conectar()
            conexao_origin2.conectar()

            query_list = Query.objects(id_project=project_id).order_by('nr_execution_order').all()

            if query_list:
                logger = Logger()  # Instancia a classe Logger
                logger.log_entry(project_id, "Início da ETL")
                for query_obj in query_list:
                    origin_query = query_obj.origin_query
                    query_destination = query_obj.query_destination
                    id_type_query = query_obj.id_type_query

                    logger.log_entry(project_id, "Início da consulta")  # Inserir log de início

                    print(f"Consulta de Origem: {origin_query}")
                    print(f"Consulta de Destino: {query_destination}")

                    origin_results = conexao_origin1.executar_query(origin_query)
                    if origin_results:
                        try:
                            with conexao_origin2.engine.connect() as connection:
                                metadata = sqlalchemy.MetaData()
                                metadata.reflect(bind=conexao_origin2.engine)
                                try:
                                    table = metadata.tables[query_destination]
                                except KeyError:
                                    raise ValueError(f"Tabela de destino '{query_destination}' não encontrada.")

                                if id_type_query == 2:
                                    truncate_stmt = sqlalchemy.sql.text(f"TRUNCATE TABLE {query_destination}")
                                    connection.execute(truncate_stmt)

                                insert_stmt = insert(table).values([result._asdict() for result in origin_results])
                                connection.execute(insert_stmt)
                                connection.commit()

                            logger.log_entry(project_id, "Consulta concluída com sucesso")  # Inserir log de conclusão
                        except SQLAlchemyError as e:
                            logger.log_entry(project_id, f"Erro ao executar a inserção: {str(e)}", error=True)
                            logger.log_entry(project_id, "Consulta finalizada como erro")

                        except ValueError as e:
                            logger.log_entry(project_id, f"{str(e)}", error=True)
                            logger.log_entry(project_id, "Consulta concluída como erro")
                    else:
                        logger.log_entry(project_id, "Nenhum resultado retornado pela consulta de origem.", error=True)
                        logger.log_entry(project_id, "Concluída consulta")

                logger.log_entry(project_id, "Finalizando ETL")
                ProjectUpdater.update_last_run(project_id)
            else:
                logger.log_entry(project_id, "Nenhuma consulta encontrada para o projeto.", error=True)

    def run(self):
         while True:
            current_time = datetime.now().time()
            current_time_str = current_time.strftime("%H:%M:%S")
            times = Time.objects(time=current_time_str)
            if times:
                self.migrate_data()
            time.sleep(0.9)


data_migration = DataMigration()
data_migration.run()
