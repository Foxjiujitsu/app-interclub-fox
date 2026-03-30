import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOX JIU-JITSU", layout="wide")

DB_FILE = "competidores.csv"
LUC_FILE = "luchas.csv" # Archivo para guardar los emparejamientos

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
    st.session_state.luchas = cargar_datos(LUC_FILE, ["ID_Lucha", "Competidor_1", "Info_1", "VS", "Competidor_2", "Info_2", "Categoría"])

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "INICIO"

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #333333; }
    .main .block-container { max-width: 600px; margin: 0 auto; padding-top: 20px !important; }
    .logo-container { text-align: center; margin-bottom: 20px; width: 100%; }
    div.stButton > button {
        background-color: #ffffff !important; color: #333333 !important;
        border: 1.5px solid #666666 !important; border-radius: 25px !important;
        width: 300px !important; height: 46px !important;
        font-weight: bold !important; font-size: 13px !important;
        text-transform: uppercase; margin-bottom: 4px !important;
    }
    div.stButton > button:hover { border-color: #ff6b00 !important; color: #ff6b00 !important; }
    .section-title { color: #ff6b00; font-size: 18px; font-weight: bold; text-align: center; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"""<div class="logo-container"><img src="https://raw.githubusercontent.com/Foxjiujitsu/app-interclub-fox/main/fox-letras-naranja.PNG" width="200"><br><b>SISTEMA DE COMPETICIÓN</b></div>""", unsafe_allow_html=True)

# --- LÓGICA DE EMPAREJAMIENTO AUTOMÁTICO ---
def generar_emparejamientos(df_filtrado, cat_nombre):
    luchas = []
    ya_emparejados = set()
    lista = df_filtrado.to_dict('records')
    
    for i, c1 in enumerate(lista):
        if c1['Nombre'] in ya_emparejados: continue
        
        mejor_oponente = None
        min_dif_peso = 999
        
        for j, c2 in enumerate(lista):
            if i == j or c2['Nombre'] in ya_emparejados: continue
            
            # REGLAS: Mismo Estilo, Mismo Cinturón, Diferente Club
            if c1['Estilo'] == c2['Estilo'] and c1['Cinturón'] == c2['Cinturón'] and c1['Club'] != c2['Club']:
                # Diferencia de edad max 2 años y peso
                dif_edad = abs(c1['Edad'] - c2['Edad'])
                dif_peso = abs(c1['Peso'] - c2['Peso'])
                
                if dif_edad <= 2 and dif_peso <= 5:
                    if dif_peso < min_dif_peso:
                        min_dif_peso = dif_peso
                        mejor_oponente = c2
        
        info1 = f"{c1['Cinturón']} | {c1['Peso']}kg | {c1['Estilo']} | {c1['Club']}"
        if mejor_oponente:
            info2 = f"{mejor_oponente['Cinturón']} | {mejor_oponente['Peso']}kg | {mejor_oponente['Estilo']} | {mejor_oponente['Club']}"
            luchas.append({"ID_Lucha": len(luchas)+1, "Competidor_1": c1['Nombre'], "Info_1": info1, "VS": "VS", "Competidor_2": mejor_oponente['Nombre'], "Info_2": info2, "Categoría": cat_nombre})
            ya_emparejados.add(c1['Nombre'])
            ya_emparejados.add(mejor_oponente['Nombre'])
        else:
            luchas.append({"ID_Lucha": len(luchas)+1, "Competidor_1": c1['Nombre'], "Info_1": info1, "VS": "VS", "Competidor_2": "SIN PAREJA", "Info_2": "---", "Categoría": cat_nombre})
            ya_emparejados.add(c1['Nombre'])
            
    return pd.DataFrame(luchas)

# --- MENÚ ---
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
    df_comp = st.session_state.df

    # SECCIÓN REGISTRO
    if st.session_state.active_tab == "REGISTRO DE COMPETIDORES":
        st.markdown("<div class='section-title'>NUEVO REGISTRO</div>", unsafe_allow_html=True)
        with st.form("reg", clear_on_submit=True):
            n = st.text_input("Nombre")
            c = st.selectbox("Cinturón", ["Blanco", "Gris", "Amarillo", "Naranja", "Verde", "Azul", "Morado", "Marrón", "Negro"])
            p = st.number_input("Peso (kg)", 5.0, 150.0, 70.0)
            e = st.number_input("Edad", 4, 90, 20)
            s = st.selectbox("Estilo", ["BJJ (GI)", "NO-GI"])
            cl = st.text_input("Academia")
            if st.form_submit_button("GUARDAR"):
                nueva = pd.DataFrame([{"Número": len(df_comp)+1, "Nombre": n, "Cinturón": c, "Peso": p, "Edad": e, "Estilo": s, "Club": cl}])
                st.session_state.df = pd.concat([df_comp, nueva], ignore_index=True)
                guardar_datos(st.session_state.df, DB_FILE)
                st.success("Guardado")

    # SECCIÓN LISTADOS
    elif st.session_state.active_tab in ["COMPETIDORES INFANTILES", "COMPETIDORES ADULTOS"]:
        es_inf = "INFANTILES" in st.session_state.active_tab
        filt = df_comp[df_comp['Edad'] <= 12] if es_inf else df_comp[df_comp['Edad'] > 12]
        st.markdown(f"<div class='section-title'>{st.session_state.active_tab}</div>", unsafe_allow_html=True)
        editado = st.data_editor(filt, use_container_width=True, hide_index=True, num_rows="dynamic")
        if st.button("GUARDAR CAMBIOS"):
            otros = df_comp[df_comp['Edad'] > 12] if es_inf else df_comp[df_comp['Edad'] <= 12]
            st.session_state.df = pd.concat([otros, editado], ignore_index=True)
            guardar_datos(st.session_state.df, DB_FILE)
            st.success("Actualizado")

    # SECCIÓN EMPAREJAMIENTOS (LA MAGIA)
    elif st.session_state.active_tab in ["EMPAREJAMIENTOS INFANTILES", "EMPAREJAMIENTOS ADULTOS"]:
        es_inf = "INFANTILES" in st.session_state.active_tab
        cat = "Infantil" if es_inf else "Adulto"
        st.markdown(f"<div class='section-title'>COMBATES {cat.upper()}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 GENERAR AUTOMÁTICO"):
                df_f = df_comp[df_comp['Edad'] <= 12] if es_inf else df_comp[df_comp['Edad'] > 12]
                st.session_state.luchas = generar_emparejamientos(df_f, cat)
                st.success("Cruces generados")
        
        # Mostrar tabla de luchas para editar
        luchas_cat = st.session_state.luchas[st.session_state.luchas['Categoría'] == cat]
        edit_luchas = st.data_editor(luchas_cat, use_container_width=True, hide_index=True, num_rows="dynamic")
        
        if st.button("💾 GUARDAR CRUCES"):
            otras_luchas = st.session_state.luchas[st.session_state.luchas['Categoría'] != cat]
            st.session_state.luchas = pd.concat([otras_luchas, edit_luchas], ignore_index=True)
            guardar_datos(st.session_state.luchas, LUC_FILE)
            st.success("Combates guardados")

    # SECCIÓN RESULTADOS
    elif "RESULTADOS" in st.session_state.active_tab:
        st.markdown(f"<div class='section-title'>{st.session_state.active_tab}</div>", unsafe_allow_html=True)
        st.info("Anota aquí los ganadores (1º, 2º, Empate)")
        res_edit = st.data_editor(st.session_state.df, use_container_width=True, hide_index=True)
        if st.button("GUARDAR PODIO"):
            st.session_state.df = res_edit
            guardar_datos(st.session_state.df, DB_FILE)
            st.success("Resultados guardados")
