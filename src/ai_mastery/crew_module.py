"""Módulo de equipo de agentes con CrewAI para postulación."""
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import json


@tool
def buscar_ofertas(keyword: str, location: str = "Madrid") -> str:
    """Busca ofertas de empleo para una keyword y ubicación."""
    from ai_mastery.scraper_web import fetch_jobs
    url = f"https://remoteok.com/remote-{keyword.replace(' ', '-')}-jobs"
    jobs = fetch_jobs(url=url)
    if not jobs:
        return "No se encontraron ofertas."
    return json.dumps(jobs, ensure_ascii=False, indent=2)


def crear_equipo_postulacion(
    cv_text: str,
    keyword: str,
    location: str = "Madrid",
    model: str = "mistral",
):
    """Crea un equipo CrewAI con tres agentes para postular a ofertas.

    Args:
        cv_text: Contenido del CV del candidato.
        keyword: Palabra clave para buscar ofertas (ej. 'python desarrollador').
        location: Ubicación de las ofertas.
        model: Modelo de Ollama a usar.

    Returns:
        Un objeto Crew listo para ejecutar.
    """
    # Configurar el LLM de Ollama (API moderna de CrewAI 1.x)
    llm = LLM(
        model=f"ollama/{model}",
        base_url="http://localhost:11434",
    )

    # Agente 1: Buscador de ofertas
    buscador = Agent(
        role="Buscador de ofertas de empleo",
        goal=f"Encontrar las mejores ofertas para {keyword} en {location}",
        backstory="Eres un experto en búsqueda de empleo que usa herramientas de web scraping.",
        tools=[buscar_ofertas],
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    # Agente 2: Analista de CV
    analista = Agent(
        role="Analista de CV",
        goal="Extraer las habilidades clave y experiencia relevante del CV del candidato",
        backstory="Eres un reclutador experimentado que analiza currículums con precisión.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    # Agente 3: Redactor de cartas de presentación
    redactor = Agent(
        role="Redactor de cartas de presentación",
        goal="Redactar una carta de presentación personalizada para una oferta específica basada en el CV del candidato",
        backstory="Eres un escritor profesional especializado en cartas de motivación.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    # Tarea 1: Buscar ofertas
    tarea_buscar = Task(
        description=f"Busca ofertas de empleo para '{keyword}' en '{location}'. "
                    f"Devuelve los resultados en formato JSON con título, empresa, ubicación y enlace.",
        expected_output="Lista de ofertas en formato JSON con título, empresa, ubicación y enlace.",
        agent=buscador,
    )

    # Tarea 2: Analizar CV
    tarea_analizar = Task(
        description=f"Analiza el siguiente CV y extrae sus principales habilidades, experiencia y puntos fuertes:\n\n{cv_text}",
        expected_output="Resumen de habilidades clave del candidato.",
        agent=analista,
    )

    # Tarea 3: Redactar carta
    tarea_redactar = Task(
        description="Selecciona la oferta más relevante de las encontradas y redacta una carta de presentación "
                    "personalizada para el candidato cuyo CV fue analizado. La carta debe mencionar la empresa, "
                    "el puesto, y destacar las habilidades del candidato que encajan con la oferta.",
        expected_output="Una carta de presentación en formato texto, dirigida al responsable de contratación de la empresa.",
        agent=redactor,
        context=[tarea_buscar, tarea_analizar],
    )

    # Crear el equipo con proceso secuencial
    crew = Crew(
        agents=[buscador, analista, redactor],
        tasks=[tarea_buscar, tarea_analizar, tarea_redactar],
        process=Process.sequential,
        verbose=False,
    )

    return crew