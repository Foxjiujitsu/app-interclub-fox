import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración FOX
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# CSS personalizado para colores Rojo, Negro y Blanco
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stButton>button {
        background-color: #E41E2D;
        color: white;
        border-radius: 10px;
        border: none;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    /* Estilo para las pestañas */
    button[data-baseweb="tab"] { color: black !important; font-weight: bold; }
    button[aria-selected="true"] { color: #E41E2D !important; border-bottom-color: #E41E2D !important; }
    </style>
    """, unsafe_allow_html=True)

# Cabecera con tus Logos
col1, col2 = st.columns([1, 2])
with col1:
    # El logo del zorro (el archivo largo de WhatsApp)
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=120)
with col2:
    # El logo de las letras FOX
    st.image("fox-letras-naranja.PNG", width=200)

st.markdown("<h2 style='text-align: center; color: black;'>REGISTRO OFICIAL INTERCLUB</h2>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Inscripción", "⚔️ Cruces", "🏆 Resultados"])

with tab1:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    with st.form("registro_fox", clear_on_submit=True):
        st.markdown("### Datos del Competidor")
        nombre = st.text_input("Nombre Completo")
        
        c1, c2 = st.columns(2)
        with c1:
            edad = st.number_input("Edad", 4, 80, step=1)
            cinturon = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
        with c2:
            peso = st.text_input("Peso (ej. -76kg)")
            estilo = st.radio("Modalidad", ["BJJ (Gi)", "NO-GI"])
            
        academia = st.text_input("Academia")
        
        enviar = st.form_submit_button("¡REGISTRARME!")

        if enviar:
            if nombre and academia:
                df = conn.read()
                # Ajustamos los nombres de las columnas para que coincidan con tu Excel
                nuevo = pd.DataFrame([{
                    "Nombre": nombre, 
                    "Edad": edad, 
                    "Cinturón": cinturon, 
                    "Peso": peso, 
                    "Academia": academia, 
                    "BJJ / NO-GI": estilo
                }])
                actualizado = pd.concat([df, nuevo], ignore_index=True)
                conn.update(data=actualizado)
                st.success(f"¡Oss {nombre}! Registro enviado a la base de datos.")
                st.balloons()
            else:
                st.error("Por favor, rellena los campos obligatorios.")

with tab2:
    st.header("⚔️ Cruces y Llaves")
    st.info("Inscripciones en proceso. Los cruces se publicarán aquí próximamente.")

with tab3:
    st.header("🏆 Podio y Fotos")
    st.write("Los resultados se subirán al finalizar el evento.")
