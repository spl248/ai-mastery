"""Flujo de Prefect para ejecutar el bot de postulación diariamente."""
from prefect import flow, task
from prefect.logging import get_run_logger
from ai_mastery import bot_integrator


@task(retries=2, retry_delay_seconds=30)
def ejecutar_bot(cv_path: str, keyword: str, location: str) -> list[dict]:
    """Tarea que ejecuta el bot de postulación."""
    logger = get_run_logger()
    logger.info(f"Iniciando bot con CV={cv_path}, keyword={keyword}, location={location}")
    try:
        resultados = bot_integrator.run_bot(cv_path=cv_path, keyword=keyword, location=location)
        logger.info(f"Bot finalizado. {len(resultados)} cartas generadas.")
        return resultados
    except Exception as e:
        logger.warning(f"No se pudo ejecutar el bot (posiblemente Ollama no disponible): {e}")
        return []


@flow(name="Bot de Postulación Diario", description="Ejecuta el bot de postulación y notifica los resultados.")
def bot_diario(
    cv_path: str = "cv.txt",
    keyword: str = "python",
    location: str = "Madrid",
) -> list[dict]:
    """Flujo diario del bot de postulación."""
    logger = get_run_logger()
    logger.info("Flujo diario iniciado.")
    resultados = ejecutar_bot(cv_path, keyword, location)
    logger.info(f"Flujo completado: {len(resultados)} cartas generadas.")
    return resultados


if __name__ == "__main__":
    bot_diario()