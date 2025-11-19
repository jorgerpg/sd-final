"""Ponto de entrada utilizado pelo Flask."""

from app import create_app

app = create_app()

if __name__ == "__main__":
  # Permite executar `python wsgi.py` localmente.
  app.run()
