import streamlit as st
import io
import contextlib
from datetime import datetime
import pandas as pd
import requests
from streamlit_modal import Modal
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.stoggle import stoggle


    
st.set_page_config(layout="centered")

# URL base da API
base_url = "http://localhost:8000"  

# Função para estilizar o card dos projetos
def style_project_card():
    st.markdown(
        """
        <style>
        .project-card {
            border-radius: 10px;
            padding: 27px;
            margin: 10px 0;
            height:180px;
            border-radius: 7px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
 # Função para estilizar o card de conexão
def style_connection_card():
        st.markdown(
            """
            <style>
            .connection-card {
                background-color: #ffff;
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
                height:100px;
                border-radius: 7px;
                box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


def get_all_projects():
    response = requests.get(f"{base_url}/GetAllProjects")
    if response.status_code == 200:
        return response.json()
    return None

# 2. horizontal menu
selected2 = option_menu(None, ["Projetos", "Logs", "Conexões", 'Scripts'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected2

# Página "Home" - Lista todos os projetos
def get_connections():
    try:
        response = requests.get(f"{base_url}/connections")

        if response.status_code == 200:
            connections_data = response.json()
            return connections_data
        else:
            st.error("Erro ao obter as conexões.")
            return []
    except Exception as e:
        st.error(f"Ocorreu um erro ao obter as conexões: {str(e)}")
        return []
    

if selected2 == "Projetos":
    style_project_card()
    
    def main():
        st.title("Exemplo de Modal com Streamlit")

    modal = Modal("Criar Projetos", key="my_modal")
    open_modal = st.button("Criar Projeto")
    if open_modal:
        modal.open()

    if modal.is_open():
        # Início do conteúdo do modal
        with modal.container():
            st.write("")

            connections_data = get_connections()

            connection_names = [""] + [connection["ds_name_connection"] for connection in connections_data]
            
            selected_connection1 = st.selectbox("Conexão de Origem:", connection_names)
            selected_connection2 = st.selectbox("Conexão de Destino:", connection_names)

            name_project = st.text_input("Nome do Projeto:")
            dt_last_run = st.date_input("Data da Última Execução:")
            fl_active = st.checkbox("Ativo", value=True)

            save_button = st.button("Salvar")
            cancel_button = st.button("Cancelar")
            
            if save_button:
                id_connection1 = None
                if selected_connection1:
                    id_connection1 = next((connection["id_connection"] for connection in connections_data if connection["ds_name_connection"] == selected_connection1), None)

                id_connection2 = None
                if selected_connection2:
                    id_connection2 = next((connection["id_connection"] for connection in connections_data if connection["ds_name_connection"] == selected_connection2), None)
                
                if id_connection1 is None or id_connection2 is None:
                    st.error("Por favor, selecione conexões válidas.")
                else:
                    new_project = {
                        "name_project": name_project,
                        "dt_last_run": datetime.combine(dt_last_run, datetime.min.time()).isoformat(),
                        "fl_active": fl_active,
                        "connection_origin1": id_connection1, 
                        "connection_origin2": id_connection2,  
                    }
                    try:
                        response = requests.post(f"{base_url}/CreateProjects", json=new_project)

                        if response.status_code == 200:
                            st.write("Projeto criado com sucesso.")
                            modal.close()
                        else:
                            st.error("Erro ao criar o projeto.")
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao criar o projeto: {str(e)}")
            elif cancel_button:
                modal.close()


    # Lista todos os projetos
    def get_connection_name(connection_id):
        try:
            response = requests.get(f"{base_url}/connections/{connection_id}")
            if response.status_code == 200:
                connection_data = response.json()
                return connection_data["ds_name_connection"]
            else:
                return f"Conexão não encontrada para o ID {connection_id}"
        except Exception as e:
            return f"Erro ao buscar conexão: {str(e)}"
        
    projects = get_all_projects()
    if projects:
        for project in projects:
            with st.container():
                st.write('<hr style="border: 1px solid #dddddd47; margin: 2px 0;">', unsafe_allow_html=True)
                st.write(f'<div class="project-card">'
                        f'<strong>Nome: </strong> {project["name_project"]} <br>'
                        f'<strong>Data da Última Execução: </strong> {project["dt_last_run"]} <br>'
                        f'<strong>Ativo:</strong> {"Sim" if project["fl_active"] == 1 else "Não"} <br>'
                        f'<strong>Conexão de Origem:</strong> {get_connection_name(project["connection_origin1"])} <br>'
                        f'<strong>Conexão de Destino:</strong> {get_connection_name(project["connection_origin2"])} </div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:                      
                    st.write("")
                    
                with col2:
                    st.write("")

                with col3:
                    delete_button = st.button("Excluir Projeto", key=f"delete_button_{project['id_project']}")
                    if delete_button:
                        response = requests.delete(f"{base_url}/DeleteProjects/{project['id_project']}")
                        if response.status_code == 200:
                            st.write(f"Projeto ID {project['id_project']} excluído com sucesso.")
                        else:
                            st.write(f"Erro ao excluir o projeto ID {project['id_project']}.")
                st.write('<hr style="border: 0.5px solid #dddddd47; margin: 10px 0;">', unsafe_allow_html=True)

    else:
        st.write("Nenhum projeto encontrado.")

# Página "Log" 
def get_all_logs():
    response = requests.get(f"{base_url}/GetAlllog")
    if response.status_code == 200:
        return response.json()
    return None

def get_filtered_logs(project_name=None, start_date=None, end_date=None, fl_error=None):
    params = {}
    if project_name:
        params["project_name"] = project_name
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if fl_error is not None:
        params["fl_error"] = fl_error

    response = requests.get(f"{base_url}/GetFilteredLogs", params=params)
    if response.status_code == 200:
        return response.json()
    return None


# Página "Logs" - Lista todos os logs filtrados
if selected2 == "Logs":
    projects = get_all_projects()
    project_names = [project["name_project"] for project in projects]
    
    with st.expander("Filtrar", expanded=False):
        selected_project_name = st.selectbox("Nome do Projeto", ["Todos os Projetos"] + project_names)
        if selected_project_name == "Todos os Projetos":
            selected_project_name = None

        start_date = st.date_input("Início")
        end_date = st.date_input("Fim")

        selected_error = st.selectbox("Erro", ["Todos", "Com Erro", "Sem Erro"])
        if selected_error == "Todos":
            selected_error = None
        elif selected_error == "Com Erro":
            selected_error = True
        elif selected_error == "Sem Erro":
            selected_error = False

        if st.button("Listar Logs"):
            logs = get_filtered_logs(
                project_name=selected_project_name,
                start_date=start_date,
                end_date=end_date,
                fl_error=selected_error
            )
            if logs:
                st.write("Lista de Logs:")
                for log in logs:
                    st.write(f"ID Log: {log['id_log']}")
                    st.write(f"ID Projeto: {log['id_project']}")
                    st.write(f"Data da Execução: {log['dt_execution']}")
                    st.write(f"Descrição do Log: {log['ds_log']}")
                    st.write(f"Erro: {'Sim' if log['fl_error'] else 'Não'}")
            else:
                st.write("Nenhum log encontrado.")

    logs = get_all_logs() 

    if logs:
        table_data = {
            "ID do Log": [log["id_log"] for log in logs],
            "ID do Projeto": [log["id_project"] for log in logs],
            "Data de Execução": [log["dt_execution"] for log in logs],
            "Descrição do Log": [log["ds_log"] for log in logs],
            "Erro": [log["fl_error"] for log in logs],
        }
        st.table(pd.DataFrame(table_data))
    else:
        st.write("Nenhum log encontrado.")

# Página de Conexão
def create_connection():
    st.write("Criar Nova Conexão:")
    ds_name_connection = st.text_input("Nome da Conexão:")
    ds_user = st.text_input("Usuário:")
    ds_connection = st.text_input("Connection String:")
    ds_password = st.text_input("Senha:", type="password")
    ds_port = st.number_input("Porta:", min_value=1)
    ds_database = st.text_input("Nome do Banco de Dados:")
    ds_connector = st.text_input("Conector:")

    if st.button("Salvar"):
        if ds_name_connection and ds_connection:
            new_connection = {
                "ds_name_connection": ds_name_connection,
                "ds_user": ds_user,
                "ds_connection": ds_connection,
                "ds_password": ds_password,
                "ds_port": ds_port,
                "ds_database": ds_database,
                "ds_connector": ds_connector,
            }
            response = requests.post(f"{base_url}/connections", json=new_connection)
            if response.status_code == 200:
                st.write("Conexão criada com sucesso.")
                st.experimental_rerun()  # Rerun the app to close the modal
            else:
                st.write("Erro ao criar a conexão.")
        else:
            st.write("Por favor, preencha pelo menos o Nome da Conexão e Connection String.")


def edit_connection(connection):
    st.write(f"Editar Conexão ID: {connection['id_connection']}")
    ds_name_connection = st.text_input("Nome da Conexão:", value=connection["ds_name_connection"])
    ds_user = st.text_input("Usuário:", value=connection["ds_user"])
    ds_connection = st.text_input("Connection String:", value=connection["ds_connection"])
    ds_password = st.text_input("Senha:", type="password", value=connection["ds_password"])
    ds_port = st.number_input("Porta:", min_value=1, value=connection["ds_port"])
    ds_database = st.text_input("Nome do Banco de Dados:", value=connection["ds_database"])
    ds_connector = st.text_input("Conector:", value=connection["ds_connector"])

    if st.button("Salvar"):
        updated_connection = {
            "ds_name_connection": ds_name_connection,
            "ds_user": ds_user,
            "ds_connection": ds_connection,
            "ds_password": ds_password,
            "ds_port": ds_port,
            "ds_database": ds_database,
            "ds_connector": ds_connector,
        }
        response = requests.put(f"{base_url}/connections/{connection['id_connection']}", json=updated_connection)
        if response.status_code == 200:
            st.write("Conexão atualizada com sucesso.")
        else:
            st.write("Erro ao atualizar a conexão.")

def delete_connection(connection):
    st.write(f"Excluir Conexão ID: {connection['id_connection']}")
    st.write(f"Nome da Conexão: {connection['ds_name_connection']}")
    st.write(f"Connection String: {connection['ds_connection']}")

    if st.button("Excluir"):
        response = requests.delete(f"{base_url}/connections/{connection['id_connection']}")
        if response.status_code == 200:
            st.write("Conexão excluída com sucesso.")
        else:
            st.write("Erro ao excluir a conexão.")

def get_all_connections():
    response = requests.get(f"{base_url}/connections")
    if response.status_code == 200:
        return response.json()
    return None



# Página de Conexões
if selected2 == "Conexões":
    connections = get_all_connections()

    if st.button("Criar Nova Conexão", key="create_new_connection_button"):
        create_connection()

    def display_connection_card(connection):
        st.write(f'<div class="connection-card">'
                 f'<strong>ID da Conexão:</strong> {connection["id_connection"]} <br>'
                 f'<strong>Nome da Conexão:</strong> {connection["ds_name_connection"]} <br>'
                 f'<strong>Connection String:</strong> {connection["ds_connection"]} <br>'
                 f'</div>', unsafe_allow_html=True)

    if connections:
        for connection in connections:
            with st.container():
                style_connection_card()  
                display_connection_card(connection)
                st.write("")  
            col1, col2 = st.columns([1, 1])
            with col1:
                edit_button = st.button("Editar conexão", key=f"edit_button_{connection['id_connection']}")
                if edit_button:
                    edit_connection(connection)
            with col2:
                delete_button = st.button("Excluir conexão", key=f"delete_button_{connection['id_connection']}")
                if delete_button:
                    delete_connection(connection)
    else:
        st.write("Nenhuma conexão encontrada.")

    


# Script
if selected2 == "Scripts":
    st.markdown(
        """
        <style>
        .stTextarea textarea {
            background-color: #000000;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    language_selection = st.selectbox("Selecione a Linguagem", ["Python", "SQL"])

    if language_selection == "Python":
        script_code = st.text_area("Código Python", height=200)
        language = "python"
    else:
        script_code = st.text_area("Código SQL", height=200)
        language = "sql"
    
    if st.button("Executar Código"):
        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            try:
                if language == "python":
                    exec(script_code)
                else:
                    st.error("A execução de SQL não está implementada atualmente.")
            except Exception as e:
                st.error(f"Ocorreu um erro na execução do código: {str(e)}")
        
        output_result = output_buffer.getvalue()

        if output_result:
            st.write("Saída:")
            st.code(output_result)
        else:
            st.write("Nenhuma saída gerada.")

    if st.button("Salvar Código"):
        if language == "python":
            query = {
                "id_project": 10,  
                "origin_query": script_code,
                "query_destination": "",
                "id_type_query": 1,  
                "nr_execution_order": 1, 
            }
            response = requests.post(f"{base_url}/CreateQueries", json=query)
            if response.status_code == 200:
                st.write("Código Python salvo com sucesso.")
            else:
                st.write("Erro ao salvar o código Python.")
        else:
            st.error("Ainda não implementado.")
