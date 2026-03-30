import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX JIU-JITSU", layout="wide")

DB_FILE = "competidores.csv"

def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["Número", "Nombre", "Cinturón", "Peso", "Edad", "Estilo", "Club"])
    return pd.DataFrame(columns=["Número", "Nombre", "Cinturón", "Peso", "Edad", "Estilo", "Club"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "INICIO"

# --- DISEÑO MÓVIL CENTRADO TOTAL ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #333333; }
    .main .block-container {
        max-width: 500px; 
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px !important;
    }
    .logo-container { text-align: center; margin-bottom: 20px; width: 100%; }
    .logo-img { width: 200px; }
    .element-container, .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    div.stButton > button {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1.5px solid #666666 !important;
        border-radius: 25px !important;
        width: 280px !important; 
        height: 46px !important;
        font-weight: bold !important;
        font-size: 13px !important;
        text-transform: uppercase;
        margin-bottom: 4px !important;
    }
    div.stButton > button:hover {
        border-color: #ff6b00 !important;
        color: #ff6b00 !important;
    }
    .section-title {
        color: #ff6b00;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div class="logo-container">
        <img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" class="logo-img">
        <p style="font-weight: bold; color: #333; font-size: 12px; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px;">
            Sistema de Competición
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- MENÚ DE BOTONES ---
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
    df_actual = st.session_state.df

    if st.session_state.active_tab == "REGISTRO":
        st.markdown("<div class='section-title'>NUEVO REGISTRO</div>", unsafe_allow_html=True)
        with st.form("form_reg", clear_on_submit=True):
            nom = st.text_input("Nombre y Apellidos")
            cin = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            pes = st.number_input("Peso (kg)", 5.0, 150.0, 70.0)
            eda = st.number_input("Edad", 4, 90, 20)
            est = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            clu = st.text_input("Academia / Club")
            if st.form_submit_button("GUARDAR REGISTRO"):
                if nom and clu:
                    num = len(df_actual) + 1
                    nueva = pd.DataFrame([{"Número": num, "Nombre": nom, "Cinturón": cin, "Peso": pes, "Edad": eda, "Estilo": est, "Club": clu}])
                    st.session_state.df = pd.concat([df_actual, nueva], ignore_index=True)
                    guardar_datos(st.session_state.df)
                    st.success(f"¡Registrado! Nº {num}")
                else:
                    st.error("Rellena Nombre y Academia")

    elif st.session_state.active_tab in ["INFANTILES", "ADULTOS"]:
        es_inf = st.session_state.active_tab == "INFANTILES"
        # Dividimos el dataframe para mostrar solo la categoría pero manteniendo referencia al original
        if es_inf:
            st.markdown("<div class='section-title'>EDITAR INFANTILES (≤ 12 años)</div>", unsafe_allow_html=True)
            subset = df_actual[df_actual['Edad'] <= 12]
        else:
            st.markdown("<div class='section-title'>EDITAR ADULTOS (> 12 años)</div>", unsafe_allow_html=True)
            subset = df_actual[df_actual['Edad'] > 12]

        # Editor de datos profesional
        # Permite borrar filas seleccionándolas y pulsando 'Suprimir'
        df_editado_subset = st.data_editor(
            subset, 
            use_container_width=True, 
            hide_index=True, 
            num_rows="dynamic" # Esto permite borrar y añadir filas
        )

        if st.button("💾 GUARDAR CAMBIOS EN ESTA LISTA"):
            # Recomponemos el dataframe: quitamos los viejos de esta categoría y ponemos los editados
            if es_inf:
                otros = df_actual[df_actual['Edad'] > 12]
            else:
                otros = df_actual[df_actual['Edad'] <= 12]
            
            st.session_state.df = pd.concat([otros, df_editado_subset], ignore_index=True)
            guardar_datos(st.session_state.df)
            st.success("¡Lista actualizada!")
            st.rerun()

    elif st.session_state.active_tab in ["EMP_INF", "EMP_ADU", "RES_INF", "RES_ADU"]:
        st.markdown("<div class='section-title'>GESTIÓN DE DATOS GENERAL</div>", unsafe_allow_html=True)
        ed_df = st.data_editor(df_actual, use_container_width=True, hide_index=True, num_rows="dynamic")
        if st.button("💾 GUARDAR CAMBIOS GENERALES"):
            st.session_state.df = ed_df
            guardar_datos(ed_df)
            st.success("Cambios guardados")
