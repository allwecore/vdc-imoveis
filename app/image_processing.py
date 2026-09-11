"""Processamento das fotos da galeria de imóveis.

Por que isso existe: foto de celular moderno costuma vir com vários
megapixels (várias vezes maior do que qualquer tela vai exibir) e
alguns megabytes de tamanho — cadastrar um imóvel com 15-20 fotos
assim faria a página do imóvel baixar dezenas de MB de imagem à toa,
péssimo em celular. Aqui cada foto é redimensionada uma vez no upload
e vira dois arquivos:

  * "full"  — versão de exibição (usada na foto principal grande e no
    lightbox), lado maior limitado a FULL_MAX_DIMENSION;
  * "thumb" — miniatura (usada na tira de thumbnails, no card, na
    busca e no grid do admin), lado maior limitado a THUMB_MAX_DIMENSION.

As duas sempre viram JPEG (conteúdo é foto real, não teria por que
preservar transparência de PNG) com qualidade fixa — troca uma foto de
celular de 4-8MB por algo na casa de algumas centenas de KB sem perda
visível em tela.
"""

import io
import uuid

from PIL import Image, ImageOps

FULL_MAX_DIMENSION = 1920
THUMB_MAX_DIMENSION = 480
JPEG_QUALITY = 85

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def allowed_photo(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def _resized_jpeg_bytes(image, max_dimension):
    """Copia a imagem redimensionada (mantendo proporção, nunca aumenta
    o que já é menor que o limite) e devolve os bytes de um JPEG."""
    copia = image.copy()
    copia.thumbnail((max_dimension, max_dimension), Image.LANCZOS)
    buffer = io.BytesIO()
    copia.save(buffer, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    return buffer.getvalue()


def process_property_photo(file_storage):
    """Recebe um FileStorage do Flask (request.files) e devolve
    (full_bytes, thumb_bytes, filename_base, erro).

    Em caso de erro (formato não suportado ou arquivo corrompido),
    devolve (None, None, None, mensagem)."""
    filename = file_storage.filename or ""
    if not allowed_photo(filename):
        return None, None, None, f'Formato não suportado em "{filename}". Use JPG, PNG ou WEBP.'

    try:
        imagem = Image.open(file_storage.stream)
        imagem.load()
    except Exception:
        return None, None, None, f'Não foi possível abrir o arquivo "{filename}" — ele pode estar corrompido.'

    # Fotos de celular trazem a orientação real só nos metadados EXIF
    # (a imagem "crua" às vezes vem deitada); sem isso a foto salva
    # girada errado.
    imagem = ImageOps.exif_transpose(imagem)
    if imagem.mode not in ("RGB", "L"):
        imagem = imagem.convert("RGB")

    try:
        full_bytes = _resized_jpeg_bytes(imagem, FULL_MAX_DIMENSION)
        thumb_bytes = _resized_jpeg_bytes(imagem, THUMB_MAX_DIMENSION)
    except Exception:
        return None, None, None, f'Não foi possível processar o arquivo "{filename}".'

    return full_bytes, thumb_bytes, uuid.uuid4().hex, None
