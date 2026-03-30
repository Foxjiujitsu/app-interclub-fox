import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO (ESTILO FORZADO AL MÁXIMO) ---
st.markdown("""
    <style>
    /* 1. Fondo y Textos Base */
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, p, span, label { color: #FFFFFF !important; font-weight: bold !important; }

    /* 2. CENTRADO TOTAL DE LOGOS */
    /* Forzamos que el contenedor de imágenes se alinee al centro */
    div[data-testid="stVerticalBlock"] > div:has(img) {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .stImage > img {
        display: block;
        margin: 0 auto;
    }

    /* 3. TÍTULO ACCESO */
    .acceso-titulo { 
        text-align: center; color: #FFFFFF; font-size: 28px; 
        font-weight: bold; margin-bottom: 20px; width: 100%; display: block;
    }

    /* 4. BOTÓN INICIAR SESIÓN (DISEÑO BLINDADO) */
    /* Forzamos el fondo naranja al botón */
    div.stButton > button {
        background-color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 10px !important;
        height: 3.5em !important;
        width: 100% !important;
    }
    
    /* FORZAMOS EL TEXTO NEGRO (Atacamos el elemento interno de Streamlit) */
    div.stButton > button p {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-transform: uppercase !important;
        margin: 0 !important;
    }

    /* Hover: Fondo negro, texto naranja */
    div.stButton > button:hover {
        background-color: #000000 !important;
        border: 2px solid #FF6B00 !important;
    }
    div.stButton > button:hover p {
        color: #FF6B00 !important;
    }

    /* 5. FORMULARIO Y INPUTS */
    [data-testid="stForm"] { border: 2px solid #FF6B00; border-radius: 15px; background-color: #0A0A0A; padding: 25px; }
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important; color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important; border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False, 'user': None})

# --- PANTALLA DE ACCESO ---
if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    
    # Logos centrados (ahora con el CSS de arriba deberían estar perfectos)
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=160)
    st.image("fox-letras-naranja.PNG", width=350)
    
    st.markdown("<div class='acceso-titulo'>Acceso Interclub</div>", unsafe_allow_html=True)
    
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

    # Botón de Registro centrado
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.session_state['modo_registro'] = True
        st.rerun()

# --- EL RESTO DEL CÓDIGO (REGISTRO Y PANELES) ---
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
                st.success("¡Registro enviado! Ahora puedes iniciar sesión.")
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
