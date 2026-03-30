import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX JIU-JITSU", layout="wide")

DB_FILE = "competidores.csv"

def cargar_datos():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Número", "Nombre", "Cinturón", "Peso", "Edad", "Club"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "INICIO"

# --- DISEÑO MÓVIL CENTRADO TOTAL ---
st.markdown("""
    <style>
    /* Fondo Blanco y reseteo de márgenes */
    .stApp { background-color: #FFFFFF; color: #333333; }
    
    /* Forzar centrado de la columna principal */
    .main .block-container {
        max-width: 400px; /* Ancho típico de un móvil */
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding-top: 30px !important;
    }

    /* Logo centrado */
    .logo-container { 
        text-align: center; 
        margin-bottom: 25px; 
        width: 100%; 
    }
    .logo-img { width: 220px; }

    /* Contenedor de botones centrado */
    .element-container, .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* Botones Simétricos y sin Iconos */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1.5px solid #666666 !important;
        border-radius: 25px !important;
        
        /* MEDIDAS FIJAS */
        width: 280px !important; 
        height: 48px !important;
        
        font-weight: bold !important;
        font-size: 14px !important;
        text-transform: uppercase;
        margin-bottom: 5px !important;
        display: block !important;
        transition: all 0.2s;
    }
    
    div.stButton > button:hover {
        border-color: #ff6b00 !important;
        color: #ff6b00 !important;
        background-color: #fffaf7 !important;
    }

    /* Títulos de secciones */
    .section-title {
        color: #ff6b00;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div class="logo-container">
        <img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" class="logo-img">
        <p style="font-weight: bold; color: #333; font-size: 14px; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px;">
            Sistema de Competición
        </p>
    </div>
    """, unsafe_allow_html=True)

df = st.session_state.df

# --- MENÚ DE BOTONES (SIN ICONOS Y CENTRADOS) ---
if st.session_state.active_tab == "INICIO":
    if st.button("REGISTRO DE COMPETIDORES"): st.session_state.active_tab = "REGISTRO"
    if st.button("COMPETIDORES INFANTILES"): st.session_state.active_tab = "INFANTILES"
    if st.button("COMPETIDORES ADULTOS"): st.session_state.active_tab = "ADULTOS"
    if st.button("EMPAREJAMIENTOS INFANTILES"): st.session_state.active_tab = "EMP_INF"
    if st.button("EMPAREJAMIENTOS ADULTOS"): st.session_state.active_tab = "EMP_ADU"
    if st.button("RESULTADOS INFANTILES"): st.session_state.active_tab = "RES_INF"
    if st.button("RESULTADOS ADULTOS"): st.session_state.active_tab = "RES_ADU"

# --- LÓGICA DE SECCIONES ---
else:
    if st.button("VOLVER AL MENÚ"):
        st.session_state.active_tab = "INICIO"
        st.rerun()
    
    st.markdown("---")

    if st.session_state.active_tab == "REGISTRO":
        st.markdown("<div class='section-title'>NUEVO REGISTRO</div>", unsafe_allow_html=True)
        with st.form("form_reg", clear_on_submit=True):
            nom = st.text_input("Nombre")
            cin = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            pes = st.number_input("Peso (kg)", 5.0, 150.0, 40.0)
            eda = st.number_input("Edad", 4, 90, 10)
            clu = st.text_input("Academia")
            if st.form_submit_button("GUARDAR"):
                num = len(df) + 1
                nueva = pd.DataFrame([{"Número": num, "Nombre": nom, "Cinturón": cin, "Peso": pes, "Edad": eda, "Club": clu}])
                st.session_state.df = pd.concat([st.session_state.df, nueva], ignore_index=True)
                guardar_datos(st.session_state.df)
                st.success("¡Registrado!")

    elif st.session_state.active_tab in ["INFANTILES", "ADULTOS"]:
        es_inf = st.session_state.active_tab == "INFANTILES"
        filt = df[df['Edad'] <= 12] if es_inf else df[df['Edad'] > 12]
        st.markdown(f"<div class='section-title'>LISTADO {'INFANTIL' if es_inf else 'ADULTO'}</div>", unsafe_allow_html=True)
        st.dataframe(filt, use_container_width=True, hide_index=True)

    elif st.session_state.active_tab in ["EMP_INF", "EMP_ADU", "RES_INF", "RES_ADU"]:
        st.markdown("<div class='section-title'>GESTIÓN DE DATOS</div>", unsafe_allow_html=True)
        ed_df = st.data_editor(df, use_container_width=True, hide_index=True)
        if st.button("GUARDAR CAMBIOS"):
            st.session_state.df = ed_df
            guardar_datos(ed_df)
            st.success("Guardado")
