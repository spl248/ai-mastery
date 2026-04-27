"""Módulo CrewAI optimizado para el bot de postulación."""
from crewai import LLM, Agent, Crew, Process, Task


def crear_equipo_postulacion(
    cv_text: str,
    keyword: str,
    location: str,
    model_name: str = "mistral",
) -> Crew:
    """Crea un equipo de agentes que genera una carta de presentación personalizada."""
    llm = LLM(model=f"ollama/{model_name}", base_url="http://localhost:11434")

    redactor = Agent(
        role="Redactor profesional de cartas de presentación",
        goal="Redactar una carta de presentación impecable, personalizada y convincente.",
        backstory=(
            "Eres un redactor senior con 15 años de experiencia en recursos humanos. "
            "Sabes exactamente qué buscan los reclutadores y cómo destacar las habilidades del candidato."
        ),
        llm=llm,
        verbose=False,
    )

    # Cargar el prompt desde el archivo YAML y rellenar los marcadores
    from ai_mastery.prompt_loader import get_prompt
    prompt_template = get_prompt("cover_letter_writer")
    prompt_filled = prompt_template.format(keyword=keyword, location=location, cv_text=cv_text)

    tarea_redactar = Task(
        description=prompt_filled,
        expected_output="Carta de presentación en texto plano, lista para enviar.",
        agent=redactor,
    )

    return Crew(
        agents=[redactor],
        tasks=[tarea_redactar],
        process=Process.sequential,
        verbose=False,
    )
