import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- CSS DEFINITIVO PARA MÓVIL Y PC ---
st.markdown("""
    <style>
    /* 1. Fondo negro total */
    .stApp { background-color: #000000; color: #FFFFFF; }

    /* 2. Forzar Centrado de Imágenes (Zorro y Logo) */
    .stImage {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    .stImage img {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* 3. Título Acceso */
    .titulo-fox { 
        text-align: center; 
        color: #FFFFFF !important; 
        font-size: 28px; 
        font-weight: bold; 
        margin: 15px 0;
    }

    /* 4. BOTÓN INICIAR SESIÓN (Corregido para que no salga blanco) */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important; /* NARANJA */
        color: #000000 !important;           /* TEXTO NEGRO */
        border: 2px solid #FF6B00 !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        opacity: 1 !important;
    }
    
    /* Forzar el color del texto dentro del botón incluso en móvil */
    div.stButton > button p {
        color: #000000 !important;
        font-weight: 900 !important;
    }

    /* 5. Inputs con bordes naranjas claros */
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #FF6B00 !important;
    }

    /* 6. Formulario */
    [data-testid="stForm"] { 
        border: 1px solid #FF6B00; 
        border-radius: 15px; 
        background-color: #0A0A0A; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False})

if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    
    # Logos (Carga local para evitar el interrogante)
    # Asegúrate de que estos nombres coincidan con tus archivos en GitHub
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=150)
    st.image("fox-letras-naranja.PNG", width=300)
    
    st.markdown("<div class='titulo-fox'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    with st.form("login_definitivo"):
        u = st.text_input("Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        
        if st.form_submit_button("INICIAR SESIÓN"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.update({'autenticado': True, 'perfil': 'Organizador'})
                st.rerun()
            elif p == "fox2026":
                st.session_state.update({'autenticado': True, 'perfil': 'Competidor'})
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.session_state['modo_registro'] = True
        st.rerun()

elif st.session_state['modo_registro']:
    # Formulario de registro...
    if st.button("Volver"):
        st.session_state['modo_registro'] = False
        st.rerun()
else:
    st.write(f"Bienvenido Panel {st.session_state['perfil']}")
    if st.button("Cerrar Sesión"):
        st.session_state['autenticado'] = False
        st.rerun()
