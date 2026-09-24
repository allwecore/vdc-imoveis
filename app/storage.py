"""Upload de arquivos enviados pelo admin (fotos de imóvel, hero, equipe,
notícias, "quem somos") para o Supabase Storage.

Por que isso existe: em produção (Vercel) o filesystem da função
serverless é somente leitura — um `open(caminho, "wb")` direto em
static/uploads/ derruba a requisição com 500 Internal Server Error.
Fotos precisam de um lugar que sobrevive entre deploys e aceita escrita
em runtime; o Supabase Storage serve isso, e o projeto já usa Supabase
para o banco.

Sem SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY configurados (ex.: rodando
local sem essas variáveis), `enabled` fica False e quem chama volta a
gravar em disco — é assim que `python app.py` local continua funcionando
sem depender de um bucket."""

import mimetypes
import os
import urllib.error
import urllib.request

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
STORAGE_BUCKET = os.environ.get("SUPABASE_STORAGE_BUCKET", "uploads")

enabled = bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)

_PUBLIC_PREFIX = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/"


def upload_public(remote_path, data, content_type=None):
    """Envia `data` (bytes) para <bucket>/<remote_path> e devolve a URL
    pública. Levanta RuntimeError se o upload falhar ou o Storage não
    estiver configurado — quem chama decide como avisar o admin."""
    if not enabled:
        raise RuntimeError(
            "Envio de imagem não configurado neste ambiente "
            "(SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY ausentes)."
        )
    content_type = content_type or mimetypes.guess_type(remote_path)[0] or "application/octet-stream"
    url = f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/{remote_path}"
    request_obj = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Content-Type": content_type,
            # Sobrescreve se por acaso já existir um arquivo com esse nome
            # (não deveria acontecer — o nome vem de uuid4 — mas evita um
            # 409 travar o cadastro à toa).
            "x-upsert": "true",
        },
    )
    try:
        with urllib.request.urlopen(request_obj, timeout=15):
            pass
    except urllib.error.HTTPError as err:
        detalhe = err.read().decode("utf-8", "ignore")
        raise RuntimeError(f"Falha ao enviar a imagem para o armazenamento ({err.code}): {detalhe}") from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Falha ao enviar a imagem para o armazenamento: {err.reason}") from err

    return _PUBLIC_PREFIX + remote_path


def delete_public(remote_path):
    """Remove um arquivo do bucket. Nunca levanta exceção — apagar uma
    foto antiga não pode impedir salvar a nova."""
    if not enabled or not remote_path:
        return
    url = f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/{remote_path}"
    request_obj = urllib.request.Request(
        url,
        method="DELETE",
        headers={
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
        },
    )
    try:
        with urllib.request.urlopen(request_obj, timeout=15):
            pass
    except urllib.error.URLError:
        pass


def is_managed_url(path):
    """True se `path` é uma URL que este módulo gerou (e portanto deve
    ser apagada via `delete_public`, não via os.remove)."""
    return bool(enabled and path and path.startswith(_PUBLIC_PREFIX))


def remote_path_from_url(path):
    return path[len(_PUBLIC_PREFIX):]
