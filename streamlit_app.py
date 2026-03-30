import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO CORREGIDO ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Arial', sans-serif; }
    h1, h2, h3, p, span, label { color: #FFFFFF !important; }

    /* Cabecera Centrada */
    [data-testid="stVerticalBlock"] > div:has(img) {
        display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
    }
    .stImage > img { display: block; margin-left: auto; margin-right: auto; }
    .acceso-interclub-titulo { text-align: center; color: #FFFFFF; font-size: 26px; font-weight: bold; margin-top: -10px; margin-bottom: 20px; }

    /* Inputs */
    .stTextInput>div>div>input, .stPasswordInput>div>div>input {
        background-color: #1A1A1A !important; color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important; border-radius: 10px !important;
    }

    /* Botón INICIAR SESIÓN (Naranja con letras negras) */
    .stButton>button {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border-radius: 10px !important;
        border: 2px solid #FF6B00 !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    .stButton>button:hover {
        background-color: #000000 !important;
        color: #FF6B00 !important;
    }

    /* Botón de Registro (Borde naranja, fondo negro) */
    div[data-testid="stVerticalBlock"] > div:last-child .stButton>button {
        background-color: #000000 !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        margin-top: 20px;
    }

    /* Radio Button Naranja */
    label[data-baseweb="radio"] > div:first-child { border-color: #FF6B00 !important; }
    label[data-baseweb="radio"][aria-checked="true"] > div:first-child { background-color: #FF6B00 !important; }
    label[data-baseweb="radio"][aria-checked="true"] > div:first-child > div { background-color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CREDENCIALES ---
ADMIN_USER = "Fox-Interclub"
ADMIN_PASS = "Interclub-Fox-2026"

if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False, 'user': None})

# --- 1. PANTALLA DE ACCESO ---
if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=140)
    st.image("fox-letras-naranja.PNG", width=320)
    st.markdown("<div class='acceso-interclub-titulo'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    with st.form("login_fox"):
        u = st.text_input("Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        if st.form_submit_button("INICIAR SESIÓN"):
            if u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state.update({'autenticado': True, 'perfil': 'Organizador', 'user': u})
                st.rerun()
            elif p == "fox2026":
                st.session_state.update({'autenticado': True, 'perfil': 'Competidor', 'user': u})
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")

    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.session_state['modo_registro'] = True
        st.rerun()

# --- 2. PANTALLA DE REGISTRO (SOLO COMPETIDOR) ---
elif st.session_state['modo_registro']:
    st.image("fox-letras-naranja.PNG", width=250)
    st.markdown("<h2 style='text-align:center; color:#FF6B00;'>NUEVA INSCRIPCIÓN</h2>", unsafe_allow_html=True)
    
    with st.form("registro_competidor"):
        st.write("Crea tu cuenta de Competidor:")
        reg_user = st.text_input("Nombre de Usuario")
        reg_email = st.text_input("Email")
        reg_pass = st.text_input("Contraseña", type="password")
        
        if st.form_submit_button("FINALIZAR REGISTRO"):
            if reg_user and reg_email and reg_pass:
                st.success("¡Registro completado! Ya puedes iniciar sesión con tu usuario.")
                st.session_state['modo_registro'] = False
            else:
                st.error("Rellena todos los campos.")

    if st.button("Volver al Inicio"):
        st.session_state['modo_registro'] = False
        st.rerun()

# --- 3. PANELES DE USUARIO ---
else:
    with st.sidebar:
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=80)
        st.write(f"Usuario: {st.session_state['user']}")
        if st.button("Cerrar Sesión"):
            st.session_state.update({'autenticado': False, 'perfil': None})
            st.rerun()

    if st.session_state['perfil'] == "Organizador":
        st.title("PANEL ORGANIZADOR")
        # Aquí iría tu tabla de Google Sheets para gestionarlo todo
    else:
        st.title("MI FICHA DE COMPETIDOR")
        st.write("Aquí podrás rellenar tu peso, cinturón y academia.")
