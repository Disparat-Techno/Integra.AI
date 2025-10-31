# Integra.AI

Integra.AI é um aplicativo (CLI + Web) para automatizar integrações com APIs usando IA generativa (Google Gemini). Ele interpreta documentação de APIs e gera código de integração (Python/Node), scripts de teste e exemplos.

## Funcionalidades
- CLI inteligente: `init`, `ai`, `connect`, `list`, `test`
- Painel Web (Flask) para listar e gerar integrações
- Integração com Google Generative Language API (Gemini)
- Geração de clientes e exemplos (templates Python)
- Logs locais e armazenamento de perfis/integrações

## Requisitos
- Python 3.11+
- Chave da Google Generative Language API (Gemini)

## Instalação (desenvolvimento)
```powershell
python -m venv .venv
.venv\Scripts\pip install -U pip
.venv\Scripts\pip install -e .
```

Crie `.env` na raiz (NÃO comitar) com:
```
GEMINI_API_KEY=
```

## Instalação global (Windows, via pipx)
1) Gere os artefatos:
```powershell
.venv\Scripts\python -m pip install -U build
.venv\Scripts\python -m build
```
2) Instale com pipx:
```powershell
py -m pip install --user pipx
py -m pipx ensurepath
pipx install .\dist\integra_ai-0.1.0-py3-none-any.whl
```
Depois, adicione `C:\Users\SEU_USUARIO\.local\bin` ao PATH se necessário.

## Uso (CLI)
```powershell
integra --help
integra init --project-name "Integra.AI" --language python
$env:GEMINI_API_KEY="<SUA_CHAVE>"; integra ai --prompt "Gerar integração com a API Uber Direct"
```

## Servidor Web (Flask)
```powershell
.venv\Scripts\python -m flask --app web.app run --debug
```

## VS Code
- `.vscode/settings.json` usa o interpretador `.venv` automaticamente.
- `.vscode/tasks.json` inclui tarefas para `integra`.

## Segurança
- NUNCA comite `.env` (já está no `.gitignore`).
- Use HTTPS e mantenha a chave em variável de ambiente.

## Dependências
```
requests typer python-dotenv flask rich pydantic structlog
```

## Exemplo de Prompt para IA (CLI)
```
Você é uma IA de integração de APIs.
Analise a seguinte documentação: [cole o texto ou URL]
Crie automaticamente o código Python de integração completo,
com autenticação, tratamento de erros e testes.
```

## Licença
MIT
