import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX INTERCLUB", page_icon="🦊", layout="centered")

# --- DISEÑO ULTRA-COMPACTO Y CORREGIDO ---
st.markdown("""
    <style>
    .stApp { background-color: #F2F2F2; color: #333333; }
    header, footer, #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Centrado de logo */
    .logo-container { display: flex; justify-content: center; width: 100%; margin-bottom: 10px; }
    
    /* Botones Naranja FOX */
    div.stButton > button {
        background-color: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    
    /* Inputs */
    .stTextInput input { border: 1px solid #DDD !important; border-radius: 10px !important; }
    
    /* Tabs del Panel */
    button[data-baseweb="tab"] { font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADOS (IMPORTANTE) ---
if 'seccion' not in st.session_state:
    st.session_state.seccion = 'login' # Secciones: login, registro, recuperar, panel
if 'perfil' not in st.session_state:
    st.session_state.perfil = None

# --- LÓGICA DE NAVEGACIÓN ---

# A. PANTALLA DE LOGIN
if st.session_state.seccion == 'login':
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="280"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Acceso Interclub</h2>", unsafe_allow_html=True)
    
    with st.container():
        u = st.text_input("Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        
        if st.button("INICIAR SESIÓN"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.perfil = 'organizador'
                st.session_state.seccion = 'panel'
                st.rerun()
            elif p == "fox2026":
                st.session_state.perfil = 'competidor'
                st.session_state.seccion = 'panel'
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

        if st.button("¿OLVIDASTE TU CONTRASEÑA?", key="btn_olvido"):
            st.session_state.seccion = 'recuperar'
            st.rerun()

    st.markdown("---")
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.session_state.seccion = 'registro'
        st.rerun()

# B. PANTALLA RECUPERAR CONTRASEÑA
elif st.session_state.seccion == 'recuperar':
    st.subheader("Recuperar Contraseña")
    email_o = st.text_input("Introduce tu email registrado")
    if st.button("ENVIAR SOLICITUD"):
        # Genera un enlace de correo automático
        mailto_link = f"mailto:robertoaxpe@gmail.com?subject=Recuperar Contraseña FOX&body=Hola, mi email es {email_o}. He olvidado mi contraseña para el Interclub."
        st.success("Pulsa el enlace de abajo para enviarnos el correo de recuperación:")
        st.markdown(f'<a href="{mailto_link}" target="_blank" style="color:#FF6B00; font-weight:bold;">📧 ENVIAR EMAIL DE SOLICITUD</a>', unsafe_allow_html=True)
    
    if st.button("Volver al Login"):
        st.session_state.seccion = 'login'
        st.rerun()

# C. PANTALLA DE REGISTRO
elif st.session_state.seccion == 'registro':
    st.subheader("Nueva Inscripción")
    with st.form("form_reg"):
        nom = st.text_input("Nombre Completo")
        mail = st.text_input("Email")
        club = st.text_input("Academia")
        if st.form_submit_button("REGISTRARME"):
            st.success("¡Registro enviado! Revisaremos tus datos.")
    
    if st.button("Volver"):
        st.session_state.seccion = 'login'
        st.rerun()

# D. PANEL INTERIOR (EL QUE NO TE SALÍA)
elif st.session_state.seccion == 'panel':
    with st.sidebar:
        st.write(f"Conectado como: **{st.session_state.perfil}**")
        if st.button("Cerrar Sesión"):
            st.session_state.seccion = 'login'
            st.session_state.perfil = None
            st.rerun()

    st.markdown(f"<h1 style='color:#FF6B00;'>PANEL {st.session_state.perfil.upper()}</h1>", unsafe_allow_html=True)
    
    # Aquí definimos qué ve cada uno
    if st.session_state.perfil == 'organizador':
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Gestión", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])
        with tab1:
            st.subheader("Panel de Administración")
            # Intento de conectar a GSheets
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df = conn.read()
                st.data_editor(df)
            except:
                st.warning("Conecta tu Google Sheet en 'Secrets' para ver los datos.")
        with tab2:
            st.write("Configuración de combates.")
        with tab4:
            st.write("Sube aquí los enlaces de las fotos.")
            
    else: # Perfil Competidor
        tab1, tab2 = st.tabs(["📝 Mi Ficha", "⚔️ Ver Cruces"])
        with tab1:
            st.write("Completa tus datos de peso y cinturón.")
