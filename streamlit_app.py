import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOX JIU-JITSU ADMIN", layout="wide")

# Estilo visual
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    div.stButton > button { background-color: #FF6B00 !important; color: white !important; border-radius: 12px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #FF6B00 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

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
    
    # CONEXIÓN REAL (SIN DATOS DE EJEMPLO)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
    except Exception as e:
        st.error(f"⚠️ ERROR DE CONEXIÓN: {e}")
        st.info("Revisa que los Secrets estén bien pegados y el Excel compartido con el email del robot.")
        st.stop()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 Inscritos", "➕ Registro Manual", "⚔️ Cruces", "🏆 Resultados", "📸 Fotos"])

    with tab1:
        st.subheader("Lista de Competidores")
        # Permite editar y borrar directamente en la tabla
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 GUARDAR CAMBIOS / BORRADOS"):
            conn.update(data=edited_df)
            st.success("¡Base de datos actualizada!")
            st.rerun()

    with tab2:
        st.subheader("Inscribir nuevo luchador")
        with st.form("manual"):
            n = st.text_input("Nombre")
            cin = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
            pe = st.number_input("Peso (kg)", 10, 150, 70)
            ed = st.number_input("Edad", 4, 80, 25)
            est = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            clu = st.text_input("Club")
            
            if st.form_submit_button("GUARDAR EN GOOGLE SHEETS"):
                if n and clu:
                    new_row = pd.DataFrame([{"Nombre":n,"Cinturón":cin,"Peso":pe,"Edad":ed,"BJJ / NO-GI":est,"Club":clu}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success(f"✅ {n} guardado en el Excel")
                    st.rerun()
                else:
                    st.warning("Rellena nombre y club")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.page = 'login'
        st.rerun()
