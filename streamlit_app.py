import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOX INTERCLUB", page_icon="🦊", layout="centered")

# --- DISEÑO DE ALTO CONTRASTE ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Etiquetas en Blanco Puro y Negrita */
    label, .stMarkdown p, .stSelectbox label, .stNumberInput label, .stTextInput label, .stRadio label {
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    
    /* Inputs y Selectores */
    input, div[data-baseweb="select"], div[data-baseweb="input"], .stRadio div {
        background-color: #1A1A1A !important;
        border: 2px solid #FF6B00 !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* Botones Naranja FOX */
    .stButton > button {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        width: 100% !important;
        border-radius: 12px !important;
        height: 3.8em !important;
        font-size: 20px !important;
        text-transform: uppercase;
    }
    .stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #FF6B00 !important;
    }

    /* Pestañas */
    button[data-baseweb="tab"] { color: #AAAAAA !important; font-size: 18px !important; }
    button[aria-selected="true"] { color: #FF6B00 !important; border-bottom: 4px solid #FF6B00 !important; }
    
    .header-fox { text-align: center; color: #FF6B00; font-size: 28px; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS DE ACCESO ---
ADMIN_USER = "Fox-Interclub"
ADMIN_PASS = "Interclub-Fox-2026"
ADMIN_EMAIL = "robertoaxpe@gmail.com"

# --- CONTROL DE SESIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'perfil' not in st.session_state:
    st.session_state['perfil'] = None

# --- PANTALLA DE SELECCIÓN DE PERFIL / LOGIN ---
if not st.session_state['autenticado']:
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=130)
    st.markdown("<div class='header-fox'>BIENVENIDO A FOX ACADEMY</div>", unsafe_allow_html=True)
    
    # El usuario elige primero CÓMO quiere entrar
    opcion_perfil = st.radio("¿Cómo deseas acceder?", ["Soy Alumno / Competidor", "Soy un Club / Academia", "Organizador"], index=0)
    
    with st.form("login_gate"):
        if opcion_perfil == "Organizador":
            u = st.text_input("Usuario o Email del Admin")
            p = st.text_input("Contraseña Maestra", type="password")
        elif opcion_perfil == "Soy un Club / Academia":
            u = st.text_input("Nombre del Club")
            p = st.text_input("Clave de Club (pide la tuya a la organización)", type="password")
        else:
            u = st.text_input("Tu Nombre Completo")
            p = st.text_input("Clave del Evento (fox2026)", type="password")
            
        entrar = st.form_submit_button("ACCEDER AL SISTEMA")
        
        if entrar:
            if opcion_perfil == "Organizador":
                if (u == ADMIN_USER or u == ADMIN_EMAIL) and p == ADMIN_PASS:
                    st.session_state.update({"autenticado": True, "perfil": "Organizador"})
                    st.rerun()
                else: st.error("Acceso denegado.")
            
            elif opcion_perfil == "Soy un Club / Academia":
                if p == "clubfox": # Clave genérica para clubs
                    st.session_state.update({"autenticado": True, "perfil": "Club", "nombre_club": u})
                    st.rerun()
                else: st.error("Clave de club incorrecta.")
                
            else: # Alumnos
                if p == "fox2026":
                    st.session_state.update({"autenticado": True, "perfil": "Alumno"})
                    st.rerun()
                else: st.error("Clave del evento incorrecta.")

# --- CONTENIDO SEGÚN PERFIL ---
else:
    with st.sidebar:
        st.write(f"Conectado como: **{st.session_state['perfil']}**")
        if st.button("Cerrar Sesión"):
            st.session_state['autenticado'] = False
            st.rerun()

    st.image("fox-letras-naranja.PNG", width=220)

    # 1. VISTA ORGANIZADOR
    if st.session_state['perfil'] == "Organizador":
        st.title("⚡ PANEL DE CONTROL")
        tabs = st.tabs(["📊 Todos los Inscritos", "⚔️ Gestionar Cruces", "📸 Subir Fotos"])
        
        with tabs[0]:
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df = conn.read()
                df_edit = st.data_editor(df, num_rows="dynamic")
                if st.button("GUARDAR EN EXCEL"):
                    conn.update(data=df_edit)
                    st.success("¡Base de datos actualizada!")
            except: st.error("Conexión fallida con el Excel.")

    # 2. VISTA CLUB
    elif st.session_state['perfil'] == "Club":
        st.title(f"🏫 ACADEMIA: {st.session_state['nombre_club']}")
        tabs = st.tabs(["👥 Mis Alumnos", "⚔️ Ver Cruces", "📸 Fotos"])
        
        with tabs[0]:
            st.write("Aquí verás y editarás solo a tus alumnos inscritos.")
            # Lógica de filtrado por academia...

    # 3. VISTA ALUMNO
    else:
        st.title("🦊 INSCRIPCIÓN ALUMNO")
        tabs = st.tabs(["📝 Formulario", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])
        
        with tabs[0]:
            with st.form("reg_alumno"):
                nom = st.text_input("Nombre Completo")
                c1, c2 = st.columns(2)
                with c1:
                    ed = st.number_input("Edad", 4, 80, step=1)
                    cin = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
                with c2:
                    pe = st.text_input("Peso (ej. -70kg)")
                    mod = st.radio("Modalidad", ["BJJ (Gi)", "NO-GI"])
                aca = st.text_input("Academia")
                
                if st.form_submit_button("REGISTRARME AHORA"):
                    # Lógica de guardado...
                    st.balloons()
