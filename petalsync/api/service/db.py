

from sqlalchemy import create_engine
from sqlalchemy.sql import text

class ConnectionDatabase:
    def __init__(self, ds_conexao):
        self.ds_conexao = ds_conexao
        self.engine = None

    def conectar(self):
        if self.ds_conexao.startswith('mysql'):
            self.engine = create_engine(self.ds_conexao)
        elif self.ds_conexao.startswith('postgresql'):
            self.ds_conexao = self.ds_conexao.replace("?charset=utf8", "")
            self.engine = create_engine(self.ds_conexao)
        elif self.ds_conexao.startswith('sqlite'):
            self.engine = create_engine(self.ds_conexao)
        elif self.engine = create_engine(self.ds_conexao):
        

        else:
            raise ValueError("Tipo de conexão não suportado")

    def executar_query(self, query):
        with self.engine.connect() as connection:
            stmt = text(query)
            result = connection.execute(stmt)
            return result.fetchall()
