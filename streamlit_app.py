import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOX JIU-JITSU ADMIN", layout="wide")

# --- ESTILOS CLONADOS ---
st.markdown("""
    <style>
    .stApp { background-color: #F2F2F2; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF; border-radius: 10px 10px 0 0; 
        padding: 10px 20px; font-weight: bold; color: #444;
    }
    .stTabs [aria-selected="true"] { background-color: #FF6B00 !important; color: white !important; }
    div.stButton > button { background-color: #FF6B00 !important; color: white !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- FUNCIÓN DE EMPAREJAMIENTO (MATCHMAKING) ---
def generar_cruces(df):
    luchadores = df.to_dict('records')
    parejas = []
    usados = set()

    for i, l1 in enumerate(luchadores):
        if i in usados: continue
        best_match = None
        
        for j, l2 in enumerate(luchadores):
            if j <= i or j in usados: continue
            
            # REGLAS: Mismo Estilo, Cinturón, Edad +/- 5 años, Peso +/- 5kg, Diferente Club
            if (l1['Estilo'] == l2['Estilo'] and 
                l1['Cinturon'] == l2['Cinturon'] and 
                abs(l1['Peso'] - l2['Peso']) <= 5 and
                l1['Club'] != l2['Club']):
                
                best_match = j
                break
        
        if best_match is not None:
            parejas.append((l1, luchadores[best_match]))
            usados.add(i)
            usados.add(best_match)
            
    return parejas

# --- PANTALLA LOGIN ---
if st.session_state.page == 'login':
    col1, col_c, col2 = st.columns([1,2,1])
    with col_c:
        st.image("https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR AL PANEL"):
            if u == "Fox-Interclub" and p == "Interclub-Fox-2026":
                st.session_state.page = 'panel'
                st.rerun()

# --- PANEL DE ORGANIZADOR ---
elif st.session_state.page == 'panel':
    st.sidebar.image("https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG", width=100)
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.page = 'login'
        st.rerun()

    st.title("🦊 PANEL DE ORGANIZADOR")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Ver Inscritos", 
        "📝 Registro Manual", 
        "⚔️ Cruces / Llaves", 
        "🏆 Resultados", 
        "📸 Fotos"
    ])

    # Cargar datos de Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
    except:
        # Datos de prueba si fallan los secrets
        df = pd.DataFrame([
            {"Nombre": "Juan Perez", "Cinturon": "Blanco", "Peso": 75, "Edad": 25, "Club": "Fox", "Estilo": "BJJ (GI)"},
            {"Nombre": "Santi Cano", "Cinturon": "Blanco", "Peso": 77, "Edad": 27, "Club": "Gracie", "Estilo": "BJJ (GI)"}
        ])

    with tab1:
        st.subheader("Lista Total de Competidores")
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Inscribir nuevo luchador")
        with st.form("manual_reg"):
            n = st.text_input("Nombre")
            c = st.selectbox("Cinturón", ["Blanco", "Azul", "Morado", "Marrón", "Negro"])
            e = st.number_input("Edad", 4, 80)
            pe = st.number_input("Peso (kg)", 10.0, 150.0)
            cl = st.text_input("Club")
            es = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            if st.form_submit_button("AÑADIR A LA LISTA"):
                st.success(f"{n} ha sido inscrito correctamente.")

    with tab3:
        st.subheader("Generador de Cruces Automático")
        if st.button("⚡ GENERAR PAREJAS POR CATEGORÍA"):
            matches = generar_cruces(df)
            if matches:
                for m in matches:
                    col_a, col_vs, col_b = st.columns([4,1,4])
                    col_a.info(f"**{m[0]['Nombre']}** ({m[0]['Club']})")
                    col_vs.write("VS")
                    col_b.warning(f"**{m[1]['Nombre']}** ({m[1]['Club']})")
            else:
                st.error("No hay suficientes luchadores que coincidan para crear parejas.")
        
        st.divider()
        st.subheader("Modificación Manual")
        st.write("Arrastra o selecciona para casar luchadores manualmente:")
        st.multiselect("Selecciona dos luchadores para una lucha manual", df['Nombre'].tolist())

    with tab4:
        st.subheader("Registro de Resultados")
        st.info("Selecciona el combate y marca al ganador.")

    with tab5:
        st.subheader("Galería de Fotos")
        st.text_input("Enlace de Google Photos o Dropbox")
        st.file_uploader("O sube una foto destacada", type=['jpg', 'png'])
