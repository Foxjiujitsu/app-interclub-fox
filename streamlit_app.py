import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CUSTOM (FUERZA BRUTA HTML/CSS) ---
st.markdown("""
    <style>
    /* Fondo negro */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Contenedor central de logos */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-bottom: 20px;
    }
    
    /* Etiquetas de texto en BLANCO BRILLANTE */
    .label-custom {
        color: #FFFFFF !important;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 5px;
        display: block;
    }

    /* BOTÓN INICIAR SESIÓN (NARANJA Y NEGRO) */
    div.stButton > button {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        text-transform: uppercase !important;
    }
    
    /* Forzar texto negro dentro del botón */
    div.stButton > button p {
        color: #000000 !important;
        font-weight: 900 !important;
    }

    /* Campos de entrada */
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 10px !important;
    }

    /* Botón de registro (Estilo diferente para que no compita) */
    .btn-registro button {
        background-color: transparent !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        margin-top: 30px !important;
    }
    
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ESTADO ---
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

# --- PANTALLA DE ACCESO ---
if not st.session_state.logueado:
    
    # 1. Logos centrados con HTML
    st.markdown("""
        <div class="header-container">
            <img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/Imagen%20de%20WhatsApp%202024-11-27%20a%20las%2014.43.24_bca11eec.jpg" width="140" style="margin-bottom:10px;">
            <img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="300">
            <h1 style="color: #FF6B00; text-align: center; margin-top: 20px;">Acceso Interclub</h1>
        </div>
    """, unsafe_allow_html=True)

    # 2. Caja de Login (Sin st.form para evitar errores de color)
    col_izq, col_centro, col_der = st.columns([0.1, 0.8, 0.1])
    
    with col_centro:
        st.markdown('<p class="label-custom">Usuario o Email</p>', unsafe_allow_html=True)
        u = st.text_input("", placeholder="Escribe aquí...", key="user_input", label_visibility="collapsed")
        
        st.markdown('<p class="label-custom">Contraseña</p>', unsafe_allow_html=True)
        p = st.text_input("", type="password", placeholder="••••••••", key="pass_input", label_visibility="collapsed")
        
        st.write("") # Espacio
        
        if st.button("INICIAR SESIÓN"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.logueado = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

    # 3. Botón de Registro
    st.markdown('<div class="btn-registro">', unsafe_allow_html=True)
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.info("Formulario de registro en mantenimiento.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA INTERIOR ---
else:
    with st.sidebar:
        if st.button("Cerrar Sesión"):
            st.session_state.logueado = False
            st.rerun()
            
    st.title("🛡️ PANEL DE CONTROL FOX")
    tabs = st.tabs(["📊 Inscritos", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])
    
    with tabs[0]:
        st.write("Bienvenido, Roberto. Aquí aparecerá tu lista de GSheets.")
