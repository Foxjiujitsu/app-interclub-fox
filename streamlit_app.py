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
    .main .block-container { max-width: 1100px; margin: 0 auto; padding-top: 10px !important; }
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

    # --- EMPAREJAMIENTOS ---
    if "EMPAREJAMIENTOS" in st.session_state.active_tab:
        es_inf = "INFANTILES" in st.session_state.active_tab
        cat_label = "Infantil" if es_inf else "Adulto"
        st.markdown(f"<div class='section-title'>ORGANIZACIÓN {cat_label.upper()}</div>", unsafe_allow_html=True)
        
        df_f = st.session_state.df[st.session_state.df['Edad'] <= 12] if es_inf else st.session_state.df[st.session_state.df['Edad'] > 12]
        
        if st.button("⚠️ REINICIAR TODA LA TABLA"):
            st.session_state.luchas = st.session_state.luchas[st.session_state.luchas['Categoría'] != cat_label]
            st.rerun()

        # Cargamos las luchas guardadas
        luchas_guardadas = st.session_state.luchas[st.session_state.luchas['Categoría'] == cat_label].copy()
        
        # Identificamos quiénes YA son pareja (Luchador 2) para no mostrarlos como Luchador 1
        nombres_ya_emparejados = set(luchas_guardadas[luchas_guardadas['Luchador_2'] != "---"]['Luchador_2'].tolist())

        # Preparamos la tabla: Todos los de la categoría menos los que ya son Luchador 2 de alguien
        data_para_tabla = []
        for _, r in df_f.iterrows():
            if r['Nombre'] not in nombres_ya_emparejados:
                # Si ya existe un cruce guardado para este Luchador 1, lo recuperamos
                existente = luchas_guardadas[luchas_guardadas['Luchador_1'] == r['Nombre']]
                if not existente.empty:
                    data_para_tabla.append(existente.iloc[0].to_dict())
                else:
                    data_para_tabla.append({
                        "Luchador_1": r['Nombre'],
                        "Ficha_1": f"{r['Cinturón']} | {r['Estilo']} | {r['Peso']}kg | {r['Club']}",
                        "VS": "VS", 
                        "Luchador_2": "---", 
                        "Ficha_2": "---",
                        "Categoría": cat_label, 
                        "Resultado_Final": "Pendiente"
                    })
        
        df_edit = pd.DataFrame(data_para_tabla)

        # Diccionario de fichas para el autocompletado instantáneo
        fichas_dict = {r['Nombre']: f"{r['Cinturón']} | {r['Estilo']} | {r['Peso']}kg | {r['Club']}" for _, r in df_f.iterrows()}
        fichas_dict["---"] = "---"

        # Opciones para el desplegable (Todos los nombres de la categoría)
        opciones_nombres = ["---"] + sorted(df_f['Nombre'].tolist())

        # EDITOR DE TABLA
        edited_df = st.data_editor(
            df_edit,
            column_config={
                "Luchador_1": st.column_config.TextColumn("Luchador 1", disabled=True),
                "Ficha_1": st.column_config.TextColumn("Ficha 1", disabled=True),
                "Luchador_2": st.column_config.SelectboxColumn("Contrincante", options=opciones_nombres),
                "Ficha_2": st.column_config.TextColumn("Ficha 2", disabled=True),
                "VS": st.column_config.TextColumn("VS", disabled=True),
                "Categoría": None, "Resultado_Final": None, "ID": None # Ocultamos columnas internas
            },
            use_container_width=True, hide_index=True
        )

        # Aplicar Ficha 2 automáticamente al seleccionar nombre
        for i, row in edited_df.iterrows():
            nombre_sel = row['Luchador_2']
            edited_df.at[i, 'Ficha_2'] = fichas_dict.get(nombre_sel, "---")

        if st.button("💾 GUARDAR COMBATES"):
            otras_cats = st.session_state.luchas[st.session_state.luchas['Categoría'] != cat_label]
            # Solo guardamos las filas que tienen un contrincante asignado o que son base
            st.session_state.luchas = pd.concat([otras_cats, edited_df], ignore_index=True)
            guardar_datos(st.session_state.luchas, LUC_FILE)
            st.success("¡Guardado! Los luchadores asignados desaparecerán de la lista de pendientes.")
            st.rerun()

    # --- RESTO DE SECCIONES (Siguen igual) ---
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
        if l_res.empty: st.warning("No hay combates cerrados.")
        else:
            res_edit = st.data_editor(l_res[["Luchador_1", "Luchador_2", "Resultado_Final"]], use_container_width=True, hide_index=True)
            if st.button("💾 GUARDAR RESULTADOS"):
                 otras = st.session_state.luchas[~( (st.session_state.luchas['Categoría'] == cat) & (st.session_state.luchas['Luchador_2'] != "---") )]
                 l_res["Resultado_Final"] = res_edit["Resultado_Final"].values
                 st.session_state.luchas = pd.concat([otras, l_res], ignore_index=True)
                 guardar_datos(st.session_state.luchas, LUC_FILE); st.success("Actualizado")
