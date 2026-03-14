import streamlit as st
import sqlite3
import pandas as pd

# 1. Configuração do Banco de Dados
conn = sqlite3.connect('cadastro.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS usuarios (nome TEXT, email TEXT, telefone TEXT)')
conn.commit()

# Define a largura desejada (ex: 400px, o padrão é ~300px)
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 100px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. Interface Streamlit
st.title("Sistema de Cadastro Remoto Luiz")
st.sidebar.header("Cadastro")

nome = st.sidebar.text_input("Nome")
email = st.sidebar.text_input("E-mail")
telefone = st.sidebar.text_input("Telefone")

if st.sidebar.button("Cadastrar"):
    c.execute('INSERT INTO usuarios VALUES (?, ?, ?)', (nome, email, telefone))
    conn.commit()
    st.success(f"Usuário {nome} cadastrado!")

# 3. Visualizar Cadastros
st.subheader("Usuários Cadastrados")
df = pd.read_sql('SELECT * FROM usuarios', conn)
st.dataframe(df)

# Fechar conexão
conn.close()
