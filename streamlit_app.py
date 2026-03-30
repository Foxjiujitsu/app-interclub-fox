import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="FOX JIU-JITSU ADMIN", layout="wide")

# BOTÓN PARA LIMPIAR CACHÉ (Aparecerá en el lateral si hay error)
if st.sidebar.button("🔄 Limpiar Conexión"):
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
    
    try:
        # Intentamos conectar sin usar la caché para evitar el error guardado
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0) # ttl=0 obliga a leer datos frescos cada vez
    except Exception as e:
        st.error(f"⚠️ ERROR DETECTADO: {e}")
        st.stop()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 Inscritos", "➕ Registro Manual", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])

    with tab1:
        st.subheader("Lista de Competidores")
        if not df.empty:
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("💾 GUARDAR CAMBIOS"):
                conn.update(data=edited_df)
                st.success("¡Base de datos actualizada!")
        else:
            st.warning("El Excel está vacío. Registra a alguien en la siguiente pestaña.")

    with tab2:
        st.subheader("Nuevo Registro")
        with st.form("manual"):
            n = st.text_input("Nombre")
            cin = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
            pe = st.number_input("Peso (kg)", 10, 150, 70)
            ed = st.number_input("Edad", 4, 80, 25)
            est = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            clu = st.text_input("Club")
            if st.form_submit_button("GUARDAR"):
                new_row = pd.DataFrame([{"Nombre":n,"Cinturón":cin,"Peso":pe,"Edad":ed,"BJJ / NO-GI":est,"Club":clu}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success("¡Registrado con éxito!")
                st.rerun()
