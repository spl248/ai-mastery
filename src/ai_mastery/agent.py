"""Agente inteligente con LangChain y Ollama (LangChain 0.3.x con AgentExecutor)."""
import math

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


@tool
def calculator(expression: str) -> str:
    """Evalúa una expresión matemática y devuelve el resultado."""
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names["__builtins__"] = {}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error al calcular: {e}"


@tool
def web_search(query: str) -> str:
    """Busca información en internet sobre una consulta."""
    return f"[Resultados simulados para: '{query}'] Esta es una búsqueda de demostración."


def create_agent(model: str = "llama3.2") -> AgentExecutor:
    """Crea un agente LangChain con herramientas de cálculo y búsqueda.
    Devuelve un AgentExecutor listo para recibir preguntas.
    """
    llm = ChatOllama(model=model, temperature=0)
    tools = [calculator, web_search]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente útil. Usa las herramientas disponibles si es necesario."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=5,
    )
    return agent_executor


def ask_agent(question: str, model: str = "llama3.2") -> str:
    """Envía una pregunta al agente y devuelve la respuesta."""
    agent_executor = create_agent(model)
    result = agent_executor.invoke({"input": question})
    return str(result["output"])
