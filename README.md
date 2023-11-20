
### Convutell

É uma aplicação web/API criada com o framework FastAPI do Python. A aplicação se conecta a um banco de dados e permite realizar consultas SQL através de uma interface web bem como agendar script python e sql com intervalos de operações de transferência e persistência em banco de dados em diferentes servidores. 


[![Demonstração](https://github.com/convutell/autconvutell/blob/main/convutell/api/assets/capa.png)](https://www.youtube.com/watch?v=y3wszkN3T6s&ab_channel=ClaytonSilva)



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


### API de Integração

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
### Instalando no Docker


Configure os arquivo `Dockerfile` e `docker-compose.yml` para adequar a configuração ideal do seu ambiente. Esta implementação do projeto para a imagem docker está em desevolvimento, portanto cabe avaliar a viabilidade das configuração dispostas. 

```bash
sudo docker-compose up -d
```
Use o comando abaixo para inicar o seu container. 

```bash
sudo docker-compose down
```

Execute no seu navegador a interface de gerenciamento da aplicação. 

```bash
172.17.0.2:8501/
```

Verifique o endereço local do seu container docker e confirme o uso na porta 8501.

Optamos por utilizar o Supervisor para monitoramento e controle dos nossos processos. Tanto a API como Processo de ETL será monitorados pelo Supervisor. Toda a configuração será passada para o controle do Supervidor através do arquivo `supervisord.conf`.

```bash

[program:etl]
command=/opt/venv/bin/python /convutell/etl.py
directory=/convutell
autostart=true
autorestart=true
startretries=3
redirect_stderr=true
stdout_logfile=/convutell/logs/etl/etl.log
stdout_logfile_maxbytes=10MB
```
O código apresentado configura um processo chamado "etl" usando o Supervisor. Esse processo é executado por um comando específico, que é a execução de um arquivo Python chamado "etl.py" dentro de um ambiente virtual. O diretório de trabalho para esse processo é definido com o mesmo nome do diretório da nossa aplicação "/convutell". O processo é configurado para iniciar automaticamente e reiniciar em caso de falha, com um máximo de três tentativas de inicialização. Os erros de saída são redirecionados para o arquivo de log "etl.log", localizado na pasta de logs "/convutell/logs/etl", e o tamanho máximo desse arquivo de log é limitado a 10MB. Essa configuração garante que o processo "etl" seja gerenciado pelo Supervisor, registrando sua saída e reiniciando-o automaticamente se necessário.

### Interface Web

A interface web é uma aplicação de gerenciamento de agendamento de scripts em SQL e Python. Essa ferramenta foi projetada para tornar o trabalho dos analistas mais eficiente, permitindo o agendamento de scripts e o acompanhamento organizado de tarefas. Além disso, ela auxilia na identificação de erros que possam ocorrer durante a execução desses scripts.

Esta aplicação foi desenvolvida em Flask e é executada em conjunto com o servidor Nginx para garantir alto desempenho e escalabilidade. Para integrá-la ao seu projeto, siga estas etapas:


Clonando o Repositório:

Você pode obter o código-fonte do projeto clonando o repositório a partir do GitHub:


```bash
https://github.com/convutell/convutell-in.git
```

Executando a Aplicação:

A aplicação pode ser executada em seu ambiente Python local, simplesmente executando o arquivo Python principal (arquivo.py).

```bash
python arquivo.py

```
No entanto, se você deseja aproveitar os benefícios do Docker, recomendamos o uso do Docker Compose para simplificar a configuração e execução da aplicação. Certifique-se de ter o Docker e o Docker Compose instalados em seu sistema.

Para iniciar a aplicação com o Docker Compose, utilize o seguinte comando na raiz do projeto clonado:


```bash
docker-compose up --build

```

Isso irá construir e executar os contêineres necessários, garantindo que a aplicação seja executada em um ambiente isolado e pronto para uso.

Após essas etapas, você poderá acessar a interface web por meio do navegador em `http://127.0.0.1:5000/projects/` e começar a usar a ferramenta para agendar e gerenciar seus scripts de forma eficaz.

![interface](https://github.com/convutell/autconvutell/blob/main/convutell/api/assets/interface.png)

Algumas funcionalidades da aplicaçção.

- Gerenciamento de consultas.
- Conexões internas e externas para diferentes projetos. 
- Análise de Logs de transações

Em desenvolvimento

- Ambiente de execução Python
- Notificações de falhas direto na aplicação
- Compartilhamento de projetos

## Etiquetas

Esse projeto é uma iniciativa de aprendizado e ajuda a comunidade, sua contribuição é super bem-vinda. Estamos abertos a críticas e sugestões.


[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0.pt-br.html)


## creator/maintainer

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/clayttonsilva/)


