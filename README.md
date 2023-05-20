
## Convutell

É uma aplicação web/API criada com o framework FastAPI do Python. A aplicação se conecta a um banco de dados e permite realizar consultas SQL através de uma interface web bem como agendar script python e sql com intervalos de operações de transferência e persistência em banco de dados em diferentes servidores. 

O criador está trabalhando na projeção de uma interface que permita gerenciar e agendar as transações de dados entre servidores, assim como acompanhar os logs de execução. Esse arcabouço será a segunda parte do projeto que se conecta a API já desenvolvida.

A aplicação é constituída de três ferramentas:

- API: Permite acesso externo, sendo a base de consumo das demais ferramentas do projeto. E permite que outras aplicações possam consumir rotas externas.

- Interface Web: Interface gráfica que permite ao usuário administre seus projetos, analise logs e defina processos de tratamento de dados.

- Serviço de execução interno: Sistema de realização de transações, responsável por executar as consultas SQL e script Python agendados através da Interface Web.

## Tecnologias adicionadas

As biliotecas corresponde a todas as aplicações do projeto. 

- [fastapi](https://fastapi.tiangolo.com/): Framework para desenvolvimento de APIs web em Python.
- [SqlAlchemy](https://www.sqlalchemy.org/): Uma ORM poderos do python que permitiu que as transações de dados fossem possível de realizar em diferentes DBMS.
- [MongoDB](https://pypi.org/project/pymongo/): Biblioteca para interagir com banco de dados MongoDB utilizando Python.
- [uvicorn](https://www.uvicorn.org/): Servidor web de alta performance para Python.
- [Pydotenv](https://pypi.org/project/pydotenv/): Biblioteca do python para gerenciar variaveis de ambientes.


## API de Integração

A api de integração é construída sobre o fastapi e permite a princípio a gestão das informações disposta em base NoSQL, sendo também consumido pelo serviço de transferência de dados. Para este projeto optamos por utilizar o MongoDB.

Em relação a ausência da interface gráfica, informamos que estamos trabalhando na construção da interface que consumirá a mesma API mencionada.


```http
  POST /CreateProjects
```
Todo script inserido é gerenciado por um projeto, que deve possuir uma informação de integração de origin e uma integreação de destino.
```
{
  "name_project": "string",
  "dt_last_run": "2023-05-20T00:35:55.243Z",
  "fl_active": 0,
  "connection_origin1": 0,
  "connection_origin2": 0
}
```
#### Configuração da API

A configuração da API é extremamente simples, basta configurar o arquivo de conexão a instância do Mongo, recomendo utilizar o [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register), um serviço cloud para armazenamento de dados NoSQL utilizando o MongoDB.   

- Crie um arquivo `.env` na raiz do projeto com as configurações de conexão ao banco de dados.

```bash
MONGODB_CONNECTION_STRING=mongodb+srv://user:password@clste.namoeclaos.mongodb.ssc/
MONGODB_CONNECTION_STRING_DB = nameColletion
```
### Instalação de pacotes

Para executar o projeto, é necessário seguir os seguintes passos:

- Clonar o repositório do projeto do Github.
- Instalar as dependências através do comando 

```bash
pip install -r requirements.txt
```
O API de integração é construída sobre o FastAPI *0.95.1* e o Python 3.7. Toda adaptação poderá ser realizada em verões subsequentes. 

- Executar o servidor web com o comando 
```bash
uvicorn app:app --reload
```
#### Instalando no Docker

A imagem do docker da aplicação está em construção. 

### Interface Web

Algumas funcionalidades já implementadas e em desenvolvimento.

- Gerenciamento de consultas.
- Conexões internas e externas para diferentes projetos. 
- Análise de Logs de transações
- Ambiente de execução Python **Recurso em desenvolvimento**

## Etiquetas

Esse projeto é uma iniciativa de aprendizado e ajuda a comunidade, sua contribuição é super bem-vinda. Estamos abertos a críticas e sugestões.


[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0.pt-br.html)


## creator/maintainer

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/clayttonsilva/)


