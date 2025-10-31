# Integra.AI

[![CI](https://github.com/Disparat-Techno/Integra.AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Disparat-Techno/Integra.AI/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Disparat-Techno/Integra.AI?display_name=tag)](https://github.com/Disparat-Techno/Integra.AI/releases)

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

---

## Comandos CLI (uso completo)

- Ajuda geral:
  - `integra --help`
- Inicializar projeto:
  - `integra init --project-name "Integra.AI" --language python`
- Gerar código via IA (Gemini):
  - `integra ai --prompt "<seu prompt>"`
  - Opções úteis: `--name <nome-integracao>` `--language python|node` `--model gemini-pro`
- Criar cliente Python "manual" apontando para uma API:
  - `integra connect --name <nome> --base-url https://api.exemplo.com --token <JWT_OPCIONAL>`
- Listar integrações existentes:
  - `integra list`
- Testar uma integração (requisição simples):
  - `integra test --name <nome> --endpoint /status --method GET`

### Exemplos rápidos (PowerShell)
- Definir chave e gerar com IA:
  - `$env:GEMINI_API_KEY="<SUA_CHAVE>"; integra ai --prompt "Gerar integração com a API Uber Direct"`
- Testar endpoint após `connect`:
  - `integra test --name meu-cliente --endpoint / --method GET`

### Variáveis de ambiente
- PowerShell (Windows):
  - `$env:GEMINI_API_KEY="<SUA_CHAVE>"`
- CMD (Windows, sessão atual):
  - `set GEMINI_API_KEY=<SUA_CHAVE>`
- Bash (Linux/Mac):
  - `export GEMINI_API_KEY=<SUA_CHAVE>`

## API Web (Flask)
- Iniciar servidor:
  - `python -m flask --app web.app run --debug`
- Endpoints:
  - `GET /` → status
  - `GET /api/integrations` → lista integrações
  - `POST /api/generate` → gera código
    - Body JSON:
      ```json
      {"prompt":"Gerar integração com X","name":"minha-integracao"}
      ```

## Instalação Global (pipx)
- Construir e instalar:
  - `python -m pip install -U build && python -m build`
  - `pipx install .\\dist\\integra_ai-0.1.0-py3-none-any.whl`
- Se necessário: adicionar `C:\\Users\\SEU_USUARIO\\.local\\bin` ao PATH.

## Troubleshooting
- 401/404 ao chamar Gemini:
  - Verifique `GEMINI_API_KEY` definida no ambiente da sessão que executa `integra`.
  - Confirme o modelo (`--model gemini-pro`) e conectividade HTTPS.
- Sem `integra` no terminal após pipx:
  - Rode `pipx ensurepath` e abra um novo terminal.

## Screenshots
<img width="982" height="515" alt="image" src="https://github.com/user-attachments/assets/d54aacf0-93c9-450d-b830-67012d14a314" />

<img width="1361" height="723" alt="image" src="https://github.com/user-attachments/assets/695e79a3-bead-4ccb-8292-23603c55eab0" />

<img width="922" height="128" alt="image" src="https://github.com/user-attachments/assets/409b761b-4817-4cc7-b94e-fcd51470458f" />

<img width="1365" height="767" alt="image" src="https://github.com/user-attachments/assets/e90e2189-601d-4256-bd96-c32f7b68b64e" />

<img width="1363" height="727" alt="image" src="https://github.com/user-attachments/assets/41293fd4-0c1d-4b96-87e0-86d79f3509c0" />




## Créditos e Contato
- Programador: Julio Campos Machado
- Empresa: Like Look Solutions
- Site: https://likelook.wixsite.com/solutions
- Contatos: (11) 97060-3441 / (11) 99294-6628
