import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX JIU-JITSU", layout="wide")

DB_FILE = "competidores.csv"

def cargar_datos():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Número", "Nombre", "Cinturón", "Peso", "Edad", "Estilo", "Club", "Resultado"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "INICIO"

# --- DISEÑO COMPACTO PARA MÓVIL ---
st.markdown("""
    <style>
    /* Fondo Blanco y eliminación de espacios */
    .stApp { background-color: #FFFFFF; color: #333333; }
    .main .block-container { padding-top: 10px !important; padding-bottom: 10px !important; }
    
    /* Imagen del logo compacta */
    .logo-container { text-align: center; margin-bottom: 10px; }
    .logo-img { width: 180px; }

    /* Botones Estilo Celular Compactos */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1.5px solid #666666 !important;
        border-radius: 20px !important;
        height: 42px !important; /* Altura reducida para que quepan todos */
        font-weight: bold !important;
        font-size: 13px !important; /* Texto más pequeño */
        text-transform: uppercase;
        width: 100%;
        margin-bottom: 2px !important;
        padding: 0px !important;
    }
    
    div.stButton > button:hover {
        border-color: #ff6b00 !important;
        color: #ff6b00 !important;
    }

    /* Títulos de secciones */
    .section-title {
        color: #ff6b00;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA CON TU LOGO DE GITHUB ---
st.markdown(f"""
    <div class="logo-container">
        <img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" class="logo-img">
        <p style="font-weight: bold; color: #333; font-size: 12px; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px;">
            Sistema de Competición
        </p>
    </div>
    """, unsafe_allow_html=True)

df = st.session_state.df

# --- MENÚ DE BOTONES (Uno debajo de otro) ---
if st.session_state.active_tab == "INICIO":
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        if st.button("📝 REGISTRO DE COMPETIDORES"): st.session_state.active_tab = "REGISTRO"
        if st.button("👶 COMPETIDORES INFANTILES"): st.session_state.active_tab = "INFANTILES"
        if st.button("🥷 COMPETIDORES ADULTOS"): st.session_state.active_tab = "ADULTOS"
        if st.button("🔗 EMPAREJAMIENTOS INFANTILES"): st.session_state.active_tab = "EMP_INF"
        if st.button("⛓️ EMPAREJAMIENTOS ADULTOS"): st.session_state.active_tab = "EMP_ADU"
        if st.button("🏆 RESULTADOS INFANTILES"): st.session_state.active_tab = "RES_INF"
        if st.button("🥇 RESULTADOS ADULTOS"): st.session_state.active_tab = "RES_ADU"

# --- LÓGICA DE SECCIONES ---
else:
    # Botón flotante para volver arriba
    if st.button("⬅️ VOLVER AL MENÚ PRINCIPAL"):
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
        st.dataframe(filt[["Número", "Nombre", "Cinturón", "Peso", "Club"]], use_container_width=True)

    elif st.session_state.active_tab in ["EMP_INF", "EMP_ADU", "RES_INF", "RES_ADU"]:
        st.markdown("<div class='section-title'>GESTIÓN DE DATOS</div>", unsafe_allow_html=True)
        ed_df = st.data_editor(df, use_container_width=True)
        if st.button("💾 GUARDAR CAMBIOS"):
            st.session_state.df = ed_df
            guardar_datos(ed_df)
            st.success("Guardado")
