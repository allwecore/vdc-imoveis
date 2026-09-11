"""Geocodificação gratuita de endereços via Nominatim (OpenStreetMap).

Por que Nominatim e não Google: é o serviço de geocodificação do próprio
OpenStreetMap, aberto, sem chave de API e sem cadastro de cartão — não
existe caminho pelo qual esta funcionalidade gere cobrança. Em troca ele
impõe uma política de uso que este módulo respeita:

  * no máximo 1 requisição por segundo (aqui: 1 a cada 1,1s, com trava
    de processo, então rajadas de salvamento entram em fila em vez de
    tomar bloqueio);
  * User-Agent identificando a aplicação (configurável no .env);
  * nada de uso em massa — daí o cache: o resultado é gravado no imóvel
    e só é reconsultado quando o endereço muda de verdade.

O módulo nunca levanta exceção para quem chama: qualquer falha vira um
GeocodeResult com status preenchido, para o cadastro do imóvel poder
seguir mesmo sem coordenada.
"""

import json
import os
import socket
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Política do Nominatim: 1 req/s. 1,1s dá folga para relógio impreciso.
MIN_INTERVAL_SECONDS = 1.1
REQUEST_TIMEOUT_SECONDS = 8

# A política do Nominatim pede um User-Agent que identifique a aplicação
# E ofereça uma forma de contato, pra eles poderem avisar antes de
# bloquear em caso de uso indevido. ANTES DE PUBLICAR, coloque um e-mail
# ou site real em NOMINATIM_USER_AGENT no .env — o padrão abaixo
# identifica a aplicação mas não tem contato nenhum.
USER_AGENT = os.environ.get("NOMINATIM_USER_AGENT", "VDC-Imoveis/1.0 (site institucional)")

# Rótulos honestos: nenhum deles promete que o pin é a porta da casa,
# porque o serviço gratuito muitas vezes só sabe a rua ou o bairro.
PRECISION_LABELS = {
    "exato": "Endereço localizado no número informado.",
    "rua": "Localização aproximada — o serviço gratuito localizou a rua, não o número exato.",
    "bairro": "Localização aproximada do bairro.",
    "cidade": "Localização aproximada da cidade.",
    "aproximado": "Localização aproximada.",
}

# Raio (em metros) do círculo desenhado no mapa por precisão. Serve para
# mostrar visualmente que aquilo é uma área, não um ponto exato.
PRECISION_RADIUS_METERS = {
    "exato": 0,
    "rua": 120,
    "bairro": 500,
    "cidade": 1500,
    "aproximado": 600,
}

STATUS_MESSAGES = {
    "ok": "",
    "nao_encontrado": (
        "Não foi possível localizar este endereço automaticamente no mapa. "
        "O imóvel foi salvo normalmente, mas o mapa não vai aparecer na página dele. "
        "Confira o CEP, a rua e o número e salve de novo."
    ),
    "limite": (
        "O serviço gratuito de mapas recusou a consulta por excesso de requisições. "
        "O imóvel foi salvo sem coordenadas — tente localizar de novo daqui a um minuto."
    ),
    "timeout": (
        "O serviço gratuito de mapas não respondeu a tempo. "
        "O imóvel foi salvo sem coordenadas — tente localizar de novo."
    ),
    "resposta_invalida": (
        "O serviço gratuito de mapas devolveu uma resposta inesperada. "
        "O imóvel foi salvo sem coordenadas — tente localizar de novo."
    ),
    "erro": (
        "Não foi possível falar com o serviço gratuito de mapas agora. "
        "O imóvel foi salvo sem coordenadas — tente localizar de novo."
    ),
}

# addresstype/type do Nominatim → nossa escala de precisão.
_PRECISION_BY_OSM_TYPE = {
    "house": "exato",
    "house_number": "exato",
    "building": "exato",
    "residential": "rua",
    "road": "rua",
    "street": "rua",
    "pedestrian": "rua",
    "footway": "rua",
    "neighbourhood": "bairro",
    "suburb": "bairro",
    "quarter": "bairro",
    "city_block": "bairro",
    "hamlet": "bairro",
    "city_district": "bairro",
    "city": "cidade",
    "town": "cidade",
    "municipality": "cidade",
    "village": "cidade",
    "administrative": "cidade",
}

_PRECISION_ORDER = ["exato", "rua", "bairro", "cidade", "aproximado"]


@dataclass(frozen=True)
class GeocodeResult:
    """Resultado de uma tentativa de geocodificação.

    latitude/longitude só vêm preenchidos quando status == "ok"."""

    status: str
    latitude: float = None
    longitude: float = None
    precision: str = None

    @property
    def ok(self):
        return self.status == "ok"

    @property
    def message(self):
        return STATUS_MESSAGES.get(self.status, STATUS_MESSAGES["erro"])


def _clean(value):
    return " ".join((value or "").split()).strip()


def build_query(street_address="", street_number="", neighborhood="", city="", state="", cep=""):
    """Monta a chave de cache do endereço.

    É esta string que fica gravada em vdc_properties.geocode_query. Se ela
    não mudou entre dois salvamentos, o endereço não mudou e não há motivo
    para consultar o Nominatim de novo. O complemento (apto, bloco) é
    deliberadamente ignorado: não muda a coordenada e só invalidaria o
    cache à toa."""
    partes = [
        _clean(street_address),
        _clean(street_number),
        _clean(neighborhood),
        _clean(city),
        _clean(state).upper(),
        "".join(ch for ch in (cep or "") if ch.isdigit()),
    ]
    return " | ".join(partes)


_throttle_lock = threading.Lock()
_last_request_at = 0.0


def _throttled_get(params):
    """Faz a chamada HTTP respeitando 1 req/s global do processo.

    Devolve a lista de resultados já decodificada, ou levanta uma das
    exceções tratadas em _attempt()."""
    global _last_request_at

    url = NOMINATIM_URL + "?" + urllib.parse.urlencode(params)
    request_obj = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Language": "pt-BR",
        },
    )

    with _throttle_lock:
        espera = MIN_INTERVAL_SECONDS - (time.monotonic() - _last_request_at)
        if espera > 0:
            time.sleep(espera)
        try:
            with urllib.request.urlopen(request_obj, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                bruto = response.read()
        finally:
            # Marca o horário mesmo em erro: uma falha também consumiu
            # uma requisição no lado deles.
            _last_request_at = time.monotonic()

    return json.loads(bruto.decode("utf-8"))


def _parse_result(item, teto_precisao=None):
    """Valida um item da resposta e devolve GeocodeResult, ou None se o
    item não tiver coordenada utilizável."""
    try:
        latitude = float(item["lat"])
        longitude = float(item["lon"])
    except (KeyError, TypeError, ValueError):
        return None
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return None

    osm_type = item.get("addresstype") or item.get("type") or item.get("class") or ""
    precisao = _PRECISION_BY_OSM_TYPE.get(osm_type, "aproximado")

    # Uma busca que já era de nível bairro não pode alegar precisão de
    # número, mesmo que o Nominatim classifique o resultado assim.
    if teto_precisao and _PRECISION_ORDER.index(precisao) < _PRECISION_ORDER.index(teto_precisao):
        precisao = teto_precisao

    return GeocodeResult(status="ok", latitude=latitude, longitude=longitude, precision=precisao)


def _attempt(params, teto_precisao=None):
    """Uma tentativa. Devolve (GeocodeResult|None, status_do_erro|None)."""
    try:
        dados = _throttled_get(params)
    except urllib.error.HTTPError as err:
        if err.code in (429, 403):
            return None, "limite"
        return None, "erro"
    except socket.timeout:
        return None, "timeout"
    except urllib.error.URLError as err:
        if isinstance(err.reason, socket.timeout):
            return None, "timeout"
        return None, "erro"
    except (ValueError, UnicodeDecodeError):  # JSON quebrado / corpo não-JSON
        return None, "resposta_invalida"
    except Exception:
        return None, "erro"

    if not isinstance(dados, list):
        return None, "resposta_invalida"
    if not dados:
        return None, None  # respondeu certo, só não achou nada

    return _parse_result(dados[0], teto_precisao), None


def geocode_address(street_address="", street_number="", neighborhood="", city="", state="", cep=""):
    """Endereço → GeocodeResult, do mais específico ao mais genérico.

    Tenta na ordem, parando na primeira que achar:
      1. busca estruturada (rua+número, cidade, UF, CEP) — a que dá
         chance real de acertar o número;
      2. busca estruturada sem CEP — CEP errado ou genérico zera o
         resultado da anterior;
      3. texto livre com o endereço inteiro;
      4. só bairro + cidade + UF, marcado como precisão de bairro.

    Cada tentativa custa ~1,1s por causa do throttle, por isso as
    tentativas que não fazem sentido (sem rua, por exemplo) são puladas.
    """
    rua = _clean(street_address)
    numero = _clean(street_number)
    bairro = _clean(neighborhood)
    cidade = _clean(city)
    uf = _clean(state).upper()
    digitos_cep = "".join(ch for ch in (cep or "") if ch.isdigit())

    base = {"format": "json", "limit": 1, "countrycodes": "br", "addressdetails": 0}
    logradouro = f"{numero} {rua}".strip() if numero else rua

    tentativas = []

    if logradouro and cidade:
        estruturada = dict(base, street=logradouro, city=cidade)
        if uf:
            estruturada["state"] = uf
        if len(digitos_cep) == 8:
            tentativas.append((dict(estruturada, postalcode=digitos_cep), None))
        tentativas.append((estruturada, None))

    livre = ", ".join(p for p in (logradouro, bairro, cidade, uf, "Brasil") if p)
    if logradouro:
        tentativas.append((dict(base, q=livre), None))

    if bairro and cidade:
        so_bairro = ", ".join(p for p in (bairro, cidade, uf, "Brasil") if p)
        tentativas.append((dict(base, q=so_bairro), "bairro"))
    elif cidade:
        so_cidade = ", ".join(p for p in (cidade, uf, "Brasil") if p)
        tentativas.append((dict(base, q=so_cidade), "cidade"))

    if not tentativas:
        return GeocodeResult(status="nao_encontrado")

    ultimo_erro = None
    for params, teto in tentativas:
        resultado, erro = _attempt(params, teto)
        if resultado is not None:
            return resultado
        if erro:
            ultimo_erro = erro
            # Limite estourado não melhora tentando de novo em seguida.
            if erro == "limite":
                break

    return GeocodeResult(status=ultimo_erro or "nao_encontrado")
