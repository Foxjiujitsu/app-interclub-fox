import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX INTERCLUB ADMIN", layout="wide")

DB_FILE = "competidores.csv"

def cargar_datos():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Nombre", "Cinturón", "Peso", "Edad", "Estilo", "Club", "Resultado", "Número"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "REGISTRO"

# --- DISEÑO ESTILO "APP MÓVIL" ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1c1e; color: white; }
    
    /* Botones Estilo Celular */
    .stButton > button {
        background-color: #2d3035 !important;
        color: white !important;
        border: 2px solid #ff6b00 !important;
        border-radius: 50px !important;
        height: 60px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        margin-bottom: 10px !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #ff6b00 !important;
        color: black !important;
    }
    
    /* Tarjetas de luchadores */
    .card {
        background-color: #2d3035;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #ff6b00;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Banner Principal
st.markdown("<h1 style='text-align: center; color: #ff6b00;'>FOX JIU-JITSU</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top: -20px;'>SISTEMA DE COMPETICIÓN</h3>", unsafe_allow_html=True)

# --- MENÚ DE BOTONES ---
col_menu = st.columns(1) # Un solo botón por fila para que parezca el móvil
with col_menu[0]:
    if st.button("📝 REGISTRO DE COMPETIDORES"): st.session_state.active_tab = "REGISTRO"
    if st.button("👶 COMPETIDORES INFANTILES"): st.session_state.active_tab = "INFANTILES"
    if st.button("🥷 COMPETIDORES ADULTOS"): st.session_state.active_tab = "ADULTOS"
    if st.button("⚔️ EMPAREJAMIENTOS"): st.session_state.active_tab = "LUCES"
    if st.button("🏆 RESULTADOS"): st.session_state.active_tab = "RESULTADOS"

st.markdown("---")

df = st.session_state.df

# --- SECCIONES ---
if st.session_state.active_tab == "REGISTRO":
    st.subheader("Nuevo Registro")
    with st.form("reg_form", clear_on_submit=True):
        nom = st.text_input("Nombre")
        col1, col2 = st.columns(2)
        with col1:
            cin = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            pes = st.number_input("Peso (kg)", 10.0, 150.0, 70.0)
        with col2:
            eda = st.number_input("Edad", 4, 80, 25)
            clu = st.text_input("Club/Academia")
        est = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
        
        if st.form_submit_button("GUARDAR REGISTRO"):
            if nom and clu:
                num = len(df) + 1
                nueva = pd.DataFrame([{"Número": num, "Nombre": nom, "Cinturón": cin, "Peso": pes, "Edad": eda, "Estilo": est, "Club": clu, "Resultado": "Pendiente"}])
                st.session_state.df = pd.concat([st.session_state.df, nueva], ignore_index=True)
                guardar_datos(st.session_state.df)
                st.success(f"¡Registrado con éxito! Nº {num}")
                st.rerun()

elif st.session_state.active_tab == "INFANTILES":
    inf = df[df['Edad'] <= 12]
    st.subheader(f"Infantiles: {len(inf)} Inscritos")
    for _, r in inf.iterrows():
        st.markdown(f"<div class='card'><b>Nº {r['Número']}</b> - {r['Nombre']} ({r['Cinturón']})<br><small>{r['Peso']}kg - {r['Club']}</small></div>", unsafe_allow_html=True)

elif st.session_state.active_tab == "ADULTOS":
    adu = df[df['Edad'] > 12]
    st.subheader(f"Adultos: {len(adu)} Inscritos")
    for _, r in adu.iterrows():
        st.markdown(f"<div class='card'><b>Nº {r['Número']}</b> - {r['Nombre']} ({r['Cinturón']})<br><small>{r['Peso']}kg - {r['Club']}</small></div>", unsafe_allow_html=True)

elif st.session_state.active_tab == "LUCES":
    st.subheader("Gestión de Luchas")
    st.info("Aquí puedes anotar los emparejamientos manualmente.")
    ed_luchas = st.data_editor(df[['Número', 'Nombre', 'Cinturón', 'Peso', 'Club']], use_container_width=True)

elif st.session_state.active_tab == "RESULTADOS":
    st.subheader("Resultados del Evento")
    res = st.data_editor(df, use_container_width=True)
    if st.button("Actualizar Podio"):
        st.session_state.df = res
        guardar_datos(res)
        st.success("Resultados guardados")
