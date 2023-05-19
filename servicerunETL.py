from sqlalchemy import create_engine
from sqlalchemy.sql import text
from time import sleep
import time
from datetime import datetime
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert
from model.db import ConnectionDestination, Project, Time, Query, Log
from mysql.connector import connect


class ConexaoBancoDados:
    def __init__(self, ds_conexao):
        self.ds_conexao = ds_conexao
        self.engine = None

    def conectar(self):
        if self.ds_conexao.startswith('mysql'):
            self.engine = create_engine(self.ds_conexao)
            print("Conectado ao banco de dados MySQL")
        elif self.ds_conexao.startswith('postgresql'):
            self.engine = create_engine(self.ds_conexao)
            print("Conectado ao banco de dados PostgreSQL")
        elif self.ds_conexao.startswith('sqlite'):
            self.engine = create_engine(self.ds_conexao)
            print("Conectado ao banco de dados SQLite")
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


class DataMigration:
    def __init__(self):
        self.metadata = sqlalchemy.MetaData()

    def migrate_data(self):
        current_time = '22:53:00'
        times = Time.objects(time=current_time)
        connections_list = []

        for time_obj in times:
            project = Project.objects(id_project=time_obj.id_project, fl_active=1,
                                  connection_origin1__ne=0, connection_origin2__ne=0).first()
            if project:
                project_id = project.id_project
                connection_origin1 = project.connection_origin1
                connection_origin2 = project.connection_origin2

                connections = ConnectionDestination.objects(id_connection__in=[connection_origin1, connection_origin2])

                for connection in connections:
                    connection_info = {
                        "ID Project": project_id,
                        "ID Connection": connection.id_connection,
                        "Name Connection": connection.ds_name_connection,
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

            ds_user_origin2 = connection_info_origin2["User"]
            ds_connection_origin2 = connection_info_origin2["IP"]
            ds_password_origin2 = connection_info_origin2["Password"]
            ds_database_origin2 = connection_info_origin2["Database"]
            ds_charset_origin2 = "utf8"
            ds_connector_origin2 = connection_info_origin2["Connector"]

            if ds_connector_origin1 == "mysql":
                ds_conexao_origin1 = f"mysql://{ds_user_origin1}:{ds_password_origin1}@{ds_connection_origin1}/{ds_database_origin1}?charset={ds_charset_origin1}"
            elif ds_connector_origin1 == "postgresql":
                ds_conexao_origin1 = f"postgresql://{ds_user_origin1}:{ds_password_origin1}@{ds_connection_origin1}/{ds_database_origin1}"
            elif ds_connector_origin1 == "sqlite":
                ds_conexao_origin1 = f"sqlite:///{ds_database_origin1}"
            else:
                raise ValueError("Tipo de conexão não suportado para a origin1")

            if ds_connector_origin2 == "mysql":
                ds_conexao_origin2 = f"mysql://{ds_user_origin2}:{ds_password_origin2}@{ds_connection_origin2}/{ds_database_origin2}?charset={ds_charset_origin2}"
            elif ds_connector_origin2 == "postgresql":
                ds_conexao_origin2 = f"postgresql://{ds_user_origin2}:{ds_password_origin2}@{ds_connection_origin2}/{ds_database_origin2}"
            elif ds_connector_origin2 == "sqlite":
                ds_conexao_origin2 = f"sqlite:///{ds_database_origin2}"
            else:
                raise ValueError("Tipo de conexão não suportado para a origin2")

            conexao_origin1 = ConexaoBancoDados(ds_conexao_origin1)
            conexao_origin2 = ConexaoBancoDados(ds_conexao_origin2)

            conexao_origin1.conectar()
            conexao_origin2.conectar()

            query_list = Query.objects(id_project=project_id).order_by('nr_execution_order').all()

            if query_list:
                logger = Logger()  # Instancia a classe Logger
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
                                table = metadata.tables[query_destination]

                                if id_type_query == 2:
                                    # Truncar (limpar) a tabela de destino
                                    truncate_stmt = sqlalchemy.sql.text(f"TRUNCATE TABLE {query_destination}")
                                    connection.execute(truncate_stmt)

                                # Inserir os resultados na tabela de destino
                                insert_stmt = insert(table).values([result._asdict() for result in origin_results])
                                connection.execute(insert_stmt)
                                connection.commit()
                            print("Inserção concluída com sucesso.")

                            logger.log_entry(project_id, "Consulta concluída com sucesso")  # Inserir log de conclusão

                        except SQLAlchemyError as e:
                            print(f"Erro ao executar a inserção: {str(e)}")
                            logger.log_entry(project_id, f"Erro ao executar a inserção: {str(e)}", error=True)
                    else:
                        print("Nenhum resultado retornado pela consulta de origem.")
                        logger.log_entry(project_id, "Nenhum resultado retornado pela consulta de origem.", error=True)
                    time.sleep(2)
                ProjectUpdater.update_last_run(project_id)
            else:
                print("Nenhuma consulta encontrada para o projeto.")
                logger.log_entry(project_id, "Nenhuma consulta encontrada para o projeto.", error=True)

        else:
            print("Nenhuma conexão encontrada.")

    def run(self):
        while True:
            current_time = '22:53:00'
            if current_time != '22:53:00':
                break 
            self.migrate_data()
            time.sleep(3600)


data_migration = DataMigration()
data_migration.run()
