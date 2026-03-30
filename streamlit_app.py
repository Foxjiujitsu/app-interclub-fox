import streamlit as st
import pandas as pd
import os
import uuid

# --- CONFIGURACIÓN DE PÁGINA PROFESIONAL ---
st.set_page_config(page_title="FOX INTERCLUB ADMIN", layout="wide")

# Archivo de base de datos interna
DB_FILE = "competidores.csv"

def cargar_datos():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "Nombre", "Cinturón", "Peso", "Edad", "Estilo", "Club", "Resultado", "Número"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

# Inicializar datos
if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "➕ Registro"

# --- ESTILOS CSS PROFESIONALES (TEMA OSCURO/NARANJA) ---
st.markdown("""
    <style>
    /* Fondo oscuro y tipografía limpia */
    .stApp { background-color: #121212; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { color: #FF6B00 !important; font-weight: 900; }
    .stMarkdown p { color: #DDDDDD; }

    /* Botones Superiores (Menú) */
    .stButton > button { 
        background-color: #262626 !important; 
        color: #DDDDDD !important; 
        border: 2px solid #3A3A3A !important;
        border-radius: 10px; font-weight: bold; 
        width: 100%; transition: all 0.3s;
        height: 60px;
        font-size: 16px;
    }
    .stButton > button:hover { 
        border-color: #FF6B00 !important; 
        color: #FFFFFF !important; 
        background-color: #1E1E1E !important;
        box-shadow: 0px 4px 10px rgba(255, 107, 0, 0.4);
    }
    .active-tab { 
        background-color: #FF6B00 !important; 
        color: #000000 !important; 
        border-color: #FF8C00 !important;
    }

    /* Tarjetas de Competidor */
    .competidor-card {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .competidor-card:hover { transform: translateY(-5px); border-color: #555555; }
    .luchador-nombre { color: #FFFFFF; font-size: 1.2rem; font-weight: bold; }
    .luchador-info { color: #AAAAAA; font-size: 0.9rem; margin-top: 5px; }
    
    /* Contadores y Kpis */
    .metric-box {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #333333;
        text-align: center;
    }
    
    /* Formularios */
    .stForm { background-color: #1E1E1E; padding: 30px; border-radius: 12px; border: 1px solid #333; }
    .stForm div[data-baseweb="input"], .stForm div[data-baseweb="select"] {
        background-color: #121212 !important;
        border: 1px solid #333 !important;
        color: #FFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA Y LOGO ---
st.markdown("<h1 style='text-align:center;'>FOX INTERCLUB JIU-JITSU ADMIN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#AAAAAA;'>Software de Organización de Combates</p>", unsafe_allow_html=True)
st.markdown("---")

# --- MENÚ DE BOTONES SUPERIORES (5 BOTONES) ---
# Creamos 5 columnas para los 5 botones
cols_menu = st.columns(5)

with cols_menu[0]:
    if st.button("➕ Registro", key="btn_reg"): st.session_state.active_tab = "➕ Registro"
with cols_menu[1]:
    if st.button("👶 Infantiles", key="btn_inf"): st.session_state.active_tab = "👶 Infantiles"
with cols_menu[2]:
    if st.button("🥷 Adultos", key="btn_adu"): st.session_state.active_tab = "🥷 Adultos"
with cols_menu[3]:
    if st.button("⚔️ Emparejamientos", key="btn_pair"): st.session_state.active_tab = "⚔️ Emparejamientos"
with cols_menu[4]:
    if st.button("🏆 Resultados", key="btn_res"): st.session_state.active_tab = "🏆 Resultados"

# --- LÓGICA DE LAS SECCIONES ---
df = st.session_state.df

# 1. SECCIÓN: REGISTRO
if st.session_state.active_tab == "➕ Registro":
    st.header("Formulario de Inscripción")
    
    with st.form("registro_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            nombre = st.text_input("Nombre completo")
            estilo = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
        with c2:
            cinto = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            edad = st.number_input("Edad", 4, 80, 25)
        with c3:
            peso = st.number_input("Peso (kg)", 10.0, 150.0, 70.0)
            club = st.text_input("Academia / Club")
        
        # Generar número único correlativo
        numero_participante = len(df) + 1
        
        submit = st.form_submit_button("REGISTRAR LUCHADOR", use_container_width=True)
        
        if submit:
            if nombre and club:
                nuevo_id = str(uuid.uuid4())[:8] # ID corto único para control interno
                nueva_fila = pd.DataFrame([{
                    "ID": nuevo_id, "Número": numero_participante, "Nombre": nombre, 
                    "Cinturón": cinto, "Peso": peso, "Edad": edad, 
                    "Estilo": estilo, "Club": club, "Resultado": "Pendiente"
                }])
                st.session_state.df = pd.concat([st.session_state.df, nueva_fila], ignore_index=True)
                guardar_datos(st.session_state.df)
                st.success(f"Registrado con Número: {numero_participante}")
                st.rerun()
            else:
                st.error("Rellena nombre y club")

# Lógica compartida para las vistas Infantiles y Adultos
def mostrar_vista_lista(lista_df, titulo_seccion):
    st.header(f"{titulo_seccion}")
    
    # Contador superior profesional
    c1, _ = st.columns([1,3])
    with c1:
        st.markdown(f"""<div class='metric-box'>
            <h4 style='color:#FFF;'>Participantes</h4>
            <h1 style='font-size:3rem; margin:0;'>{len(lista_df)}</h1>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Grid de tarjetas
    if not lista_df.empty:
        for _, r in lista_df.iterrows():
            st.markdown(f"""
            <div class='competidor-card'>
                <div class='luchador-nombre'>Nº {r['Número']}: {r['Nombre']}</div>
                <div class='luchador-info'>
                    <b>Cinto:</b> {r['Cinturón']} | <b>Peso:</b> {r['Peso']}kg | 
                    <b>Edad:</b> {r['Edad']} | <b>Club:</b> {r['Club']} | <b>Estilo:</b> {r['Estilo']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay inscritos en esta categoría.")

# 2. SECCIÓN: INFANTILES
elif st.session_state.active_tab == "👶 Infantiles":
    # Filtrar menores de 12 (incluido) y ordenar por cinturón (luego edad)
    infantiles_df = df[df['Edad'] <= 12].sort_values(by=["Cinturón", "Edad"])
    mostrar_vista_lista(infantiles_df, "Competidores Infantiles (≤ 12 años)")

# 3. SECCIÓN: ADULTOS
elif st.session_state.active_tab == "🥷 Adultos":
    # Filtrar mayores de 13 y ordenar por cinturón (luego edad)
    adultos_df = df[df['Edad'] > 12].sort_values(by=["Cinturón", "Edad"])
    mostrar_vista_lista(adultos_df, "Competidores Adultos (≥ 13 años)")

# 4. SECCIÓN: EMPAREJAMIENTOS
elif st.session_state.active_tab == "⚔️ Emparejamientos":
    st.header("Organización de Luchas")
    
    # Inicializar el editor manual si no existe
    if 'luchas_manual' not in st.session_state:
        st.session_state.luchas_manual = pd.DataFrame(columns=["Luchador A", "Luchador B", "Categoría (Edad/Cinto)"])
    
    st.subheader("🛠️ Panel de Emparejamiento Manual")
    st.info("Escribe el nombre o número de los luchadores en las celdas para casar las luchas.")
    
    luchas_edit = st.data_editor(st.session_state.luchas_manual, num_rows="dynamic", use_container_width=True)
    
    if st.button("GUARDAR EMPAREJAMIENTOS"):
        st.session_state.luchas_manual = luchas_edit
        st.success("Luchas guardadas")

# 5. SECCIÓN: RESULTADOS
elif st.session_state.active_tab == "🏆 Resultados":
    st.header("Actualización de Títulos")
    st.subheader("Edita directamente en la tabla")
    
    # Permitir edición de la base de datos principal
    df_edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="res_table")
    
    if st.button("GUARDAR RESULTADOS"):
        st.session_state.df = df_edited
        guardar_datos(st.session_state.df)
        st.success("Base de datos actualizada")
        st.rerun()
