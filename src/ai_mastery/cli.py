"""CLI principal de ai-mastery."""
import click

@click.group()
def cli() -> None:
    """AI Mastery — Tu laboratorio de excelencia en IA."""
    pass

@cli.command()
def hello() -> None:
    """Comando de prueba."""
    click.echo("🔥 AI Mastery activado. Empieza la leyenda.")

if __name__ == "__main__":
    cli()
