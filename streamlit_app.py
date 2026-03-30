import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX INTERCLUB", page_icon="🦊", layout="centered")

# --- DISEÑO ULTRA-COMPACTO Y CENTRADO FORZADO ---
st.markdown("""
    <style>
    /* 1. Fondo y Base */
    .stApp { 
        background-color: #F2F2F2; 
        color: #333333; 
    }
    
    /* Ocultar elementos innecesarios */
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Reducir el padding superior para ganar espacio */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }

    /* 2. CENTRADO TOTAL DE LOGO (CSS DIRECTO) */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 10px;
    }

    /* 3. Título Centrado */
    .titulo-mini {
        text-align: center;
        color: #1A1A1A !important;
        font-size: 24px;
        font-weight: 800;
        margin-top: 5px;
        margin-bottom: 15px;
    }

    /* 4. Inputs Compactos */
    .stTextInput input, .stPasswordInput input {
        background-color: #FFFFFF !important;
        height: 45px !important;
        border-radius: 10px !important;
        border: 1px solid #DDD !important;
    }
    
    /* Reducir espacio entre los widgets de entrada */
    [data-testid="stVerticalBlock"] > div {
        margin-top: -8px !important;
    }

    /* 5. BOTÓN INICIAR SESIÓN (Naranja Premium) */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-top: 15px !important;
        box-shadow: 0 4px 10px rgba(255, 107, 0, 0.2) !important;
    }

    /* 6. Footer de Registro */
    .btn-reg-link {
        text-align: center;
        margin-top: 20px;
    }
    .btn-reg-link button {
        background-color: transparent !important;
        color: #FF6B00 !important;
        border: none !important;
        font-weight: bold !important;
        text-decoration: underline !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ESTADO ---
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

# --- PANTALLA DE ACCESO ---
if not st.session_state.logueado:
    
    # 1. LOGO CENTRADO CON HTML (Soluciona el problema del lateral izquierdo)
    # He subido el tamaño a 280 para que se vea mejor
    st.markdown("""
        <div class="logo-container">
            <img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="280">
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='titulo-mini'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    # 2. Formulario centrado
    _, col_centro, _ = st.columns([0.05, 0.9, 0.05])
    
    with col_centro:
        u = st.text_input("Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        
        if st.button("INICIAR SESIÓN"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.logueado = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        
        st.markdown("<p style='text-align:center; font-size:0.8rem; color:#666; margin-top:10px;'>¿OLVIDASTE TU CONTRASEÑA?</p>", unsafe_allow_html=True)

    # 3. Registro al final
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.info("Registro en proceso")

# --- PANEL INTERIOR ---
else:
    st.success("Sesión Iniciada")
    if st.button("Cerrar Sesión"):
        st.session_state.logueado = False
        st.rerun()
