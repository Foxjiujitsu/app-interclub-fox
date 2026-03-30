import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="FOX JIU-JITSU ADMIN", layout="wide")

# Limpieza de caché forzada
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
    
    # Intentar conectar con triple red de seguridad
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        if df is None or df.empty:
            # Si el excel está vacío, creamos la estructura base
            df = pd.DataFrame(columns=["Nombre", "Cinturón", "Peso", "Edad", "BJJ / NO-GI", "Club"])
    except Exception as e:
        # Si falla la lectura, creamos una tabla vacía para no bloquear la app
        df = pd.DataFrame(columns=["Nombre", "Cinturón", "Peso", "Edad", "BJJ / NO-GI", "Club"])
        st.warning("⚠️ Nota: Conectado, pero el Excel parece estar vacío o sin formato.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 Inscritos", "➕ Registro Manual", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])

    with tab1:
        st.subheader("Lista de Competidores")
        # El editor de datos permitirá añadir filas si está vacío
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 GUARDAR CAMBIOS"):
            try:
                conn.update(data=edited_df)
                st.success("¡Datos sincronizados con Google Sheets!")
                st.rerun()
            except Exception as ex:
                st.error(f"Error al guardar: {ex}")

    with tab2:
        st.subheader("Registro Manual")
        with st.form("manual"):
            n = st.text_input("Nombre")
            cin = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
            pe = st.number_input("Peso (kg)", 10, 150, 70)
            ed = st.number_input("Edad", 4, 80, 25)
            est = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            clu = st.text_input("Club")
            if st.form_submit_button("AÑADIR LUCHADOR"):
                if n and clu:
                    new_row = pd.DataFrame([{"Nombre":n,"Cinturón":cin,"Peso":pe,"Edad":ed,"BJJ / NO-GI":est,"Club":clu}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("¡Luchador guardado!")
                    st.rerun()
                else:
                    st.error("Faltan datos obligatorios.")
