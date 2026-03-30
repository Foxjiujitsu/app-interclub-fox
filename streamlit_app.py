import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INTERCLUB FOX", page_icon="🦊", layout="centered")

# --- DISEÑO CORPORATIVO NEGRO Y NARANJA DEFINITIVO ---
st.markdown("""
    <style>
    /* 1. Fondo principal y textos base */
    .stApp { 
        background-color: #000000; 
        color: #FFFFFF; 
        font-family: 'Arial', sans-serif; 
    }
    h1, h2, h3, p, span, label { color: #FFFFFF !important; }

    /* 2. Cabecera Centrada Totalmente */
    .stImage > img { 
        display: block; 
        margin-left: auto; 
        margin-right: auto; 
    }
    
    /* Forzar centrado de bloques verticales */
    [data-testid="stVerticalBlock"] {
        align-items: center;
    }

    /* 3. Títulos */
    .interclub-titulo { 
        text-align: center; 
        color: #FF6B00; 
        font-size: 50px; 
        font-weight: bold; 
        margin-top: -10px; 
    }
    .registro-subtitulo { 
        text-align: center; 
        font-size: 18px; 
        color: #888888; 
        margin-bottom: 20px; 
    }

    /* 4. Pestañas (Tabs) */
    button[data-baseweb="tab"] { 
        color: #888888 !important; 
        font-weight: bold; 
    }
    button[aria-selected="true"] { 
        color: #FFFFFF !important; 
        border-bottom: 3px solid #FF6B00 !important; 
    }

    /* 5. Contenedor del Formulario */
    [data-testid="stForm"] { 
        border: 2px solid #FF6B00; 
        border-radius: 15px; 
        background-color: #0A0A0A; 
        padding: 25px; 
    }

    /* 6. Campos de Entrada (Inputs) - SIN DOBLE RECUADRO */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #FF6B00 !important;
        border-radius: 8px !important;
    }

    /* 7. Radio Button (BJJ / NO-GI) en NARANJA */
    div[data-testid="stMarkdownContainer"] p { color: white !important; }
    label[data-baseweb="radio"] div:first-child { border-color: #FF6B00 !important; }
    label[data-baseweb="radio"][aria-checked="true"] div:first-child { 
        background-color: #FF6B00 !important; 
        border-color: #FF6B00 !important; 
    }

    /* 8. Botón REGISTRARME (Naranja/Negro -> Negro/Naranja) */
    .stButton > button {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        height: 3em !important;
        width: 100% !important;
        transition: 0.3s !important;
    }
    .stButton > button:hover {
        background-color: #000000 !important;
        color: #FF6B00 !important;
        border-color: #FF6B00 !important;
    }

    /* Tarjetas informativas */
    .fox-card { 
        border: 1px solid #FF6B00; 
        border-radius: 10px; 
        background-color: #1A1A1A; 
        padding: 20px; 
        text-align: center; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.image("Imagen de WhatsApp 2024-11-27 a las 14.43.24_bca11eec.jpg", width=180)
st.image("fox-letras-naranja.PNG", width=380)

st.markdown("<div class='interclub-titulo'>INTERCLUB</div>", unsafe_allow_html=True)
st.markdown("<div class='registro-subtitulo'>Registro Oficial de Competidores</div>", unsafe_allow_html=True)

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs(["📝 Inscripción", "⚔️ Cruces", "🏆 Resultados", "📸 Fotografías"])

with tab1:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    with st.form("registro_fox", clear_on_submit=True):
        st.markdown("<h3 style='color: #FF6B00; border-bottom: 1px solid #FF6B00;'>Datos del Competidor</h3>", unsafe_allow_html=True)
        
        nombre = st.text_input("Nombre Completo")
        
        c1, c2 = st.columns(2)
        with c1:
            edad = st.number_input("Edad", 4, 80, step=1)
            cinturon = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
        with c2:
            peso = st.text_input("Peso (ej. -76kg)")
            estilo = st.radio("Modalidad", ["BJJ (Gi)", "NO-GI"])
            
        academia = st.text_input("Academia / Equipo")
        
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
                    st.success(f"¡Oss {nombre}! Registro enviado.")
                    st.balloons()
                except:
                    st.error("Error al conectar con la base de datos.")
            else:
                st.warning("Rellena los campos obligatorios.")

with tab2:
    st.markdown("<div class='fox-card'><h3 style='color:#FF6B00'>⚔️ Cruces</h3><p>Se publicarán al cierre de inscripciones.</p></div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='fox-card'><h3 style='color:#FF6B00'>🏆 Resultados</h3><p>Disponibles tras el evento.</p></div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='fox-card'><h3 style='color:#FF6B00'>📸 Fotografías</h3><p>Aquí subiremos los enlaces para descargar las fotos oficiales del Interclub.</p></div>", unsafe_allow_html=True)
