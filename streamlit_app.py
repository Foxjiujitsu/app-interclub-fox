import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="FOX JIU-JITSU ADMIN", layout="wide")

if 'page' not in st.session_state: st.session_state.page = 'login'

if st.session_state.page == 'login':
    _, col, _ = st.columns([1,2,1])
    with col:
        st.image("fox-letras-naranja.PNG")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER AL PANEL"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.page = 'panel'
                st.rerun()

elif st.session_state.page == 'panel':
    st.title("🦊 PANEL DE GESTIÓN")
    
    # CONEXIÓN DIRECTA POR URL (Más estable)
    url = "https://docs.google.com/spreadsheets/d/11K7imjP8a96LUiJRe4m7sxUOSH1DSNUBglPDK0Olxao/edit#gid=0"
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    try:
        df = conn.read(spreadsheet=url, ttl=0)
    except:
        df = pd.DataFrame(columns=["Nombre", "Cinturón", "Peso", "Edad", "BJJ / NO-GI", "Club"])

    tab1, tab2 = st.tabs(["👥 Inscritos", "➕ Registro Manual"])

    with tab1:
        st.subheader("Lista de Competidores")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            if st.button("🗑️ Borrar todo"):
                conn.update(spreadsheet=url, data=pd.DataFrame(columns=df.columns))
                st.rerun()
        else:
            st.info("No hay inscritos todavía.")

    with tab2:
        st.subheader("Nuevo Registro")
        with st.form("registro"):
            n = st.text_input("Nombre")
            c = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
            p = st.number_input("Peso (kg)", 10, 150, 70)
            e = st.number_input("Edad", 4, 80, 25)
            s = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            cl = st.text_input("Club")
            
            if st.form_submit_button("GUARDAR LUCHADOR"):
                if n and cl:
                    nueva_fila = pd.DataFrame([{"Nombre":n,"Cinturón":c,"Peso":p,"Edad":e,"BJJ / NO-GI":s,"Club":cl}])
                    df_final = pd.concat([df, nueva_fila], ignore_index=True)
                    # Forzamos la actualización usando la URL exacta
                    conn.update(spreadsheet=url, data=df_final)
                    st.success("✅ ¡Guardado con éxito!")
                    st.rerun()

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.page = 'login'
        st.rerun()
