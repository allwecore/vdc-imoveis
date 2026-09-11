import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


def _sqlalchemy_uri(database_url: str) -> str:
    """SQLAlchemy needs the psycopg3 dialect prefix; DATABASE_URL uses the plain postgres scheme."""
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


class Config:
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = _sqlalchemy_uri(os.environ["DATABASE_URL"])
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        # DATABASE_URL aponta pro pooler do Supabase (porta 6543, PgBouncer em modo
        # transaction) — ele não suporta prepared statements nomeados persistindo entre
        # conexões do pool. Sem isso, qualquer commit que atualize/insira mais de uma
        # linha (executemany) quebra com "DuplicatePreparedStatement".
        "connect_args": {"prepare_threshold": None},
    }
    WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads", "hero")
    PROPERTY_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads", "imoveis")
    POST_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads", "noticias")
    TEAM_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads", "equipe")
    ABOUT_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads", "quem-somos")
    # 60MB: cobre um cadastro de imóvel com várias fotos de celular
    # (sem compressão prévia) numa única requisição. As fotos são
    # redimensionadas no servidor logo depois (ver image_processing.py)
    # — este limite é só o teto do que a requisição pode trazer bruta.
    MAX_CONTENT_LENGTH = 60 * 1024 * 1024
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)  # login do admin expira sozinho
