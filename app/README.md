# VDC Imóveis — Site

Primeira tela (home) da VDC Imóveis em Flask, seguindo a identidade visual em `../Identidade Visual/DESIGN.md`.

Passou por uma auditoria de UX com a skill `ui-ux-pro-max` (`.claude/skills/ui-ux-pro-max/`): toques mínimos de 44×44px em botões de ícone, estados de foco visíveis em todo elemento interativo, avisos (toasts) com auto-dismiss e `aria-live`/`role=alert`, feedback de carregamento no envio de formulários, e uma escala de z-index documentada (`--vdc-z-*` em `style.css`) em vez de valores arbitrários.

**Bug corrigido:** o reordenar de fotos do hero (`/admin/hero`, setas ↑/↓) quebrava com `DuplicatePreparedStatement` — o `DATABASE_URL` do Supabase aponta pro pooler em modo transaction (porta 6543), que não suporta prepared statements do psycopg3 persistindo entre conexões do pool. Corrigido em `config.py` com `connect_args={"prepare_threshold": None}`. Isso protege qualquer operação futura que grave mais de uma linha no mesmo commit, não só essa tela.

**Aprimoramentos de UI/UX (segunda passada, com as skills `ui-ux-pro-max`/`design`):**
- A aba "Busca Avançada" do hero, que antes só mudava de cor sem fazer nada, agora abre filtros de verdade (tipo, bairro, venda/aluguel, faixa de preço) ligados a `/imoveis`.
- Seções da home entram com fade + 16px de subida ao rolar a página — animação que já estava especificada no `DESIGN.md` (seção 10) mas nunca tinha sido implementada. Respeita `prefers-reduced-motion` e degrada bem sem JavaScript (classe `html.js`).
- Capa dos cards de imóvel dá um leve zoom no hover do card.
- Estados vazios ("nenhum imóvel encontrado", "carteira vazia", "sem favoritos") ganharam ícone + título + ação, em vez de uma frase solta.

## Rodar localmente

```bash
pip install -r requirements.txt
python app.py
```

Abre em http://localhost:5000

## Configuração

Copie `.env.example` para `.env` e preencha:

- `DATABASE_URL` — string de conexão do Postgres (Supabase).
- `FLASK_SECRET_KEY` — chave para sessão/flash messages.
- `WHATSAPP_NUMBER` — número no formato `55DDDNUMERO` (hoje é um placeholder, troque pelo número real da VDC).
- `ADMIN_PASSWORD` — senha do painel `/admin/hero` (ver abaixo).

## Banco de dados

Três tabelas próprias, prefixadas com `vdc_` para não colidir com outros projetos que já existem no mesmo projeto Supabase:

- `vdc_properties` — imóveis exibidos na home e na busca. Seis registros de exemplo já estão cadastrados (bairros de Vitória da Conquista) — troque pelos imóveis reais quando houver um painel de cadastro.
- `vdc_leads` — contatos enviados pelo formulário da seção "Fale com a VDC".
- `vdc_hero_slides` — fotos do carrossel do topo da home.

## Trocar as fotos do hero

Acesse **`/admin/hero`** (usuário `admin`, senha em `ADMIN_PASSWORD` no `.env`, autenticação HTTP Basic). Lá dá para:

- Enviar uma nova foto (JPG/PNG/WEBP, até 8MB) com uma descrição;
- Reordenar com as setas ↑ / ↓;
- Pausar uma foto sem apagar (ela some do carrossel, mas fica salva);
- Excluir definitivamente (remove o arquivo do disco também).

As fotos ficam em `static/uploads/hero/`. Hoje o carrossel está com 3 fotos de banco de imagens (Unsplash, uso livre) só como exemplo de composição — troque pelas fotos reais dos imóveis/fachadas da VDC assim que possível. Se todas as fotos forem removidas, a home volta sozinha para um visual de marca (arco dourado sobre navy) em vez de quebrar.

## Cabeçalho: menu e favoritos

- **Dropdown "Imóveis"** no menu principal: Comprar / Alugar / Ver todos, com filtro por `status` já funcionando em `/imoveis?status=venda|aluguel`.
- **Botão "Menu"**: abre um mega menu (colunas Imóveis / A VDC / Atendimento + card de destaque), igual em desktop e mobile — não existe mais um menu mobile separado.
- **Favoritos**: ícone de coração no cabeçalho e em cada card de imóvel. Guardado no `localStorage` do navegador (chave `vdc_favorites`), sem precisar de login. Não depende do banco — é por navegador/dispositivo.
- Conteúdo do menu e da navegação vem de `content.py` (`NAV_LINKS`, `MEGA_MENU_COLUMNS`) — para adicionar um item, edite lá, não no HTML.

## Estrutura

- `app.py` — rotas (`/`, `/imoveis` busca, `/contato` POST, `/admin/hero*`).
- `models.py` — modelos SQLAlchemy.
- `content.py` — textos e listas de conteúdo estático (nav, especialidades, equipe, selos).
- `templates/` — Jinja2, com `partials/` para header, footer e botão do WhatsApp, e `admin/` para o painel de imagens.
- `static/css/tokens.css` — cópia literal dos design tokens da marca.
- `static/css/style.css` — estilos da home construídos sobre os tokens.
- `static/uploads/hero/` — fotos do carrossel, geridas pelo `/admin/hero`.

## O que falta para produção

- Substituir o número de WhatsApp placeholder.
- Trocar os 6 imóveis de exemplo por dados reais (ou construir um painel de cadastro, no mesmo espírito do `/admin/hero`).
- Trocar as 3 fotos de banco de imagens do hero pelas fotos reais da VDC via `/admin/hero`.
- Preencher nomes reais do consultor e do(a) arquiteto(a) na equipe (hoje há dois placeholders genéricos ao lado de Deyse Fontes e Dr. José Ângelo, que já constam no `DESIGN.md`).
- Trocar `FLASK_SECRET_KEY` e `ADMIN_PASSWORD` por valores fortes gerados para produção, e usar um servidor WSGI (gunicorn/waitress) em vez do servidor de desenvolvimento do Flask.
- Se o site for para produção, considerar mover o armazenamento de fotos do disco local para um bucket (Supabase Storage, S3) — hoje elas vivem em `static/uploads/hero/`, o que não sobrevive a deploys sem disco persistente (ex.: Heroku, containers efêmeros).
