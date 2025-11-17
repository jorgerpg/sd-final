# sd-final

Aplicação completa de sorteios com backend Flask, frontend Flask + Bootstrap e proxy Nginx com balanceamento entre múltiplas instâncias da API.

## Requisitos

- Docker e Docker Compose
- Python 3.10+ (apenas se quiser rodar o script de teste automático)

## Como subir o ambiente

```bash
docker compose up --build
# ou detached
docker compose up -d
```

Serviços disponíveis:

- Frontend: http://localhost
- API (via nginx): http://localhost/api

## Script de teste/demonstração

O script `scripts/demo_raffle.py` cria um fluxo completo automaticamente:

1. Registra um organizador + N participantes com e-mails únicos.
2. Cria um sorteio.
3. Faz todos os usuários entrarem no sorteio.
4. Inicia o sorteio com o organizador e mostra o vencedor.

> Importante: mantenha o `docker compose up` rodando antes de executar o script.

### Executando

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests

python scripts/demo_raffle.py \
  --participants 5 \
  --api-base http://localhost/api
```

Opções disponíveis:

- `--participants`: número de participantes além do organizador (default 3)
- `--api-base`: URL base da API (default `http://localhost/api` ou variável `API_URL`)
- `--title`: título customizado para o sorteio

## Fluxo manual

1. Registre um usuário no frontend.
2. Crie um sorteio.
3. Abra múltiplas abas / usuários para entrar no sorteio.
4. Observe a atualização em tempo real da tela de detalhes (participantes, status e vencedor).
