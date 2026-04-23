"""Módulo de automatización web con Playwright."""
from typing import Any, Optional

from playwright.sync_api import sync_playwright


def fetch_page_titles(url: str = "https://techcrunch.com/") -> Optional[list[str]]:
    """Extrae los títulos de los artículos de una página web.

    Args:
        url: URL de la página a analizar.

    Returns:
        Una lista de títulos o None si ocurre un error.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            page.wait_for_selector("h2 a, h3 a", timeout=10000)
            titles = page.eval_on_selector_all(
                "h2 a, h3 a",
                "elements => elements.map(el => el.textContent?.trim() || '')"
            )
            browser.close()
            return [t for t in titles if t]
    except Exception as e:
        print(f"❌ Error al extraer títulos: {e}")
        return None


def fetch_jobs(
    url: str = "https://remoteok.com/remote-python-jobs",
    job_selector: str = "tr.job",
    title_selector: str = "td.company_and_position_mobile a h2",
    company_selector: str = "td.company_and_position_mobile a h3",
    location_selector: str = "td.company_and_position_mobile div.location",
) -> list[dict[str, Any]]:
    """Extrae ofertas de empleo de una página web y las devuelve como lista de diccionarios.

    Args:
        url: URL de la página de ofertas.
        job_selector: Selector CSS para cada tarjeta de oferta.
        title_selector: Selector CSS para el título del puesto.
        company_selector: Selector CSS para el nombre de la empresa.
        location_selector: Selector CSS para la ubicación.

    Returns:
        Una lista de diccionarios con 'title', 'company', 'location' y 'link'.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            page.wait_for_selector(job_selector, timeout=10000)
            job_cards = page.query_selector_all(job_selector)
            jobs = []
            for card in job_cards[:10]:
                title_el = card.query_selector(title_selector)
                company_el = card.query_selector(company_selector)
                location_el = card.query_selector(location_selector)
                link_el = card.query_selector("a")
                job = {
                    "title": title_el.inner_text().strip() if title_el else "N/A",
                    "company": company_el.inner_text().strip() if company_el else "N/A",
                    "location": location_el.inner_text().strip() if location_el else "N/A",
                    "link": link_el.get_attribute("href") if link_el else url,
                }
                jobs.append(job)
            browser.close()
            return jobs
    except Exception as e:
        print(f"❌ Error al extraer ofertas: {e}")
        return []


def save_jobs_to_json(jobs: list[dict[str, Any]], filename: str = "jobs.json") -> bool:
    """Guarda una lista de ofertas de empleo en un archivo JSON.

    Args:
        jobs: Lista de diccionarios con las ofertas.
        filename: Nombre del archivo de salida.

    Returns:
        True si se guardó correctamente, False en caso de error.
    """
    import json
    from datetime import datetime

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "count": len(jobs),
                "jobs": jobs
            }, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(jobs)} ofertas guardadas en {filename}")
        return True
    except Exception as e:
        print(f"❌ Error al guardar JSON: {e}")
        return False
