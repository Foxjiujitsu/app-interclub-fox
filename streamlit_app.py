import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="FOX JIU-JITSU ADMIN", layout="wide")

if 'page' not in st.session_state: st.session_state.page = 'login'

# --- LOGIN ---
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

# --- PANEL DE GESTIÓN ---
elif st.session_state.page == 'panel':
    st.title("🦊 PANEL DE GESTIÓN")
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lectura de datos
    try:
        df = conn.read(ttl=0)
    except:
        df = pd.DataFrame(columns=["Nombre", "Cinturón", "Peso", "Edad", "BJJ / NO-GI", "Club"])

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 Inscritos", "➕ Registro Manual", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])

    with tab1:
        st.subheader("Lista de Competidores")
        if not df.empty:
            # Editor simplificado
            edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("💾 GUARDAR CAMBIOS"):
                conn.update(data=edited)
                st.success("¡Base de datos actualizada!")
                st.rerun()
        else:
            st.info("No hay inscritos. Registra a alguien en la siguiente pestaña.")

    with tab2:
        st.subheader("Registro Manual")
        with st.form("reg_manual", clear_on_submit=True):
            n = st.text_input("Nombre")
            c = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
            pe = st.number_input("Peso (kg)", 10, 150, 70)
            ed = st.number_input("Edad", 4, 80, 25)
            est = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            cl = st.text_input("Club")
            
            if st.form_submit_button("AÑADIR LUCHADOR"):
                if n and cl:
                    nueva_fila = pd.DataFrame([{"Nombre":n,"Cinturón":c,"Peso":pe,"Edad":ed,"BJJ / NO-GI":est,"Club":cl}])
                    # Si df está vacío, usamos solo la nueva fila
                    df_final = pd.concat([df, nueva_fila], ignore_index=True) if not df.empty else nueva_fila
                    conn.update(data=df_final)
                    st.success(f"✅ {n} guardado.")
                    st.rerun()
                else:
                    st.error("Rellena Nombre y Club")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.page = 'login'
        st.rerun()
