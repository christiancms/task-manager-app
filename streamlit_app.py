import streamlit as st
import sqlite3
import pandas as pd

# Conectar ao banco de dados SQLite (cria o arquivo se não existir)
conn = sqlite3.connect('todo_list.db')
c = conn.cursor()

# Criar a tabela 'todos' se não existir
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY,
            task TEXT,
            status TEXT
        )
    ''')
    conn.commit()

# Funções CRUD para interagir com o banco de dados
def add_data(task, status):
    c.execute('INSERT INTO todos(task, status) VALUES (?, ?)', (task, status))
    conn.commit()

def view_all_data():
    c.execute('SELECT * FROM todos')
    return c.fetchall()

def view_unique_tasks():
    c.execute('SELECT DISTINCT task FROM todos')
    return c.fetchall()

def get_task(task):
    c.execute('SELECT * FROM todos WHERE task="{}"'.format(task))
    return c.fetchall()

def edit_task_data(new_task, new_status, task):
    c.execute("UPDATE todos SET task = ?, status = ? WHERE task = ?", (new_task, new_status, task))
    conn.commit()

def delete_data(task):
    c.execute('DELETE FROM todos WHERE task="{}"'.format(task))
    conn.commit()

# Interface Streamlit
def main():
    st.title("Aplicativo CRUD com Streamlit e SQLite")
    
    menu = ["Criar", "Ver Tarefas", "Atualizar", "Deletar"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    create_table()

    # Operação CREATE
    if choice == "Criar":
        st.subheader("Adicionar Tarefa")
        with st.form(key='add_form', clear_on_submit=True):
            task = st.text_input("Tarefa")
            status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"])
            submit_button = st.form_submit_button("Adicionar Tarefa")
            if submit_button and task:
                add_data(task, status)
                st.success(f"Tarefa adicionada: '{task}'")
            elif submit_button:
                st.warning("O campo de tarefa não pode ficar vazio.")

    # Operação READ
    elif choice == "Ver Tarefas":
        st.subheader("Visualizar Tarefas")
        result = view_all_data()
        df = pd.DataFrame(result, columns=['ID', 'Tarefa', 'Status'])
        st.dataframe(df)

    # Operação UPDATE
    elif choice == "Atualizar":
        st.subheader("Atualizar Tarefa")
        list_of_tasks = [i[0] for i in view_unique_tasks()]
        selected_task = st.selectbox("Selecione a tarefa para atualizar", list_of_tasks)
        if selected_task:
            task_details = get_task(selected_task)
            if task_details:
                task_text = task_details[0][1]
                task_status = task_details[0][2]
                new_task = st.text_input("Nova Tarefa", task_text)
                new_status = st.selectbox("Novo Status", ["Pendente", "Em Andamento", "Concluído"], index=["Pendente", "Em Andamento", "Concluído"].index(task_status))
                if st.button("Atualizar"):
                    edit_task_data(new_task, new_status, task_text)
                    st.success(f"Tarefa atualizada de '{task_text}' para '{new_task}'")
            else:
                 st.warning("Tarefa não encontrada.")

    # Operação DELETE
    elif choice == "Deletar":
        st.subheader("Deletar Tarefa")
        result = view_all_data()
        df = pd.DataFrame(result, columns=['ID', 'Tarefa', 'Status'])
        st.dataframe(df)
        list_of_tasks = [i[0] for i in view_unique_tasks()]
        selected_task_to_delete = st.selectbox("Selecione a tarefa para deletar", list_of_tasks)
        if st.button("Deletar Tarefa") and selected_task_to_delete:
            delete_data(selected_task_to_delete)
            st.warning(f"Tarefa deletada: '{selected_task_to_delete}'")

if __name__ == '__main__':
    main()


