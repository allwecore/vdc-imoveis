"""Conteúdo estático da home — textos, especialidades, equipe e selos da VDC Imóveis."""

NAV_LINKS = [
    {
        "label": "Imóveis",
        "href": "/imoveis",
        "children": [
            {"label": "Comprar", "href": "/imoveis?status=venda"},
            {"label": "Alugar", "href": "/imoveis?status=aluguel"},
            {"label": "Ver todos os imóveis", "href": "/imoveis"},
        ],
    },
    {
        # Agrupado num dropdown: com Quem somos + Equipe soltos, a linha do
        # cabeçalho não cabia mais em 1200px e a marca era espremida.
        "label": "A VDC",
        "href": "/quem-somos",
        "children": [
            {"label": "Quem somos", "href": "/quem-somos"},
            {"label": "Especialidades", "href": "/#especialidades"},
            {"label": "Nossa equipe", "href": "/equipe"},
        ],
    },
    {"label": "Notícias", "href": "/noticias"},
    {"label": "Contato", "href": "/#contato"},
]

MEGA_MENU_COLUMNS = [
    {
        "title": "Imóveis",
        "links": [
            {"label": "Comprar", "href": "/imoveis?status=venda"},
            {"label": "Alugar", "href": "/imoveis?status=aluguel"},
            {"label": "Ver todos os imóveis", "href": "/imoveis"},
        ],
    },
    {
        "title": "A VDC",
        "links": [
            {"label": "Quem somos", "href": "/quem-somos"},
            {"label": "Especialidades", "href": "/#especialidades"},
            {"label": "Nossa equipe", "href": "/equipe"},
            {"label": "Credenciais", "href": "/#credenciais"},
        ],
    },
    {
        "title": "Notícias",
        "links": [
            {"label": "Todas as notícias", "href": "/noticias"},
            {"label": "Mercado imobiliário", "href": "/noticias?categoria=mercado"},
            {"label": "Financiamento", "href": "/noticias?categoria=financiamento"},
            {"label": "Investimento", "href": "/noticias?categoria=investimento"},
        ],
    },
    {
        "title": "Atendimento",
        "links": [
            {"label": "Falar com um consultor", "href": "/#contato"},
            {"label": "Instagram @vdcimoveis", "href": "https://instagram.com/vdcimoveis"},
            {"label": "Meus favoritos", "action": "favorites"},
        ],
    },
]

QUICK_FILTERS = [
    "Casas à venda",
    "Apartamentos em Recreio",
    "Aluguel no Centro",
    "Salas comerciais",
    "Candeias",
    "Alto Maron",
]

SPECIALTIES = [
    {
        "label": "Consultoria",
        "title": "Consultoria imobiliária",
        "text": "Um consultor dedicado do primeiro contato à assinatura, com conhecimento real do mercado de Vitória da Conquista.",
        "icon": "consultoria",
    },
    {
        "label": "Engenharia",
        "title": "Engenharia civil",
        "text": "Nossa engenheira avalia a estrutura do imóvel antes da assinatura, com laudo técnico fundamentado.",
        "icon": "engenharia",
    },
    {
        "label": "Arquitetura",
        "title": "Projeto e viabilidade",
        "text": "Leitura de planta, viabilidade de reforma e avaliação de projeto realizadas antes da compra.",
        "icon": "arquitetura",
    },
    {
        "label": "Jurídico",
        "title": "Assessoria jurídica",
        "text": "Contrato, documentação e due diligence conduzidos por advogado, na mesma mesa da negociação.",
        "icon": "juridico",
    },
]

SEALS = [
    "CRECI 35889",
    "LAUDO TÉCNICO",
    "ASSESSORIA JURÍDICA",
    "SEGURO LOCATÍCIO",
]

FOOTER_COLUMNS = [
    {
        "title": "Imóveis",
        "links": [
            {"label": "Comprar", "href": "/imoveis?status=venda"},
            {"label": "Alugar", "href": "/imoveis?status=aluguel"},
        ],
    },
    {
        "title": "A VDC",
        "links": [
            {"label": "Quem somos", "href": "/quem-somos"},
            {"label": "Especialidades", "href": "/#especialidades"},
            {"label": "Nossa equipe", "href": "/equipe"},
            {"label": "Notícias", "href": "/noticias"},
            {"label": "Contato", "href": "/#contato"},
        ],
    },
]

# A equipe (vdc_team_members) e o WhatsApp/Instagram (vdc_site_settings)
# viraram dados editáveis em /admin/equipe e /admin/configuracoes — não
# são mais constantes daqui. Ver models.py (TeamMember, SiteSettings).
