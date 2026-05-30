# AI Army Backend

Small Flask API for deploying local AI Army agent prompts through Anthropic.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
$env:ANTHROPIC_API_KEY = "replace_with_your_rotated_key"
python server.py
```

## Endpoints

- `GET /` - human-readable backend home
- `GET /health` - human-readable health page
- `GET /agents` - human-readable agent directory
- `GET /agents/<agent_id>` - human-readable agent detail page
- `POST /agents/<agent_id>/deploy` - human-readable deploy result
- `GET /api/health` - JSON health endpoint
- `GET /api/agents` - JSON agent list
- `POST /api/agents/<agent_id>/deploy` - JSON deploy result

Do not commit API keys or personal financial details. Keep private context in local notes or a secure secrets manager, then pass only the minimum needed context at runtime.
