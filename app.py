"""Dashboard del Bot de Postulación – AI Mastery Día 15."""
import streamlit as st
import sys
import os
import tempfile
from datetime import datetime

# Añadir la carpeta src/ al path para que el contenedor Docker encuentre ai_mastery
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

def main():
    st.set_page_config(page_title="AI Mastery Bot Dashboard", page_icon="🤖")
    st.title("🤖 Panel de Control – Bot de Postulación Autónomo")
    st.markdown("Monitoriza y ejecuta el bot de postulación desde aquí. **Modo simulación** (no se envían postulaciones reales).")

    with st.sidebar:
        st.header("⚙️ Configuración")
        cv_text_input = st.text_area(
            "Pega aquí el texto de tu CV",
            height=200,
            placeholder="Desarrollador Python con experiencia en automatización, IA y web scraping..."
        )
        keyword = st.text_input("Keyword", value="python")
        location = st.text_input("Location", value="Madrid")
        run_btn = st.button("🚀 Ejecutar Bot", type="primary")

    if run_btn:
        if not cv_text_input.strip():
            st.error("Por favor, pega el texto de tu CV.")
            return

        # Guardar el texto del CV en un archivo temporal
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", dir="/tmp", encoding="utf-8") as tmp:
            tmp.write(cv_text_input)
            cv_path = tmp.name
        st.success("CV almacenado temporalmente.")

        from ai_mastery import bot_integrator

        with st.spinner("Ejecutando bot... esto puede tardar unos minutos ⏳"):
            try:
                results = bot_integrator.run_bot(cv_path, keyword, location)
            except Exception as e:
                st.exception(e)
                results = None

        os.unlink(cv_path)

        if not results:
            st.warning("No se generaron cartas. Revisa los parámetros o la disponibilidad de ofertas.")
            return

        st.success(f"✅ Bot finalizado. {len(results)} cartas generadas.")
        for i, res in enumerate(results, 1):
            with st.expander(f"📩 Postulación {i}: {res['job'].get('title', 'N/A')} en {res['job'].get('company', 'N/A')}"):
                st.text(f"Timestamp: {res['timestamp']}")
                st.markdown("**Carta de presentación (primeros 500 caracteres):**")
                st.code(str(res['cover_letter'])[:500])

    st.markdown("---")
    st.caption(f"Ejecución actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()