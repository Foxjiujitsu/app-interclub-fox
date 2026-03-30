import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX JIU-JITSU", page_icon="🦊", layout="centered")

# --- CSS RADICAL PARA CLONAR EL DISEÑO ---
st.markdown("""
    <style>
    /* 1. Fondo y Base */
    .stApp { background-color: #F2F2F2; color: #333333; }
    header, footer, #MainMenu {visibility: hidden;}
    
    /* 2. Estilo de Contenedores y Logos */
    .logo-container { display: flex; justify-content: center; width: 100%; margin-bottom: 20px; padding-top: 10px; }
    
    /* 3. Títulos y Etiquetas */
    .titulo-seccion { text-align: center; color: #1A1A1A; font-size: 26px; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; }
    .sub-titulo { text-align: center; color: #1A1A1A; font-size: 18px; font-weight: 700; margin-bottom: 20px; }
    label p { font-weight: 600 !important; color: #444 !important; margin-bottom: -5px !important; }

    /* 4. Inputs con Sombra y Bordes Suaves (Clon Imagen) */
    .stTextInput input, .stPasswordInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 12px !important;
        height: 48px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08) !important;
    }

    /* 5. BOTONES NARANJA PREMUM (Efecto Degradado/Sombra) */
    div.stButton > button {
        background: linear-gradient(180deg, #FF6B00 0%, #D45900 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 15px !important;
        height: 3.8em !important;
        width: 100% !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 6px 15px rgba(212, 89, 0, 0.4) !important;
        text-transform: uppercase;
        margin-top: 10px;
    }
    
    /* Botones de enlace (texto plano) */
    .btn-link button {
        background: transparent !important;
        color: #444 !important;
        box-shadow: none !important;
        text-decoration: none !important;
        font-size: 0.85rem !important;
        margin-top: -10px !important;
    }

    /* 6. Ajustes de Formulario de Registro (Columnas Compactas) */
    .row-flex { display: flex; gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- NAVEGACIÓN ---

# 1. PÁGINA DE LOGIN
if st.session_state.page == 'login':
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="280"></div>', unsafe_allow_html=True)
    st.markdown("<div class='titulo-seccion'>Acceso Interclub</div>", unsafe_allow_html=True)
    
    u = st.text_input("Usuario o Email", placeholder="👤")
    p = st.text_input("Contraseña", type="password", placeholder="🔒")
    
    if st.button("INICIAR SESIÓN"):
        if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
            st.session_state.page = 'dashboard'
            st.rerun()
        else: st.error("Credenciales incorrectas")

    st.markdown("<div class='btn-link'>", unsafe_allow_html=True)
    if st.button("¿OLVIDASTE TU CONTRASEÑA?"):
        st.session_state.page = 'forgot'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    if st.button("¿AÚN NO ESTÁS INSCRITO? REGÍSTRATE AQUÍ"):
        st.session_state.page = 'register'
        st.rerun()

# 2. PÁGINA RECUPERAR CONTRASEÑA (CLON IDENTICO)
elif st.session_state.page == 'forgot':
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="200"></div>', unsafe_allow_html=True)
    st.markdown("<div class='titulo-seccion'>RECUPERAR CONTRASEÑA</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; padding: 0 20px; font-size:14px;'>Introduce el correo electrónico asociado a tu cuenta para recibir las instrucciones de restablecimiento.</p>", unsafe_allow_html=True)
    
    email_rec = st.text_input("Correo electrónico", placeholder="✉️")
    
    if st.button("ENVIAR INSTRUCCIONES"):
        st.success("Correo enviado")
    
    st.markdown("<div class='btn-link'>", unsafe_allow_html=True)
    if st.button("¿Volver al inicio de sesión? Haz clic aquí"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 3. PÁGINA DE REGISTRO (CON TODOS LOS CAMPOS DE TU IMAGEN)
elif st.session_state.page == 'register':
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="200"></div>', unsafe_allow_html=True)
    st.markdown("<div class='titulo-seccion' style='font-size:20px;'>FORMULARIO DE REGISTRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-titulo' style='font-size:16px;'>INFORMACIÓN DE LUCHADOR</div>", unsafe_allow_html=True)
    
    with st.container():
        nom = st.text_input("Nombre y Apellidos")
        cin = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
        club = st.text_input("Club")
        
        # Fila para Peso y Edad (Compacto como en la imagen)
        c1, c2 = st.columns(2)
        with c1: peso = st.number_input("Peso (kg)", min_value=10, max_value=200, step=1)
        with c2: edad = st.number_input("Edad", min_value=4, max_value=80, step=1)
        
        estilo = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI", "AMBOS"])
        
        st.markdown("<div class='sub-titulo' style='font-size:16px; margin-top:15px;'>EMAIL Y CONTRASEÑA</div>", unsafe_allow_html=True)
        reg_mail = st.text_input("Email", placeholder="✉️ Email")
        reg_pass = st.text_input("Contraseña", type="password", placeholder="🔒 Contraseña")
        
        if st.button("REGISTRARSE"):
            st.success("¡Inscripción realizada!")
            
    if st.button("VOLVER"):
        st.session_state.page = 'login'
        st.rerun()

# 4. DASHBOARD (CONEXIÓN GOOGLE SHEETS CORREGIDA)
elif st.session_state.page == 'dashboard':
    st.markdown("<h1 style='color:#FF6B00; text-align:center;'>PANEL DE GESTIÓN</h1>", unsafe_allow_html=True)
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        st.dataframe(df, use_container_width=True)
    except:
        st.error("⚠️ Error: Conecta el Google Sheets en los 'Secrets' de Streamlit.")
        
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.page = 'login'
        st.rerun()
