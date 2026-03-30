import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX INTERCLUB", page_icon="🦊", layout="centered")

# --- DISEÑO CLONADO (FONDO CLARO / BOTÓN NARANJA) ---
st.markdown("""
    <style>
    /* 1. Fondo claro y textos oscuros */
    .stApp { 
        background-color: #F8F9FA; 
        color: #333333; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    
    /* 2. Ocultar menús de Streamlit */
    header, footer, #MainMenu {visibility: hidden;}

    /* 3. Centrado total de la cabecera */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 20px;
    }

    /* 4. Título Acceso Interclub */
    .acceso-titulo {
        text-align: center;
        color: #1A1A1A !important;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 20px;
    }

    /* 5. Etiquetas de los campos (Usuario/Contraseña) */
    label, [data-testid="stWidgetLabel"] p {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-bottom: 5px !important;
    }

    /* 6. Inputs (Fondo blanco, borde sutil) */
    .stTextInput input, .stPasswordInput input {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1px solid #DDDDDD !important;
        border-radius: 12px !important;
        height: 50px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    /* Borde naranja al hacer clic */
    .stTextInput input:focus {
        border-color: #FF6B00 !important;
    }

    /* 7. BOTÓN INICIAR SESIÓN (Naranja con letras blancas) */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 15px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(255, 107, 0, 0.3) !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #E66000 !important;
        transform: translateY(-1px);
    }

    /* 8. Links de abajo (¿Olvidaste...? / Registro) */
    .footer-links {
        text-align: center;
        margin-top: 15px;
        color: #666666;
        font-size: 0.9rem;
    }
    
    /* Botón de registro (Transparente abajo) */
    .btn-registro {
        margin-top: 25px;
    }
    .btn-registro button {
        background-color: transparent !important;
        color: #888888 !important;
        border: none !important;
        font-weight: 500 !important;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

# --- PANTALLA DE ACCESO ---
if not st.session_state.logueado:
    
    # Logos centrados (usando las imágenes que ya tienes en GitHub)
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=140)
    st.image("fox-letras-naranja.PNG", width=320)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div class='acceso-titulo'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    # Usamos columnas para darle ese aire de "tarjeta" centrada
    col1, col_centro, col2 = st.columns([0.1, 0.8, 0.1])
    
    with col_centro:
        u = st.text_input("Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        
        st.write("") # Espacio
        
        if st.button("INICIAR SESIÓN"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.logueado = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        
        st.markdown("<div class='footer-links'>¿OLVIDASTE TU CONTRASEÑA?</div>", unsafe_allow_html=True)

    # Botón de registro al final
    st.markdown("<div class='btn-registro'>", unsafe_allow_html=True)
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.info("Formulario de registro próximamente")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANEL INTERIOR ---
else:
    with st.sidebar:
        if st.button("Cerrar Sesión"):
            st.session_state.logueado = False
            st.rerun()
    st.title("BIENVENIDO AL PANEL FOX")
    st.write("Tu sesión se ha iniciado correctamente con el nuevo diseño claro.")
