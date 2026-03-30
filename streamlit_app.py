import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- CSS PROFESIONAL "ANTI-ERRORES" ---
st.markdown("""
    <style>
    /* 1. Fondo y Base */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* 2. OCULTAR ICONOS DE STREAMLIT (GitHub y Enlaces) */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .css-15zrgzn {display: none;}
    a.viewerBadge_container__1QS13 {display: none;}
    button.StyledFullScreenButton {display: none;}
    .element-container:has(#acceso-interclub) a { display: none; }

    /* 3. CENTRADO TOTAL DE LOGOS */
    .stImage { display: flex; justify-content: center; }
    .stImage img { margin: 0 auto; }

    /* 4. TEXTOS (Blanco Puro y legibles) */
    label, p, .stMarkdown p {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* 5. INPUTS (Borde único naranja, sin sombras) */
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 10px !important;
        box-shadow: none !important; /* Quita el doble color */
    }

    /* 6. BOTÓN INICIAR SESIÓN (Naranja con letras negras) */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        height: 3em !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #FF6B00 !important;
    }

    /* 7. BOTÓN REGISTRO (Diseño más elegante) */
    [data-testid="stForm"] + div .stButton button {
        background-color: transparent !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---
# Centramos logos manualmente para asegurar
st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=150)
st.image("fox-letras-naranja.PNG", width=300)

st.markdown("<h1 id='acceso-interclub' style='text-align: center; color: white;'>Acceso Interclub</h1>", unsafe_allow_html=True)

with st.form("login"):
    user = st.text_input("Usuario o Email")
    pwd = st.text_input("Contraseña", type="password")
    submit = st.form_submit_button("INICIAR SESIÓN")
    
    if submit:
        # Aquí iría tu lógica de login
        st.write("Validando...")

st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ")
