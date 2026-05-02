import streamlit as st
from supabase import create_client, Client
import pandas as pd


# 1. CONEXÃO AO SUPABASE
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase = init_connection()

# Configuração da página
st.set_page_config(page_title="Cadastro de Clientes", layout="wide")
st.title("💼 Sistema Comercial - Cadastro de Clientes")


# Funções CRUD
def get_clientes():
    return supabase.table("clientes").select("*").order("id").execute().data


def add_cliente(nome, email, telefone):
    return supabase.table("clientes").insert({"nome": nome, "email": email, "telefone": telefone}).execute()


def update_cliente(id, nome, email, telefone):
    return supabase.table("clientes").update({"nome": nome, "email": email, "telefone": telefone}).eq("id", id).execute()


def delete_cliente(id):
    return supabase.table("clientes").delete().eq("id", id).execute()


# --- INTERFACE ---
menu = ["Listar/Pesquisar", "Cadastrar", "Editar/Excluir"]
choice = st.sidebar.selectbox("Menu", menu)

# --- TELA 1: LISTAR E PESQUISAR ---
if choice == "Listar/Pesquisar":
    st.subheader("Clientes Cadastrados")

    # Campo de pesquisa
    search = st.text_input("Pesquisar por nome ou email")

    data = get_clientes()
    df = pd.DataFrame(data)

    if not df.empty:
        if search:
            df = df[df['nome'].str.contains(search, case=False) | df['email'].str.contains(search, case=False)]

        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum cliente cadastrado.")

# --- TELA 2: CADASTRAR ---
elif choice == "Cadastrar":
    st.subheader("Novo Cliente")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        submit = st.form_submit_button("Cadastrar")

        if submit:
            if nome and email:
                add_cliente(nome, email, telefone)
                st.success(f"Cliente {nome} adicionado!")
                st.rerun()
            else:
                st.error("Nome e Email são obrigatórios.")

# --- TELA 3: ATUALIZAR/EXCLUIR ---
elif choice == "Editar/Excluir":
    st.subheader("Gerenciar Cliente")
    data = get_clientes()
    df = pd.DataFrame(data)

    if not df.empty:
        client_id = st.selectbox("Selecione o Cliente ID", df['id'].tolist())
        cliente_info = df[df['id'] == client_id].iloc[0]

        with st.form("form_edit"):
            new_nome = st.text_input("Nome", value=cliente_info['nome'])
            new_email = st.text_input("Email", value=cliente_info['email'])
            new_telefone = st.text_input("Telefone", value=cliente_info['telefone'])

            col1, col2 = st.columns(2)
            with col1:
                update_btn = st.form_submit_button("Atualizar")
            with col2:
                delete_btn = st.form_submit_button("Excluir")

            if update_btn:
                update_cliente(client_id, new_nome, new_email, new_telefone)
                st.success("Dados atualizados!")
                st.rerun()

            if delete_btn:
                delete_cliente(client_id)
                st.warning("Cliente excluído!")
                st.rerun()
    else:
        st.info("Nenhum cliente para gerenciar.")
