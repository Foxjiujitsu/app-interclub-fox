import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX INTERCLUB", page_icon="🦊", layout="centered")

# --- DISEÑO ULTRA-COMPACTO (ANTI-SCROLL) ---
st.markdown("""
    <style>
    /* 1. Fondo y Base */
    .stApp { 
        background-color: #F2F2F2; 
        color: #333333; 
        overflow: hidden; /* Evita el scroll global si es posible */
    }
    
    /* Ocultar elementos innecesarios para ganar espacio */
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Reducir el padding superior de la app */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    /* 2. Contenedor de Logos Compacto */
    .header-compact {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 5px;
    }

    /* 3. Título pequeño */
    .titulo-mini {
        text-align: center;
        color: #1A1A1A !important;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    /* 4. Inputs más bajos (Compactos) */
    .stTextInput input, .stPasswordInput input {
        background-color: #FFFFFF !important;
        height: 40px !important; /* Más bajo para ahorrar espacio */
        border-radius: 8px !important;
        border: 1px solid #DDD !important;
    }
    
    /* Reducir espacio entre los widgets */
    [data-testid="stVerticalBlock"] > div {
        margin-top: -10px !important;
    }

    /* 5. BOTÓN INICIAR SESIÓN (Naranja con letras BLANCAS) */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        height: 3em !important;
        width: 100% !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-top: 10px !important;
    }

    /* 6. Link Footer muy pequeño */
    .link-mini {
        text-align: center;
        margin-top: 5px;
        color: #666666 !important;
        font-size: 0.7rem;
        font-weight: bold;
    }
    
    /* Botón registro al final */
    .btn-reg-mini button {
        background-color: transparent !important;
        color: #FF6B00 !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 0.8rem !important;
        text-decoration: underline !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ESTADO ---
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

# --- PANTALLA DE ACCESO COMPACTA ---
if not st.session_state.logueado:
    
    # 1. Cabecera con logo reducido para que no empuje todo hacia abajo
    st.markdown('<div class="header-compact">', unsafe_allow_html=True)
    st.image("fox-letras-naranja.PNG", width=220) # Reducido de 320 a 220
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div class='titulo-mini'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    # 2. Formulario en columna central compacta
    _, col_centro, _ = st.columns([0.05, 0.9, 0.05])
    
    with col_centro:
        u = st.text_input("Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        
        if st.button("INICIAR SESIÓN"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.logueado = True
                st.rerun()
            else:
                st.error("Error")
        
        st.markdown("<div class='link-mini'>¿OLVIDASTE TU CONTRASEÑA?</div>", unsafe_allow_html=True)

    # 3. Registro al final (Pegado abajo)
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.info("Registro disponible pronto")

# --- PANEL INTERIOR ---
else:
    st.success("Logueado")
    if st.button("Cerrar Sesión"):
        st.session_state.logueado = False
        st.rerun()
