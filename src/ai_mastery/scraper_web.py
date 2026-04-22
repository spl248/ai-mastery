"""Módulo de automatización web con Playwright."""
from playwright.sync_api import sync_playwright
from typing import Optional


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
            # Esperar a que los títulos estén visibles
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