from __future__ import annotations
from flask import Flask, jsonify, request, render_template # Importar render_template
from dotenv import load_dotenv
from pathlib import Path

from integra_ai.core.storage import list_integrations, save_integration_metadata
from integra_ai.core.generator import save_generated_code, render_python_client
from integra_ai.ai.gemini import generate_code
from integra_ai.core.config import AppConfig

load_dotenv()

app = Flask(__name__)


@app.get("/")
def index():
    # Renderizar o template HTML para a interface do usuário
    return render_template("index.html")


@app.get("/api/integrations")
def api_list():
    return jsonify({"items": list_integrations()})


@app.post("/api/generate")
def api_generate():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt")
    name = data.get("name")
    # Obter o modelo da requisição ou usar "gemini-1.5-flash" como padrão
    model_to_use = data.get("model", "gemini-1.5-flash")

    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    cfg = AppConfig.load()
    integ_name = name or "integration"
    code = None
    try:
        code = generate_code(prompt, model=model_to_use)  # Passar o modelo explicitamente
    except Exception as e:  # fallback offline
        # Produce a minimal client template as a stub
        code = render_python_client(base_url="https://httpbin.org", token=None)
    path = save_generated_code(integ_name, cfg.language, code)
    save_integration_metadata(integ_name, {"generated_file": str(path), "language": cfg.language})
    return jsonify({"saved_to": str(path)})
