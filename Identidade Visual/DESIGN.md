# VDC IMÓVEIS — Sistema de Identidade Visual

**Versão 1.0 · Agosto/2026**
Documento-fonte para posts, site, materiais impressos e geração assistida por IA.

---

## 1. Fundamento da marca

### O que a VDC é (e por que isso define o visual)

A VDC não é uma imobiliária comum. Ela nasceu da parceria entre **um consultor de imóveis e uma engenheira civil**, e depois somou **arquiteto** e **advogado**. Quatro competências técnicas na mesma mesa: comercial, engenharia, projeto e jurídico.

Isso é o ativo real da marca — e é o que o visual precisa comunicar antes de qualquer coisa. Não vendemos "sonho de casa própria" genérico. Vendemos **segurança técnica na maior compra da vida de alguém**, em Vitória da Conquista (BA).

| Eixo | Posição da VDC |
|---|---|
| Categoria | Consultoria imobiliária integrada (não "portal de anúncios") |
| Diferencial | Engenharia + Arquitetura + Jurídico internos |
| Território | Vitória da Conquista e região — Bahia |
| Público | Compradores de médio/alto padrão, investidores, proprietários que querem locar com segurança, empresas buscando ponto comercial |
| Prova | CRECI 35889, laudo técnico, assessoria jurídica, parcerias (Tokio Marine, Porto Seguro) |

### Personalidade

Cinco atributos, em ordem de peso. Toda peça deve passar no teste dos três primeiros.

1. **Técnica** — precisão, medida, laudo. Nada é "achismo".
2. **Institucional** — porte de escritório, não de corretor autônomo.
3. **Confiável** — sóbria, estável, sem euforia de vendas.
4. **Acolhedora** — atendimento humano, nome próprio, WhatsApp direto.
5. **Aspiracional** — o imóvel bonito é o prêmio, não o grito.

**Não somos:** gritados, promocionais, "última chance", neon, adesivos vermelhos, emoji em excesso.

### Tagline e mensagens fixas

- **Assinatura principal:** *Conectando você ao seu lugar ideal.*
- **Assinatura técnica (uso institucional):** *Consultoria, engenharia e jurídico na mesma mesa.*
- **Descritor:** Consultoria Imobiliária · CRECI 35889

---

## 2. O símbolo: o Arco VDC

O logotipo é um monograma **VDC** dentro de um **ciclo de duas setas** — uma dourada descendo pela direita, uma navy subindo pela esquerda. Não é ornamento: é o ciclo do negócio imobiliário (**compra → posse → valorização → nova negociação**) e o ciclo de trabalho da equipe (**consultoria → engenharia → jurídico → entrega**).

Esse arco é o **elemento-assinatura de todo o sistema.** Ele reaparece, sempre em fragmento, como:

- **Recorte de foto em arco/círculo** (já usado no hero do site — manter e sistematizar)
- **Fio dourado curvo** separando seções
- **Marca d'água em 6% de opacidade** em fundos navy sólidos
- **Cantoneira de 90°** em cards de imóvel

> **Regra de ouro:** o arco aparece **uma vez por peça**, em escala grande. Repetido, vira papel de parede e perde a força.

### Uso do logotipo

| Situação | Versão |
|---|---|
| Fundo branco ou claro | Colorida (navy + dourado) |
| Fundo navy sólido | Monocromática branca, ou navy+dourado com o "VDC" branco |
| Fundo fotográfico | Branca sobre véu navy 55% — nunca direto sobre a foto |
| Tamanho mínimo digital | 40 px de altura (símbolo) / 96 px (símbolo + "IMÓVEIS") |
| Área de respiro | Igual à altura da letra "V" em todos os lados |

**Proibido:** distorcer proporção, girar o arco, trocar as cores das setas, aplicar sombra/brilho, colocar dentro de caixa colorida, usar o símbolo sem o arco completo.

---

## 3. Cores

Todos os valores abaixo foram **amostrados diretamente do logotipo e do site atual** — não são aproximações inventadas. A paleta é intencionalmente pequena: duas cores de marca, um bege de apoio, uma escala neutra.

### 3.1 Cores primárias

| Token | Hex | Amostrado de | Papel |
|---|---|---|---|
| `navy-900` | `#152B43` | Monograma do logo | Fundos institucionais escuros, o próprio logo |
| `navy-700` | `#283B62` | **Cor-mãe do site** (títulos, faixas, menu) | Títulos, faixas de seção, botões primários |
| `navy-500` | `#5272B2` | Item ativo do menu | Estado ativo, links, hover |
| `navy-300` | `#8FA3C8` | derivado | Ícones sobre navy, bordas sutis |
| `navy-100` | `#E7ECF5` | derivado | Fundos de bloco, chips, tabela zebrada |

`navy-700 #283B62` é **a cor da VDC**. Se a peça tiver uma cor só, é essa.

### 3.2 Dourado

| Token | Hex | Amostrado de | Papel |
|---|---|---|---|
| `gold-300` | `#F2D376` | Brilho superior da seta | Apenas ponto alto de gradiente metálico |
| `gold-500` | `#C9A44E` | Corpo da seta dourada | **Cor de destaque.** Fios, ícones, preço, selo |
| `gold-700` | `#8F7534` | Sombra da seta | Sombra do gradiente metálico, hover de fio |
| `sand-400` | `#CBB492` | Ícones de linha do site | Ilustrações de linha, molduras leves |
| `sand-100` | `#F5EFE6` | derivado | Fundo alternativo quente (seções de depoimento) |

**Gradiente metálico oficial** (só para o arco e selos, nunca para texto ou botão):
`linear-gradient(135deg, #8F7534 0%, #C9A44E 35%, #F2D376 55%, #C9A44E 78%, #8F7534 100%)`

**Gradiente tonal** (botões e superfícies sólidas grandes — rodapé, faixas navy, CTA):
dois tons da mesma cor, 160°, sem os picos de brilho do metálico. Já era usado nas capas de card de imóvel; a pedido do usuário ("cores muito sólidas... degradê suave e linear") virou o padrão pra qualquer superfície que hoje é uma cor chapada só.
- Navy: `linear-gradient(160deg, var(--vdc-navy-700), var(--vdc-navy-900))`
- Dourado: `linear-gradient(160deg, var(--vdc-gold-700), var(--vdc-gold-500))`

Diferença do metálico: 2 tons (não 5), sem ponto de brilho alto, ângulo fixo em 160°. É sutil o bastante pra não brigar com o texto do botão — o metálico continua proibido em botão/texto por causa disso.

### 3.3 Neutros e funcionais

| Token | Hex | Papel |
|---|---|---|
| `white` | `#FFFFFF` | Fundo padrão |
| `off-white` | `#F7F8FA` | Fundo de seção alternada |
| `gray-400` | `#C9CED8` | Bordas, divisores, placeholder |
| `gray-600` | `#616E89` | **Texto corrido secundário** (amostrado do site) |
| `ink` | `#1A1F2B` | Texto corrido principal em fundo claro |
| `success` | `#1F7A4C` | Confirmações. *(WhatsApp mantém o verde oficial `#25D366` — é marca de terceiro, não altere)* |
| `alert` | `#B4472E` | Erros e avisos. Terracota, não vermelho puro — não briga com o dourado |
| `instagram-gradient` | `linear-gradient(45deg, #FEDA75, #FA7E1E, #D62976, #962FBF, #4F5BD5)` | Gradiente oficial da marca Instagram — mesma exceção do WhatsApp, terceiro, não altere |

### 3.4 Proporção de uso — regra 60/30/10

- **60 %** branco / off-white (respiro é o que dá ar de "premium")
- **30 %** navy (`navy-700` e `navy-900`)
- **10 %** dourado + bege — **nunca mais que isso.** Dourado em excesso vira bijuteria.

### 3.5 Acessibilidade — contrastes verificados

| Combinação | Razão | Veredito |
|---|---|---|
| `navy-700` sobre branco | **11,1 : 1** | ✅ AAA — combinação padrão de texto |
| `gray-600` sobre branco | **5,1 : 1** | ✅ AA para texto corrido |
| `gold-500` sobre `navy-700` | **4,7 : 1** | ⚠️ Só títulos ≥ 24 px, ícones, fios e bordas. **Nunca texto corrido** |
| `gold-500` sobre branco | **2,4 : 1** | ❌ Decorativo apenas. Nunca texto |
| `sand-400` sobre branco | **2,0 : 1** | ❌ Só ícone de linha decorativo (uso atual do site é aceitável, mas o rótulo abaixo do ícone precisa ser navy) |
| Branco sobre `navy-700` | 11,1 : 1 | ✅ AAA |

---

## 4. Tipografia

**Atualizado (auditoria de tipografia, ago/2026):** a Lato foi trocada pela Hanken Grotesk no papel de texto corrido — uma varredura mecânica de identidade visual sinalizou a Lato como uma das faces mais usadas da web (perdia a distinção que o Archivo e o IBM Plex Mono já tinham). A Hanken Grotesk mantém a mesma **temperatura** (legível, sóbria, sem serifa dramática, ótima em parágrafo longo e tela pequena) e, por ser também uma grotesca, cria mais parentesco visual com o Archivo dos títulos do que a Lato — antes eram duas famílias de naturezas diferentes (grotesca + humanista clássica) convivendo lado a lado.

### 4.1 As três vozes

| Papel | Fonte | Por quê |
|---|---|---|
| **Display / Títulos** | **Archivo** (600, 700) | Grotesca de traço reto e ombros firmes. Em caixa alta com tracking apertado, tem porte de placa de obra e de fachada de escritório — exatamente o cruzamento engenharia + institucional da VDC. |
| **Texto** | **Hanken Grotesk** (400, 600, 700) | Grotesca humanista, quente e legível, sem o excesso de uso da Lato — mantém a mesma temperatura sóbria e acrescenta mais caráter próprio. Por ser grotesca como o Archivo, os dois se comportam como uma família só em vez de duas vozes desencontradas. Excelente em parágrafo longo e em tela pequena. |
| **Dados / Utilitária** | **IBM Plex Mono** (500) | **Esta é a aposta do sistema.** Preço, metragem, CRECI, código do imóvel e coordenadas saem em monoespaçada. É a assinatura que traduz "aqui tem laudo, medida e número conferido" sem precisar dizer. Nenhuma imobiliária da região faz isso. |

**Fallback (e-mail, Office, sistemas sem webfont):** Archivo → Arial Black/Arial · Hanken Grotesk → Segoe UI/Arial · IBM Plex Mono → Consolas/Courier New.

```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=Hanken+Grotesk:wght@400;600;700&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
```

### 4.2 Escala tipográfica (base 16 px, razão 1,25)

| Token | Tamanho | Fonte / Peso | Tracking | Uso |
|---|---|---|---|---|
| `display` | 61 px | Archivo 700 | −0,02em | Hero do site, capa de carrossel |
| `h1` | 49 px | Archivo 700 | −0,02em | Título de página |
| `h2` | 39 px | Archivo 700 | −0,01em | Título de seção |
| `h3` | 31 px | Archivo 600 | 0 | Sub-seção, nome do imóvel |
| `h4` | 25 px | Archivo 600 | 0 | Card |
| `eyebrow` | 13 px | Archivo 600 · CAIXA ALTA | **+0,14em** | Rótulo acima do título. Sempre em `gold-500` ou `navy-500` |
| `lead` | 19 px | Hanken Grotesk 400 | 0 | Parágrafo de abertura |
| `body` | 16 px | Hanken Grotesk 400 | 0 | Texto corrido — altura de linha 1,65 |
| `small` | 14 px | Hanken Grotesk 400 | 0 | Legenda, nota de rodapé |
| `data` | 16–31 px | IBM Plex Mono 500 | +0,02em | Preço, m², CRECI, código |
| `caption` | 12 px | IBM Plex Mono 500 · CAIXA ALTA | +0,1em | Etiqueta de foto, crédito |

**Regras de composição**
- Título em caixa alta: **máximo 5 palavras**. Acima disso, use caixa alta e baixa.
- Largura de parágrafo: **60–75 caracteres**. No site atual, alguns blocos passam disso.
- Nunca mais de **dois pesos** de Archivo numa mesma peça.
- Nunca centralize parágrafo com mais de 2 linhas.

---

## 5. Espaçamento, grid e forma

### Escala de espaçamento (base 4 px)
`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 160`

Nada fora dessa lista. Se precisou de 27 px, arredonde para 24 ou 32.

### Grid
| | |
|---|---|
| Colunas | 12 (desktop) · 8 (tablet) · 4 (mobile) |
| Gutter | 24 px |
| Largura máxima do conteúdo | 1200 px |
| Margem lateral | 24 px (mobile) · 48 px (tablet) · 80 px (desktop) |
| Padding vertical de seção | 96 px desktop · 64 px tablet · 48 px mobile |
| Breakpoints | 480 · 768 · 1024 · 1280 px |

### Raio de canto — a marca é reta

| Elemento | Raio |
|---|---|
| Faixas, seções, imagens de destaque | **0** |
| Inputs, cards, chips | **4 px** |
| Botões (`.vdc-btn` e variantes) | **círculo total** (pílula) |
| Foto-retrato, avatar, selo, ícone circular | **círculo total** |

O contraste entre **reto absoluto** e **círculo perfeito** é herdado do logo (monograma reto dentro de arco circular). É o que dá coerência sem esforço. Cantos de 12/16/24 px — o arredondado genérico de dashboard — estão fora do sistema: nunca um meio-termo, sempre um dos dois polos. Botões migraram do reto (4 px) pro círculo total a pedido do usuário — "mais modernos, evitar algo muito quadrado" — mantendo o sistema binário em vez de abrir uma terceira categoria de raio.

### Sombras — discretas, tiradas de arquitetura

```css
--shadow-sm: 0 1px 2px rgba(21,43,67,.08);
--shadow-md: 0 4px 16px rgba(21,43,67,.10);
--shadow-lg: 0 16px 48px rgba(21,43,67,.14);
```

Sem sombra colorida, sem glow, sem "neumorfismo".

### Fios e divisores
- **Fio dourado:** 2 px, `gold-500`, largura de 64 px, sob títulos de seção. Já existe no card do hero — sistematizado aqui.
- **Divisor neutro:** 1 px `gray-400`.

---

## 6. Componentes

### Botões

| Variante | Fundo | Texto | Borda | Uso |
|---|---|---|---|---|
| Primário | `navy-700` | branco | — | "Falar com consultor", "Enviar" |
| Secundário | transparente | `navy-700` | 1,5 px `navy-700` | "Ver imóveis" |
| Ouro | `gold-500` | `navy-900` | — | **Um por tela.** CTA principal do hero |
| WhatsApp | `#25D366` | branco | — | Contato direto |
| Instagram | gradiente `instagram-gradient` | branco | — | Botão flutuante, mesmo padrão do WhatsApp |

Altura 48 px · padding 16/32 px · raio 4 px · Archivo 600, 15 px, caixa alta, tracking +0,06em.
**Hover:** escurece 8 % + translada 1 px para cima, 160 ms.
**Foco:** contorno de 2 px `gold-500` com offset 2 px — visível e obrigatório.

### Card de imóvel
```
┌──────────────────────────────┐
│  [ foto 4:3, raio 0 ]        │
│  ┌──────────┐                │  ← chip de status, canto superior esquerdo da foto
│  │ À VENDA  │  navy-700      │     Archivo 600 · 12px · caixa alta
│  └──────────┘                │
├──────────────────────────────┤
│  JARDIM GUANABARA            │  ← eyebrow · gold-500
│  Casa 3 dormitórios          │  ← h4 Archivo 600 navy-700
│  ────                        │  ← fio dourado 2px · 40px
│  R$ 550.000                  │  ← data · IBM Plex Mono 500 · 25px · navy-700
│  180 m² · 3 quartos · 2 vagas│  ← small Hanken Grotesk gray-600
│                              │
│  [ Falar com consultor ]     │  ← botão secundário largura total
└──────────────────────────────┘
```
Borda 1 px `gray-400`, sombra `sm`; no hover, sombra `md` e borda `gold-500`.

### Selo de credencial
Círculo `navy-900`, anel de 1,5 px `gold-500`, texto branco em IBM Plex Mono caixa alta.
Usos: `CRECI 35889`, `LAUDO TÉCNICO`, `ASSESSORIA JURÍDICA`.
São as provas concretas da marca — merecem tratamento de selo, não de bullet point.

### Bloco de equipe (o ativo mais subaproveitado)
Foto circular, nome em Archivo 600 navy-700, função em `eyebrow` dourado, registro profissional em IBM Plex Mono:
`Deyse Fontes · ENGENHARIA CIVIL · CREA-BA` / `Dr. José Ângelo · JURÍDICO · OAB-BA`
Mostrar rosto e registro é o que diferencia a VDC de um perfil de anúncios.

### Formulário
Input: altura 48 px, borda 1 px `gray-400`, raio 4 px, fundo branco, texto `ink` 16 px (nunca menos que 16 px no mobile — abaixo disso o iOS dá zoom). Foco: borda `navy-500` + anel `gold-500` 2 px.

---

## 7. Fotografia e imagem

### Hierarquia do que fotografar
1. **Imóvel real, luz de fim de tarde** — fachada em ângulo de 3/4, nunca de frente chapado.
2. **Detalhe construtivo** — esquadria, acabamento, laje, planta impressa. É a prova visual da engenharia.
3. **Equipe em contexto** — no escritório, na obra, com o cliente. Rosto humano vende consultoria.
4. **Vitória da Conquista** — bairro, rua, referência local. Ancoragem territorial.

### Tratamento
- Temperatura levemente quente (+200 K), contraste médio, sombras abertas.
- **Nada de HDR estourado nem de céu roxo/laranja artificial.**
- Verticais rigorosamente corrigidas — linha torta destrói a promessa de precisão técnica.
- Máscaras permitidas: retângulo reto, círculo total, **arco de 90° do logo**.
- Véu para texto sobre foto: `navy-900` em 55 %, ou faixa navy sólida cobrindo no máximo 45 % da imagem.

### O que corrigir no material atual
> Os posts de Instagram usam adesivos vermelhos/laranja, setas grandes e caixas de texto empilhadas — a linguagem visual de corretor autônomo. Funciona no curto prazo e conflita frontalmente com o posicionamento técnico e com o logo navy/dourado. **Substituir a etiqueta vermelha de preço pela etiqueta navy com fio dourado** é a mudança de maior impacto e menor custo do sistema inteiro.

---

## 8. Redes sociais

### Formatos
| Peça | Dimensão |
|---|---|
| Feed quadrado | 1080 × 1080 |
| Feed retrato (padrão) | 1080 × 1350 |
| Story / Reels | 1080 × 1920 |
| Capa de Reels no grid | 1080 × 1350, **assunto centralizado nos 1080 × 1080 centrais** |
| Capa de destaque | 1080 × 1080, ícone de linha `sand-400` sobre `navy-700` |

### Grade do post (1080 × 1350)
- Margem de segurança: **80 px** em todos os lados.
- Faixa inferior navy de **160 px** com logo à esquerda (altura 56 px) e `@vdcimoveis` em IBM Plex Mono à direita.
- Título: máximo 5 palavras, Archivo 700, 72–96 px, caixa alta.
- Etiqueta de preço: retângulo navy, raio 4 px, texto IBM Plex Mono 48 px branco, fio dourado de 4 px na base.
- Arco do logo em marca d'água a 6 %, sangrando por um canto — **um por post**.

### Padrão de grid do perfil
Sequência de três em rotação, para o perfil ler como catálogo e não como mural:
**1. Imóvel** (foto grande, etiqueta de preço) → **2. Institucional/Técnico** (fundo navy, dado ou dica) → **3. Equipe/Bastidor** (rosto, entrega de chave, obra).

### Capas de destaque
Manter os oito atuais (Clube VDC, Condomínios, Construção, Contato, Jurídico, Localização, Entregas), mas padronizar: ícone de linha 2 px `sand-400`, centralizado, sobre círculo `navy-700` sólido. Hoje eles variam de estilo e peso.

---

## 9. Voz e escrita

**Tom:** especialista que explica, não vendedor que empurra.

| Faça | Não faça |
|---|---|
| "Casa de 180 m² no Jardim Guanabara. Laudo técnico incluso." | "🔥🔥 OPORTUNIDADE IMPERDÍVEL!!!" |
| "Financiamento Caixa aprovado para este imóvel." | "CORRE QUE É SÓ HOJE" |
| "Nossa engenheira avalia a estrutura antes de você assinar." | "O melhor negócio da cidade" |
| "Falar com um consultor" | "Clique aqui" |

- Números sempre concretos: metragem, dormitórios, vagas, bairro, valor.
- Um emoji por post, no máximo — e nunca no título.
- Preço por extenso em real: `R$ 550.000` (ponto de milhar, sem centavos).
- Sempre citar **bairro + cidade**: a busca local é o principal canal.
- Fechamento padrão dos posts: *Conectando você ao seu lugar ideal. · CRECI 35889*

---

## 10. Movimento (site)

Discreto e curto. A marca é sóbria; animação demais denuncia template.

| Gesto | Especificação |
|---|---|
| Entrada de seção | fade + 16 px de subida, 400 ms, `cubic-bezier(.2,.8,.2,1)`, uma vez |
| Hover de card | elevação de sombra + 2 px de subida, 160 ms |
| Hover de botão | escurece 8 %, 160 ms |
| Arco do logo no carregamento | desenho do traço em 900 ms — **uma vez, só na home** |
| Carrossel de imóveis | 500 ms, easing de saída |

`prefers-reduced-motion: reduce` → tudo vira corte seco. Obrigatório.

---

## 11. Auditoria do material atual

Nota por dimensão, baseada nas telas enviadas.

| # | Dimensão | Nota | Observação |
|---|---|---|---|
| 1 | Consistência de cor | **7/10** | Navy `#283B62` bem aplicado no site. Quebra grave nos posts (vermelho/laranja fora da paleta). |
| 2 | Hierarquia tipográfica | **5/10** | "Equipe de especialistas" em corpo enorme e leve compete com o parágrafo ao lado; falta escala definida. |
| 3 | Ritmo de espaçamento | **4/10** | Bloco de contato com espaços vazios grandes e desiguais; o mapa e o formulário não se alinham a um grid. |
| 4 | Consistência de componente | **6/10** | Os três cards "Consultores especializados" estão bons. Os oito destaques do Instagram variam de estilo. |
| 5 | Responsividade | **?** | Não avaliável pelas capturas — testar em 375 px de largura. |
| 6 | Modo escuro | **N/A** | Não necessário. O navy sólido já cumpre o papel de contraste. |
| 7 | Animação | **N/A** | Sem evidência nas capturas. |
| 8 | Acessibilidade | **5/10** | Bege `#CBB492` em ícone é decorativo e passa; texto de corpo em `#616E89` passa em AA. Verificar estados de foco no formulário. |
| 9 | Densidade | **6/10** | Site respira bem. Posts do Instagram estão saturados de adesivos. |
| 10 | Acabamento | **4/10** | Foto do escritório no hero (mesa, extintor, porta) está abaixo do padrão da foto de fundo. É o ponto mais visível a corrigir. |

**Média: 5,3 / 10** — base sólida de cor e logo, execução inconsistente entre canais.

### As cinco correções de maior retorno
1. Trocar a foto circular do hero por uma foto profissional da equipe ou de um imóvel entregue.
2. Aposentar as etiquetas vermelhas/laranja dos posts; adotar a etiqueta navy + fio dourado.
3. Fixar a escala tipográfica da seção 4 em todo o site.
4. Alinhar o bloco de contato ao grid de 12 colunas.
5. Padronizar as oito capas de destaque do Instagram.

---

## 12. Erros comuns a evitar

- Dourado ocupando mais de 10 % da peça.
- Dourado em texto pequeno ou sobre branco (contraste 2,4:1 — ilegível).
- Gradiente navy→dourado em fundo ou botão. O gradiente metálico é **só do arco e dos selos**.
- Efeito "vidro fosco" sobre foto de imóvel.
- Cantos de 16 px ou mais.
- Mais de um arco por peça.
- Logo direto sobre foto sem véu.
- Ícones de estilos diferentes na mesma peça (linha e sólido misturados).
- Texto centralizado em parágrafos longos.

---

## Arquivos que acompanham este documento

| Arquivo | Conteúdo |
|---|---|
| `design-tokens.json` | Todos os tokens em JSON, prontos para Figma, Tailwind ou Style Dictionary |
| `vdc-tokens.css` | Variáveis CSS + classes utilitárias, para colar em qualquer projeto |
| `design-preview.html` | Página interativa com paleta, tipografia e componentes renderizados |
| `PROMPTS-IA.md` | Kit de prompts para gerar posts, imagens e sites com IA mantendo a identidade |
