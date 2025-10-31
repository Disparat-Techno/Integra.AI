from __future__ import annotations
import json
from pathlib import Path
from typing import Optional
import typer
from rich import print
from rich.table import Table

from .core.config import AppConfig
from .core.storage import list_integrations, save_integration_metadata, load_integration_metadata, slugify
from .core.generator import save_generated_code, render_python_client
from .core.testing import simple_request_test
from .ai.gemini import generate_code

app = typer.Typer(add_completion=False, help="Integra.AI - Automatize integrações com APIs usando IA generativa")


@app.command()
def init(
    project_name: str = typer.Option("Integra.AI", prompt=True, help="Nome do projeto"),
    language: str = typer.Option("python", prompt=True, help="Linguagem alvo (python|node)"),
    write_env: bool = typer.Option(True, help="Criar .env se não existir"),
):
    cfg = AppConfig(project_name=project_name, language=language)
    cfg.save()

    Path("integrations").mkdir(exist_ok=True)
    Path("profiles").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

    env_path = Path(".env")
    if write_env and not env_path.exists():
        env_path.write_text("GEMINI_API_KEY=\n", encoding="utf-8")
        print("[green]Criado .env (preencha GEMINI_API_KEY)[/green]")

    print(f"[bold green]Projeto inicializado:[/bold green] {cfg.project_name} | linguagem={cfg.language}")


@app.command()
def list():  # noqa: A001 - intentional name
    items = list_integrations()
    if not items:
        print("[yellow]Nenhuma integração encontrada.[/yellow]")
        raise typer.Exit(code=0)

    table = Table(title="Integrações")
    table.add_column("Nome")
    for name in items:
        table.add_row(name)
    print(table)


@app.command()
def ai(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Prompt para geração de código"),
    name: Optional[str] = typer.Option(None, help="Nome da integração (opcional)"),
    language: Optional[str] = typer.Option(None, help="Override de linguagem (python|node)"),
    model: str = typer.Option("gemini-1.5-flash", help="Modelo Gemini"),
):
    cfg = AppConfig.load()
    lang = language or cfg.language
    integ_name = name or slugify(prompt)[:40]

    code = generate_code(prompt=prompt, model=model)
    path = save_generated_code(integ_name, lang, code)

    meta = {"name": integ_name, "language": lang, "generated_file": str(path)}
    save_integration_metadata(integ_name, meta)

    print(f"[green]Código gerado e salvo em:[/green] {path}")


@app.command()
def connect(
    name: str = typer.Option(..., help="Nome da integração"),
    base_url: str = typer.Option(..., help="Base URL da API"),
    token: Optional[str] = typer.Option(None, help="Token/JWT (opcional)"),
):
    code = render_python_client(base_url=base_url, token=token)
    path = save_generated_code(name, "python", code)
    meta = {
        "name": name,
        "language": "python",
        "base_url": base_url,
        "generated_file": str(path),
        "auth": "Bearer" if token else "None",
    }
    save_integration_metadata(name, meta)
    print(f"[green]Cliente gerado em:[/green] {path}")


@app.command()
def test(
    name: str = typer.Option(..., help="Nome da integração"),
    endpoint: str = typer.Option("/", help="Endpoint para testar"),
    method: str = typer.Option("GET", help="Método HTTP"),
):
    meta = load_integration_metadata(name)
    if not meta:
        print("[red]Integração não encontrada.[/red]")
        raise typer.Exit(code=1)

    base_url = meta.get("base_url") or typer.prompt("Base URL")
    headers = {}
    if meta.get("auth") == "Bearer":
        headers["Authorization"] = "Bearer <TOKEN>"  # substitua pelo token real se necessário

    status, text = simple_request_test(base_url, endpoint, method, headers)
    print(f"[bold]Status:[/bold] {status}\n[text]\n{text[:1000]}\n[/text]")


if __name__ == "__main__":
    app()
