import streamlit as st
import sqlite3

st.title("Sistema de Vendas")

# Banco de dados
def conectar ():
    return sqlite3.connect("database.db")

def criar_tabela():
    # Estou criando minha conexão com o banco de dados
    conexao = conectar()

    # Criar uma ligação com o banco de dados
    cursor = conexao.cursor()

    # Executando comando no BD
    cursor.execute('''
                  CREATE TABLE IF NOT EXISTS clientes 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nome TEXT,
                  sexo TEXT,
                  email TEXT)
                  ''')
    conexao.commit()
    conexao.close()

def inserir_cliente(nome, sexo, email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO clientes (nome, sexo, email)
        VALUES (?, ?, ?)
        ''', (nome, sexo, email))
    conexao.commit()
    conexao.close()

def listar_clientes():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM clientes')
        clientes = cursor.fetchall()
        conexao.close()
        return clientes

def atualizar_cliente(id, nome, sexo, email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
    UPDATE clientes
    SET nome = ?, sexo = ?, email = ?
    WHERE id = ?
    ''', (nome, sexo, email, id))
    conexao.commit()
    conexao.close()

def deletar_cliente(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conexao.commit()
    conexao.close()

#Front End - Menu checkbox 
criar_tabela()
menu = ["Cadastrar", "Listar / Editar / Excluir"]
escolha = st.sidebar.selectbox ("Menu", menu)

# Cadastrar

if escolha == "Cadastrar":
    st.subheader ("Novo Cliente")

    with st.form(key='form_cliente'):
        nome = st.text_input("Nome")
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
        email = st.text_input("Email")
        submit = st.form_submit_button("Cadastrar")

        if submit:
            inserir_cliente (nome, sexo, email)
            st.success(f"Cliente {nome} cadastrado com sucesso!")

elif escolha == "Listar / Editar / Excluir":
    st.subheader("Clientes Cadastrados")

    clientes = listar_clientes()
    if not clientes:
        st.info("Nenhum cliente cadastrado.")

    else:
        for c in clientes:
            with st.expander(f"{c[1]} - {c[2]}"):
                novo_nome = st.text_input(f"Nome - ID {c[0]}", value=c[1], key=f"nome_{c[0]}")
                novo_sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"], index=["Masculino", "Feminino", "Outro"].index(c[2]), key=f"sexo_{c[0]}")
            novo_email = st.text_input ("Email", value =c[3], key=f"email_{c[0]}")

            col1, col2 = st.columns(2)

            if col1.button("Atualizar", key=f"atualizar_{c[0]}"):  
                atualizar_cliente(c[0], novo_nome, novo_sexo, novo_email)
                st.success(f"Cliente {novo_nome} atualizado com sucesso!")
                st.rerun

            if col2.button("Excluir", key=f"excluir_{c[0]}"):
                deletar_cliente(c[0])
                st.warning (f"Cliente {c[1]} excluído")
                st.rerun()
