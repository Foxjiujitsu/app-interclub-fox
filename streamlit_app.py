import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX INTERCLUB", page_icon="🦊", layout="centered")

# --- DISEÑO CLONADO 100% (IDENTICO A LAS IMAGENES) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #333333; }
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Centrado de Logo */
    .logo-container { display: flex; justify-content: center; width: 100%; margin-bottom: 20px; padding-top: 10px; }
    
    /* Título Acceso */
    .titulo-fox { text-align: center; color: #1A1A1A; font-size: 28px; font-weight: 800; margin-bottom: 20px; }

    /* Inputs Estilo Premium (Blancos con sombra) */
    .stTextInput input, .stPasswordInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 12px !important;
        height: 50px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }

    /* Botón NARANJA con Texto BLANCO (Identico imagen) */
    div.stButton > button {
        background-color: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 15px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.2) !important;
    }
    
    /* Etiquetas */
    label p { font-weight: 600 !important; color: #444 !important; }
    
    /* Tabs */
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# --- NAVEGACIÓN DE PÁGINAS ---

# 1. PÁGINA DE LOGIN
if st.session_state.page == 'login':
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="280"></div>', unsafe_allow_html=True)
    st.markdown("<div class='titulo-fox'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    u = st.text_input("Usuario o Email")
    p = st.text_input("Contraseña", type="password")
    
    if st.button("INICIAR SESIÓN"):
        if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
            st.session_state.user_role = 'organizador'
            st.session_state.page = 'dashboard'
            st.rerun()
        elif p == "fox2026":
            st.session_state.user_role = 'competidor'
            st.session_state.page = 'dashboard'
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    if st.button("¿OLVIDASTE TU CONTRASEÑA?"):
        st.session_state.page = 'forgot'
        st.rerun()
    
    st.markdown("<div style='text-align:center; margin-top:20px;'>---</div>", unsafe_allow_html=True)
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.session_state.page = 'register'
        st.rerun()

# 2. PÁGINA RECUPERAR (Funcionalidad Automática Gratis)
elif st.session_state.page == 'forgot':
    st.subheader("Recuperar Cuenta")
    email_rec = st.text_input("Introduce tu email")
    if st.button("SOLICITAR CLAVE"):
        # Esto abre el correo del usuario con los datos listos para enviarte a ti
        mailto = f"mailto:robertoaxpe@gmail.com?subject=Recuperar Clave FOX&body=Hola, mi correo es {email_rec}. Olvidé mi clave."
        st.markdown(f'<a href="{mailto}" target="_blank" style="background-color:#FF6B00; color:white; padding:15px; text-decoration:none; border-radius:10px; display:block; text-align:center;">📧 ENVIAR EMAIL DE SOLICITUD</a>', unsafe_allow_html=True)
    
    if st.button("Volver al Login"):
        st.session_state.page = 'login'
        st.rerun()

# 3. PÁGINA DE REGISTRO
elif st.session_state.page == 'register':
    st.subheader("Formulario de Inscripción")
    with st.form("reg_form"):
        st.text_input("Nombre Completo")
        st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
        st.text_input("Academia / Club")
        if st.form_submit_button("ENVIAR REGISTRO"):
            st.success("¡Registro enviado con éxito!")
    if st.button("Volver"):
        st.session_state.page = 'login'
        st.rerun()

# 4. DASHBOARD PRINCIPAL (ORGANIZADOR / COMPETIDOR)
elif st.session_state.page == 'dashboard':
    st.markdown(f"<h1 style='color:#FF6B00;'>PANEL {st.session_state.user_role.upper()}</h1>", unsafe_allow_html=True)
    
    if st.session_state.user_role == 'organizador':
        tab1, tab2, tab3 = st.tabs(["📊 Inscritos", "⚔️ Generar Cruces", "⚙️ Ajustes"])
        with tab1:
            st.write("### Lista de Competidores")
            try:
                # Conexión real a Google Sheets
                conn = st.connection("gsheets", type=GSheetsConnection)
                data = conn.read()
                st.dataframe(data, use_container_width=True)
            except Exception as e:
                st.error("Error de conexión con Google Sheets. Revisa los 'Secrets' en Streamlit.")
        with tab2:
            st.info("Aquí aparecerán los brackets de competición.")
    
    else: # Vista Competidor
        tab1, tab2 = st.tabs(["👤 Mi Perfil", "📅 Horarios"])
        with tab1:
            st.write("Bienvenido a tu ficha de competidor.")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.page = 'login'
        st.session_state.user_role = None
        st.rerun()
