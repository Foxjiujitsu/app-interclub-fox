import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO CLONADO DE LA IMAGEN (CSS) ---
st.markdown("""
    <style>
    /* 1. Fondo negro total */
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Arial', sans-serif; }
    
    /* 2. CENTRADO DE LOGOS (Forzado para Móvil y PC) */
    .header-fox-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-bottom: 25px;
        margin-top: 15px;
    }
    
    /* 3. TÍTULO 'Acceso Interclub' */
    .titulo-acceso-fox { 
        text-align: center; color: #FFFFFF; font-size: 28px; 
        font-weight: bold; margin-bottom: 30px; margin-top: 10px;
    }

    /* 4. CAJA DE FORMULARIO CON BORDE NARANJA (Clonado) */
    [data-testid="stForm"] { 
        border: 2px solid #FF6B00; 
        border-radius: 15px; 
        background-color: #0A0A0A; 
        padding: 30px; 
        margin-top: 20px;
    }

    /* 5. ETIQUETAS DE TEXTO (Usuario, Contraseña) EN BLANCO PURO */
    label, [data-testid="stWidgetLabel"] p, .stMarkdown p {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        opacity: 1 !important;
    }

    /* 6. INPUTS (Grises oscuros con borde naranja claro) */
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important; 
        color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important; 
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    /* 7. BOTÓN INICIAR SESIÓN (Naranja brillante con letras negras) */
    div.stButton > button:first-child {
        background-color: #FF6B00 !important;
        color: #000000 !important; /* Texto NEGRO */
        border: 2px solid #FF6B00 !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-transform: uppercase !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Hover: Fondo negro, texto naranja */
    div.stButton > button:hover {
        background-color: #000000 !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
    }
    div.stButton > button:hover p {
        color: #FF6B00 !important;
    }

    /* 8. Botón de Registro Unificado centrado */
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        st.markdown("---")
        if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
            st.session_state['modo_registro'] = True
            st.rerun()

    /* 9. Ocultar iconos de enlace y basura de Streamlit */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False, 'user': None})

# --- PANTALLA DE ACCESO (LOGIN CLONADO) ---
if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    
    # 1. Logos Centrados con HTML
    st.markdown("""
        <div class="header-fox-container">
            <img src="Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg" width="160" style="margin-bottom:15px;">
            <img src="fox-letras-naranja.PNG" width="350">
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='titulo-acceso-fox'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    with st.form("login_central_fox_definitivo"):
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

    # Botón de Registro Unificado centrado
    _, col_btn, _ = st.columns([1, 3, 1])
    with col_btn:
        st.markdown("---")
        if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
            st.session_state['modo_registro'] = True
            st.rerun()

# --- PANTALLA DE REGISTRO ---
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

# --- CONTENIDO DE LA APP TRAS LOGUEARSE ---
else:
    with st.sidebar:
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=100)
        st.write(f"OSS! **{st.session_state['user']}**")
        if st.button("Cerrar Sesión"):
            st.session_state.update({'autenticado': False, 'perfil': None, 'user': None})
            st.rerun()

    st.title(f"BIENVENIDO AL PANEL {st.session_state['perfil'].upper()}")
