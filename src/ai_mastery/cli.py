"""CLI principal de ai-mastery."""
import os
import click
from ai_mastery.utils import timer

@click.group()
def cli() -> None:
    """AI Mastery — Tu laboratorio de excelencia en IA."""
    pass

@cli.command()
def hello() -> None:
    """Comando de prueba."""
    click.echo("🔥 AI Mastery activado. Empieza la leyenda.")

@cli.command()
@click.argument("nombre_proyecto")
def init(nombre_proyecto: str) -> None:
    """Crea un nuevo proyecto con plantilla básica."""
    if os.path.exists(nombre_proyecto):
        click.echo(f"❌ Error: La carpeta '{nombre_proyecto}' ya existe.")
        return
    
    os.makedirs(f"{nombre_proyecto}/src")
    
    with open(f"{nombre_proyecto}/README.md", "w", encoding="utf-8") as f:
        f.write(f"# {nombre_proyecto}\n\nProyecto creado con AI Mastery.\n")
    
    click.echo(f"✅ Proyecto '{nombre_proyecto}' creado con éxito.")
    click.echo(f"   Estructura: {nombre_proyecto}/src/")

@cli.command()
def test() -> None:
    """Ejecuta los tests del proyecto con pytest."""
    import subprocess
    import sys
    
    click.echo("🧪 Ejecutando tests...\n")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/"], capture_output=False)
    
    if result.returncode == 0:
        click.echo("\n✅ Todos los tests pasaron.")
    else:
        click.echo("\n❌ Algunos tests fallaron. Revisa la salida anterior.")
        sys.exit(result.returncode)

@cli.command()
@click.argument("script", required=False)
@timer
def run(script: str | None = None) -> None:
    """Ejecuta un script de demostración. Si no se especifica, ejecuta demo.py."""
    import subprocess
    import sys
    
    if script is None:
        script = "scripts/demo.py"
    
    if not os.path.exists(script):
        click.echo(f"❌ Error: El script '{script}' no existe.")
        sys.exit(1)
    
    click.echo(f"🚀 Ejecutando script: {script}\n")
    result = subprocess.run([sys.executable, script], capture_output=False)
    
    if result.returncode == 0:
        click.echo(f"\n✅ Script '{script}' ejecutado con éxito.")
    else:
        click.echo(f"\n❌ El script '{script}' falló con código {result.returncode}.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    cli()