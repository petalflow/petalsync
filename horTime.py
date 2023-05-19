import time
from datetime import datetime
from model.db import Time, Project, ConnectionDestination
#from serviceShETL import ConexaoBancoDados

def check_time():
    #current_time = datetime.now().strftime("%H:%M:%S")
    current_time = '22:53:00'
    times = Time.objects(time=current_time)
    for time_obj in times:
        project = Project.objects(id_project=time_obj.id_project, fl_active=1,
                                  connection_origin1__ne=0, connection_origin2__ne=0).first()
        if project:
            project_id = project.id_project
            connection_origin1 = project.connection_origin1
            connection_origin2 = project.connection_origin2

            connections = ConnectionDestination.objects(id_connection__in=[connection_origin1, connection_origin2])

            # capturar os dados de conexaão com o banco de dados.
            connections_list = []

            # Adicionar as informações de cada conexão à lista
            for connection in connections:
                connection_info = {
                    "ID Connection": connection.id_connection,
                    "Name Connection": connection.ds_name_connection,
                    "IP": connection.ds_connection,
                    "Password": connection.ds_password,
                    "Port": connection.ds_port,
                    "Database": connection.ds_database,
                    "Connector": connection.ds_connector
                }
                connections_list.append(connection_info)
            
            """for connection_info in connections_list:
                print(connection_info)"""

            return connections_list
            # buscar consultas na tabela consulta para o id_projeto pegando pela ordem
            # em seguida inserir no log mensagem padrão,
        #

while True:
    #current_time = datetime.now().strftime("%H:%M:%S")
    current_time = '22:53:00'
    if current_time != '22:53:00':
        break 
    check_time()
    time.sleep(0.9)  
