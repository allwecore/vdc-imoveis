# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Compradores de imóvel de médio/alto padrão (para quem essa é a maior compra da vida — decisão de alto risco), investidores, proprietários que querem alugar um imóvel com segurança, e empresas buscando ponto comercial — em Vitória da Conquista (BA) e região. Confirmado pelo usuário como ainda válido.

## Product Purpose

VDC Imóveis é uma consultoria imobiliária integrada, não um portal de anúncios. Existe para dar segurança técnica na maior compra da vida do cliente, reunindo em uma única mesa: consultoria comercial, engenharia civil, arquitetura e assessoria jurídica. Sucesso é o cliente decidir com laudo técnico e assessoria jurídica, nunca com achismo.

## Positioning

O que um concorrente não pode copiar de verdade: engenharia civil, arquitetura e jurídico internos, na mesma equipe que faz a consultoria comercial — não uma imobiliária tradicional terceirizando avaliação técnica e due diligence. Prova concreta: CRECI 35889, laudo técnico, assessoria jurídica, parcerias de seguro (Tokio Marine, Porto Seguro, citadas no material de marca).

## Operating Context

Atendimento presencial em Vitória da Conquista (BA), com WhatsApp como canal direto de contato. Fluxo típico: visitante busca imóvel (texto livre ou filtros — tipo, bairro, venda/aluguel, preço máximo) → vê imóveis em destaque → entra em contato com um consultor (formulário no site ou WhatsApp) → consultor conduz a negociação com apoio técnico/jurídico da equipe.

## Capabilities and Constraints

- Escopo confirmado com o usuário: só corretagem e consultoria imobiliária (compra, venda, aluguel) com apoio técnico interno. Outras frentes sugeridas pelos destaques do Instagram do material de marca (ex.: "Clube VDC", incorporação, gestão de condomínio) **não** fazem parte do produto hoje — são só categorias de conteúdo, não serviços.
- Site atual: Flask + Jinja2 + SQLAlchemy, Postgres via Supabase (pooler em modo transaction — prepared statements desabilitados na conexão por isso). Home com hero em carrossel (fotos geridas por painel admin protegido por senha), busca com filtros básicos/avançados, formulário de contato, favoritos client-side (localStorage).
- Dados de imóveis hoje são de exemplo/placeholder — a carteira real ainda não está no sistema.
- Fotos do hero hoje são de banco de imagens (uso livre), só para composição — ainda não substituídas por fotos reais de imóveis/fachadas da VDC.
- Número de WhatsApp no site é placeholder, ainda não é o número real da empresa.
- Dois papéis da equipe (Consultor de Imóveis, Arquiteto(a)) ficam sem nome próprio por decisão explícita do usuário, até que o dado real seja fornecido — não inventar nome.

## Brand Commitments

CRECI 35889. Assinatura principal: "Conectando você ao seu lugar ideal." Assinatura técnica institucional: "Consultoria, engenharia e jurídico na mesma mesa." Identidade visual completa (cor, tipografia, componentes, voz, regras de uso) documentada em `Identidade Visual/DESIGN.md` — esse arquivo é a autoridade visual do produto e não deve ser reescrito a partir daqui.

## Evidence on Hand

- Equipe com nome confirmado: Deyse Fontes (Engenharia Civil, CREA-BA), Dr. José Ângelo (Jurídico, OAB-BA).
- CRECI 35889 é fato real confirmado.
- Parcerias de seguro citadas no material de marca: Tokio Marine, Porto Seguro (não verificadas além da menção no `DESIGN.md`).
- Instagram: @vdcimoveis.
- Ausências que trabalho futuro não deve inventar: fotos reais de imóveis, carteira real de imóveis, número de WhatsApp real, nomes dos outros 2 integrantes da equipe (consultor, arquiteto/a), anos de mercado ou ano de fundação (não documentado em nenhum lugar).

## Product Principles

1. Segurança técnica antes de qualquer coisa — laudo, medida e assessoria jurídica, nunca achismo.
2. Prova concreta em vez de promessa vaga — credenciais e registros profissionais em destaque, não bullet points genéricos.
3. Tom de especialista que explica, nunca de vendedor que empurra — sem urgência artificial, sem "oferta imperdível".
4. Ancoragem territorial forte — bairro + Vitória da Conquista sempre citados; é o principal canal de busca do cliente.
5. Honestidade sobre dados de exemplo — nunca apresentar imóvel, foto, estatística ou depoimento fabricado como se fosse real.

## Accessibility & Inclusion

Sem requisito específico do cliente além dos padrões já aplicados no site (contraste AA/AAA verificado, alvos de toque ≥40–44px, navegação por teclado, `prefers-reduced-motion` respeitado).
