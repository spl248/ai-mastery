"""Módulo de equipo de agentes con CrewAI para postulación."""
import json

from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import tool


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
    """Crea un equipo CrewAI con tres agentes para postular a ofertas."""
    llm = LLM(
        model=f"ollama/{model}",
        base_url="http://localhost:11434",
    )

    buscador = Agent(
        role="Buscador de ofertas de empleo",
        goal=f"Encontrar las mejores ofertas para {keyword} en {location}",
        backstory="Eres un experto en búsqueda de empleo que usa web scraping.",
        tools=[buscar_ofertas],
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    analista = Agent(
        role="Analista de CV",
        goal="Extraer las habilidades clave y experiencia relevante del CV del candidato",
        backstory="Eres un reclutador experimentado que analiza currículums con precisión.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    redactor = Agent(
        role="Redactor de cartas de presentación",
        goal="Redactar una carta personalizada para una oferta basada en el CV",
        backstory="Eres un escritor profesional especializado en cartas de motivación.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    tarea_buscar = Task(
        description=(
            f"Busca ofertas de empleo para '{keyword}' en '{location}'. "
            "Devuelve los resultados en formato JSON con título, empresa, ubicación y enlace."
        ),
        expected_output="Lista de ofertas en formato JSON con título, empresa, ubicación y enlace.",
        agent=buscador,
    )

    tarea_analizar = Task(
        description=(
            f"Analiza el siguiente CV y extrae sus habilidades clave:\n\n{cv_text}"
        ),
        expected_output="Resumen de habilidades clave del candidato.",
        agent=analista,
    )

    tarea_redactar = Task(
        description=(
            "Selecciona la oferta más relevante de las encontradas y redacta una carta "
            "de presentación personalizada para el candidato cuyo CV fue analizado. "
            "La carta debe mencionar la empresa, el puesto, y destacar "
            "las habilidades del candidato."
        ),
        expected_output="Una carta de presentación en formato texto.",
        agent=redactor,
        context=[tarea_buscar, tarea_analizar],
    )

    crew = Crew(
        agents=[buscador, analista, redactor],
        tasks=[tarea_buscar, tarea_analizar, tarea_redactar],
        process=Process.sequential,
        verbose=False,
    )

    return crew
