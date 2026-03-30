import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOX JIU-JITSU ACADEMY", layout="wide")

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

# --- DISEÑO "CLEAN & WHITE" ---
st.markdown("""
    <style>
    /* Fondo Blanco Total */
    .stApp { background-color: #FFFFFF; color: #333333; }
    
    /* Botones Estilo Imagen (Blanco con borde gris y texto naranja/marrón) */
    div.stButton > button {
        background-color: #fcfcfc !important;
        color: #b86b3e !important; /* Color similar al de la imagen */
        border: 2px solid #666666 !important;
        border-radius: 30px !important;
        height: 70px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        text-transform: uppercase;
        width: 100%;
        margin-bottom: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    
    div.stButton > button:hover {
        background-color: #f0f0f0 !important;
        border-color: #b86b3e !important;
    }

    /* Tarjetas de luchadores para fondo blanco */
    .card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #eeeeee;
        border-left: 5px solid #b86b3e;
        margin-bottom: 10px;
        color: #333333;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }

    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ESTILO LOGO ---
st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #b86b3e; font-family: sans-serif; font-size: 60px; margin-bottom: 0;">FOX</h1>
        <p style="letter-spacing: 5px; font-weight: bold; color: #333; margin-top: -15px;">JIU-JITSU ACADEMY</p>
        <h2 style="color: #333; font-weight: bold; margin-top: 20px; font-size: 24px;">SISTEMA DE COMPETICIÓN</h2>
    </div>
    """, unsafe_allow_html=True)

# --- MENÚ DE BOTONES (COMO EN LA IMAGEN) ---
# He usado una sola columna para que ocupen todo el ancho y parezca un móvil
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    if st.button("📝 REGISTRO DE COMPETIDORES"): st.session_state.active_tab = "REGISTRO"
    if st.button("👦 COMPETIDORES INFANTILES"): st.session_state.active_tab = "INFANTILES"
    if st.button("🥷 COMPETIDORES ADULTOS"): st.session_state.active_tab = "ADULTOS"
    if st.button("🔗 EMPAREJAMIENTOS INFANTILES"): st.session_state.active_tab = "EMP_INF"
    if st.button("⛓️ EMPAREJAMIENTOS ADULTOS"): st.session_state.active_tab = "EMP_ADU"
    if st.button("🏆 RESULTADOS INFANTILES"): st.session_state.active_tab = "RES_INF"
    if st.button("🥇 RESULTADOS ADULTOS"): st.session_state.active_tab = "RES_ADU"
    
    if st.session_state.active_tab != "INICIO":
        if st.button("⬅️ VOLVER AL MENÚ"): 
            st.session_state.active_tab = "INICIO"
            st.rerun()

st.markdown("---")

df = st.session_state.df

# --- SECCIONES ---

if st.session_state.active_tab == "REGISTRO":
    st.markdown("<h3 style='color: #b86b3e;'>NUEVO REGISTRO</h3>", unsafe_allow_html=True)
    with st.form("form_reg", clear_on_submit=True):
        nom = st.text_input("Nombre y Apellidos")
        c1, c2 = st.columns(2)
        with c1:
            cin = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            pes = st.number_input("Peso (kg)", 5.0, 150.0, 40.0)
        with c2:
            eda = st.number_input("Edad", 4, 90, 10)
            clu = st.text_input("Academia")
        est = st.selectbox("Modalidad", ["BJJ (GI)", "NO-GI"])
        
        if st.form_submit_button("CONFIRMAR REGISTRO"):
            if nom and clu:
                num = len(df) + 1
                nueva = pd.DataFrame([{"Número": num, "Nombre": nom, "Cinturón": cin, "Peso": pes, "Edad": eda, "Estilo": est, "Club": clu, "Resultado": "Pendiente"}])
                st.session_state.df = pd.concat([st.session_state.df, nueva], ignore_index=True)
                guardar_datos(st.session_state.df)
                st.success(f"Registrado correctamente: Nº {num}")

elif st.session_state.active_tab in ["INFANTILES", "ADULTOS"]:
    es_infantil = st.session_state.active_tab == "INFANTILES"
    filtro_df = df[df['Edad'] <= 12] if es_infantil else df[df['Edad'] > 12]
    
    st.markdown(f"<h3 style='color: #b86b3e;'>LISTADO {'INFANTIL' if es_infantil else 'ADULTO'}</h3>", unsafe_allow_html=True)
    st.write(f"Total registrados: {len(filtro_df)}")
    
    for _, r in filtro_df.iterrows():
        st.markdown(f"""<div class='card'>
            <b>Nº {r['Número']} - {r['Nombre']}</b><br>
            Cinto: {r['Cinturón']} | Peso: {r['Peso']}kg | Club: {r['Club']}
        </div>""", unsafe_allow_html=True)

elif st.session_state.active_tab in ["EMP_INF", "EMP_ADU"]:
    st.markdown("<h3 style='color: #b86b3e;'>GESTIÓN DE EMPAREJAMIENTOS</h3>", unsafe_allow_html=True)
    st.info("Utiliza esta tabla para casar las luchas manualmente.")
    st.data_editor(df, use_container_width=True)

elif st.session_state.active_tab in ["RES_INF", "RES_ADU"]:
    st.markdown("<h3 style='color: #b86b3e;'>PODIO Y RESULTADOS</h3>", unsafe_allow_html=True)
    edited_df = st.data_editor(df, use_container_width=True)
    if st.button("💾 GUARDAR RESULTADOS FINALES"):
        st.session_state.df = edited_df
        guardar_datos(edited_df)
        st.success("Resultados actualizados en el sistema.")
