"""Módulo integrador del bot de postulación con logs detallados."""
import logging
from datetime import datetime
from typing import Any

from ai_mastery import crew_module
from ai_mastery.scraper_web import fetch_jobs

# Configurar el logger
log = logging.getLogger("bot_integrator")
log.setLevel(logging.INFO)
if not log.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S")
    )
    log.addHandler(handler)


def run_bot(
    cv_path: str,
    keyword: str,
    location: str = "Madrid",
    model: str = "mistral",
) -> list[dict[str, Any]]:
    """Ejecuta el bot completo en modo simulación y devuelve los resultados con logs.

    Args:
        cv_path: Ruta al archivo de texto con el CV.
        keyword: Palabra clave para buscar ofertas.
        location: Ubicación de las ofertas.
        model: Modelo de Ollama a usar.

    Returns:
        Lista de diccionarios con 'job', 'cover_letter' y 'logs'.
    """
    log_msg = (
        f"🤖 Iniciando bot de postulación. "
        f"CV: {cv_path}, keyword: {keyword}, location: {location}"
    )
    log.info(log_msg)

    # 1. Leer el CV
    log.info("📄 Leyendo el CV...")
    try:
        with open(cv_path, "r", encoding="utf-8") as f:
            cv_text = f.read()
        log.info(f"✅ CV leído correctamente ({len(cv_text)} caracteres).")
    except FileNotFoundError:
        log.error(f"❌ No se encontró el archivo de CV: {cv_path}")
        return []

    # 2. Extraer ofertas
    log.info(f"🌐 Buscando ofertas para '{keyword}' en '{location}'...")
    url = f"https://remoteok.com/remote-{keyword.replace(' ', '-')}-jobs"
    jobs = fetch_jobs(url=url)
    if not jobs:
        log.warning("⚠️ No se encontraron ofertas.")
        return []
    log.info(f"✅ {len(jobs)} ofertas encontradas.")

    # 3. Generar cartas para cada oferta con el equipo CrewAI
    results = []
    for i, job in enumerate(jobs[:3], 1):
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        log.info(
            f"✍️ Generando carta para oferta {i}/{min(3, len(jobs))}: "
            f"{title} en {company}"
        )
        try:
            crew = crew_module.crear_equipo_postulacion(
                cv_text, keyword, location, model
            )
            carta = str(crew.kickoff())
            results.append({
                "job": job,
                "cover_letter": carta,
                "timestamp": datetime.now().isoformat(),
            })
            log.info(f"✅ Carta generada para {company}.")
        except Exception as e:
            log.error(f"❌ Error generando carta para {company}: {e}")
            results.append({
                "job": job,
                "cover_letter": f"Error: {e}",
                "timestamp": datetime.now().isoformat(),
            })

    log.info(f"🏁 Bot finalizado. {len(results)} cartas generadas.")
    return results
