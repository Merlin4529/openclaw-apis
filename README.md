# OpenClaw APIs

Gestión segura de APIs OPENCLAW

## Setup
pip install -r requirements.txt
cp .env.example .env
# Editar .env con credenciales

## Uso
from apis.footystats_api import FootyStatsAPI
api = FootyStatsAPI()
