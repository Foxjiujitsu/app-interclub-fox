import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="INTERCLUB FOX - SISTEMA", page_icon="🦊", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #121212; border-right: 1px solid #FF6B00; }
    .stButton > button { 
        background-color: #FF6B00 !important; color: #000000 !important; 
        font-weight: bold; width: 100%; border-radius: 10px;
    }
    .stButton > button:hover { background-color: #000000 !important; color: #FF6B00 !important; border: 1px solid #FF6B00; }
    [data-testid="stForm"] { border: 2px solid #FF6B00; background-color: #0A0A0A; border-radius: 15px; }
    .stTextInput input, .stNumberInput input { background-color: #1A1A1A !important; color: white !important; border: 1px solid #FF6B00 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A DATOS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR: SELECTOR DE ROL ---
with st.sidebar:
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=100)
    st.title("ACCESO FOX")
    rol = st.selectbox("Entrar como:", ["Competidor", "Club", "Organizador"])
    
    password = ""
    if rol == "Organizador":
        password = st.text_input("Contraseña Organizador", type="password")
    elif rol == "Club":
        password = st.text_input("Contraseña Club", type="password")
        nombre_club = st.text_input("Nombre de tu Academia")

# --- LÓGICA DE VISUALIZACIÓN ---

# 1. PERFIL ORGANIZADOR
if rol == "Organizador" and password == "adminfox": # <--- Cambia 'adminfox' por tu clave
    st.header("⚡ Panel de Control - Organizador")
    
    tab_admin1, tab_admin2, tab_admin3 = st.tabs(["👥 Gestión Inscritos", "⚔️ Cruces y Resultados", "📸 Fotos"])
    
    df = conn.read()
    
    with tab_admin1:
        st.subheader("Todos los Competidores")
        # El organizador puede editar la tabla directamente
        df_editado = st.data_editor(df, num_rows="dynamic")
        if st.button("Guardar Cambios en Inscritos"):
            conn.update(data=df_editado)
            st.success("Base de datos actualizada.")

    with tab_admin2:
        st.subheader("Control de Cruces")
        publicar = st.toggle("🚀 PUBLICAR CRUCES (Hacer visibles para todos)")
        st.session_state['cruces_publicados'] = publicar
        
        st.info("Aquí puedes definir los ganadores y editar los enfrentamientos.")
        # Simulación de tabla de resultados/cruces
        df_resultados = st.data_editor(df[['Nombre', 'Cinturón', 'Peso', 'Academia']]) 
        if st.button("Actualizar Resultados"):
            st.success("Resultados guardados.")

    with tab_admin3:
        link_fotos = st.text_input("Enlace de la carpeta de fotos (Google Drive/Photos)")
        if st.button("Actualizar Galería"):
            st.success("Enlace de fotos publicado.")

# 2. PERFIL CLUB
elif rol == "Club" and password == "clubfox": # <--- Cambia 'clubfox' por la clave para clubs
    st.header(f"🏫 Gestión de Club: {nombre_club}")
    
    tab_club1, tab_club2, tab_club3 = st.tabs(["📝 Mis Alumnos", "⚔️ Cruces", "📸 Fotos"])
    
    df = conn.read()
    mis_alumnos = df[df['Academia'].str.contains(nombre_club, case=False, na=False)]
    
    with tab_club1:
        st.subheader("Editar Inscripciones de mi Club")
        df_club_edit = st.data_editor(mis_alumnos)
        if st.button("Guardar Cambios del Club"):
            # Lógica para actualizar solo sus filas (necesitaría ID, pero simplificamos)
            st.warning("Función de guardado parcial en desarrollo. Contacte con admin.")

    with tab_club2:
        if st.session_state.get('cruces_publicados', False):
            st.write("Cruces publicados por la organización.")
            st.dataframe(mis_alumnos[['Nombre', 'Peso', 'Cinturón']])
        else:
            st.warning("Los cruces aún no han sido autorizados por el Organizador.")

# 3. PERFIL COMPETIDOR (VISTA PÚBLICA)
else:
    if rol != "Competidor":
        st.error("Contraseña incorrecta")
    
    # Cabecera centrada
    st.image("fox-letras-naranja.PNG", width=300)
    st.markdown("<h1 style='text-align: center; color: #FF6B00;'>INTERCLUB</h1>", unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.tabs(["📝 Inscripción", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])
    
    with t1:
        with st.form("registro"):
            nombre = st.text_input("Nombre Completo")
            c1, c2 = st.columns(2)
            with c1:
                edad = st.number_input("Edad", 4, 80)
                cint = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
            with c2:
                peso = st.text_input("Peso")
                mod = st.radio("Modalidad", ["BJJ (Gi)", "NO-GI"])
            aca = st.text_input("Academia")
            if st.form_submit_button("¡REGISTRARME!"):
                df = conn.read()
                nuevo = pd.DataFrame([{"Nombre": nombre, "Edad": edad, "Cinturón": cint, "Peso": peso, "Academia": aca, "BJJ / NO-GI": mod}])
                conn.update(data=pd.concat([df, nuevo], ignore_index=True))
                st.balloons()

    with t2:
        if st.session_state.get('cruces_publicados', False):
            st.success("¡Cruces Disponibles!")
            # Aquí se mostraría la tabla de cruces
        else:
            st.info("⚔️ El organizador está preparando los cruces. Se publicarán en breve.")

    with t3:
        st.write("Los resultados aparecerán aquí tras los combates.")

    with t4:
        st.write("📸 Las fotos se podrán descargar aquí al finalizar el evento.")
