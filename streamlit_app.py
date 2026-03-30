import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="FOX JIU-JITSU ADMIN", layout="wide")

# Limpieza de caché
if st.sidebar.button("🔄 Reiniciar Conexión"):
    st.cache_data.clear()
    st.rerun()

if 'page' not in st.session_state: st.session_state.page = 'login'

if st.session_state.page == 'login':
    _, col, _ = st.columns([1,2,1])
    with col:
        st.image("fox-letras-naranja.PNG")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER AL PANEL"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.page = 'panel'
                st.rerun()

elif st.session_state.page == 'panel':
    st.title("🦊 PANEL DE GESTIÓN")
    
    # CONEXIÓN REFORZADA
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Leemos los datos directamente
        df = conn.read(ttl=0)
        if df is None or df.empty:
            df = pd.DataFrame(columns=["Nombre", "Cinturón", "Peso", "Edad", "BJJ / NO-GI", "Club"])
    except Exception as e:
        df = pd.DataFrame(columns=["Nombre", "Cinturón", "Peso", "Edad", "BJJ / NO-GI", "Club"])
        st.warning("Conectado. Esperando datos del Excel...")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 Inscritos", "➕ Registro Manual", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])

    with tab1:
        st.subheader("Lista de Competidores")
        # Cambiamos st.data_editor por un método que no bloquee la escritura inicial
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="editor_tabla")
        
        if st.button("💾 GUARDAR CAMBIOS EN LA TABLA"):
            conn.update(data=edited_df)
            st.success("¡Cambios guardados en Google Sheets!")
            st.rerun()

    with tab2:
        st.subheader("Registro Manual")
        with st.form("manual_form", clear_on_submit=True):
            n = st.text_input("Nombre")
            cin = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
            pe = st.number_input("Peso (kg)", 10, 150, 70)
            ed = st.number_input("Edad", 4, 80, 25)
            est = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            clu = st.text_input("Club")
            
            submit = st.form_submit_button("AÑADIR LUCHADOR")
            
            if submit:
                if n and clu:
                    # Creamos la nueva fila
                    nueva_fila = pd.DataFrame([{"Nombre":n,"Cinturón":cin,"Peso":pe,"Edad":ed,"BJJ / NO-GI":est,"Club":clu}])
                    # Combinamos y actualizamos
                    df_final = pd.concat([df, nueva_fila], ignore_index=True)
                    conn.update(data=df_final)
                    st.success(f"✅ {n} añadido correctamente.")
                    st.rerun()
                else:
                    st.error("Rellena Nombre y Club.")
