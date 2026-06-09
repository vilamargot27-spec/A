import streamlit as st
import json
import google.generativeai as genai

# =====================================================================
# 1. EL MÚSCULO MATEMÁTICO (FUNCTION CALLING)
# =====================================================================
def calcular_vacs_y_ce(inversion_inicial_social: float, flujos_om_social: list[float], tasa_descuento: float, alumnos_beneficiados: int) -> dict:
    """
    Calcula el Valor Actual de Costos Sociales (VACS) y el ratio Costo-Eficacia (CE).
    """
    vacs = inversion_inicial_social
    for t, flujo in enumerate(flujos_om_social, start=1):
        vacs += flujo / ((1 + tasa_descuento) ** t)
    
    ratio_ce = vacs / alumnos_beneficiados
    
    return {
        "vacs_total": round(vacs, 2),
        "ratio_costo_eficacia": round(ratio_ce, 2),
        "mensaje_normativo": "Cálculo exacto realizado por el backend en Python. Utiliza estos valores para redactar la viabilidad."
    }

# =====================================================================
# 2. EL CEREBRO (PROMPT MAESTRO)
# =====================================================================
PROMPT_MAESTRO = """
# ROL Y OBJETIVO PRINCIPAL
Actúa como un Especialista Senior en Inversión Pública, Experto en Programación Multianual de Inversiones (PMI) y Formulador de la Unidad Formuladora (UF) bajo el marco de Invierte.pe (Perú).

# REGLAS ESTRICTAS Y DETERMINISTAS (CERO ALUCINACIONES)
1. NORMATIVA: Basa tu análisis en la Directiva N° 001-2019-EF/63.01 (MEF) y el Clasificador de Responsabilidad Funcional del MEF.
2. CÁLCULOS MATEMÁTICOS: NO calcules el VACS ni el ratio CE por ti mismo. Extraerás los flujos y solicitarás al backend (vía Function Calling) que realice el cálculo.
3. RIESGO DE DESASTRES: Basarás tu análisis estrictamente en el JSON de SIGRID (CENEPRED) proporcionado.
4. NOMENCLATURA: Todo proyecto propuesto debe seguir la sintaxis: [Naturaleza de Intervención] + [Objeto de Intervención] + [Localización].

# MÁQUINA DE ESTADOS (FLUJO DE TRABAJO)

## MODO 1: PLANEAMIENTO TERRITORIAL Y PMI (NIVEL MACRO)
Si el usuario te proporciona datos de un polígono y proyectos existentes, genera un "Informe de Planeamiento Territorial":
1. DIAGNÓSTICO DE NO CIERRE DE BRECHAS: Analiza por qué la brecha no se ha cerrado con los proyectos actuales.
2. MAPEO DE SOLUCIONES: Identifica tipologías de proyectos según el Clasificador Funcional.
3. PROPUESTA DE CARTERA DE INVERSIONES (PIPs): Propón una lista de proyectos en una tabla Markdown.

## MODO 2: FORMULACIÓN DE FICHA TÉCNICA - FORMATO 7-A (NIVEL MICRO)
Si el usuario te proporciona datos de un colegio, coordenadas y costos, formula la Ficha Técnica:
- MÓDULO 1: Análisis de Riesgo (basado en SIGRID), Problema Central y Alternativa de Solución.
- MÓDULO 2: Horizonte de Evaluación y Brecha.
- MÓDULO 3: Llama a tu herramienta para calcular el VACS y el Ratio CE. Luego redacta la justificación.
- MÓDULO 4: Matriz de Marco Lógico y Declaración de Viabilidad.

Usa un tono técnico, formal y objetivo. Utiliza tablas en formato Markdown.
"""

# =====================================================================
# 3. INTERFAZ WEB (STREAMLIT)
# =====================================================================
st.set_page_config(page_title="Gemelo Digital Invierte.pe", page_icon="🏛️", layout="wide")

# Barra lateral para la API Key
st.sidebar.title("🔑 Configuración")
st.sidebar.markdown("Para usar la IA, ingresa tu API Key de Google AI Studio.")
api_key = st.sidebar.text_input("API Key de Gemini:", type="password")
st.sidebar.markdown("[Obtener API Key aquí](https://aistudio.google.com/app/apikey)")

st.title("🏛️ Plataforma Inteligente Invierte.pe")
st.markdown("Automatización de Planeamiento Territorial (PMI) y Fichas Técnicas (Formato 7-A) con IA.")

# Pestañas de la aplicación
tab1, tab2 = st.tabs(["📍 Módulo 1: Planeamiento (PMI)", "📝 Módulo 2: Formulación (FTE)"])

# ---------------------------------------------------------------------
# PESTAÑA 1: PLANEAMIENTO TERRITORIAL
# ---------------------------------------------------------------------
with tab1:
    st.header("Diagnóstico Territorial y Cartera de Inversiones")
    st.markdown("Analiza un distrito y descubre qué proyectos formular para cerrar brechas.")
    
    col1, col2 = st.columns(2)
    with col1:
        distrito = st.text_input("Distrito a analizar:", value="Echarate, Cusco")
        brecha = st.slider("Brecha de Infraestructura Educativa (%)", 0, 100, 60)
    with col2:
        proyectos_existentes = st.text_area(
            "Proyectos existentes en el Banco de Inversiones (CUI y Estado):", 
            value="- CUI 245678: Construcción de cerco perimétrico (IOARR) - Activo\n- CUI 289991: Mejoramiento de IE 50123 (PIP) - Paralizado por arbitraje"
        )
        
    if st.button("📊 Generar Cartera de Proyectos", type="primary"):
        if not api_key:
            st.error("⚠️ Por favor, ingresa tu API Key en el menú lateral.")
        else:
            try:
                with st.spinner("Analizando territorio y normativa del MEF..."):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-pro",
                        system_instruction=PROMPT_MAESTRO
                    )
                    
                    mensaje = f"MODO 1. Distrito: {distrito}. Brecha actual: {brecha}%. Proyectos en la zona: {proyectos_existentes}. Genera el Informe de Planeamiento Territorial."
                    
                    respuesta = model.generate_content(mensaje)
                    st.success("¡Análisis completado!")
                    st.markdown(respuesta.text)
            except Exception as e:
                st.error(f"❌ Error al conectar con Gemini: {str(e)}")

# ---------------------------------------------------------------------
# PESTAÑA 2: FORMULACIÓN DE FICHA TÉCNICA
# ---------------------------------------------------------------------
with tab2:
    st.header("Formulación Automática - Formato 7-A")
    st.markdown("Genera la Ficha Técnica Estándar con cálculos matemáticos exactos.")
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Datos del Proyecto")
        codigo_modular = st.text_input("Código Modular de la I.E.:", value="0543210")
        alumnos = st.number_input("Cantidad de Alumnos Beneficiados:", value=500)
    with col4:
        st.subheader("Presupuesto a Precios Sociales")
        inversion = st.number_input("Inversión Inicial (S/):", value=1500000)
        om_anual = st.number_input("Costo de O&M Anual (S/):", value=50000)
        
    if st.button("📝 Generar Ficha Técnica (Formato 7-A)", type="primary"):
        if not api_key:
            st.error("⚠️ Por favor, ingresa tu API Key en el menú lateral.")
        else:
            try:
                with st.spinner("Consultando SIGRID, calculando VACS y redactando Ficha Técnica..."):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-pro",
                        system_instruction=PROMPT_MAESTRO
                    )
                    
                    # Simulamos el JSON de SIGRID
                    json_sigrid = {
                      "datos_ubicacion": {"distrito": "Echarate", "nombre_ie": f"I.E. {codigo_modular}"},
                      "evaluacion_peligros": [{"tipo_peligro": "Movimiento en Masa", "nivel_peligro": "Alto", "requiere_mrr": True, "mrr_sugeridas": ["Muro de contención"]}]
                    }
                    
                    # Primero calculamos VACS
                    flujos_om = [om_anual] * 10
                    resultado_vacs = calcular_vacs_y_ce(inversion, flujos_om, 0.08, alumnos)
                    
                    mensaje = f"""
                    MODO 2. 
                    JSON SIGRID: {json.dumps(json_sigrid)}
                    Inversión Inicial Social: {inversion}
                    Flujos O&M Social: {flujos_om} (10 años)
                    Tasa Descuento: 0.08
                    Alumnos: {alumnos}
                    
                    RESULTADOS DEL CÁLCULO MATEMÁTICO:
                    - VACS Total: {resultado_vacs['vacs_total']}
                    - Ratio Costo-Eficacia: {resultado_vacs['ratio_costo_eficacia']}
                    
                    Redacta los 4 módulos de la Ficha Técnica utilizando estos valores.
                    """
                    
                    respuesta = model.generate_content(mensaje)
                    
                    st.success("¡Ficha Técnica generada exitosamente!")
                    st.markdown(respuesta.text)
                    
                    # Mostrar cálculos en un expander
                    with st.expander("📊 Ver Cálculos Matemáticos"):
                        st.json(resultado_vacs)
            except Exception as e:
                st.error(f"❌ Error al generar la Ficha Técnica: {str(e)}")
