# sd-final

Aplicação completa de sorteios com backend Flask, frontend Flask + Bootstrap e proxy Nginx com balanceamento entre múltiplas instâncias da API.

## Estrutura do projeto

- `api-sorteio/`: API REST em Flask responsável por autenticação, CRUD de sorteios, inscrição de participantes e escolha do vencedor. Usa SQLAlchemy para mapear `User`, `Raffle` e `RaffleParticipant`, organiza a lógica em camadas (`services`, `repositories`, `routes`) e expõe os endpoints consumidos pelo frontend.
- `frontend/`: Aplicação Flask que renderiza as telas Bootstrap, mantém sessão do usuário e orquestra o fluxo (login/registro, criação de sorteios, listagem filtrada, detalhe, entrada e início do sorteio) chamando a API via HTTP.
- `nginx/`: Arquivo `nginx.conf` com o proxy reverso e o load balancer round-robin apontando para as duas instâncias do backend. Também direciona `/api` para a API e `/` para o frontend.
- `docker-compose.yml`: Orquestra todos os containers, redes e volumes persistentes (como o `db_data` do Postgres).
- `logs/`: Montado no container do Nginx para inspecionar `access.log` e `error.log` da borda.
- `scripts/demo_raffle.py`: Script utilitário que dirige um fluxo completo de sorteio chamando a API, excelente para testes e demonstrações automatizadas.

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

## Containers e responsabilidades

- `db (sorteio-db)`: Banco Postgres 15 que armazena usuários, sorteios e relações de participação. Possui volume persistente `db_data` para manter os dados entre reinicializações.
- `api-sorteio-1` e `api-sorteio-2`: Duas réplicas idênticas da API Flask (`api-sorteio/`). Cada uma sobe o mesmo código, conecta no Postgres via `DATABASE_URL`, expõe os endpoints `/api/auth` e `/api/raffles` e garante tolerância a falhas/balanceamento.
- `frontend (sorteio-frontend)`: Flask server responsável pelas páginas HTML. Consome a API através do hostname `nginx` configurado, mantém sessão do usuário, aplica filtros locais de busca/“meus sorteios” e envia ações (entrar/iniciar).
- `nginx (sorteio-nginx)`: Proxy reverso exposto na porta 80. Encaminha `/api` para as duas instâncias do backend (balanceamento round-robin) e encaminha as demais rotas para o container `frontend`, além de centralizar logs em `./logs`.

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
5. Apenas o criador visualiza o botão **Iniciar Sorteio**, garantindo que participantes não finalizem o sorteio.

## Filtros e busca

Na página `/raffles` a listagem suporta:

- Campo de busca por título (case-insensitive, aplica-se antes de renderizar os cards).
- Checkbox “Mostrar apenas meus sorteios” para usuários autenticados, filtrando por `creator_id`.

Ambos filtros funcionam apenas no frontend (a API continua retornando todos os sorteios), então a URL reflete os parâmetros (`/raffles?q=nome&mine=1`) e pode ser compartilhada para reproduzir o mesmo resultado.
