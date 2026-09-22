import json
import os
import secrets
import uuid
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

import content
import geocoding
import image_processing
from config import Config
from extensions import db
from models import (
    POST_CATEGORY_LABELS,
    PROPERTY_TYPE_LABELS,
    AboutPage,
    HeroSlide,
    Lead,
    Post,
    Property,
    PropertyPhoto,
    SiteSettings,
    TeamMember,
    slugify,
)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    for folder_key in (
        "UPLOAD_FOLDER",
        "PROPERTY_UPLOAD_FOLDER",
        "POST_UPLOAD_FOLDER",
        "TEAM_UPLOAD_FOLDER",
        "ABOUT_UPLOAD_FOLDER",
    ):
        try:
            os.makedirs(app.config[folder_key], exist_ok=True)
        except OSError:
            # Read-only filesystem (e.g. Vercel serverless) — uploads need
            # external storage there; startup should still succeed.
            pass

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now(timezone.utc).year}

    return app


app = create_app()


def require_admin(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def _save_upload(file, config_key, subfolder):
    """Salva uma imagem enviada na pasta indicada e devolve o caminho
    relativo a /static (ou None se não veio arquivo). Upload simples,
    1 arquivo por vez — usada por equipe, "quem somos", notícias e hero.
    A galeria de fotos do imóvel usa um caminho próprio, com
    redimensionamento e miniatura (ver image_processing.py e
    _apply_property_photos)."""
    if not file or file.filename == "":
        return None, None
    if not allowed_image(file.filename):
        return None, "Formato de imagem não suportado. Use JPG, PNG ou WEBP."
    extension = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    stored_name = f"{uuid.uuid4().hex}.{extension}"
    file.save(os.path.join(app.config[config_key], stored_name))
    return f"uploads/{subfolder}/{stored_name}", None


def _delete_upload(image_path):
    if not image_path:
        return
    file_path = os.path.join(os.path.dirname(__file__), "static", image_path)
    if os.path.exists(file_path):
        os.remove(file_path)


def header_context():
    settings = SiteSettings.get()
    return {
        "nav_links": content.NAV_LINKS,
        "mega_menu_columns": content.MEGA_MENU_COLUMNS,
        "footer_columns": content.FOOTER_COLUMNS,
        "whatsapp_number": settings.whatsapp_number,
        "instagram_handle": settings.instagram_handle,
        "instagram_url": settings.instagram_url,
    }


def search_filter_options():
    neighborhoods = [
        row[0]
        for row in db.session.query(Property.neighborhood).distinct().order_by(Property.neighborhood).all()
    ]
    return {
        "property_type_options": PROPERTY_TYPE_LABELS,
        "neighborhood_options": neighborhoods,
    }


@app.route("/")
def index():
    featured = (
        Property.query.filter_by(featured=True)
        .order_by(Property.created_at.desc(), Property.id.desc())
        .limit(6)
        .all()
    )
    hero_slides = (
        HeroSlide.query.filter_by(active=True)
        .order_by(HeroSlide.sort_order.asc(), HeroSlide.id.asc())
        .all()
    )
    team = TeamMember.query.order_by(TeamMember.sort_order.asc(), TeamMember.id.asc()).all()
    return render_template(
        "index.html",
        quick_filters=content.QUICK_FILTERS,
        specialties=content.SPECIALTIES,
        team=team,
        seals=content.SEALS,
        properties=featured,
        hero_slides=hero_slides,
        **header_context(),
        **search_filter_options(),
    )


SEARCH_SORT_OPTIONS = {
    "recentes": ("Mais recentes", (Property.created_at.desc(), Property.id.desc())),
    "menor_preco": ("Menor preço", (Property.price.asc(),)),
    "maior_preco": ("Maior preço", (Property.price.desc(),)),
}


@app.route("/imoveis")
def search():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    tipo = request.args.get("tipo", "").strip()
    bairro = request.args.get("bairro", "").strip()
    preco_max = request.args.get("preco_max", "").strip()
    quartos = request.args.get("quartos", "").strip()
    sort = request.args.get("sort", "").strip()
    if sort not in SEARCH_SORT_OPTIONS:
        sort = "recentes"

    query = Property.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                Property.title.ilike(like),
                Property.neighborhood.ilike(like),
                Property.property_type.ilike(like),
            )
        )
    if status in ("venda", "aluguel"):
        query = query.filter(Property.status == status)
    if tipo in PROPERTY_TYPE_LABELS:
        query = query.filter(Property.property_type == tipo)
    if bairro:
        query = query.filter(Property.neighborhood == bairro)
    if preco_max.isdigit():
        query = query.filter(Property.price <= int(preco_max))
    if quartos.isdigit():
        query = query.filter(Property.bedrooms >= int(quartos))

    results = query.order_by(*SEARCH_SORT_OPTIONS[sort][1]).all()
    map_points = [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price_formatted,
            "neighborhood": p.neighborhood,
            "type_label": p.type_label,
            "status": p.status,
            "bedrooms": p.bedrooms,
            "area_m2": round(float(p.area_m2)),
            "lat": float(p.latitude),
            "lng": float(p.longitude),
            "url": url_for("property_detail", property_id=p.id),
        }
        for p in results
        if p.latitude is not None and p.longitude is not None
    ]
    return render_template(
        "search.html",
        properties=results,
        map_points=map_points,
        query=q,
        status=status,
        tipo=tipo,
        bairro=bairro,
        preco_max=preco_max,
        quartos=quartos,
        sort=sort,
        sort_options=SEARCH_SORT_OPTIONS,
        **header_context(),
        **search_filter_options(),
    )


@app.route("/imovel/<int:property_id>")
def property_detail(property_id):
    """Página pública do imóvel. O mapa é montado a partir da coordenada
    já gravada no banco — nenhuma geocodificação acontece aqui, por mais
    visitas que a página receba."""
    prop = db.get_or_404(Property, property_id)
    similares = (
        Property.query.filter(Property.id != prop.id, Property.neighborhood == prop.neighborhood)
        .order_by(Property.created_at.desc())
        .limit(3)
        .all()
    )
    if not similares:
        similares = (
            Property.query.filter(Property.id != prop.id, Property.property_type == prop.property_type)
            .order_by(Property.created_at.desc())
            .limit(3)
            .all()
        )
    return render_template("imovel.html", prop=prop, similares=similares, **header_context())


@app.route("/equipe")
def team():
    members = TeamMember.query.order_by(TeamMember.sort_order.asc(), TeamMember.id.asc()).all()
    return render_template("equipe.html", members=members, **header_context())


@app.route("/quem-somos")
def about():
    return render_template("quem-somos.html", page=AboutPage.get(), **header_context())


@app.route("/noticias")
def news():
    q = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "").strip()

    published = Post.query.filter_by(published=True)

    # Contagem por categoria sai da carteira publicada inteira, não do
    # resultado filtrado — senão o número ao lado de cada filtro mudaria
    # a cada busca e deixaria de dizer "quantos existem nessa categoria".
    counts = dict(
        db.session.query(Post.category, db.func.count(Post.id))
        .filter(Post.published.is_(True))
        .group_by(Post.category)
        .all()
    )
    categories = [
        {"value": value, "label": label, "count": counts.get(value, 0)}
        for value, label in POST_CATEGORY_LABELS.items()
        if counts.get(value, 0)
    ]

    query = published
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Post.title.ilike(like), Post.excerpt.ilike(like), Post.body.ilike(like))
        )
    if categoria in POST_CATEGORY_LABELS:
        query = query.filter(Post.category == categoria)

    posts = query.order_by(Post.created_at.desc(), Post.id.desc()).all()
    # O card grande de "mais recente" só faz sentido na visão sem filtro:
    # com busca ou categoria ativa, todos os resultados têm o mesmo peso.
    featured = posts[0] if posts and not q and not categoria else None
    rest = posts[1:] if featured else posts

    return render_template(
        "noticias.html",
        featured=featured,
        posts=rest,
        total=len(posts),
        categories=categories,
        query=q,
        categoria=categoria,
        **header_context(),
    )


@app.route("/noticias/<slug>")
def news_post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    related = (
        Post.query.filter(Post.published.is_(True), Post.id != post.id, Post.category == post.category)
        .order_by(Post.created_at.desc(), Post.id.desc())
        .limit(3)
        .all()
    )
    return render_template("noticia.html", post=post, related=related, **header_context())


@app.route("/contato", methods=["POST"])
def contato():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not phone:
        flash("Preencha nome e telefone para que um consultor possa retornar.", "error")
        return redirect(url_for("index") + "#contato")

    lead = Lead(name=name, phone=phone, email=email or None, message=message or None)
    db.session.add(lead)
    db.session.commit()

    flash("Recebemos seus dados. Um consultor da VDC vai falar com você em breve.", "success")
    return redirect(url_for("index") + "#contato")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    next_url = request.values.get("next") or url_for("admin_properties")

    if request.method == "GET":
        return render_template("admin/login.html", next=next_url)

    password = request.form.get("password", "")
    admin_password = app.config["ADMIN_PASSWORD"]

    if not admin_password:
        flash("ADMIN_PASSWORD não configurada no .env — avise quem cuida do servidor.", "error")
        return redirect(url_for("admin_login", next=next_url))

    if not secrets.compare_digest(password, admin_password):
        flash("Senha incorreta.", "error")
        return redirect(url_for("admin_login", next=next_url))

    session.permanent = True
    session["is_admin"] = True
    return redirect(next_url)


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("is_admin", None)
    flash("Sessão encerrada.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin/hero", methods=["GET"])
@require_admin
def admin_hero():
    slides = HeroSlide.query.order_by(HeroSlide.sort_order.asc(), HeroSlide.id.asc()).all()
    return render_template("admin/hero.html", slides=slides)


@app.route("/admin/hero/upload", methods=["POST"])
@require_admin
def admin_hero_upload():
    file = request.files.get("image")
    alt_text = request.form.get("alt_text", "").strip()

    if not file or file.filename == "":
        flash("Selecione uma imagem para enviar.", "error")
        return redirect(url_for("admin_hero"))

    if not allowed_image(file.filename):
        flash("Formato não suportado. Use JPG, PNG ou WEBP.", "error")
        return redirect(url_for("admin_hero"))

    extension = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    stored_name = f"{uuid.uuid4().hex}.{extension}"
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], stored_name))

    max_order = db.session.query(db.func.max(HeroSlide.sort_order)).scalar() or 0
    slide = HeroSlide(
        image_path=f"uploads/hero/{stored_name}",
        alt_text=alt_text or "Imóvel VDC Imóveis",
        sort_order=max_order + 1,
        active=True,
    )
    db.session.add(slide)
    db.session.commit()

    flash("Imagem adicionada ao carrossel do hero.", "success")
    return redirect(url_for("admin_hero"))


@app.route("/admin/hero/<int:slide_id>/toggle", methods=["POST"])
@require_admin
def admin_hero_toggle(slide_id):
    slide = db.get_or_404(HeroSlide, slide_id)
    slide.active = not slide.active
    db.session.commit()
    return redirect(url_for("admin_hero"))


@app.route("/admin/hero/<int:slide_id>/move", methods=["POST"])
@require_admin
def admin_hero_move(slide_id):
    direction = request.form.get("direction")
    slide = db.get_or_404(HeroSlide, slide_id)
    neighbor_query = HeroSlide.query.filter(HeroSlide.id != slide.id)
    if direction == "up":
        neighbor = (
            neighbor_query.filter(HeroSlide.sort_order <= slide.sort_order)
            .order_by(HeroSlide.sort_order.desc())
            .first()
        )
    else:
        neighbor = (
            neighbor_query.filter(HeroSlide.sort_order >= slide.sort_order)
            .order_by(HeroSlide.sort_order.asc())
            .first()
        )
    if neighbor:
        slide.sort_order, neighbor.sort_order = neighbor.sort_order, slide.sort_order
        db.session.commit()
    return redirect(url_for("admin_hero"))


@app.route("/admin/hero/<int:slide_id>/delete", methods=["POST"])
@require_admin
def admin_hero_delete(slide_id):
    slide = db.get_or_404(HeroSlide, slide_id)
    file_path = os.path.join(os.path.dirname(__file__), "static", slide.image_path)
    db.session.delete(slide)
    db.session.commit()
    if os.path.exists(file_path):
        os.remove(file_path)
    flash("Imagem removida.", "success")
    return redirect(url_for("admin_hero"))


@app.route("/admin/equipe", methods=["GET"])
@require_admin
def admin_team():
    members = TeamMember.query.order_by(TeamMember.sort_order.asc(), TeamMember.id.asc()).all()
    return render_template("admin/equipe.html", members=members)


def _team_member_payload(form):
    return {
        "name": form.get("name", "").strip(),
        "role": form.get("role", "").strip(),
        "credential": form.get("credential", "").strip(),
        "initials": form.get("initials", "").strip().upper()[:2],
        "bio": form.get("bio", "").replace(chr(13) + chr(10), chr(10)).replace(chr(13), chr(10)).strip(),
        "placeholder": form.get("placeholder") == "on",
    }


def _validate_team_member_payload(data):
    if not data["name"] or not data["role"]:
        return "Preencha nome e função."
    if not data["initials"]:
        return "Preencha as iniciais (até 2 letras, usadas no avatar)."
    return None


@app.route("/admin/equipe/novo", methods=["GET", "POST"])
@require_admin
def admin_team_new():
    if request.method == "GET":
        return render_template("admin/equipe_form.html", member=None)

    data = _team_member_payload(request.form)
    error = _validate_team_member_payload(data)
    if error:
        flash(error, "error")
        return redirect(url_for("admin_team_new"))

    photo_path, photo_error = _save_upload(request.files.get("photo"), "TEAM_UPLOAD_FOLDER", "equipe")
    if photo_error:
        flash(photo_error, "error")
        return redirect(url_for("admin_team_new"))

    max_order = db.session.query(db.func.max(TeamMember.sort_order)).scalar() or 0
    member = TeamMember(sort_order=max_order + 1, photo_path=photo_path, **data)
    db.session.add(member)
    db.session.commit()
    flash("Integrante da equipe cadastrado.", "success")
    return redirect(url_for("admin_team"))


@app.route("/admin/equipe/<int:member_id>/editar", methods=["GET", "POST"])
@require_admin
def admin_team_edit(member_id):
    member = db.get_or_404(TeamMember, member_id)
    if request.method == "GET":
        return render_template("admin/equipe_form.html", member=member)

    data = _team_member_payload(request.form)
    error = _validate_team_member_payload(data)
    if error:
        flash(error, "error")
        return redirect(url_for("admin_team_edit", member_id=member_id))

    member.name = data["name"]
    member.role = data["role"]
    member.credential = data["credential"]
    member.initials = data["initials"]
    member.bio = data["bio"]
    member.placeholder = data["placeholder"]

    photo_path, photo_error = _save_upload(request.files.get("photo"), "TEAM_UPLOAD_FOLDER", "equipe")
    if photo_error:
        flash(photo_error, "error")
        return redirect(url_for("admin_team_edit", member_id=member_id))
    if photo_path:
        _delete_upload(member.photo_path)
        member.photo_path = photo_path
    elif request.form.get("remove_image") == "1":
        _delete_upload(member.photo_path)
        member.photo_path = None
    db.session.commit()
    flash("Integrante da equipe atualizado.", "success")
    return redirect(url_for("admin_team"))


@app.route("/admin/equipe/<int:member_id>/move", methods=["POST"])
@require_admin
def admin_team_move(member_id):
    direction = request.form.get("direction")
    member = db.get_or_404(TeamMember, member_id)
    neighbor_query = TeamMember.query.filter(TeamMember.id != member.id)
    if direction == "up":
        neighbor = (
            neighbor_query.filter(TeamMember.sort_order <= member.sort_order)
            .order_by(TeamMember.sort_order.desc())
            .first()
        )
    else:
        neighbor = (
            neighbor_query.filter(TeamMember.sort_order >= member.sort_order)
            .order_by(TeamMember.sort_order.asc())
            .first()
        )
    if neighbor:
        member.sort_order, neighbor.sort_order = neighbor.sort_order, member.sort_order
        db.session.commit()
    return redirect(url_for("admin_team"))


@app.route("/admin/equipe/<int:member_id>/excluir", methods=["POST"])
@require_admin
def admin_team_delete(member_id):
    member = db.get_or_404(TeamMember, member_id)
    photo_path = member.photo_path
    db.session.delete(member)
    db.session.commit()
    _delete_upload(photo_path)
    flash("Integrante removido.", "success")
    return redirect(url_for("admin_team"))


@app.route("/admin/quem-somos", methods=["GET", "POST"])
@require_admin
def admin_about():
    page = AboutPage.get()
    if request.method == "GET":
        return render_template("admin/quem-somos.html", page=page)

    campos = (
        "hero_eyebrow", "hero_title", "hero_highlight", "hero_lead",
        "stats", "history", "badge_value", "badge_label",
        "mission", "vision", "values_list",
    )
    for campo in campos:
        valor = request.form.get(campo, "")
        setattr(page, campo, valor.replace(chr(13) + chr(10), chr(10)).replace(chr(13), chr(10)).strip())

    for campo, arquivo in (("hero_image_path", "hero_image"), ("history_image_path", "history_image")):
        caminho, erro = _save_upload(request.files.get(arquivo), "ABOUT_UPLOAD_FOLDER", "quem-somos")
        if erro:
            flash(erro, "error")
            return redirect(url_for("admin_about"))
        if caminho:
            _delete_upload(getattr(page, campo))
            setattr(page, campo, caminho)
        elif request.form.get(f"remove_{arquivo}") == "1":
            _delete_upload(getattr(page, campo))
            setattr(page, campo, None)

    db.session.commit()
    flash("Página \"Quem somos\" atualizada.", "success")
    return redirect(url_for("admin_about"))


@app.route("/admin/configuracoes", methods=["GET", "POST"])
@require_admin
def admin_settings():
    settings = SiteSettings.get()
    if request.method == "GET":
        return render_template("admin/configuracoes.html", settings=settings)

    whatsapp_number = request.form.get("whatsapp_number", "").strip()
    instagram_handle = request.form.get("instagram_handle", "").strip()
    instagram_url = request.form.get("instagram_url", "").strip()

    if not whatsapp_number.isdigit():
        flash("WhatsApp: use só números, com DDI e DDD (ex.: 5577912345678).", "error")
        return redirect(url_for("admin_settings"))
    if instagram_url and not instagram_url.startswith("https://"):
        flash("Link do Instagram precisa começar com https://.", "error")
        return redirect(url_for("admin_settings"))

    settings.whatsapp_number = whatsapp_number
    settings.instagram_handle = instagram_handle
    settings.instagram_url = instagram_url
    settings.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    flash("Configurações atualizadas.", "success")
    return redirect(url_for("admin_settings"))


def _safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _apply_geocoding(prop, data, force=False):
    """Preenche latitude/longitude do imóvel a partir do endereço.

    Só chama o Nominatim quando precisa: se o endereço não mudou desde a
    última consulta e já existe coordenada gravada, reaproveita o que
    está no banco (requisito de "evitar consultas desnecessárias"). O
    admin nunca digita coordenada — tudo aqui é automático.

    Devolve a mensagem de aviso para o admin, ou None se deu tudo certo.
    Nunca levanta exceção: falha de geocodificação não pode impedir o
    cadastro do imóvel."""
    query = geocoding.build_query(
        street_address=data["street_address"],
        street_number=data["street_number"],
        neighborhood=data["neighborhood"],
        city=data["city"],
        state=data["state"],
        cep=data["cep"],
    )
    ja_tem_coordenada = prop.latitude is not None and prop.longitude is not None
    if not force and ja_tem_coordenada and prop.geocode_query == query:
        return None

    endereco_mudou = prop.geocode_query != query
    resultado = geocoding.geocode_address(
        street_address=data["street_address"],
        street_number=data["street_number"],
        neighborhood=data["neighborhood"],
        city=data["city"],
        state=data["state"],
        cep=data["cep"],
    )

    prop.geocode_query = query
    prop.geocode_status = resultado.status
    prop.geocoded_at = datetime.now(timezone.utc)

    if resultado.ok:
        prop.latitude = resultado.latitude
        prop.longitude = resultado.longitude
        prop.geocode_precision = resultado.precision
        return None

    # Falhou. Se o endereço mudou, a coordenada antiga aponta para o
    # endereço velho e vira mentira — some com ela. Se o endereço é o
    # mesmo (ex.: nova tentativa que bateu no limite do serviço),
    # preserva o que já estava certo.
    if endereco_mudou:
        prop.latitude = None
        prop.longitude = None
        prop.geocode_precision = None
    return resultado.message


def _property_payload(form):
    cover_tone = form.get("cover_tone", "navy").strip()
    status = form.get("status", "venda").strip()
    return {
        "title": form.get("title", "").strip(),
        "property_type": form.get("property_type", "").strip(),
        "status": status if status in ("venda", "aluguel") else "venda",
        "neighborhood": form.get("neighborhood", "").strip(),
        "cep": form.get("cep", "").strip(),
        "street_address": form.get("street_address", "").strip(),
        "street_number": form.get("street_number", "").strip(),
        "complement": form.get("complement", "").strip(),
        # city/state são NOT NULL no banco: campo vazio cai no padrão da
        # imobiliária em vez de quebrar o insert.
        "city": form.get("city", "").strip() or "Vitória da Conquista",
        "state": (form.get("state", "").strip() or "BA").upper()[:2],
        "price": form.get("price", "").strip(),
        "area_m2": form.get("area_m2", "").strip(),
        "bedrooms": _safe_int(form.get("bedrooms", "").strip() or "0"),
        "parking_spots": _safe_int(form.get("parking_spots", "").strip() or "0"),
        "description": form.get("description", "").strip(),
        "featured": form.get("featured") == "on",
        "cover_tone": cover_tone if cover_tone in ("navy", "gold", "sand") else "navy",
    }


def _validate_property_payload(data):
    if not data["title"] or not data["neighborhood"]:
        return "Preencha título e bairro."
    if data["property_type"] not in PROPERTY_TYPE_LABELS:
        return "Escolha um tipo de imóvel válido."
    try:
        price = float(data["price"])
        area = float(data["area_m2"])
        if price <= 0 or area <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return "Valor e área precisam ser números maiores que zero."
    return None


def _delete_property_image_file(image_path):
    if not image_path:
        return
    file_path = os.path.join(os.path.dirname(__file__), "static", image_path)
    if os.path.exists(file_path):
        os.remove(file_path)


def _delete_photo_files(photo):
    """Remove os dois arquivos (exibição + miniatura) de uma foto da
    galeria. Chame antes do commit que apaga a linha, ou guarde os
    caminhos antes — depois de deletado o objeto não tem mais atributos."""
    _delete_property_image_file(photo.url)
    _delete_property_image_file(photo.thumb_url)


def _sync_cover_image_path(prop):
    """Mantém vdc_properties.image_path = url da foto principal atual.

    Isso é o que permite os cards, a busca e o popup do mapa
    continuarem lendo prop.image_path sem saber que a galeria existe —
    ver comentário no model Property."""
    principal = prop.primary_photo
    prop.image_path = principal.url if principal else None


def _resolve_photo_ref(ref, existentes_por_id, novas_por_indice):
    """"existing:123" -> a foto já salva com id 123; "new:0" -> a
    foto recém-processada nesta mesma requisição, na posição 0 da
    lista de arquivos enviada. None se a referência não bate com nada
    (campo adulterado, ou a foto falhou ao processar)."""
    if not ref or ":" not in ref:
        return None
    tipo, valor = ref.split(":", 1)
    try:
        chave = int(valor)
    except ValueError:
        return None
    if tipo == "existing":
        return existentes_por_id.get(chave)
    if tipo == "new":
        return novas_por_indice.get(chave)
    return None


def _apply_property_photos(prop, form, files):
    """Aplica de uma vez as mudanças da galeria vindas do formulário do
    admin: exclusões, fotos novas, ordem final e foto principal — tudo
    o que o gerenciador client-side (property-photos.js) monta em 3
    campos ocultos antes do submit:

      deleted_photo_ids  JSON com os ids das fotos existentes a apagar
      photos_order       JSON com a ordem final, cada item
                          "existing:<id>" ou "new:<índice em `files`>"
      primary_photo_ref  a referência (mesmo formato) da foto principal

    `prop` precisa já ter um id (fazer flush antes de chamar, se for
    cadastro novo). Fotos que falharem ao processar são puladas — as
    demais são salvas normalmente; devolve a mensagem de erro da
    última falha (ou None se todas as fotos novas processaram bem)."""
    deleted_ids = set()
    raw_deleted = (form.get("deleted_photo_ids") or "").strip()
    if raw_deleted:
        try:
            deleted_ids = {int(x) for x in json.loads(raw_deleted)}
        except (ValueError, TypeError):
            deleted_ids = set()

    for photo in list(prop.photos):
        if photo.id in deleted_ids:
            _delete_photo_files(photo)
            prop.photos.remove(photo)  # cascade="delete-orphan" cuida do DELETE

    erro = None
    novas_por_indice = {}
    for indice, file in enumerate(files):
        if not file or file.filename == "":
            continue
        full_bytes, thumb_bytes, nome_base, erro_arquivo = image_processing.process_property_photo(file)
        if erro_arquivo:
            erro = erro_arquivo
            continue
        full_name, thumb_name = f"{nome_base}.jpg", f"{nome_base}_thumb.jpg"
        pasta = app.config["PROPERTY_UPLOAD_FOLDER"]
        with open(os.path.join(pasta, full_name), "wb") as fh:
            fh.write(full_bytes)
        with open(os.path.join(pasta, thumb_name), "wb") as fh:
            fh.write(thumb_bytes)
        photo = PropertyPhoto(
            url=f"uploads/imoveis/{full_name}",
            thumb_url=f"uploads/imoveis/{thumb_name}",
            sort_order=0, is_primary=False,
        )
        # prop.photos.append (não db.session.add + property_id solto):
        # setar só a FK crua deixa a coleção prop.photos em memória
        # desatualizada até um refresh — e _sync_cover_image_path lê
        # exatamente essa coleção logo abaixo pra achar a principal.
        prop.photos.append(photo)
        novas_por_indice[indice] = photo

    existentes_por_id = {photo.id: photo for photo in prop.photos if photo.id is not None}

    raw_order = (form.get("photos_order") or "").strip()
    try:
        ordem_refs = json.loads(raw_order) if raw_order else []
    except (ValueError, TypeError):
        ordem_refs = []

    ordenadas, vistas = [], set()
    for ref in ordem_refs:
        foto = _resolve_photo_ref(ref, existentes_por_id, novas_por_indice)
        if foto is not None and foto not in vistas:
            ordenadas.append(foto)
            vistas.add(foto)
    # Qualquer foto que não veio no campo de ordem (JS não rodou, ou uma
    # referência não bateu) entra no fim em vez de sumir silenciosamente.
    for foto in list(existentes_por_id.values()) + list(novas_por_indice.values()):
        if foto not in vistas:
            ordenadas.append(foto)
            vistas.add(foto)

    for posicao, foto in enumerate(ordenadas):
        foto.sort_order = posicao

    principal_ref = (form.get("primary_photo_ref") or "").strip()
    principal = _resolve_photo_ref(principal_ref, existentes_por_id, novas_por_indice) if principal_ref else None
    if principal is None and ordenadas:
        principal = ordenadas[0]
    for foto in ordenadas:
        foto.is_primary = foto is principal

    _sync_cover_image_path(prop)
    return erro


PROPERTIES_PER_PAGE = 10


@app.route("/admin/imoveis", methods=["GET"])
@require_admin
def admin_properties():
    page = request.args.get("page", 1, type=int)
    pagination = Property.query.order_by(Property.created_at.desc(), Property.id.desc()).paginate(
        page=page, per_page=PROPERTIES_PER_PAGE, error_out=False
    )
    return render_template(
        "admin/imoveis.html",
        properties=pagination.items,
        pagination=pagination,
        total_count=Property.query.count(),
        featured_count=Property.query.filter_by(featured=True).count(),
    )


@app.route("/admin/imoveis/novo", methods=["GET", "POST"])
@require_admin
def admin_properties_new():
    if request.method == "GET":
        return render_template("admin/imoveis_form.html", prop=None, **search_filter_options())

    data = _property_payload(request.form)
    error = _validate_property_payload(data)
    if error:
        flash(error, "error")
        return redirect(url_for("admin_properties_new"))

    prop = Property(
        title=data["title"], property_type=data["property_type"], status=data["status"],
        neighborhood=data["neighborhood"], city=data["city"], state=data["state"],
        cep=data["cep"] or None, street_address=data["street_address"] or None,
        street_number=data["street_number"] or None, complement=data["complement"] or None,
        price=float(data["price"]), area_m2=float(data["area_m2"]),
        bedrooms=data["bedrooms"], parking_spots=data["parking_spots"],
        description=data["description"] or None, featured=data["featured"], cover_tone=data["cover_tone"],
    )
    aviso = _apply_geocoding(prop, data)
    db.session.add(prop)
    # flush (não commit): garante prop.id sem fechar a transação — as
    # fotos precisam desse id pra serem gravadas na mesma tabela, e um
    # erro de foto ainda pode dar rollback em tudo junto.
    db.session.flush()

    erro_foto = _apply_property_photos(prop, request.form, request.files.getlist("photos"))
    db.session.commit()
    flash("Imóvel cadastrado com sucesso.", "success")
    if aviso:
        flash(aviso, "error")
    if erro_foto:
        flash(erro_foto, "error")
    return redirect(url_for("admin_properties"))


@app.route("/admin/imoveis/<int:property_id>/editar", methods=["GET", "POST"])
@require_admin
def admin_properties_edit(property_id):
    prop = db.get_or_404(Property, property_id)
    if request.method == "GET":
        return render_template("admin/imoveis_form.html", prop=prop, **search_filter_options())

    data = _property_payload(request.form)
    error = _validate_property_payload(data)
    if error:
        flash(error, "error")
        return redirect(url_for("admin_properties_edit", property_id=property_id))

    prop.title = data["title"]
    prop.property_type = data["property_type"]
    prop.status = data["status"]
    prop.neighborhood = data["neighborhood"]
    prop.city = data["city"]
    prop.state = data["state"]
    prop.cep = data["cep"] or None
    prop.street_address = data["street_address"] or None
    prop.street_number = data["street_number"] or None
    prop.complement = data["complement"] or None
    # _apply_geocoding decide sozinho se precisa consultar o serviço:
    # endereço igual ao da última consulta não gera requisição nova.
    aviso = _apply_geocoding(prop, data)
    prop.price = float(data["price"])
    prop.area_m2 = float(data["area_m2"])
    prop.bedrooms = data["bedrooms"]
    prop.parking_spots = data["parking_spots"]
    prop.description = data["description"] or None
    prop.featured = data["featured"]
    prop.cover_tone = data["cover_tone"]

    erro_foto = _apply_property_photos(prop, request.form, request.files.getlist("photos"))
    db.session.commit()
    flash("Imóvel atualizado.", "success")
    if aviso:
        flash(aviso, "error")
    if erro_foto:
        flash(erro_foto, "error")
    return redirect(url_for("admin_properties"))


@app.route("/admin/imoveis/<int:property_id>/localizar", methods=["POST"])
@require_admin
def admin_properties_geocode(property_id):
    """Nova tentativa manual de localizar o endereço no mapa.

    Existe para o caso em que a geocodificação falhou por motivo passageiro
    (limite de requisições, timeout): o admin não precisa reabrir e salvar
    o imóvel inteiro só para tentar de novo."""
    prop = db.get_or_404(Property, property_id)
    data = {
        "street_address": prop.street_address or "",
        "street_number": prop.street_number or "",
        "complement": prop.complement or "",
        "neighborhood": prop.neighborhood or "",
        "city": prop.city or "",
        "state": prop.state or "",
        "cep": prop.cep or "",
    }
    aviso = _apply_geocoding(prop, data, force=True)
    db.session.commit()
    if aviso:
        flash(aviso, "error")
    else:
        flash(f"Endereço localizado. {prop.map_precision_label}", "success")
    return redirect(url_for("admin_properties"))


@app.route("/admin/imoveis/<int:property_id>/destaque", methods=["POST"])
@require_admin
def admin_properties_toggle_featured(property_id):
    prop = db.get_or_404(Property, property_id)
    prop.featured = not prop.featured
    db.session.commit()
    return redirect(url_for("admin_properties"))


@app.route("/admin/imoveis/<int:property_id>/excluir", methods=["POST"])
@require_admin
def admin_properties_delete(property_id):
    prop = db.get_or_404(Property, property_id)
    # Guarda os caminhos antes do delete — depois do commit as linhas
    # (e os objetos Python) não existem mais pra consultar.
    arquivos = [(photo.url, photo.thumb_url) for photo in prop.photos]
    db.session.delete(prop)  # cascade cuida das linhas de vdc_property_photos
    db.session.commit()
    for url, thumb_url in arquivos:
        _delete_property_image_file(url)
        _delete_property_image_file(thumb_url)
    flash("Imóvel removido.", "success")
    return redirect(url_for("admin_properties"))


def _save_post_image(file):
    """Valida e salva a imagem de capa da notícia; devolve o caminho
    relativo (ou None se não veio arquivo)."""
    if not file or file.filename == "":
        return None, None
    if not allowed_image(file.filename):
        return None, "Formato de imagem não suportado. Use JPG, PNG ou WEBP."
    extension = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    stored_name = f"{uuid.uuid4().hex}.{extension}"
    file.save(os.path.join(app.config["POST_UPLOAD_FOLDER"], stored_name))
    return f"uploads/noticias/{stored_name}", None


def _delete_post_image_file(image_path):
    if not image_path:
        return
    file_path = os.path.join(os.path.dirname(__file__), "static", image_path)
    if os.path.exists(file_path):
        os.remove(file_path)


def _unique_slug(title, post_id=None):
    """Slug do título, com sufixo numérico se já existir outro post com o
    mesmo (dois títulos iguais são possíveis; a URL precisa ser única)."""
    base = slugify(title)
    candidate = base
    suffix = 2
    while True:
        clash = Post.query.filter(Post.slug == candidate)
        if post_id is not None:
            clash = clash.filter(Post.id != post_id)
        if clash.first() is None:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1


def _post_payload(form):
    category = form.get("category", "").strip()
    return {
        "title": form.get("title", "").strip(),
        "category": category if category in POST_CATEGORY_LABELS else "mercado",
        "excerpt": form.get("excerpt", "").strip(),
        # Guarda o corpo já com quebra "\n" (o navegador manda "\r\n"),
        # pra separação de parágrafos não depender do cliente que enviou.
        "body": form.get("body", "").replace("\r\n", "\n").replace("\r", "\n").strip(),
        "published": form.get("published") == "on",
    }


def _validate_post_payload(data):
    if not data["title"]:
        return "O título da notícia é obrigatório."
    if not data["body"]:
        return "Escreva o conteúdo da notícia."
    return None


@app.route("/admin/noticias", methods=["GET"])
@require_admin
def admin_news():
    posts = Post.query.order_by(Post.created_at.desc(), Post.id.desc()).all()
    return render_template(
        "admin/noticias.html",
        posts=posts,
        published_count=sum(1 for p in posts if p.published),
    )


@app.route("/admin/noticias/nova", methods=["GET", "POST"])
@require_admin
def admin_news_new():
    if request.method == "GET":
        return render_template("admin/noticias_form.html", post=None, categories=POST_CATEGORY_LABELS)

    data = _post_payload(request.form)
    error = _validate_post_payload(data)
    if error:
        flash(error, "error")
        return redirect(url_for("admin_news_new"))

    image_path, image_error = _save_post_image(request.files.get("image"))
    if image_error:
        flash(image_error, "error")
        return redirect(url_for("admin_news_new"))

    post = Post(
        title=data["title"],
        slug=_unique_slug(data["title"]),
        category=data["category"],
        excerpt=data["excerpt"],
        body=data["body"],
        published=data["published"],
        image_path=image_path,
    )
    db.session.add(post)
    db.session.commit()
    flash("Notícia publicada." if post.published else "Notícia salva como rascunho.", "success")
    return redirect(url_for("admin_news"))


@app.route("/admin/noticias/<int:post_id>/editar", methods=["GET", "POST"])
@require_admin
def admin_news_edit(post_id):
    post = db.get_or_404(Post, post_id)
    if request.method == "GET":
        return render_template("admin/noticias_form.html", post=post, categories=POST_CATEGORY_LABELS)

    data = _post_payload(request.form)
    error = _validate_post_payload(data)
    if error:
        flash(error, "error")
        return redirect(url_for("admin_news_edit", post_id=post_id))

    image_path, image_error = _save_post_image(request.files.get("image"))
    if image_error:
        flash(image_error, "error")
        return redirect(url_for("admin_news_edit", post_id=post_id))

    if image_path:
        _delete_post_image_file(post.image_path)
        post.image_path = image_path
    elif request.form.get("remove_image") == "1":
        _delete_post_image_file(post.image_path)
        post.image_path = None

    # O slug só é refeito quando o título muda: links já compartilhados
    # de uma notícia continuam funcionando se o texto for só corrigido.
    if data["title"] != post.title:
        post.slug = _unique_slug(data["title"], post_id=post.id)
    post.title = data["title"]
    post.category = data["category"]
    post.excerpt = data["excerpt"]
    post.body = data["body"]
    post.published = data["published"]
    db.session.commit()
    flash("Notícia atualizada.", "success")
    return redirect(url_for("admin_news"))


@app.route("/admin/noticias/<int:post_id>/publicar", methods=["POST"])
@require_admin
def admin_news_toggle_published(post_id):
    post = db.get_or_404(Post, post_id)
    post.published = not post.published
    db.session.commit()
    return redirect(url_for("admin_news"))


@app.route("/admin/noticias/<int:post_id>/excluir", methods=["POST"])
@require_admin
def admin_news_delete(post_id):
    post = db.get_or_404(Post, post_id)
    image_path = post.image_path
    db.session.delete(post)
    db.session.commit()
    _delete_post_image_file(image_path)
    flash("Notícia removida.", "success")
    return redirect(url_for("admin_news"))


if __name__ == "__main__":
    app.run(debug=True)
