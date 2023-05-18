from sqlalchemy import create_engine
from sqlalchemy.sql import text
from config.db import ConnectionDestination, Project
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


project = Project.objects.first()
connection_origin1 = project.connection_origin1

conection_destination = ConnectionDestination.objects(id_connection=connection_origin1).first()

if conection_destination:
    ds_user = conection_destination.ds_user
    ds_connection = conection_destination.ds_connection
    ds_password = conection_destination.ds_password
    ds_database = conection_destination.ds_database
    ds_charset = "utf8"
    ds_connector = conection_destination.ds_connector
    
    if ds_connector == "mysql":
        ds_conexao = f"mysql://{ds_user}:{ds_password}@{ds_connection}/{ds_database}?charset={ds_charset}"
    elif ds_connector == "postgresql":
        ds_conexao = f"postgresql://{ds_user}:{ds_password}@{ds_connection}/{ds_database}"
    elif ds_connector == "sqlite":
        ds_conexao = f"sqlite:///{ds_database}"
    else:
        raise ValueError("Tipo de conexão não suportado")
    
    conexao = ConexaoBancoDados(ds_conexao)
    conexao.conectar()
    
    resultados = conexao.executar_query("SELECT * FROM TB_USUARIO")
    for resultado in resultados:
        print(resultado)
else:
    print("Nenhum resultado encontrado.")
