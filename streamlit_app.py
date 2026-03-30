import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO (ESTILO FORZADO) ---
st.markdown("""
    <style>
    /* Fondo y Textos Base */
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, p, span, label { color: #FFFFFF !important; font-weight: bold !important; }

    /* CENTRADO DE LOGOS */
    .stImage { display: flex !important; justify-content: center !important; }
    
    /* TÍTULO ACCESO */
    .acceso-titulo { 
        text-align: center; color: #FFFFFF; font-size: 28px; 
        font-weight: bold; margin-bottom: 20px; width: 100%; display: block;
    }

    /* BOTÓN INICIAR SESIÓN (DISEÑO BLINDADO) */
    /* Atacamos el botón y cualquier texto/párrafo dentro de él */
    div.stButton > button {
        background-color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 10px !important;
        height: 3.5em !important;
        width: 100% !important;
        opacity: 1 !important;
        transition: 0.3s !important;
    }
    
    /* ESTO ES LO MÁS IMPORTANTE: Forzamos el texto NEGRO */
    div.stButton > button div, 
    div.stButton > button p, 
    div.stButton > button span {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-transform: uppercase !important;
    }

    /* Hover: Fondo negro, texto naranja */
    div.stButton > button:hover {
        background-color: #000000 !important;
        border: 2px solid #FF6B00 !important;
    }
    div.stButton > button:hover p,
    div.stButton > button:hover span,
    div.stButton > button:hover div {
        color: #FF6B00 !important;
    }

    /* FORMULARIO */
    [data-testid="stForm"] { border: 2px solid #FF6B00; border-radius: 15px; background-color: #0A0A0A; padding: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False, 'user': None})

# --- PANTALLA DE ACCESO ---
if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    
    # Centrado manual con columnas
    col_izq, col_centro, col_der = st.columns([1, 3, 1])
    
    with col_centro:
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=160)
        st.image("fox-letras-naranja.PNG", use_container_width=True)
        
        st.markdown("<div class='acceso-titulo'>Acceso Interclub</div>", unsafe_allow_html=True)
        
        with st.form("login_fox"):
            u = st.text_input("Usuario o Email")
            p = st.text_input("Contraseña", type="password")
            
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
    _, col_btn, _ = st.columns([0.5, 3, 0.5])
    with col_btn:
        if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
            st.session_state['modo_registro'] = True
            st.rerun()

# --- EL RESTO DEL CÓDIGO (REGISTRO Y PANELES) SIGUE IGUAL ---
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
