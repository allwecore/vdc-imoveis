import re
import unicodedata

from extensions import db
from geocoding import PRECISION_LABELS as GEOCODE_PRECISION_LABELS
from geocoding import PRECISION_RADIUS_METERS as GEOCODE_PRECISION_RADIUS

PROPERTY_TYPE_LABELS = {
    "casa": "Casa",
    "casa_condominio": "Casa em Condomínio",
    "apartamento": "Apartamento",
    "comercial": "Imóvel Comercial",
    "terreno": "Terreno",
    "sitio_chacara": "Sítio & Chácara",
}

STATUS_LABELS = {
    "venda": "À Venda",
    "aluguel": "Para Alugar",
}

POST_CATEGORY_LABELS = {
    "mercado": "Mercado imobiliário",
    "financiamento": "Financiamento",
    "investimento": "Investimento",
    "bairros": "Bairros da cidade",
    "juridico": "Jurídico e documentação",
    "engenharia": "Engenharia e reforma",
}


def slugify(value):
    """Título → slug de URL: sem acento, minúsculo, hifens no lugar de
    espaço/pontuação. Usado nas URLs de /noticias/<slug>."""
    normalized = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return normalized or "noticia"


class Property(db.Model):
    __tablename__ = "vdc_properties"
    __table_args__ = {"schema": "vdcimoveis"}

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False, default="venda")
    neighborhood = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False, default="Vitória da Conquista")
    state = db.Column(db.Text, nullable=False, default="BA")
    cep = db.Column(db.Text)
    street_address = db.Column(db.Text)
    street_number = db.Column(db.Text)
    complement = db.Column(db.Text)
    latitude = db.Column(db.Numeric(9, 6))
    longitude = db.Column(db.Numeric(9, 6))
    # Preenchidos pelo backend na geocodificação; o admin nunca digita.
    geocode_query = db.Column(db.Text)
    geocode_precision = db.Column(db.Text)
    geocode_status = db.Column(db.Text)
    geocoded_at = db.Column(db.DateTime(timezone=True))
    price = db.Column(db.Numeric(12, 2), nullable=False)
    area_m2 = db.Column(db.Numeric(8, 2), nullable=False)
    bedrooms = db.Column(db.SmallInteger, nullable=False, default=0)
    parking_spots = db.Column(db.SmallInteger, nullable=False, default=0)
    highlight = db.Column(db.Text)
    description = db.Column(db.Text)
    featured = db.Column(db.Boolean, nullable=False, default=False)
    cover_tone = db.Column(db.Text, nullable=False, default="navy")
    # Legado: cache da URL da foto principal (ver PropertyPhoto mais
    # abaixo). Mantido sincronizado pela aplicação — todo card, busca e
    # popup de mapa que já lia este campo continua funcionando sem
    # nenhuma alteração, mesmo depois da galeria de múltiplas fotos.
    image_path = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    photos = db.relationship(
        "PropertyPhoto", back_populates="property",
        order_by="PropertyPhoto.sort_order", cascade="all, delete-orphan",
    )

    @property
    def type_label(self):
        return PROPERTY_TYPE_LABELS.get(self.property_type, self.property_type)

    @property
    def status_label(self):
        return STATUS_LABELS.get(self.status, self.status)

    @property
    def price_formatted(self):
        value = f"{self.price:,.0f}".replace(",", ".")
        suffix = "/mês" if self.status == "aluguel" else ""
        return f"R$ {value}{suffix}"

    @property
    def description_paragraphs(self):
        """Mesma regra do corpo das notícias: o textarea do admin chega com
        quebra CRLF, então normaliza antes de separar os parágrafos."""
        text = (self.description or "").replace("\r\n", "\n").replace("\r", "\n")
        return [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]

    @property
    def street_line(self):
        """"Rua das Acácias, 120 — apto 302" (só as partes que existem)."""
        rua = ", ".join(p for p in (self.street_address, self.street_number) if p)
        if rua and self.complement:
            return f"{rua} — {self.complement}"
        return rua or self.complement or ""

    @property
    def full_address(self):
        """Endereço para exibição na página do imóvel."""
        linhas = [self.street_line, self.neighborhood, f"{self.city} - {self.state}"]
        if self.cep:
            linhas.append(f"CEP {self.cep}")
        return " · ".join(p for p in linhas if p)

    @property
    def has_map(self):
        """O mapa público só aparece quando existe coordenada gravada —
        nunca geocodificamos na hora de exibir."""
        return self.latitude is not None and self.longitude is not None

    @property
    def map_precision(self):
        return self.geocode_precision or "aproximado"

    @property
    def map_precision_label(self):
        return GEOCODE_PRECISION_LABELS.get(self.map_precision, GEOCODE_PRECISION_LABELS["aproximado"])

    @property
    def map_radius_m(self):
        """Raio do círculo de imprecisão; 0 quando o número foi localizado."""
        return GEOCODE_PRECISION_RADIUS.get(self.map_precision, 600)

    @property
    def primary_photo(self):
        """A foto marcada como principal, ou a primeira da galeria se
        nenhuma estiver marcada (não deveria acontecer — todo imóvel com
        fotos tem uma principal —, mas cobre o caso defensivamente)."""
        for photo in self.photos:
            if photo.is_primary:
                return photo
        return self.photos[0] if self.photos else None

    @property
    def has_gallery(self):
        return len(self.photos) > 0


class PropertyPhoto(db.Model):
    """Uma foto da galeria de um imóvel. property.image_path é mantido
    sincronizado com a url da foto principal (ver _sync_cover_image_path
    em app.py) — todo código que já lia image_path (cards, busca, popup
    do mapa) continua funcionando sem alteração."""

    __tablename__ = "vdc_property_photos"
    __table_args__ = {"schema": "vdcimoveis"}

    id = db.Column(db.BigInteger, primary_key=True)
    property_id = db.Column(db.BigInteger, db.ForeignKey("vdcimoveis.vdc_properties.id", ondelete="CASCADE"), nullable=False)
    url = db.Column(db.Text, nullable=False)
    thumb_url = db.Column(db.Text)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_primary = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    property = db.relationship("Property", back_populates="photos")


class HeroSlide(db.Model):
    __tablename__ = "vdc_hero_slides"
    __table_args__ = {"schema": "vdcimoveis"}

    id = db.Column(db.BigInteger, primary_key=True)
    image_path = db.Column(db.Text, nullable=False)
    alt_text = db.Column(db.Text, nullable=False, default="")
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())


class Post(db.Model):
    """Notícia/artigo do blog (aba "Notícias"). O corpo é texto puro com
    quebras de linha — cada linha em branco vira um parágrafo na hora de
    exibir (ver body_paragraphs), sem editor rich-text nem HTML solto do
    admin, que abriria espaço pra injeção de marcação na página."""

    __tablename__ = "vdc_posts"
    __table_args__ = {"schema": "vdcimoveis"}

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False, unique=True)
    category = db.Column(db.Text, nullable=False, default="mercado")
    excerpt = db.Column(db.Text, nullable=False, default="")
    body = db.Column(db.Text, nullable=False, default="")
    image_path = db.Column(db.Text)
    published = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    @property
    def category_label(self):
        return POST_CATEGORY_LABELS.get(self.category, self.category)

    @property
    def date_formatted(self):
        return self.created_at.strftime("%d/%m/%Y") if self.created_at else ""

    @property
    def body_paragraphs(self):
        # O navegador envia textarea com quebra CRLF (regra do HTML), então
        # dividir direto em "\n\n" nunca casava e o texto inteiro virava um
        # parágrafo só. Normaliza a quebra antes de separar, e aceita mais
        # de uma linha em branco entre parágrafos.
        text = (self.body or "").replace("\r\n", "\n").replace("\r", "\n")
        return [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]

    @property
    def reading_minutes(self):
        words = len((self.body or "").split())
        return max(1, round(words / 200))


class Lead(db.Model):
    __tablename__ = "vdc_leads"
    __table_args__ = {"schema": "vdcimoveis"}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    message = db.Column(db.Text)
    source = db.Column(db.Text, nullable=False, default="site_home")
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())


class TeamMember(db.Model):
    __tablename__ = "vdc_team_members"
    __table_args__ = {"schema": "vdcimoveis"}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    credential = db.Column(db.Text, nullable=False, default="")
    initials = db.Column(db.Text, nullable=False, default="")
    bio = db.Column(db.Text, nullable=False, default="")
    photo_path = db.Column(db.Text)
    placeholder = db.Column(db.Boolean, nullable=False, default=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    @property
    def bio_paragraphs(self):
        text = (self.bio or "").replace("\r\n", "\n").replace("\r", "\n")
        return [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]


class AboutPage(db.Model):
    """Conteúdo da aba "Quem somos" — uma linha só (id=1), no mesmo
    modelo do SiteSettings. Fica no banco em vez de fixo no código
    porque é a história da empresa: só a VDC sabe o texto certo."""

    __tablename__ = "vdc_about_page"
    __table_args__ = {"schema": "vdcimoveis"}

    id = db.Column(db.BigInteger, primary_key=True)
    hero_eyebrow = db.Column(db.Text, nullable=False, default="Nossa história")
    hero_title = db.Column(db.Text, nullable=False, default="")
    hero_highlight = db.Column(db.Text, nullable=False, default="")
    hero_lead = db.Column(db.Text, nullable=False, default="")
    hero_image_path = db.Column(db.Text)

    stats = db.Column(db.Text, nullable=False, default="")  # "valor | rótulo" por linha

    history = db.Column(db.Text, nullable=False, default="")
    history_image_path = db.Column(db.Text)
    badge_value = db.Column(db.Text, nullable=False, default="")
    badge_label = db.Column(db.Text, nullable=False, default="")

    mission = db.Column(db.Text, nullable=False, default="")
    vision = db.Column(db.Text, nullable=False, default="")
    values_list = db.Column(db.Text, nullable=False, default="")  # um valor por linha

    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    @staticmethod
    def get():
        page = db.session.get(AboutPage, 1)
        if page is None:
            page = AboutPage(id=1)
            db.session.add(page)
            db.session.commit()
        return page

    @staticmethod
    def _lines(raw):
        text = (raw or "").replace("\r\n", "\n").replace("\r", "\n")
        return [line.strip() for line in text.split("\n") if line.strip()]

    @property
    def stat_items(self):
        """Cada linha vira "valor | rótulo"; linha sem "|" vira só o valor."""
        items = []
        for line in self._lines(self.stats):
            value, _, label = line.partition("|")
            items.append({"value": value.strip(), "label": label.strip()})
        return items

    @property
    def value_items(self):
        return self._lines(self.values_list)

    @property
    def history_paragraphs(self):
        text = (self.history or "").replace("\r\n", "\n").replace("\r", "\n")
        return [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]


class SiteSettings(db.Model):
    __tablename__ = "vdc_site_settings"
    __table_args__ = {"schema": "vdcimoveis"}

    id = db.Column(db.BigInteger, primary_key=True)
    whatsapp_number = db.Column(db.Text, nullable=False, default="")
    instagram_handle = db.Column(db.Text, nullable=False, default="")
    instagram_url = db.Column(db.Text, nullable=False, default="")
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    @staticmethod
    def get():
        """Linha única (id=1) — criada com valores em branco na primeira
        chamada se, por algum motivo, ainda não existir."""
        settings = db.session.get(SiteSettings, 1)
        if settings is None:
            settings = SiteSettings(id=1)
            db.session.add(settings)
            db.session.commit()
        return settings
