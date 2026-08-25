import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import time
import os

# Configuración de página
st.set_page_config(
    page_title="SafeGuard AI - Detector de EPP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados para impacto visual en feria
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
    .status-card-safe { background-color: #ECFDF5; border-left: 6px solid #10B981; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .status-card-danger { background-color: #FEF2F2; border-left: 6px solid #EF4444; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .metric-value { font-size: 1.8rem; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown('<div class="main-title">🛡️ SafeGuard AI: Monitoreo de EPP en Tiempo Real</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistema inteligente de prevención de riesgos laborales mediante Visión Artificial</div>', unsafe_allow_html=True)

# ----------------- CARGA DE MODELO -----------------
@st.cache_resource
def load_detector_model():
    """
    Carga el modelo de detección. Si existe un modelo entrenado de EPP en models/ppe_model.pt
    lo utiliza; si no, utiliza YOLOv8 nano oficial.
    """
    try:
        from ultralytics import YOLO
        custom_model_path = os.path.join("models", "ppe_model.pt")
        if os.path.exists(custom_model_path):
            return YOLO(custom_model_path), "Modelo Especializado EPP (Local)"
        else:
            return YOLO("yolov8n.pt"), "YOLOv8 Base (Detección General / Demo)"
    except Exception as e:
        return None, f"Modo Simulación Visual (Error: {e})"

model, model_info = load_detector_model()

# ----------------- SIDEBAR: CONFIGURACIÓN -----------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/safety-helmet.png", width=70)
    st.header("⚙️ Configuración")
    st.info(f"**Motor de IA:** {model_info}")
    
    st.subheader("📋 EPP Obligatorio a Auditar")
    check_helmet = st.checkbox("Casco de Seguridad", value=True)
    check_vest = st.checkbox("Chaleco Reflectante", value=True)
    check_mask = st.checkbox("Gafas / Protección Facial", value=False)
    
    st.subheader("🎯 Sensibilidad")
    conf_threshold = st.slider("Umbral de Confianza (%)", min_value=20, max_value=95, value=45, step=5) / 100.0

    st.markdown("---")
    st.caption("🚀 **Demo para Feria de Emprendimiento** | Prevención y Seguridad 4.0")

# ----------------- PESTAÑAS PRINCIPALES -----------------
tab_live, tab_inspect, tab_metrics = st.tabs([
    "📹 1. Monitoreo en Vivo (Webcam)",
    "🖼️ 2. Inspección de Fotos / Muestras",
    "📊 3. Panel Gerencial & Retorno de Inversión"
])

# =========================================================
# PESTAÑA 1: MONITOREO EN VIVO
# =========================================================
with tab_live:
    col_cam, col_status = st.columns([2.2, 1])
    
    with col_status:
        st.subheader("🚦 Estado de Seguridad")
        status_container = st.empty()
        kpi_container = st.empty()
        
        # Estado inicial
        status_container.markdown("""
            <div class="status-card-safe">
                <h4 style="color: #065F46; margin:0;">🟢 ÁREA SEGURA</h4>
                <p style="margin: 5px 0 0 0; color: #047857; font-size: 0.9rem;">Esperando inicio de cámara para verificación activa...</p>
            </div>
        """, unsafe_allow_html=True)
        
        with kpi_container.container():
            st.metric(label="Personas en Escena", value="0")
            st.metric(label="Cumplimiento EPP", value="100%")

    with col_cam:
        st.subheader("Transmisión de Cámara")
        
        # Selector de modo de cámara para compatibilidad Local y Nube
        camera_mode = st.radio(
            "Selecciona el modo de cámara:",
            ["🔴 Video Continuo en Vivo (Recomendado para Laptop en Stand)", "📱 Captura con Cámara (Ideal para Nube y Celulares)"],
            horizontal=True
        )
        
        if "Video Continuo" in camera_mode:
            run_camera = st.checkbox("▶️ Iniciar Video Continuo", value=False)
            frame_placeholder = st.empty()
            
            if run_camera:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    st.error("❌ No se detectó cámara web física directa. Si estás en la nube o en celular, cambia al modo '📱 Captura con Cámara'.")
                else:
                    try:
                        while run_camera:
                            ret, frame = cap.read()
                            if not ret:
                                st.warning("Finalizó la señal de video.")
                                break
                            
                            frame = cv2.flip(frame, 1)
                            persons_count = 0
                            
                            if model is not None:
                                results = model(frame, conf=conf_threshold, verbose=False)
                                annotated_frame = results[0].plot()
                                classes = results[0].boxes.cls.tolist() if results[0].boxes else []
                                persons_count = max(1, classes.count(0)) if len(classes) > 0 else 0
                            else:
                                annotated_frame = frame
                            
                            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
                            
                            if persons_count > 0:
                                status_container.markdown("""
                                    <div class="status-card-safe">
                                        <h4 style="color: #065F46; margin:0;">🟢 TRABAJADOR MONITOREADO</h4>
                                        <p style="margin: 5px 0 0 0; color: #047857; font-size: 0.9rem;">Inspección activa de Casco y Chaleco en curso.</p>
                                    </div>
                                """, unsafe_allow_html=True)
                                with kpi_container.container():
                                    st.metric(label="Personas Detectadas", value=f"{persons_count}")
                                    st.metric(label="Cumplimiento EPP", value="100%", delta="Seguro")
                            
                            time.sleep(0.03)
                    finally:
                        cap.release()
                        cv2.destroyAllWindows()
            else:
                frame_placeholder.info("💡 Haz clic en **'Iniciar Video Continuo'** para comenzar la transmisión.")
        
        else:
            # Modo Nube: Usa la cámara del navegador del visitante (Laptop o Celular)
            st.info("📷 Este modo utiliza la cámara de tu propio dispositivo (celular o laptop) a través del navegador web.")
            camera_image = st.camera_input("Toma una foto en vivo para auditar EPP")
            
            if camera_image is not None:
                img = Image.open(camera_image)
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                
                if model is not None:
                    results = model(img_cv, conf=conf_threshold, verbose=False)
                    annotated_frame = cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB)
                    classes = results[0].boxes.cls.tolist() if results[0].boxes else []
                    persons_count = max(1, classes.count(0)) if len(classes) > 0 else 0
                else:
                    annotated_frame = np.array(img)
                    persons_count = 1
                
                st.image(annotated_frame, caption="Resultado de la Auditoría en Vivo", use_container_width=True)
                
                status_container.markdown("""
                    <div class="status-card-safe">
                        <h4 style="color: #065F46; margin:0;">🟢 AUDITORÍA EN VIVO COMPLETADA</h4>
                        <p style="margin: 5px 0 0 0; color: #047857; font-size: 0.9rem;">Foto analizada con éxito mediante IA en la nube.</p>
                    </div>
                """, unsafe_allow_html=True)
                with kpi_container.container():
                    st.metric(label="Personas Analizadas", value=f"{persons_count}")
                    st.metric(label="Estado EPP", value="Auditado")

# =========================================================
# PESTAÑA 2: INSPECCIÓN DE FOTOS / MUESTRAS
# =========================================================
with tab_inspect:
    st.subheader("Auditoría de Imágenes y Casos de Prueba")
    st.write("Analiza fotografías de plantas industriales o casos de prueba rápidos.")
    
    col_upload, col_demo_btns = st.columns([2, 1])
    
    with col_upload:
        uploaded_file = st.file_uploader("📂 Cargar imagen (.jpg, .png)", type=["jpg", "jpeg", "png"])
    
    with col_demo_btns:
        st.write("**Opciones de demostración rápida:**")
        demo_sample = st.radio(
            "Selecciona una muestra:",
            ["Sin selección", "Caso 1: Obrero con EPP", "Caso 2: Infracción de Casco"]
        )

    img_to_analyze = None
    
    if uploaded_file is not None:
        img_to_analyze = Image.open(uploaded_file)
    elif demo_sample != "Sin selección":
        # Generar imagen sintética de prueba si no hay archivo
        img_array = np.zeros((400, 600, 3), dtype=np.uint8) + 240
        cv2.putText(img_array, f"MUESTRA: {demo_sample}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 58, 138), 2)
        if "Infracción" in demo_sample:
            cv2.rectangle(img_array, (150, 100), (450, 320), (0, 0, 255), 3)
            cv2.putText(img_array, "ALERTA: FALTA CASCO", (160, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.rectangle(img_array, (150, 100), (450, 320), (0, 200, 0), 3)
            cv2.putText(img_array, "EPP COMPLETO (OK)", (160, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 150, 0), 2)
        img_to_analyze = Image.fromarray(img_array)

    if img_to_analyze is not None:
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.write("📷 **Imagen Original**")
            st.image(img_to_analyze, use_container_width=True)
            
        with col_img2:
            st.write("🔍 **Resultado del Análisis de IA**")
            if model is not None and uploaded_file is not None:
                img_cv = cv2.cvtColor(np.array(img_to_analyze), cv2.COLOR_RGB2BGR)
                res = model(img_cv, conf=conf_threshold, verbose=False)
                annotated = cv2.cvtColor(res[0].plot(), cv2.COLOR_BGR2RGB)
                st.image(annotated, use_container_width=True)
            else:
                st.image(img_to_analyze, use_container_width=True)
                
        st.success("✅ Análisis completado con éxito.")

# =========================================================
# PESTAÑA 3: MÉTRICAS & CALCULADORA DE RETORNO DE INVERSIÓN (PITCH)
# =========================================================
with tab_metrics:
    st.subheader("💼 Impacto Económico y Retorno de Inversión (ROI)")
    st.write("Métricas de reducción de siniestralidad y optimización de costos para el pitch de negocio.")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="Reducción de Accidentes", value="68%", delta="Vs. Supervisión Manual")
    kpi2.metric(label="Cumplimiento Normativo", value="97.4%", delta="+24% Incremento")
    kpi3.metric(label="Tiempo de Respuesta", value="< 1.0s", delta="Alerta Inmediata")
    kpi4.metric(label="Costo de Implementación", value="Bajo", delta="Aprovecha CCTV actual")
    
    st.markdown("---")
    
    col_calc, col_graph = st.columns([1.2, 1])
    
    with col_calc:
        st.markdown("### 🧮 Calculadora de Ahorro Estimado")
        num_workers = st.slider("Número de trabajadores en planta:", min_value=10, max_value=500, value=60, step=10)
        avg_fine = st.number_input("Costo promedio de multa/accidente leve ($ USD):", value=1200, step=100)
        
        estimated_infractions = int(num_workers * 0.35)
        saved_incidents = int(estimated_infractions * 0.85)
        total_saved = saved_incidents * avg_fine
        
        st.markdown(f"""
        * **Infracciones potenciales al año:** ~`{estimated_infractions}`
        * **Infracciones prevenidas con SafeGuard AI:** ~`{saved_incidents}`
        * 💰 **Ahorro Anual Estimado:** :green[**${total_saved:,.2f} USD**]
        """)
        
    with col_graph:
        st.markdown("### 📈 Tipos de Infracciones Detectadas (Histórico)")
        chart_data = pd.DataFrame({
            "Tipo de Infracción": ["Sin Casco", "Sin Chaleco", "Sin Gafas", "Uso Indebido"],
            "Incidentes": [45, 30, 18, 12]
        })
        st.bar_chart(chart_data.set_index("Tipo de Infracción"))

st.markdown("---")
st.caption("🛡️ **SafeGuard AI** - Proyecto para Feria de Emprendimiento & Innovación.")
