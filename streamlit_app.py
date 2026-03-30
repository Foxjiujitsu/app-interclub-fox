import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX INTERCLUB", page_icon="🦊", layout="centered")

# --- DISEÑO CLONADO 100% (ESTILO CLARO / PREMIUM) ---
st.markdown("""
    <style>
    /* 1. Fondo General (Gris muy claro/Blanco) */
    .stApp { 
        background-color: #F2F2F2; 
        color: #333333; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }
    
    /* 2. Ocultar elementos de Streamlit */
    header, footer, #MainMenu {visibility: hidden;}

    /* 3. Contenedor de Logos Centrados */
    .header-fox-premium {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-bottom: 30px;
        padding-top: 20px;
    }

    /* 4. Título 'Acceso Interclub' en Negro */
    .titulo-negro {
        text-align: center;
        color: #1A1A1A !important;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 25px;
    }

    /* 5. Etiquetas de Input (Usuario/Contraseña) en Gris Oscuro */
    label, [data-testid="stWidgetLabel"] p {
        color: #444444 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 8px !important;
    }

    /* 6. Inputs Blancos con Sombra Suave (Efecto Imagen) */
    .stTextInput input, .stPasswordInput input {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 12px !important;
        height: 55px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        font-size: 16px !important;
    }
    
    /* 7. BOTÓN INICIAR SESIÓN (Naranja con letras BLANCAS - Idéntico imagen) */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important;
        color: #FFFFFF !important; /* Texto BLANCO como en la foto */
        border: none !important;
        border-radius: 15px !important;
        height: 3.8em !important;
        width: 100% !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        text-transform: uppercase;
        box-shadow: 0 6px 12px rgba(255, 107, 0, 0.2) !important;
        margin-top: 10px;
    }

    /* 8. Links Inferiores (¿Olvidaste...? / Registro) */
    .link-footer {
        text-align: center;
        margin-top: 20px;
        color: #666666 !important;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Estilo para el botón de registro al final de la página */
    .btn-registro-final {
        margin-top: 40px;
        text-align: center;
    }
    .btn-registro-final button {
        background-color: transparent !important;
        color: #888888 !important;
        border: none !important;
        font-weight: bold !important;
        text-decoration: none !important;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE LOGIN ---
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

# --- PANTALLA DE ACCESO (EL CLON) ---
if not st.session_state.logueado:
    
    # Cabecera con Logo FOX
    st.markdown('<div class="header-fox-premium">', unsafe_allow_html=True)
    # Solo usamos el logo de letras FOX como en la imagen
    st.image("fox-letras-naranja.PNG", width=320)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div class='titulo-negro'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    # Contenedor central
    col1, col_centro, col2 = st.columns([0.05, 0.9, 0.05])
    
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
        
        st.markdown("<div class='link-footer'>¿OLVIDASTE TU CONTRASEÑA?</div>", unsafe_allow_html=True)

    # Botón inferior de registro
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.info("Formulario de registro en proceso.")

# --- PANTALLA INTERIOR ---
else:
    with st.sidebar:
        if st.button("Cerrar Sesión"):
            st.session_state.logueado = False
            st.rerun()
    st.title("Bienvenido al Panel de Control")
    st.write("Has accedido correctamente con el nuevo diseño.")
