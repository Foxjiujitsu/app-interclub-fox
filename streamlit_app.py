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

# Inicializar estados
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
    .main .block-container { max-width: 800px; margin: 0 auto; padding-top: 20px !important; }
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

# --- ALGORITMO DE EMPAREJAMIENTO ---
def generar_emparejamientos(df_filtrado, es_infantil):
    luchas = []
    ya_emparejados = set()
    lista = df_filtrado.to_dict('records')
    cat_nombre = "Infantil" if es_infantil else "Adulto"
    max_dif_edad = 2 if es_infantil else 10
    
    for i, c1 in enumerate(lista):
        if c1['Nombre'] in ya_emparejados: continue
        mejor_oponente = None
        min_dif_peso = 999
        
        for j, c2 in enumerate(lista):
            if i == j or c2['Nombre'] in ya_emparejados: continue
            if str(c1['Estilo']) == str(c2['Estilo']) and str(c1['Cinturón']) == str(c2['Cinturón']) and str(c1['Club']).strip().lower() != str(c2['Club']).strip().lower():
                dif_edad = abs(c1['Edad'] - c2['Edad'])
                dif_peso = abs(c1['Peso'] - c2['Peso'])
                if dif_edad <= max_dif_edad and dif_peso <= 5:
                    if dif_peso < min_dif_peso:
                        min_dif_peso = dif_peso
                        mejor_oponente = c2
        
        ficha1 = f"{c1['Cinturón']} | {c1['Estilo']} | {c1['Club']}"
        if mejor_oponente:
            ficha2 = f"{mejor_oponente['Cinturón']} | {mejor_oponente['Estilo']} | {mejor_oponente['Club']}"
            luchas.append({"ID": len(luchas)+1, "Luchador_1": c1['Nombre'], "Ficha_1": ficha1, "VS": "VS", "Luchador_2": mejor_oponente['Nombre'], "Ficha_2": ficha2, "Categoría": cat_nombre, "Resultado_Final": "Pendiente"})
            ya_emparejados.add(c1['Nombre'])
            ya_emparejados.add(mejor_oponente['Nombre'])
        else:
            luchas.append({"ID": len(luchas)+1, "Luchador_1": c1['Nombre'], "Ficha_1": ficha1, "VS": "VS", "Luchador_2": "---", "Ficha_2": "---", "Categoría": cat_nombre, "Resultado_Final": "Pendiente"})
            ya_emparejados.add(c1['Nombre'])
    return pd.DataFrame(luchas)

# --- NAVEGACIÓN ---
if st.session_state.active_tab == "INICIO":
    opciones = ["REGISTRO DE COMPETIDORES", "COMPETIDORES INFANTILES", "COMPETIDORES ADULTOS", "EMPAREJAMIENTOS INFANTILES", "EMPAREJAMIENTOS ADULTOS", "RESULTADOS INFANTILES", "RESULTADOS ADULTOS"]
    for op in opciones:
        if st.button(op): 
            st.session_state.active_tab = op
            st.rerun()
else:
    if st.button("⬅️ VOLVER AL MENÚ"):
        st.session_state.active_tab = "INICIO"
        st.rerun()
    st.markdown("---")

    # REGISTRO
    if st.session_state.active_tab == "REGISTRO DE COMPETIDORES":
        with st.form("reg"):
            n = st.text_input("Nombre")
            c = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            p = st.number_input("Peso (kg)", 5.0, 150.0, 70.0)
            e = st.number_input("Edad", 4, 90, 20)
            s = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            cl = st.text_input("Academia")
            if st.form_submit_button("GUARDAR"):
                nueva = pd.DataFrame([{"Número": len(st.session_state.df)+1, "Nombre": n, "Cinturón": c, "Peso": p, "Edad": e, "Estilo": s, "Club": cl}])
                st.session_state.df = pd.concat([st.session_state.df, nueva], ignore_index=True)
                guardar_datos(st.session_state.df, DB_FILE)
                st.success("Registrado")

    # LISTADOS
    elif st.session_state.active_tab in ["COMPETIDORES INFANTILES", "COMPETIDORES ADULTOS"]:
        es_inf = "INFANTILES" in st.session_state.active_tab
        filt = st.session_state.df[st.session_state.df['Edad'] <= 12] if es_inf else st.session_state.df[st.session_state.df['Edad'] > 12]
        st.markdown(f"<div class='section-title'>{st.session_state.active_tab}</div>", unsafe_allow_html=True)
        edit = st.data_editor(filt, use_container_width=True, hide_index=True, num_rows="dynamic")
        if st.button("💾 GUARDAR LISTA"):
            otros = st.session_state.df[st.session_state.df['Edad'] > 12] if es_inf else st.session_state.df[st.session_state.df['Edad'] <= 12]
            st.session_state.df = pd.concat([otros, edit], ignore_index=True)
            guardar_datos(st.session_state.df, DB_FILE)
            st.success("Guardado")

    # EMPAREJAMIENTOS
    elif st.session_state.active_tab in ["EMPAREJAMIENTOS INFANTILES", "EMPAREJAMIENTOS ADULTOS"]:
        es_inf = "INFANTILES" in st.session_state.active_tab
        cat = "Infantil" if es_inf else "Adulto"
        if st.button("🔄 GENERAR AUTOMÁTICO"):
            df_f = st.session_state.df[st.session_state.df['Edad'] <= 12] if es_inf else st.session_state.df[st.session_state.df['Edad'] > 12]
            st.session_state.luchas = generar_emparejamientos(df_f, es_inf)
        
        filt_luchas = st.session_state.luchas[st.session_state.luchas['Categoría'] == cat]
        edit_l = st.data_editor(filt_luchas, use_container_width=True, hide_index=True, num_rows="dynamic")
        if st.button("💾 GUARDAR COMBATES"):
            otras = st.session_state.luchas[st.session_state.luchas['Categoría'] != cat]
            st.session_state.luchas = pd.concat([otras, edit_l], ignore_index=True)
            guardar_datos(st.session_state.luchas, LUC_FILE)
            st.success("Combates fijados")

    # RESULTADOS (Aquí está lo que pedías)
    elif st.session_state.active_tab in ["RESULTADOS INFANTILES", "RESULTADOS ADULTOS"]:
        es_inf = "INFANTILES" in st.session_state.active_tab
        cat = "Infantil" if es_inf else "Adulto"
        st.markdown(f"<div class='section-title'>PODIO {cat.upper()}</div>", unsafe_allow_html=True)
        
        # Filtramos las luchas guardadas para esta categoría
        luchas_res = st.session_state.luchas[st.session_state.luchas['Categoría'] == cat]
        
        if luchas_res.empty:
            st.warning("Primero debes generar y guardar los emparejamientos.")
        else:
            st.info("Escribe en 'Resultado_Final': 1º Nombre, 2º Nombre o Empate")
            # Mostramos la tabla con los nombres, fichas y la casilla para el resultado
            res_final = st.data_editor(
                luchas_res[["Luchador_1", "Ficha_1", "VS", "Luchador_2", "Ficha_2", "Resultado_Final"]], 
                use_container_width=True, 
                hide_index=True
            )
            
            if st.button("💾 GUARDAR RESULTADOS"):
                # Actualizamos el dataframe global de luchas
                otras = st.session_state.luchas[st.session_state.luchas['Categoría'] != cat]
                # Recuperamos la columna Categoría que quitamos para la vista limpia
                res_final['Categoría'] = cat
                res_final['ID'] = range(1, len(res_final) + 1)
                st.session_state.luchas = pd.concat([otras, res_final], ignore_index=True)
                guardar_datos(st.session_state.luchas, LUC_FILE)
                st.success("¡Resultados guardados con éxito!")
