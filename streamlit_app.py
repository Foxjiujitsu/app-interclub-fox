import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX INTERCLUB - ACCESO", page_icon="🦊", layout="centered")

# --- ESTILOS CSS (NEGRO Y NARANJA) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stForm"] { border: 2px solid #FF6B00; background-color: #0A0A0A; border-radius: 15px; padding: 30px; }
    .stButton > button { 
        background-color: #FF6B00 !important; color: #000000 !important; 
        font-weight: bold; width: 100%; border-radius: 10px; height: 3em;
    }
    .stButton > button:hover { background-color: #FFFFFF !important; color: #FF6B00 !important; }
    input { background-color: #1A1A1A !important; color: white !important; border: 1px solid #FF6B00 !important; }
    .login-header { text-align: center; color: #FF6B00; font-size: 35px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS FICTICIA DE USUARIOS (ORGANIZADOR) ---
ADMIN_USER = "Fox-Interclub"
ADMIN_PASS = "Interclub-Fox-2026"
ADMIN_EMAIL = "robertoaxpe@gmail.com"

# --- ESTADO DE LA SESIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'rol' not in st.session_state:
    st.session_state['rol'] = None

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state['autenticado']:
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=150)
    st.markdown("<div class='login-header'>ACCESO ACADEMY</div>", unsafe_allow_html=True)
    
    tab_login, tab_recover = st.tabs(["Entrar", "¿Olvidaste tu contraseña?"])
    
    with tab_login:
        with st.form("login_form"):
            user = st.text_input("Nombre de Usuario o Email")
            pwd = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("INICIAR SESIÓN")
            
            if submit:
                # Validación Organizador
                if (user == ADMIN_USER or user == ADMIN_EMAIL) and pwd == ADMIN_PASS:
                    st.session_state['autenticado'] = True
                    st.session_state['rol'] = "Organizador"
                    st.rerun()
                # Validación genérica para alumnos/clubs (puedes ampliar esto)
                elif user != "" and pwd == "fox2026": 
                    st.session_state['autenticado'] = True
                    st.session_state['rol'] = "Usuario"
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

    with tab_recover:
        st.write("Introduce tu email para recuperar el acceso.")
        email_recover = st.text_input("Correo electrónico registrado")
        if st.button("RECUPERAR"):
            if email_recover == ADMIN_EMAIL:
                st.success(f"Se ha enviado un código de recuperación a {ADMIN_EMAIL} (Simulación)")
            else:
                st.error("Este correo no está registrado en la base de datos de FOX.")

# --- CONTENIDO DE LA APP (SOLO SI ESTÁ AUTENTICADO) ---
else:
    # Barra lateral para cerrar sesión
    with st.sidebar:
        st.image("fox-letras-naranja.PNG", width=150)
        st.write(f"Conectado como: **{st.session_state['rol']}**")
        if st.button("Cerrar Sesión"):
            st.session_state['autenticado'] = False
            st.rerun()

    # Título principal
    st.image("fox-letras-naranja.PNG", width=300)
    st.markdown(f"<h1 style='text-align: center; color: #FF6B00;'>PANEL {st.session_state['rol'].upper()}</h1>", unsafe_allow_html=True)

    # Conexión a GSheets
    conn = st.connection("gsheets", type=GSheetsConnection)

    # VISTA ORGANIZADOR
    if st.session_state['rol'] == "Organizador":
        t1, t2, t3, t4 = st.tabs(["📊 Inscritos", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])
        
        with t1:
            st.subheader("Gestión de Competidores")
            df = conn.read()
            # El organizador puede editar todo
            df_editado = st.data_editor(df, num_rows="dynamic")
            if st.button("GUARDAR CAMBIOS EN EXCEL"):
                conn.update(data=df_editado)
                st.success("¡Base de datos actualizada!")
        
        with t2:
            st.subheader("Creador de Cruces")
            publicar = st.checkbox("Publicar cruces para alumnos y clubs")
            # Aquí pondrías la lógica para crear los combates
            st.info("Configura aquí los emparejamientos.")

    # VISTA USUARIO (ALUMNOS/CLUBS)
    else:
        t1, t2, t3, t4 = st.tabs(["📝 Inscribirse", "⚔️ Ver Cruces", "🏆 Resultados", "📸 Fotos"])
        
        with t1:
            with st.form("registro"):
                st.subheader("Formulario de Inscripción")
                nombre = st.text_input("Nombre Completo")
                c1, c2 = st.columns(2)
                with c1:
                    edad = st.number_input("Edad", 4, 80)
                    cint = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
                with c2:
                    peso = st.text_input("Peso")
                    mod = st.radio("Modalidad", ["BJJ (Gi)", "NO-GI"])
                aca = st.text_input("Academia")
                
                if st.form_submit_button("ENVIAR REGISTRO"):
                    df = conn.read()
                    nuevo = pd.DataFrame([{"Nombre": nombre, "Edad": edad, "Cinturón": cint, "Peso": peso, "Academia": aca, "BJJ / NO-GI": mod}])
                    conn.update(data=pd.concat([df, nuevo], ignore_index=True))
                    st.balloons()
                    st.success("¡Registro completado!")

        with t2:
            st.info("Los cruces aparecerán aquí cuando el Organizador los autorice.")
