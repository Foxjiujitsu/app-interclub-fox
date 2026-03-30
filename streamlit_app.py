import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO RADICAL (TEXTO NEGRO SOBRE BOTÓN NARANJA) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Centrado de imágenes */
    .stImage { display: flex; justify-content: center; }

    /* Forzar visibilidad del botón de INICIAR SESIÓN */
    /* Lo ponemos naranja con letras negras gruesas */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        height: 3.5em !important;
        width: 100% !important;
    }
    div.stButton > button:first-child p {
        color: #000000 !important;
        font-weight: 900 !important;
    }

    /* Inputs con bordes naranjas */
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important;
    }
    
    /* Ocultar iconos de enlace y basura de Streamlit */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CONTROL DE NAVEGACIÓN (SESSION STATE) ---
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

# --- PANTALLA 1: ACCESO ---
if not st.session_state.logueado:
    
    # Centrado usando columnas vacías a los lados
    col1, col_centro, col2 = st.columns([1, 2, 1])
    
    with col_centro:
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=150)
        st.image("fox-letras-naranja.PNG", width=300)
        st.markdown("<h2 style='text-align: center;'>Acceso Interclub</h2>", unsafe_allow_html=True)
        
        with st.form("login_oficial"):
            u = st.text_input("Usuario o Email")
            p = st.text_input("Contraseña", type="password")
            btn_entrar = st.form_submit_button("INICIAR SESIÓN")
            
            if btn_entrar:
                if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                    st.session_state.logueado = True
                    st.rerun() # ESTO es lo que te lleva a la página interior
                else:
                    st.error("Credenciales incorrectas")

    st.markdown("---")
    st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ")

# --- PANTALLA 2: INTERIOR (PANEL ORGANIZADOR) ---
else:
    # Barra lateral para salir
    with st.sidebar:
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=100)
        if st.button("Cerrar Sesión"):
            st.session_state.logueado = False
            st.rerun()

    st.markdown("<h1 style='color: #FF6B00;'>PANEL ORGANIZADOR</h1>", unsafe_allow_html=True)
    
    # Aquí están las pestañas que pediste
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Inscritos", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])

    with tab1:
        st.subheader("Gestión de Fichas de Alumnos")
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read()
            st.data_editor(df, num_rows="dynamic") # Aquí puedes editar inscritos directamente
        except:
            st.error("Conecta tu Google Sheet en los Secrets.")

    with tab2:
        st.subheader("Configuración de Cruces")
        st.info("Aquí podrás diseñar las llaves de los combates.")

    with tab3:
        st.subheader("Resultados del Evento")
        st.write("Registra los ganadores de cada llave.")

    with tab4:
        st.subheader("Galería de Fotos")
        st.write("Sube o enlaza las fotos del Interclub aquí.")
