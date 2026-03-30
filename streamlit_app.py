import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN BÁSICA ---
st.set_page_config(page_title="FOX INTERCLUB ADMIN", layout="wide")

# Archivo donde se guardan los datos (interno de la app)
DB_FILE = "competidores.csv"

def cargar_datos():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "Nombre", "Cinturón", "Peso", "Edad", "Estilo", "Club", "Resultado"])

def guardar_datos(df):
    df.to_csv(DB_FILE, index=False)

# Inicializar datos
if 'df' not in st.session_state:
    st.session_state.df = cargar_datos()

# --- INTERFAZ ---
st.title("🦊 FOX INTERCLUB - ORGANIZADOR")

menu = ["➕ Registro", "👶 Infantiles (hasta 12)", "🥷 Adultos (13+)", "⚔️ Emparejamientos", "🏆 Resultados"]
choice = st.sidebar.radio("MENÚ", menu)

# 1. REGISTRO
if choice == "➕ Registro":
    st.header("Registrar Competidor")
    with st.form("reg"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo")
            cinto = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            peso = st.number_input("Peso (kg)", 10.0, 150.0, 70.0)
        with col2:
            edad = st.number_input("Edad", 4, 80, 25)
            estilo = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            club = st.text_input("Academia / Club")
        
        if st.form_submit_button("AÑADIR A LA LISTA"):
            if nombre and club:
                nuevo_id = len(st.session_state.df) + 1
                nueva_fila = pd.DataFrame([{"ID": nuevo_id, "Nombre": nombre, "Cinturón": cinto, "Peso": peso, "Edad": edad, "Estilo": estilo, "Club": club, "Resultado": "Pendiente"}])
                st.session_state.df = pd.concat([st.session_state.df, nueva_fila], ignore_index=True)
                guardar_datos(st.session_state.df)
                st.success(f"Registrado con ID: {nuevo_id}")
            else:
                st.error("Falta nombre o club")

# 2. INFANTILES
elif choice == "👶 Infantiles (hasta 12)":
    inf = st.session_state.df[st.session_state.df['Edad'] <= 12].sort_values(by="Cinturón")
    st.header(f"Infantiles: {len(inf)} participantes")
    st.table(inf[["ID", "Nombre", "Cinturón", "Peso", "Edad", "Club"]])

# 3. ADULTOS
elif choice == "🥷 Adultos (13+)":
    adu = st.session_state.df[st.session_state.df['Edad'] > 12].sort_values(by="Cinturón")
    st.header(f"Adultos: {len(adu)} participantes")
    st.table(adu[["ID", "Nombre", "Cinturón", "Peso", "Edad", "Club"]])

# 4. EMPAREJAMIENTOS (Luchas Casadas)
elif choice == "⚔️ Emparejamientos":
    st.header("Generar Luchas Casadas")
    st.info("Se emparejan por Peso, Cinto y Edad, evitando el mismo Club.")
    
    # Editor manual de luchas
    if 'luchas' not in st.session_state:
        st.session_state.luchas = pd.DataFrame(columns=["Luchador A", "Luchador B", "Categoría"])
    
    luchas_edit = st.data_editor(st.session_state.luchas, num_rows="dynamic", use_container_width=True)
    if st.button("Guardar Emparejamientos"):
        st.session_state.luchas = luchas_edit
        st.success("Luchas guardadas")

# 5. RESULTADOS
elif choice == "🏆 Resultados":
    st.header("Resultados Finales")
    res_df = st.data_editor(st.session_state.df, use_container_width=True)
    if st.button("Actualizar Podio"):
        st.session_state.df = res_df
        guardar_datos(st.session_state.df)
        st.success("Resultados actualizados")
