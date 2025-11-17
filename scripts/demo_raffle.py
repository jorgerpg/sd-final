#!/usr/bin/env python3
"""
Script de demonstração para testar as principais features de sorteios.

- Cria automaticamente usuários (organizador + participantes)
- Cria um sorteio
- Faz cada usuário entrar no sorteio
- Inicia o sorteio com o organizador
- Exibe o vencedor e o estado final

Requer que a API esteja acessível (por padrão em http://localhost/api).
"""

import argparse
import os
import sys
from datetime import datetime
from typing import Dict, List

import requests

DEFAULT_API_BASE = os.getenv("API_URL", "http://localhost/api")


def _auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"} if token else {}


class DemoClient:
    def __init__(self, api_base: str):
        self.api_base = api_base.rstrip("/")

    # --------- Usuários ---------
    def register_user(self, name: str, email: str, password: str) -> bool:
        resp = requests.post(
            f"{self.api_base}/auth/register",
            json={"name": name, "email": email, "password": password},
            timeout=10,
        )
        if resp.status_code == 200:
            print(f"[OK] Usuário criado: {name} ({email})")
            return True

        body = resp.json()
        print(f"[WARN] Não foi possível registrar {email}: {body.get('error')}")
        return False

    def login(self, email: str, password: str) -> Dict:
        resp = requests.post(
            f"{self.api_base}/auth/login",
            json={"email": email, "password": password},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def ensure_account(self, name: str, email: str, password: str) -> Dict:
        created = self.register_user(name, email, password)
        session = self.login(email, password)
        if created:
            print(f"[OK] Login realizado para {name}")
        return session

    # --------- Sorteios ---------
    def create_raffle(self, token: str, title: str, description: str) -> int:
        resp = requests.post(
            f"{self.api_base}/raffles/",
            json={"title": title, "description": description},
            headers=_auth_headers(token),
            timeout=10,
        )
        resp.raise_for_status()
        raffle_id = resp.json()["id"]
        print(f"[OK] Sorteio criado (ID: {raffle_id})")
        return raffle_id

    def join_raffle(self, token: str, raffle_id: int, user_name: str) -> None:
        resp = requests.post(
            f"{self.api_base}/raffles/{raffle_id}/join",
            headers=_auth_headers(token),
            timeout=10,
        )
        if resp.status_code == 200:
            print(f"[OK] {user_name} entrou no sorteio {raffle_id}")
        else:
            print(f"[WARN] {user_name} não conseguiu entrar: {resp.text}")

    def start_raffle(self, token: str, raffle_id: int) -> Dict:
        resp = requests.post(
            f"{self.api_base}/raffles/{raffle_id}/start",
            headers=_auth_headers(token),
            timeout=10,
        )
        resp.raise_for_status()
        print(f"[OK] Sorteio {raffle_id} iniciado/finalizado")
        return resp.json()

    def get_raffle(self, raffle_id: int) -> Dict:
        resp = requests.get(f"{self.api_base}/raffles/{raffle_id}", timeout=10)
        resp.raise_for_status()
        return resp.json()


def build_demo_users(total_participants: int) -> List[Dict]:
    """Gera usuários com e-mails únicos para evitar conflitos."""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    users = [
        {
            "role": "organizer",
            "name": "Organizador Demo",
            "email": f"organizador-{timestamp}@example.com",
            "password": "SenhaDemo123!",
        }
    ]

    for idx in range(1, total_participants + 1):
        users.append(
            {
                "role": "participant",
                "name": f"Participante {idx}",
                "email": f"participante{idx}-{timestamp}@example.com",
                "password": "SenhaDemo123!",
            }
        )
    return users


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa um fluxo completo de sorteio com usuários fictícios."
    )
    parser.add_argument(
        "--api-base",
        default=DEFAULT_API_BASE,
        help=f"URL base da API (default: {DEFAULT_API_BASE})",
    )
    parser.add_argument(
        "--participants",
        type=int,
        default=3,
        help="Quantidade de participantes além do organizador (default: 3)",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Título customizado do sorteio (default: gera dinamicamente)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    client = DemoClient(args.api_base)

    users = build_demo_users(args.participants)
    sessions = {}
    for user in users:
        sessions[user["role"], user["email"]] = client.ensure_account(
            user["name"], user["email"], user["password"]
        )

    organizer_user = next(user for user in users if user["role"] == "organizer")
    organizer_session = sessions[("organizer", organizer_user["email"])]

    raffle_title = args.title or f"Sorteio Demo {datetime.utcnow():%Y-%m-%d %H:%M:%S}"
    raffle_id = client.create_raffle(
        organizer_session["token"], raffle_title, "Sorteio criado pelo script demo."
    )

    for user in users:
        if user["role"] == "organizer":
            # Organizador também participa para validar a feature (opcional)
            client.join_raffle(
                organizer_session["token"], raffle_id, organizer_user["name"]
            )
            continue

        session = sessions[(user["role"], user["email"])]
        client.join_raffle(session["token"], raffle_id, user["name"])

    client.start_raffle(organizer_session["token"], raffle_id)
    final_state = client.get_raffle(raffle_id)

    print("\n=== Resultado ===")
    print(f"Status final: {final_state['status']}")
    if final_state.get("winner"):
        winner = final_state["winner"]
        print(f"Vencedor: {winner['name']} <{winner['email']}>")
    else:
        print("Nenhum vencedor definido.")

    print("\nParticipantes:")
    for participant in final_state.get("participants", []):
        user = participant["user"]
        print(f" - {user['name']} <{user['email']}>")

    print("\nScript finalizado com sucesso.")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"[ERRO] Requisição falhou: {exc} -> {exc.response.text}")
        sys.exit(1)
    except requests.RequestException as exc:
        print(f"[ERRO] Falha de comunicação com a API: {exc}")
        sys.exit(1)
