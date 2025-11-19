"""Ponto central para instâncias compartilhadas (ex.: SQLAlchemy)."""

from flask_sqlalchemy import SQLAlchemy

# Um único objeto `db` é importado pelos demais módulos para evitar
# inicializações duplicadas e facilitar a configuração no factory.
db = SQLAlchemy()
