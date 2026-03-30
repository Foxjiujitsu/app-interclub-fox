import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO (ESTILO ULTRA-FORZADO) ---
st.markdown("""
    <style>
    /* 1. Fondo y Textos Base */
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, p, span, label { color: #FFFFFF !important; font-weight: bold !important; }

    /* 2. CENTRADO TOTAL DE LOGOS (HTML Directo) */
    .centered-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    /* 3. BOTÓN INICIAR SESIÓN (NEGRO SOBRE NARANJA/BLANCO) */
    /* Forzamos el botón para que sea Naranja y el texto NEGRO */
    div.stButton > button {
        background-color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 10px !important;
        height: 3.5em !important;
        width: 100% !important;
    }
    
    /* ESTA ES LA CLAVE: Forzamos el color NEGRO en todas las capas internas del botón */
    div.stButton > button * {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-transform: uppercase !important;
    }

    /* Hover: Invertimos a fondo negro y letras naranjas */
    div.stButton > button:hover {
        background-color: #000000 !important;
        border: 2px solid #FF6B00 !important;
    }
    div.stButton > button:hover * {
        color: #FF6B00 !important;
    }

    /* Formulario e Inputs */
    [data-testid="stForm"] { border: 2px solid #FF6B00; border-radius: 15px; background-color: #0A0A0A; padding: 25px; }
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important; color: #FFFFFF !important;
        border: 1px solid #FF6B00 !important; border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False, 'user': None})

# --- PANTALLA DE ACCESO ---
if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    
    # Centrado de Logos usando un contenedor HTML para asegurar el eje central
    st.markdown("""
        <div class="centered-container">
            <img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/Imagen%20de%20WhatsApp%202024-11-27%20a%20las%2014.43.24_bca11eec.jpg" width="160">
            <img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="350">
            <h2 style="color: white; margin-top: 20px;">Acceso Interclub</h2>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_fox"):
        u = st.text_input("Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        
        # El botón de inicio
        if st.form_submit_button("INICIAR SESIÓN"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.update({'autenticado': True, 'perfil': 'Organizador', 'user': u})
                st.rerun()
            elif p == "fox2026":
                st.session_state.update({'autenticado': True, 'perfil': 'Competidor', 'user': u})
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")

    # Botón de Registro
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.session_state['modo_registro'] = True
        st.rerun()

# --- REGISTRO Y PANELES ---
elif st.session_state['modo_registro']:
    st.image("fox-letras-naranja.PNG", width=250)
    st.markdown("<h2 style='text-align:center; color:#FF6B00;'>NUEVA INSCRIPCIÓN</h2>", unsafe_allow_html=True)
    
    tipo = st.radio("¿Qué deseas registrar?", ["Soy un Competidor", "Soy un Club"])
    
    with st.form("registro_unico"):
        st.write(f"Crea tu cuenta como {tipo}:")
        reg_user = st.text_input("Nombre de Usuario")
        reg_email = st.text_input("Correo Electrónico")
        reg_pass = st.text_input("Contraseña", type="password")
        
        if st.form_submit_button("FINALIZAR REGISTRO"):
            if reg_user and reg_email and reg_pass:
                st.success("¡Registro enviado! Ya puedes iniciar sesión.")
                st.session_state['modo_registro'] = False
                st.rerun()
            else:
                st.error("Rellena todos los campos.")
    
    if st.button("Volver al Inicio"):
        st.session_state['modo_registro'] = False
        st.rerun()

else:
    st.title(f"OSS! PANEL {st.session_state['perfil'].upper()}")
    if st.button("Cerrar Sesión"):
        st.session_state.update({'autenticado': False, 'perfil': None})
        st.rerun()
