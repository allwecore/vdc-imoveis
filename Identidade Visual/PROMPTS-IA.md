# VDC IMÓVEIS — Kit de Prompts para IA

Como usar a identidade visual em ChatGPT, Claude, Midjourney, Flux, Gemini, Canva IA, Lovable/v0 e afins.
Companheiro do `DESIGN.md`.

---

## 1. Bloco-base — cole no início de QUALQUER conversa

Este é o bloco mais importante do kit. Ele carrega a identidade inteira em um texto curto.

```
Você é o diretor de arte da VDC IMÓVEIS, consultoria imobiliária de Vitória da
Conquista (BA) formada por consultor de imóveis, engenheira civil, arquiteto e
advogado. CRECI 35889. Tagline: "Conectando você ao seu lugar ideal."

Posicionamento: segurança técnica na maior compra da vida do cliente.
Personalidade: técnica, institucional, confiável, acolhedora, aspiracional.
NUNCA: gritada, promocional, "oferta imperdível", emoji em excesso.

PALETA (não use nenhuma cor fora desta lista):
- Navy 700 #283B62 — cor principal (títulos, faixas, botões)
- Navy 900 #152B43 — fundos escuros, o logo
- Navy 500 #5272B2 — links e estados ativos
- Navy 100 #E7ECF5 — fundos de bloco claros
- Dourado 500 #C9A44E — destaque, fios, selos, preço (MÁXIMO 10% da peça)
- Areia 400 #CBB492 — ícones de linha, decorativo
- Branco #FFFFFF / Off-white #F7F8FA — fundo padrão
- Cinza 600 #616E89 — texto secundário
- Ink #1A1F2B — texto principal
Proporção obrigatória: 60% neutro / 30% navy / 10% dourado.
Dourado NUNCA em texto pequeno nem sobre branco (contraste 2,4:1).

TIPOGRAFIA:
- Títulos: Archivo 600/700, caixa alta com tracking -0.02em (máx. 5 palavras)
- Texto: Hanken Grotesk 400/600, entrelinha 1.65, largura 60-75 caracteres
- Preço, m², CRECI, códigos: IBM Plex Mono 500 (assinatura da marca)

FORMA:
- Cantos: 0 em faixas e imagens; 4px em botões, inputs e cards; círculo total
  em fotos-retrato e selos. NUNCA 8px, 12px, 16px ou mais.
- Espaçamento só na escala: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px
- Sombras discretas e frias: 0 4px 16px rgba(21,43,67,.10). Sem glow.

ELEMENTO-ASSINATURA: o arco do logo (círculo de duas setas, uma dourada e uma
navy). Aparece UMA vez por peça, em escala grande: recorte circular de foto,
fio dourado curvo, ou marca d'água a 6% de opacidade.

PROIBIDO: gradiente navy-dourado em fundo ou botão, glassmorphism, vermelho ou
laranja, cantos muito arredondados, mais de um arco por peça, logo sobre foto
sem véu navy, ícones de estilos misturados.
```

---

## 2. Posts de Instagram — texto + arte

### 2.1 Post de imóvel

```
[BLOCO-BASE]

Crie um post 1080x1350 para o Instagram da VDC.
Imóvel: {tipo} no bairro {bairro}, Vitória da Conquista. {m²} m²,
{quartos} quartos, {vagas} vagas. Valor R$ {valor}. Diferenciais: {lista}.

Estrutura obrigatória:
- Margem de segurança de 80px em todos os lados
- Foto do imóvel ocupando o topo, sangrando nas laterais
- Etiqueta de preço: retângulo navy #283B62, canto 4px, valor em IBM Plex Mono
  branco 48px, fio dourado #C9A44E de 4px na base. NADA de adesivo vermelho.
- Título em Archivo 700 caixa alta, no máximo 5 palavras
- Ficha técnica em IBM Plex Mono: m², quartos, vagas — separados por " · "
- Faixa inferior navy de 160px com o logo à esquerda e @vdcimoveis à direita
- Arco do logo em marca d'água 6%, sangrando por um canto

Escreva também a legenda: 3 a 5 linhas, tom de especialista, números concretos,
bairro + cidade citados, no máximo 1 emoji, terminando com
"Conectando você ao seu lugar ideal. · CRECI 35889" e 8 hashtags locais.
```

### 2.2 Post institucional / educativo (fundo navy)

```
[BLOCO-BASE]

Post 1080x1350, fundo navy #283B62 sólido, sobre o tema: {tema}.
Ex.: "O que a vistoria com laudo técnico verifica antes de você assinar."
- Rótulo dourado em caixa alta no topo (13px, tracking 0.14em)
- Título branco em Archivo 700, máximo 5 palavras
- 3 itens numerados em IBM Plex Mono (01 / 02 / 03) com explicação em Hanken Grotesk
- Assinatura da engenheira ou do advogado, com o registro profissional
- Arco em marca d'água 6% no canto inferior direito
```

### 2.3 Carrossel (5 cards)

```
[BLOCO-BASE]

Carrossel de 5 cards 1080x1350 sobre {tema}.
Card 1 — capa: fundo navy, título grande, rótulo dourado, sem foto
Cards 2-4 — conteúdo: fundo branco, um argumento por card, número em Plex Mono
Card 5 — CTA: fundo navy, logo centralizado, "Falar com um consultor",
         telefones e CRECI 35889
Elemento de continuidade entre os cards: um fio dourado de 2px que atravessa
todos na mesma altura vertical.
```

### 2.4 Rotação do grid do perfil

Publique nesta ordem para o perfil ler como catálogo, não como mural:
**1. Imóvel** → **2. Institucional/técnico** → **3. Equipe/bastidor** → repete.

---

## 3. Geração de imagem (Midjourney / Flux / GPT Image / Nano Banana)

> Regra: **a IA gera o cenário, não o logo.** Logo e texto entram depois, no editor. Modelos de imagem deformam logotipo e erram acento em português.

### 3.1 Fachada de imóvel — foto principal

```
Professional real estate photography, contemporary Brazilian house facade,
three-quarter angle, golden hour warm light spilling from interior windows,
clean rendered walls and dark aluminum frames, tropical landscaping, wet
driveway reflections, deep blue dusk sky, architectural photography, shot on
35mm tilt-shift lens, perfectly corrected verticals, natural color grading,
subtle warmth, high detail, no people
--ar 4:5 --style raw
```

### 3.2 Interior

```
Interior architectural photography, Brazilian upper-middle-class living room,
neutral sand and warm white palette, dark navy accents, large windows with soft
daylight, wood floor, minimal styling, no clutter, wide angle 24mm, corrected
verticals, editorial real estate magazine quality, no people, no text
--ar 4:5 --style raw
```

### 3.3 Equipe / escritório (para substituir a foto atual do hero)

```
Corporate lifestyle photography, small Brazilian real estate consultancy team of
four professionals reviewing architectural blueprints on a light wood table,
modern office with navy blue accent wall, warm natural window light, business
casual attire, candid collaborative moment, shallow depth of field 50mm f/2,
authentic and warm, documentary style, no text
--ar 3:2 --style raw
```

### 3.4 Textura de fundo para post navy

```
Abstract architectural background, deep navy blue #283B62, subtle concrete and
brushed metal texture, soft raking light from top left, thin gold light streak,
minimal, elegant, no objects, no text, negative space in the center
--ar 4:5
```

### Negative prompt padrão (cole em todos)

```
--no text, watermark, logo, letters, signage, distorted architecture, tilted
verticals, HDR halos, oversaturated purple orange sky, fisheye, cluttered
props, stock-photo smiles, plastic skin, extra fingers
```

### Ajuste de estilo por plataforma
- **Midjourney:** `--style raw --ar 4:5 --v 7`
- **Flux:** troque `--ar 4:5` por "aspect ratio 4:5" e descreva a luz com mais detalhe.
- **GPT Image / Nano Banana:** pode citar as cores em hex diretamente; costuma acertar mais fiel.

---

## 4. Sites e landing pages (Lovable, v0, Bolt, Claude, Cursor)

```
[BLOCO-BASE]

Construa uma landing page para a VDC IMÓVEIS em {React + Tailwind / HTML+CSS}.
Use exatamente as variáveis CSS do arquivo vdc-tokens.css.

Seções, nesta ordem:
1. HERO — foto de imóvel ao entardecer com véu navy 55%; título em Archivo 700
   caixa alta; subtítulo "Consultoria, engenharia e jurídico na mesma mesa";
   um único botão dourado "Falar com um consultor"; à direita, recorte circular
   com foto da equipe (assinatura do arco)
2. QUATRO ESPECIALIDADES — Consultoria, Engenharia Civil, Arquitetura, Jurídico.
   Ícones de linha 2px em areia #CBB492, título navy, texto cinza. Grid 4 colunas
3. IMÓVEIS EM DESTAQUE — grid de cards conforme o componente card de imóvel:
   chip de status, bairro em rótulo dourado, preço em IBM Plex Mono
4. EQUIPE — fotos circulares, nome em Archivo, função em rótulo dourado,
   registro profissional (CRECI / CREA / OAB) em IBM Plex Mono
5. PROVA — selos circulares navy com anel dourado: CRECI 35889, LAUDO TÉCNICO,
   ASSESSORIA JURÍDICA, SEGURO LOCATÍCIO
6. DEPOIMENTOS — fundo navy, aspas douradas, texto branco
7. CONTATO — formulário alinhado ao grid de 12 colunas, telefones dos três
   especialistas com botão WhatsApp, endereço e mapa
8. RODAPÉ — navy 900, logo, links, CRECI

Requisitos técnicos: responsivo a partir de 375px; foco de teclado visível com
anel dourado de 2px; prefers-reduced-motion respeitado; imagens com alt em
português; largura máxima de conteúdo 1200px; padding de seção 96/64/48px.
```

### Prompt de revisão (rode depois de gerar)

```
Revise a página contra o design system da VDC e liste toda violação:
1. Alguma cor fora da paleta?
2. O dourado passa de 10% da área?
3. Algum canto arredondado além de 4px ou círculo total?
4. Algum espaçamento fora da escala 4/8/12/16/24/32/48/64/96/128?
5. Mais de um arco por seção?
6. Texto dourado sobre branco (proibido)?
7. Título em caixa alta com mais de 5 palavras?
8. Parágrafo com mais de 75 caracteres por linha?
9. Estado de foco visível em todo elemento interativo?
10. Preço e metragem estão em IBM Plex Mono?
Devolva a lista de problemas com a correção de cada um.
```

---

## 5. Textos e legendas

```
[BLOCO-BASE]

Escreva {quantidade} legendas para o Instagram da VDC sobre {tema}.
Tom: especialista que explica, não vendedor que empurra.
Regras: números concretos (m², quartos, valor, bairro); bairro + "Vitória da
Conquista" sempre citados; no máximo 1 emoji e nunca no início; sem "imperdível",
"corre", "última chance", "sonho realizado"; CTA sempre "Fale com um consultor"
ou "Chame no WhatsApp"; fechar com
"Conectando você ao seu lugar ideal. · CRECI 35889".
Entregue também 8 hashtags, misturando locais e de categoria.
```

---

## 6. Checklist antes de publicar

- [ ] Toda cor está na paleta?
- [ ] Dourado ocupa no máximo 10 %?
- [ ] Um único arco na peça?
- [ ] Título com no máximo 5 palavras em caixa alta?
- [ ] Preço e metragem em IBM Plex Mono?
- [ ] Logo com respiro e sobre fundo adequado (véu se for foto)?
- [ ] Nenhum vermelho, laranja ou adesivo promocional?
- [ ] Bairro + cidade citados?
- [ ] CRECI 35889 presente?
- [ ] Verticais da foto corrigidas?
- [ ] Legível em miniatura de 150 px?
