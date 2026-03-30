import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOX ACADEMY - ACCESO", page_icon="🦊", layout="centered")

# --- DISEÑO PROFESIONAL NEGRO Y NARANJA ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Textos en Blanco Brillante */
    label, .stMarkdown p, .stTextInput label {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
    
    /* Inputs con borde naranja */
    input {
        background-color: #1A1A1A !important;
        border: 2px solid #FF6B00 !important;
        color: white !important;
        border-radius: 10px !important;
        height: 45px !important;
    }

    /* Botón Entrar (Naranja) */
    .stButton > button {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        width: 100% !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        font-size: 18px !important;
    }

    /* Botón Registrarse (Negro con borde Naranja) */
    div[data-testid="stVerticalBlock"] > div:last-child .stButton > button {
        background-color: #000000 !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        margin-top: 20px;
    }

    .header-fox { text-align: center; color: #FF6B00; font-size: 32px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- CREDENCIALES MAESTRAS ---
ADMIN_USER = "Fox-Interclub"
ADMIN_PASS = "Interclub-Fox-2026"

# --- LÓGICA DE NAVEGACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False})

# --- PANTALLA DE ACCESO ÚNICA ---
if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=150)
    st.markdown("<div class='header-fox'>ACCESO FOX ACADEMY</div>", unsafe_allow_html=True)
    
    with st.form("login_unico"):
        u = st.text_input("Nombre de Usuario / Email")
        p = st.text_input("Contraseña", type="password")
        entrar = st.form_submit_button("INICIAR SESIÓN")
        
        if entrar:
            # 1. Chequeo Organizador (Oculto)
            if u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state.update({'autenticado': True, 'perfil': 'Organizador'})
                st.rerun()
            # 2. Chequeo Club
            elif p == "clubfox":
                st.session_state.update({'autenticado': True, 'perfil': 'Club', 'user': u})
                st.rerun()
            # 3. Chequeo Alumno
            elif p == "fox2026":
                st.session_state.update({'autenticado': True, 'perfil': 'Alumno', 'user': u})
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

    # BOTÓN PARA DARSE DE ALTA
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.session_state['modo_registro'] = True
        st.rerun()

# --- PANTALLA DE REGISTRO (ALTA NUEVA) ---
elif st.session_state['modo_registro']:
    st.markdown("<h2 style='color:#FF6B00; text-align:center;'>NUEVA INSCRIPCIÓN</h2>", unsafe_allow_html=True)
    tipo = st.radio("¿Qué deseas registrar?", ["Soy un Alumno / Competidor", "Soy un Club / Academia"])
    
    if tipo == "Soy un Alumno / Competidor":
        with st.form("alta_alumno"):
            st.write("Completa tus datos para el Interclub:")
            # Aquí van tus campos de nombre, peso, etc...
            nombre = st.text_input("Nombre Completo")
            academia = st.text_input("Academia")
            if st.form_submit_button("FINALIZAR REGISTRO"):
                # Lógica de guardado en GSheets...
                st.success("¡Inscrito correctamente! Ahora puedes loguearte.")
                st.session_state['modo_registro'] = False
                st.rerun()
    else:
        st.write("Formulario para registro de Clubes próximamente.")

    if st.button("Volver al Inicio"):
        st.session_state['modo_registro'] = False
        st.rerun()

# --- CONTENIDO DE LA APP (TRAS LOGUEARSE) ---
else:
    with st.sidebar:
        st.write(f"Sesión: **{st.session_state['perfil']}**")
        if st.button("Cerrar Sesión"):
            st.session_state['autenticado'] = False
            st.rerun()

    # Aquí va el resto de tu App según el perfil...
    st.image("fox-letras-naranja.PNG", width=250)
    st.title(f"BIENVENIDO AL PANEL {st.session_state['perfil'].upper()}")
