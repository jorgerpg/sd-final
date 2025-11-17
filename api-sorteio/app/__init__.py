import time

from flask import Flask
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError, OperationalError

from app.config import get_config
from app.extensions import db
from app.routes.auth_routes import bp as auth_bp
from app.routes.raffle_routes import bp as raffle_bp


def wait_for_db(engine, retries=10, delay_sec=1):
    """Aguarda o Postgres ficar pronto antes de inspecionar/criar tabelas."""
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError as exc:
            print(f">> Banco indisponível (tentativa {attempt}/{retries}): {exc}")
            if attempt == retries:
                raise
            time.sleep(delay_sec)


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)

    # Verificação segura se as tabelas já existem
    with app.app_context():
        wait_for_db(db.engine)
        inspector = inspect(db.engine)

        tables = inspector.get_table_names()

        # se nenhuma tabela existe, cria todas
        if not tables:
            print(">> Nenhuma tabela encontrada, criando...")
            try:
                db.create_all()
            except IntegrityError as exc:
                # Se outro container criar as tabelas ao mesmo tempo,
                # tratamos o erro e seguimos normalmente.
                db.session.rollback()
                print(f">> Corrida detectada ao criar tabelas, ignorando: {exc}")
            else:
                print(">> Tabelas criadas com sucesso.")
        else:
            print(">> Tabelas já existem. Nenhuma ação necessária.")

    # Registrar rotas
    app.register_blueprint(auth_bp)
    app.register_blueprint(raffle_bp)

    return app
