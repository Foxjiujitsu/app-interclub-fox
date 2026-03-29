import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración FOX
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊")

# Estilo visual Rojo, Negro y Blanco
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stButton>button {
        background-color: #E41E2D;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    h1, h2, h3 { color: #000000; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦊 INTERCLUB FOX")

tab1, tab2, tab3 = st.tabs(["📝 Inscripción", "⚔️ Cruces", "🏆 Resultados"])

with tab1:
    st.header("Formulario de Registro")
    # Conexión a tu Google Sheet
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    with st.form("registro"):
        nombre = st.text_input("Nombre Completo")
        col1, col2 = st.columns(2)
        with col1:
            edad = st.number_input("Edad", 4, 80)
            cinturon = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
        with col2:
            peso = st.text_input("Peso (kg)")
            estilo = st.radio("Estilo de lucha", ["BJJ", "NO-GI"])
        
        academia = st.text_input("Academia")
        submit = st.form_submit_button("¡REGISTRARME!")

        if submit:
            if nombre and academia:
                # Leer datos y añadir nuevo
                df = conn.read()
                nuevo = pd.DataFrame([{"Nombre": nombre, "Edad": edad, "Cinturón": cinturon, "Peso": peso, "Academia": academia, "BJJ / NO-GI": estilo}])
                actualizado = pd.concat([df, nuevo], ignore_index=True)
                conn.update(data=actualizado)
                st.success("¡Registro completado! Oss.")
                st.balloons()
            else:
                st.error("Por favor rellena nombre y academia.")

with tab2:
    st.info("Los cruces aparecerán aquí una vez cierren las inscripciones.")

with tab3:
    st.write("Aquí subiremos las fotos y los podios.")
