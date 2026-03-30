import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO (ESTILO BOMBARDEO DE COLOR) ---
st.markdown("""
    <style>
    /* 1. Fondo y Textos Base */
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Arial', sans-serif; }
    h1, h2, h3, p, span, label, div { color: #FFFFFF !important; font-weight: bold !important; }

    /* 2. Forzar Centrado de Imágenes en Móvil y PC */
    .stImage {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    .stImage img {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* 3. Título de Acceso Centrado */
    .acceso-titulo-fox { 
        text-align: center; 
        color: #FFFFFF !important; 
        font-size: 30px; 
        font-weight: 900 !important; 
        margin-top: 10px; 
        margin-bottom: 25px; 
        width: 100%;
        display: block;
    }

    /* 4. BOTÓN INICIAR SESIÓN (DISEÑO BLINDADO TOTAL) */
    /* Naranja con letras NEGRAS ABSOLUTAS -> Hover Negro con letras naranjas */
    div.stButton > button {
        background-color: #FF6B00 !important;
        color: #000000 !important; /* Forzamos el color NEGRO al botón */
        border: 2px solid #FF6B00 !important;
        border-radius: 12px !important;
        height: 3.8em !important;
        width: 100% !important;
        transition: all 0.3s ease-in-out;
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* BOMBARDEO DE COLOR NEGRO A TODOS LOS ELEMENTOS INTERNOS DEL BOTÓN */
    div.stButton > button p,
    div.stButton > button span,
    div.stButton > button label,
    div.stButton > button div,
    div.stButton > button .stMarkdown {
        color: #000000 !important; /* Forzamos el color NEGRO al texto interno */
        font-weight: 900 !important;
        font-size: 19px !important;
        text-transform: uppercase !important;
        margin: 0 !important;
        opacity: 1 !important;
    }

    /* Hover: Fondo negro, texto naranja */
    div.stButton > button:hover {
        background-color: #000000 !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
    }
    div.stButton > button:hover p,
    div.stButton > button:hover span {
        color: #FF6B00 !important;
    }

    /* 5. Inputs (Bordes Naranjas) */
    .stTextInput input, .stPasswordInput input {
        background-color: #1A1A1A !important; 
        color: #FFFFFF !important;
        border: 2px solid #FF6B00 !important; 
        border-radius: 12px !important;
    }
    
    /* 6. Formulario */
    [data-testid="stForm"] { 
        border: 2px solid #FF6B00; 
        border-radius: 15px; 
        background-color: #0A0A0A; 
        padding: 30px; 
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.update({'autenticado': False, 'perfil': None, 'modo_registro': False, 'user': None})

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state['autenticado'] and not st.session_state['modo_registro']:
    
    # 1. Logos Centrados con columns (Método más estable en móvil)
    col1, col_centro, col2 = st.columns([1, 2, 1])
    with col_centro:
        # Volvemos a cargar desde el propio código para rapidez y fiabilidad
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=160)
        st.image("fox-letras-naranja.PNG", use_container_width=True)
    
    st.markdown("<div class='acceso-titulo-fox'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    with st.form("login_central_fox_definitivo"):
        u = st.text_input("Nombre de Usuario o Email")
        p = st.text_input("Contraseña", type="password")
        
        # El botón con el estilo blindado
        if st.form_submit_button("INICIAR SESIÓN"):
            # Credenciales Organizador (Secretas)
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.update({'autenticado': True, 'perfil': 'Organizador', 'user': u})
                st.rerun()
            # Lógica Competidores (De momento genérica para pruebas)
            elif p == "fox2026":
                st.session_state.update({'autenticado': True, 'perfil': 'Competidor', 'user': u})
                st.rerun()
            else:
                st.error("Credenciales incorrectas. (Usa fox2026 para Competidor)")

    # Botón de Registro Unificado centrado
    _, col_btn, _ = st.columns([1, 3, 1])
    with col_btn:
        st.markdown("---")
        if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
            st.session_state['modo_registro'] = True
            st.rerun()

# --- PANTALLA DE REGISTRO (ALTA NUEVA SOLICITUD) ---
elif st.session_state['modo_registro']:
    # Cabecera de Registro
    st.image("fox-letras-naranja.PNG", width=250)
    st.markdown("<h2 style='color:#FF6B00; text-align:center; font-weight:bold;'>NUEVA INSCRIPCIÓN</h2>", unsafe_allow_html=True)
    st.write("Selecciona tu perfil para solicitar acceso al Interclub FOX.")
    
    tipo_registro = st.radio("¿Qué deseas registrar?", ["Soy un Competidor", "Soy un Club"])
    
    with st.form("solicitud_alta_fox", clear_on_submit=True):
        st.markdown(f"<h3 style='color:#FF6B00;'>Datos de Acceso ({tipo_registro})</h3>", unsafe_allow_html=True)
        reg_user = st.text_input("Nombre de Usuario (para login)")
        reg_email = st.text_input("Correo Electrónico (Email)")
        reg_pass1 = st.text_input("Contraseña", type="password")
        reg_pass2 = st.text_input("Repite la Contraseña", type="password")
        st.info("Una vez enviado, la organización validará tu cuenta en 24h.")
        enviar_solicitud = st.form_submit_button("FINALIZAR REGISTRO")
        if enviar_solicitud:
            st.success("¡Solicitud enviada! Nos pondremos en contacto por email. Oss.")
            st.balloons()

    if st.button("Volver al Inicio (Login)"):
        st.session_state['modo_registro'] = False
        st.rerun()

# --- CONTENIDO TRAS LOGUEARSE (PANEL DE CONTROL) ---
else:
    with st.sidebar:
        st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=100)
        st.write(f"🦊 OSS! **{st.session_state['user']}**")
        if st.button("Cerrar Sesión"):
            st.session_state.update({'autenticado': False, 'perfil': None, 'user': None})
            st.rerun()

    st.markdown(f"<h1 style='text-align: center; color: #FF6B00;'>PANEL {st.session_state['perfil'].upper()}</h1>", unsafe_allow_html=True)
    st.write("Bienvenido al sistema oficial del Interclub FOX.")
    # Aquí iría el resto de la App según el perfil...
