import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOX JIU-JITSU", layout="wide")

DB_FILE = "competidores.csv"
LUC_FILE = "luchas.csv"

def cargar_datos(archivo, columnas):
    if os.path.exists(archivo):
        try: return pd.read_csv(archivo)
        except: return pd.DataFrame(columns=columnas)
    return pd.DataFrame(columns=columnas)

def guardar_datos(df, archivo):
    df.to_csv(archivo, index=False)

if 'df' not in st.session_state:
    st.session_state.df = cargar_datos(DB_FILE, ["Número", "Nombre", "Cinturón", "Peso", "Edad", "Estilo", "Club"])
if 'luchas' not in st.session_state:
    st.session_state.luchas = cargar_datos(LUC_FILE, ["ID", "Luchador_1", "Ficha_1", "VS", "Luchador_2", "Ficha_2", "Categoría", "Resultado_Final"])

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "INICIO"

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #333333; }
    .main .block-container { max-width: 1000px; margin: 0 auto; padding-top: 10px !important; }
    .logo-container { text-align: center; margin-bottom: 10px; width: 100%; }
    div.stButton > button {
        background-color: #ffffff !important; color: #333333 !important;
        border: 1.5px solid #666666 !important; border-radius: 25px !important;
        width: 280px !important; height: 42px !important;
        font-weight: bold !important; font-size: 12px !important;
        text-transform: uppercase; margin-bottom: 2px !important;
    }
    div.stButton > button:hover { border-color: #ff6b00 !important; color: #ff6b00 !important; }
    .section-title { color: #ff6b00; font-size: 18px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"""<div class="logo-container"><img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="180"><br><b>SISTEMA DE COMPETICIÓN</b></div>""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if st.session_state.active_tab == "INICIO":
    opciones = ["REGISTRO DE COMPETIDORES", "COMPETIDORES INFANTILES", "COMPETIDORES ADULTOS", "EMPAREJAMIENTOS INFANTILES", "EMPAREJAMIENTOS ADULTOS", "RESULTADOS INFANTILES", "RESULTADOS ADULTOS"]
    for op in opciones:
        if st.button(op): 
            st.session_state.active_tab = op
            st.rerun()
else:
    if st.button("VOLVER AL MENÚ"):
        st.session_state.active_tab = "INICIO"
        st.rerun()
    st.markdown("---")

    # --- EMPAREJAMIENTOS DINÁMICOS MEJORADOS ---
    if "EMPAREJAMIENTOS" in st.session_state.active_tab:
        es_inf = "INFANTILES" in st.session_state.active_tab
        cat_label = "Infantil" if es_inf else "Adulto"
        st.markdown(f"<div class='section-title'>ORGANIZACIÓN DE COMBATES {cat_label.upper()}</div>", unsafe_allow_html=True)
        
        # 1. Obtenemos competidores de la categoría
        df_f = st.session_state.df[st.session_state.df['Edad'] <= 12] if es_inf else st.session_state.df[st.session_state.df['Edad'] > 12]
        
        # 2. Cargamos luchas existentes
        luchas_cat = st.session_state.luchas[st.session_state.luchas['Categoría'] == cat_label].copy()
        
        # 3. Si está vacío, creamos la lista base con todos los nombres
        if luchas_cat.empty and not df_f.empty:
            nuevas = []
            for _, r in df_f.iterrows():
                nuevas.append({
                    "ID": r['Número'], "Luchador_1": r['Nombre'],
                    "Ficha_1": f"{r['Cinturón']} | {r['Estilo']} | {r['Peso']}kg | {r['Club']}",
                    "VS": "VS", "Luchador_2": "---", "Ficha_2": "---",
                    "Categoría": cat_label, "Resultado_Final": "Pendiente"
                })
            luchas_cat = pd.DataFrame(nuevas)

        # 4. LÓGICA DE FILTRADO: Quitar de Luchador 1 a los que ya son Luchador 2
        asignados_como_l2 = set(luchas_cat[luchas_cat['Luchador_2'] != "---"]['Luchador_2'].tolist())
        luchas_visibles = luchas_cat[~luchas_cat['Luchador_1'].isin(asignados_como_l2)]

        # Nombres disponibles para el desplegable
        todos_nombres = ["---"] + df_f['Nombre'].tolist()
        disponibles_l2 = [n for n in todos_nombres if n not in set(luchas_visibles['Luchador_1'].tolist()) or n == "---"]

        # 5. EDITOR DE TABLA
        edit_l = st.data_editor(
            luchas_visibles,
            column_config={
                "Luchador_1": st.column_config.TextColumn("Luchador 1", disabled=True),
                "Ficha_1": st.column_config.TextColumn("Ficha 1", disabled=True),
                "Luchador_2": st.column_config.SelectboxColumn("Elegir Contrincante", options=disponibles_l2),
                "Ficha_2": st.column_config.TextColumn("Ficha 2", disabled=True),
                "Resultado_Final": st.column_config.TextColumn("Resultado", disabled=True)
            },
            use_container_width=True, hide_index=True, num_rows="dynamic"
        )

        if st.button("💾 GUARDAR COMBATES"):
            # Actualizar fichas de los elegidos
            for i, row in edit_l.iterrows():
                if row['Luchador_2'] != "---":
                    m = st.session_state.df[st.session_state.df['Nombre'] == row['Luchador_2']]
                    if not m.empty:
                        r2 = m.iloc[0]
                        edit_l.at[i, 'Ficha_2'] = f"{r2['Cinturón']} | {r2['Estilo']} | {r2['Peso']}kg | {r2['Club']}"
            
            # Guardar y limpiar la tabla (quitará a los L2 de la columna L1 automáticamente al recargar)
            otras = st.session_state.luchas[st.session_state.luchas['Categoría'] != cat_label]
            st.session_state.luchas = pd.concat([otras, edit_l], ignore_index=True)
            guardar_datos(st.session_state.luchas, LUC_FILE)
            st.success("Combates sincronizados. Los luchadores asignados han sido emparejados.")
            st.rerun()

    # --- RESTO DE SECCIONES ---
    elif "REGISTRO" in st.session_state.active_tab:
        with st.form("reg"):
            n = st.text_input("Nombre"); c = st.selectbox("Cinto", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            p = st.number_input("Peso", 5.0, 150.0, 70.0); e = st.number_input("Edad", 4, 90, 20)
            s = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"]); cl = st.text_input("Academia")
            if st.form_submit_button("GUARDAR"):
                nueva = pd.DataFrame([{"Número": len(st.session_state.df)+1, "Nombre": n, "Cinturón": c, "Peso": p, "Edad": e, "Estilo": s, "Club": cl}])
                st.session_state.df = pd.concat([st.session_state.df, nueva], ignore_index=True)
                guardar_datos(st.session_state.df, DB_FILE); st.success("Registrado")

    elif "RESULTADOS" in st.session_state.active_tab:
        es_inf = "INFANTILES" in st.session_state.active_tab; cat = "Infantil" if es_inf else "Adulto"
        l_res = st.session_state.luchas[(st.session_state.luchas['Categoría'] == cat) & (st.session_state.luchas['Luchador_2'] != "---")].copy()
        if l_res.empty: st.warning("No hay combates cerrados para puntuar.")
        else:
            res_edit = st.data_editor(l_res[["Luchador_1", "Luchador_2", "Resultado_Final"]], use_container_width=True, hide_index=True)
            if st.button("💾 GUARDAR RESULTADOS"):
                 otras = st.session_state.luchas[~( (st.session_state.luchas['Categoría'] == cat) & (st.session_state.luchas['Luchador_2'] != "---") )]
                 l_res["Resultado_Final"] = res_edit["Resultado_Final"].values
                 st.session_state.luchas = pd.concat([otras, l_res], ignore_index=True)
                 guardar_datos(st.session_state.luchas, LUC_FILE); st.success("Podio actualizado")

    elif "COMPETIDORES" in st.session_state.active_tab:
        es_inf = "INFANTILES" in st.session_state.active_tab
        filt = st.session_state.df[st.session_state.df['Edad'] <= 12] if es_inf else st.session_state.df[st.session_state.df['Edad'] > 12]
        edit = st.data_editor(filt, use_container_width=True, hide_index=True, num_rows="dynamic")
        if st.button("💾 GUARDAR LISTA"):
            otros = st.session_state.df[st.session_state.df['Edad'] > 12] if es_inf else st.session_state.df[st.session_state.df['Edad'] <= 12]
            st.session_state.df = pd.concat([otros, edit], ignore_index=True)
            guardar_datos(st.session_state.df, DB_FILE); st.success("Lista guardada")
