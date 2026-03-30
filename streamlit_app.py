import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO REFINADO (FORZANDO COLORES) ---
st.markdown("""
    <style>
    /* 1. Fondo y Textos */
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, p, span, label { color: #FFFFFF !important; font-weight: bold !important; }

    /* 2. Centrado Real de Imágenes */
    .stImage {
        display: flex;
        justify-content: center;
    }
    .stImage > img {
        margin-left: auto;
        margin-right: auto;
    }

    /* 3. Título de Cabecera */
    .acceso-titulo { text-align: center; color: #FFFFFF; font-size: 28px; font-weight: bold; margin-top: 10px; margin-bottom: 20px; }

    /* 4. Inputs (Bordes Naranjas) */
    .stTextInput>div>div>input, .stPasswordInput>div>div>input {
        background-color: #1A1A1A !important; color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important; border-radius: 10px !important;
    }

    /* 5. BOTÓN INICIAR SESIÓN (FORZADO NARANJA) */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border-radius: 10px !important;
        border: 2px solid #FF6B00 !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-transform: uppercase !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    div.stButton > button:hover {
        background-color: #000000 !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
    }

    /* 6. Radio Button (Selección naranja) */
    label[data-baseweb="radio"] > div:first-child { border-color: #FF6B00 !important; }
    label[data-baseweb="radio"][aria-checked="true"] > div:first-child { background-color: #FF6B00 !important; }
    label[data-baseweb="radio"][aria-checked="true"] > div:first-child > div { background-color: #000000 !important; }

    /* 7. Contenedor de Formulario */
    [data-testid="stForm"] { border: 2px solid #FF6B00; border-radius: 15px; background-color: #0A0A0A; padding: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False, 'user': None})

# --- PANTALLA DE ACCESO ---
if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    # Centrado manual con columnas para asegurar posición
    _, col_logo, _ = st.columns([0.5, 2, 0.5])
    with col_logo:
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=150)
        st.image("fox-letras-naranja.PNG", use_column_width=True)
    
    st.markdown("<div class='acceso-titulo'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    with st.form("login_fox"):
        u = st.text_input("Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        # El botón ahora tiene el estilo forzado por CSS
        if st.form_submit_button("INICIAR SESIÓN"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
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

# --- PANTALLA DE REGISTRO ---
elif st.session_state['modo_registro']:
    _, col_logo, _ = st.columns([1, 2, 1])
    with col_logo:
        st.image("fox-letras-naranja.PNG", use_column_width=True)
    
    st.markdown("<h2 style='text-align:center; color:#FF6B00;'>NUEVA INSCRIPCIÓN</h2>", unsafe_allow_html=True)
    
    tipo = st.radio("¿Qué deseas registrar?", ["Soy un Competidor", "Soy un Club"])
    
    with st.form("registro_unico"):
        st.write(f"Crea tu cuenta como {tipo}:")
        reg_user = st.text_input("Nombre de Usuario")
        reg_email = st.text_input("Correo Electrónico")
        reg_pass = st.text_input("Contraseña", type="password")
        
        if st.form_submit_button("FINALIZAR REGISTRO"):
            if reg_user and reg_email and reg_pass:
                st.success("¡Registro enviado! Ahora puedes iniciar sesión.")
                st.session_state['modo_registro'] = False
                st.rerun()
            else:
                st.error("Rellena todos los campos.")

    if st.button("Volver al Inicio"):
        st.session_state['modo_registro'] = False
        st.rerun()

# --- PANELES TRAS LOGIN ---
else:
    with st.sidebar:
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=80)
        st.write(f"OSS! **{st.session_state['user']}**")
        if st.button("Cerrar Sesión"):
            st.session_state.update({'autenticado': False, 'perfil': None})
            st.rerun()

    if st.session_state['perfil'] == "Organizador":
        st.title("🛡️ PANEL ORGANIZADOR")
        st.write("Bienvenido, Roberto.")
    else:
        st.title("🥋 MI FICHA DE COMPETIDOR")
