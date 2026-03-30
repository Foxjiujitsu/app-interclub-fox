import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- CSS RADICAL Y DEFINITIVO ---
st.markdown("""
    <style>
    /* 1. Fondo y Textos Base */
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    
    /* 2. OCULTAR ELEMENTOS INNECESARIOS */
    #MainMenu, header, footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 3. CENTRADO ABSOLUTO DE LOGOS */
    /* Este bloque fuerza a que cualquier imagen o bloque de imagen se centre sí o sí */
    [data-testid="stImage"], .stImage, [data-testid="stVerticalBlock"] > div:has(img) {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        width: 100% !important;
    }
    .stImage img {
        display: block !important;
        margin: 0 auto !important;
    }

    /* 4. TEXTOS DE ETIQUETAS (Usuario, Contraseña...) */
    /* Forzamos blanco puro para que no salgan grises */
    label, .stMarkdown p, [data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        opacity: 1 !important;
    }

    /* 5. INPUTS (Corrección de doble línea y color) */
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 10px !important;
        /* Eliminamos sombras internas que crean el efecto de doble línea */
        box-shadow: none !important;
        -webkit-appearance: none !important;
    }

    /* 6. BOTÓN INICIAR SESIÓN (EL FALLO MÁS REPETIDO) */
    /* Atacamos directamente el botón de formulario de Streamlit */
    button[kind="primaryFormSubmit"], .stButton > button {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        height: 3.5em !important;
        width: 100% !important;
        opacity: 1 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Forzamos que el texto dentro del botón sea NEGRO */
    button[kind="primaryFormSubmit"] p, .stButton > button p {
        color: #000000 !important;
        font-weight: 900 !important;
    }

    /* 7. BOTÓN REGISTRO (Abajo del formulario) */
    [data-testid="stForm"] + div .stButton button {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border: none !important;
        margin-top: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA DE LOGOS ---
# Usamos un contenedor vacío para ayudar al centrado
st.write("") 
st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=150)
st.image("fox-letras-naranja.PNG", width=350)

# Título centrado sin icono de enlace
st.markdown("<h1 style='text-align: center; color: white; margin-top: -10px;'>Acceso Interclub</h1>", unsafe_allow_html=True)

# --- FORMULARIO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

with st.form("login_oficial"):
    u = st.text_input("Usuario o Email")
    p = st.text_input("Contraseña", type="password")
    submit = st.form_submit_button("INICIAR SESIÓN")
    
    if submit:
        if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
            st.session_state['autenticado'] = True
            st.success("Acceso concedido")
        else:
            st.error("Credenciales incorrectas")

# --- BOTÓN REGISTRO ---
st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ")
