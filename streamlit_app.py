import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
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
    st.session_state.df = cargar_datos(DB_FILE, ["Número", "Nombre", "Cinturón", "Peso", "Edad", "Estilo", "Club", "Resultado"])
if 'luchas' not in st.session_state:
    st.session_state.luchas = cargar_datos(LUC_FILE, ["ID_Lucha", "Competidor_1", "Info_1", "VS", "Competidor_2", "Info_2", "Categoría"])

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "INICIO"

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #333333; }
    .main .block-container { max-width: 700px; margin: 0 auto; padding-top: 20px !important; }
    .logo-container { text-align: center; margin-bottom: 20px; width: 100%; }
    div.stButton > button {
        background-color: #ffffff !important; color: #333333 !important;
        border: 1.5px solid #666666 !important; border-radius: 25px !important;
        width: 320px !important; height: 46px !important;
        font-weight: bold !important; font-size: 13px !important;
        text-transform: uppercase; margin-bottom: 4px !important;
    }
    div.stButton > button:hover { border-color: #ff6b00 !important; color: #ff6b00 !important; }
    .section-title { color: #ff6b00; font-size: 20px; font-weight: bold; text-align: center; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"""<div class="logo-container"><img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="220"><br><b>SISTEMA DE COMPETICIÓN</b></div>""", unsafe_allow_html=True)

# --- ALGORITMO DE EMPAREJAMIENTO CON REGLAS DE EDAD ---
def generar_emparejamientos(df_filtrado, es_infantil):
    luchas = []
    ya_emparejados = set()
    lista = df_filtrado.to_dict('records')
    cat_nombre = "Infantil" if es_infantil else "Adulto"
    
    # REGLA CRÍTICA: 2 años para niños, 10 años para adultos
    max_dif_edad = 2 if es_infantil else 10
    
    for i, c1 in enumerate(lista):
        if c1['Nombre'] in ya_emparejados: continue
        
        mejor_oponente = None
        min_dif_peso = 999
        
        for j, c2 in enumerate(lista):
            if i == j or c2['Nombre'] in ya_emparejados: continue
            
            # FILTROS ESTRICTOS: Mismo Estilo, Mismo Cinto, DIFERENTE Club
            mismo_estilo = str(c1['Estilo']) == str(c2['Estilo'])
            mismo_cinto = str(c1['Cinturón']) == str(c2['Cinturón'])
            diff_club = str(c1['Club']).strip().lower() != str(c2['Club']).strip().lower()
            
            if mismo_estilo and mismo_cinto and diff_club:
                dif_edad = abs(c1['Edad'] - c2['Edad'])
                dif_peso = abs(c1['Peso'] - c2['Peso'])
                
                # REGLA DE EDAD Y PESO (Máx 5kg de diferencia)
                if dif_edad <= max_dif_edad and dif_peso <= 5:
                    if dif_peso < min_dif_peso:
                        min_dif_peso = dif_peso
                        mejor_oponente = c2
        
        info1 = f"{c1['Cinturón']} | {c1['Peso']}kg | {c1['Estilo']} | {c1['Club']}"
        if mejor_oponente:
            info2 = f"{mejor_oponente['Cinturón']} | {mejor_oponente['Peso']}kg | {mejor_oponente['Estilo']} | {mejor_oponente['Club']}"
            luchas.append({
                "ID": len(luchas)+1, 
                "Luchador_1": c1['Nombre'], "Ficha_1": info1, 
                "VS": "VS", 
                "Luchador_2": mejor_oponente['Nombre'], "Ficha_2": info2, 
                "Categoría": cat_nombre
            })
            ya_emparejados.add(c1['Nombre'])
            ya_emparejados.add(mejor_oponente['Nombre'])
        else:
            # Si no hay pareja, queda registrado para completar a mano
            luchas.append({
                "ID": len(luchas)+1, 
                "Luchador_1": c1['Nombre'], "Ficha_1": info1, 
                "VS": "VS", 
                "Luchador_2": "⚠️ BUSCAR PAREJA", "Ficha_2": "---", 
                "Categoría": cat_nombre
            })
            ya_emparejados.add(c1['Nombre'])
            
    return pd.DataFrame(luchas)

# --- NAVEGACIÓN ---
if st.session_state.active_tab == "INICIO":
    st.write("")
    if st.button("REGISTRO DE COMPETIDORES"): st.session_state.active_tab = "REGISTRO"
    if st.button("COMPETIDORES INFANTILES"): st.session_state.active_tab = "INF"
    if st.button("COMPETIDORES ADULTOS"): st.session_state.active_tab = "ADU"
    if st.button("EMPAREJAMIENTOS INFANTILES"): st.session_state.active_tab = "EMP_INF"
    if st.button("EMPAREJAMIENTOS ADULTOS"): st.session_state.active_tab = "EMP_ADU"
    if st.button("RESULTADOS INFANTILES"): st.session_state.active_tab = "RES_INF"
    if st.button("RESULTADOS ADULTOS"): st.session_state.active_tab = "RES_ADU"

else:
    if st.button("⬅️ VOLVER AL MENÚ"):
        st.session_state.active_tab = "INICIO"
        st.rerun()
    
    st.markdown("---")
    df_comp = st.session_state.df

    # SECCIONES DE LISTADO Y EDICIÓN
    if st.session_state.active_tab in ["INF", "ADU"]:
        es_inf = st.session_state.active_tab == "INF"
        filt = df_comp[df_comp['Edad'] <= 12] if es_inf else df_comp[df_comp['Edad'] > 12]
        st.markdown(f"<div class='section-title'>LISTA {'INFANTIL' if es_inf else 'ADULTA'}</div>", unsafe_allow_html=True)
        editado = st.data_editor(filt, use_container_width=True, hide_index=True, num_rows="dynamic")
        if st.button("💾 GUARDAR CAMBIOS"):
            otros = df_comp[df_comp['Edad'] > 12] if es_inf else df_comp[df_comp['Edad'] <= 12]
            st.session_state.df = pd.concat([otros, editado], ignore_index=True)
            guardar_datos(st.session_state.df, DB_FILE)
            st.success("Lista guardada")

    # SECCIONES DE EMPAREJAMIENTO
    elif st.session_state.active_tab in ["EMP_INF", "EMP_ADU"]:
        es_inf = st.session_state.active_tab == "EMP_INF"
        cat_txt = "Infantil" if es_inf else "Adulto"
        st.markdown(f"<div class='section-title'>CRUCES {cat_txt.upper()}</div>", unsafe_allow_html=True)
        
        if st.button("🔄 GENERAR EMPAREJAMIENTOS AUTOMÁTICOS"):
            df_f = df_comp[df_comp['Edad'] <= 12] if es_inf else df_comp[df_comp['Edad'] > 12]
            st.session_state.luchas = generar_emparejamientos(df_f, es_inf)
            st.success(f"Emparejamientos realizados (niños <2 años / adultos <10 años)")

        luchas_filtradas = st.session_state.luchas[st.session_state.luchas['Categoría'] == cat_txt]
        edit_luchas = st.data_editor(luchas_filtradas, use_container_width=True, hide_index=True, num_rows="dynamic")
        
        if st.button("💾 GUARDAR ESTOS COMBATES"):
            otras = st.session_state.luchas[st.session_state.luchas['Categoría'] != cat_txt]
            st.session_state.luchas = pd.concat([otras, edit_luchas], ignore_index=True)
            guardar_datos(st.session_state.luchas, LUC_FILE)
            st.success("Emparejamientos fijados")

    # SECCIÓN REGISTRO
    elif st.session_state.active_tab == "REGISTRO":
        st.markdown("<div class='section-title'>NUEVO REGISTRO</div>", unsafe_allow_html=True)
        with st.form("registro"):
            n = st.text_input("Nombre")
            c = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            p = st.number_input("Peso (kg)", 5.0, 150.0, 70.0)
            e = st.number_input("Edad", 4, 90, 20)
            s = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            cl = st.text_input("Academia")
            if st.form_submit_button("AÑADIR LUCHADOR"):
                nueva = pd.DataFrame([{"Número": len(df_comp)+1, "Nombre": n, "Cinturón": c, "Peso": p, "Edad": e, "Estilo": s, "Club": cl, "Resultado": "Pendiente"}])
                st.session_state.df = pd.concat([df_comp, nueva], ignore_index=True)
                guardar_datos(st.session_state.df, DB_FILE)
                st.success(f"{n} registrado con éxito")

    # SECCIÓN RESULTADOS
    elif "RES" in st.session_state.active_tab:
        st.markdown(f"<div class='section-title'>{st.session_state.active_tab}</div>", unsafe_allow_html=True)
        res_edit = st.data_editor(st.session_state.df, use_container_width=True, hide_index=True)
        if st.button("💾 GUARDAR PODIO"):
            st.session_state.df = res_edit
            guardar_datos(st.session_state.df, DB_FILE)
            st.success("Resultados actualizados")
