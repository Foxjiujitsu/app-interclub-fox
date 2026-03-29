import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración FOX
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO NEGRO Y NARANJA ---
st.markdown("""
    <style>
    /* Fondo principal en negro */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Estilo para los títulos y textos */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* Botón "¡REGISTRARME!" en Naranja */
    .stButton>button {
        background-color: #FF6B00; /* Naranja FOX */
        color: white;
        border-radius: 10px;
        border: none;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        font-size: 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #CC5500;
        border: 1px solid white;
    }

    /* Pestañas (Tabs) */
    button[data-baseweb="tab"] {
        color: #888888 !important;
    }
    button[aria-selected="true"] {
        color: #FF6B00 !important;
        border-bottom-color: #FF6B00 !important;
    }

    /* Estilo de los cuadros de entrada (Inputs) */
    input, select, textarea {
        background-color: #1A1A1A !important;
        color: white !important;
        border: 1px solid #333333 !important;
    }

    /* El contenedor del formulario */
    [data-testid="stForm"] {
        border: 1px solid #FF6B00;
        border-radius: 15px;
        background-color: #0A0A0A;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
# Ajustamos logos para que se vean bien sobre fondo negro
col1, col2 = st.columns([1, 2])
with col1:
    st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=120)
with col2:
    st.image("fox-letras-naranja.PNG", width=220)

st.markdown("<h1 style='text-align: center; color: #FF6B00;'>INTERCLUB FOX</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Registro Oficial de Competidores</p>", unsafe_allow_html=True)

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["📝 Inscripción", "⚔️ Cruces", "🏆 Resultados"])

with tab1:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    with st.form("registro_fox", clear_on_submit=True):
        st.markdown("<h3 style='color: #FF6B00;'>Datos del Guerrero</h3>", unsafe_allow_html=True)
        nombre = st.text_input("Nombre Completo")
        
        c1, c2 = st.columns(2)
        with c1:
            edad = st.number_input("Edad", 4, 80, step=1)
            cinturon = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
        with c2:
            peso = st.text_input("Peso (ej. -76kg o Leve)")
            estilo = st.radio("Modalidad", ["BJJ (Gi)", "NO-GI"])
            
        academia = st.text_input("Academia / Equipo")
        
        # El botón de acción
        enviar = st.form_submit_button("¡REGISTRARME!")

        if enviar:
            if nombre and academia:
                try:
                    df = conn.read()
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
                    st.success(f"¡Oss {nombre}! Tu inscripción se ha guardado correctamente.")
                    st.balloons()
                except Exception as e:
                    st.error("Error al conectar con el Excel. Revisa los permisos.")
            else:
                st.warning("Completa nombre y academia para continuar.")

with tab2:
    st.markdown("<h2 style='color: #FF6B00;'>⚔️ Próximos Combates</h2>", unsafe_allow_html=True)
    st.write("Los emparejamientos se publicarán aquí cuando se cierren las inscripciones.")

with tab3:
    st.markdown("<h2 style='color: #FF6B00;'>🏆 Resultados Finales</h2>", unsafe_allow_html=True)
    st.write("Podios y fotos disponibles al terminar el interclub.")
