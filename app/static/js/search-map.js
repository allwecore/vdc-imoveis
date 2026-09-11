// Página /imoveis — mapa interativo (Leaflet + OpenStreetMap, API
// pública, sem chave) ao lado da lista de cards. Carregado só nesta
// página (ver {% block extra_scripts %} em search.html), não em main.js.
document.addEventListener("DOMContentLoaded", () => {
  // A altura de .vdc-search__split (100vh - offset) precisa do offset
  // real de cabeçalho + barra de filtros, não de um "154px" chutado —
  // a barra quebra pra 2 linhas em algumas larguras (ex.: 1024px) e o
  // chute fixo deixava a seção mais alta que a tela, cortando o mapa.
  // Medido de novo no resize porque a quebra de linha da barra muda
  // com a largura; um segundo cálculo 300ms depois do load cobre troca
  // tardia de fonte web que também pode mudar essa altura.
  function setSearchOffset() {
    const header = document.querySelector(".vdc-header");
    const bar = document.querySelector(".vdc-search__bar");
    if (!header || !bar) return;
    const offset = header.offsetHeight + bar.offsetHeight;
    document.documentElement.style.setProperty("--vdc-search-offset", `${offset}px`);
  }
  setSearchOffset();
  setTimeout(setSearchOffset, 300);
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(setSearchOffset, 150);
  });

  // Cada select da barra de filtros já busca sozinho ao trocar de
  // valor — só o campo de texto livre exige Enter ou clique no botão,
  // pra não disparar uma busca a cada tecla digitada.
  const filterForm = document.querySelector("[data-search-filters]");
  if (filterForm) {
    filterForm.querySelectorAll("select").forEach((select) => {
      select.addEventListener("change", () => filterForm.submit());
    });
  }

  // "Mapa fixo, só a lista rola": .vdc-search__list já tem overflow-y
  // próprio, mas isso só captura o scroll quando o mouse está EM CIMA
  // da lista. Rolar com o mouse sobre o mapa (ou o espaço vazio ao
  // redor) ainda rolaria a página inteira, arrastando o mapa junto —
  // esse listener redireciona qualquer scroll dentro da seção pra
  // lista, e só deixa a página rolar de verdade (revelando o rodapé)
  // quando a lista já chegou no topo ou no fim dela mesma.
  const splitEl = document.querySelector(".vdc-search__split");
  const listEl = document.querySelector(".vdc-search__list");
  if (splitEl && listEl) {
    splitEl.addEventListener(
      "wheel",
      (event) => {
        if (listEl.scrollHeight <= listEl.clientHeight) return; // lista curta, nada pra rolar dentro dela
        const atTop = listEl.scrollTop <= 0;
        const atBottom = listEl.scrollTop + listEl.clientHeight >= listEl.scrollHeight - 1;
        if ((event.deltaY < 0 && atTop) || (event.deltaY > 0 && atBottom)) return;
        event.preventDefault();
        listEl.scrollTop += event.deltaY;
      },
      { passive: false }
    );
  }

  const mapEl = document.getElementById("properties-map");
  if (!mapEl || typeof L === "undefined") return;

  let points = [];
  try {
    points = JSON.parse(mapEl.dataset.mapPoints || "[]");
  } catch (err) {
    points = [];
  }

  const VITORIA_DA_CONQUISTA = [-14.8619, -40.8444];
  const center = points.length
    ? [
        points.reduce((sum, p) => sum + p.lat, 0) / points.length,
        points.reduce((sum, p) => sum + p.lng, 0) / points.length,
      ]
    : VITORIA_DA_CONQUISTA;

  const map = L.map(mapEl, { scrollWheelZoom: false }).setView(center, 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  // Zoom com a roda do mouse só depois de um clique — evita "prender"
  // o scroll da página quando o visitante só está passando o mouse
  // por cima do mapa pra continuar rolando a lista.
  map.on("click", () => map.scrollWheelZoom.enable());
  mapEl.addEventListener("mouseleave", () => map.scrollWheelZoom.disable());

  // Leaflet mede o container só na criação; sem isso, redimensionar a
  // janela (ou girar o celular) deixa os tiles desalinhados com o
  // tamanho novo de .vdc-search__map.
  let mapResizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(mapResizeTimer);
    mapResizeTimer = setTimeout(() => map.invalidateSize(), 150);
  });

  const clusterGroup = L.markerClusterGroup({
    maxClusterRadius: 50,
    iconCreateFunction(cluster) {
      const count = cluster.getChildCount();
      const sizeClass =
        count < 5 ? "vdc-map-cluster--small" : count < 15 ? "vdc-map-cluster--medium" : "vdc-map-cluster--large";
      return L.divIcon({
        html: `<div>${count}</div>`,
        className: `vdc-map-cluster ${sizeClass}`,
        iconSize: [40, 40],
      });
    },
  });

  // Sincronização lista ↔ mapa: um único ponto de verdade sobre "qual
  // imóvel está selecionado agora", usado tanto por quem clica num
  // card quanto por quem clica num pin.
  const markersById = new Map();
  let selectedMarker = null;

  function markSelectedCard(id) {
    document.querySelectorAll(".vdc-search__cards .vdc-card.is-selected").forEach((el) => {
      el.classList.remove("is-selected");
    });
    const card = document.getElementById(`imovel-${id}`);
    if (card) card.classList.add("is-selected");
  }

  function markSelectedMarker(marker) {
    if (selectedMarker && selectedMarker !== marker) {
      const prevPin = selectedMarker.getElement()?.querySelector(".vdc-map-pin");
      if (prevPin) prevPin.classList.remove("is-selected");
    }
    selectedMarker = marker;
    const pin = marker.getElement()?.querySelector(".vdc-map-pin");
    if (pin) pin.classList.add("is-selected");
  }

  // Clique num card da lista → mapa localiza, "des-clusteriza" se
  // precisar (zoomToShowLayer), centraliza e abre o popup do imóvel.
  function selectFromList(id) {
    const marker = markersById.get(id);
    markSelectedCard(id);
    if (!marker) return; // imóvel sem coordenada — nada pra fazer no mapa
    const focus = () => {
      map.panTo(marker.getLatLng());
      markSelectedMarker(marker);
      marker.openPopup();
    };
    if (typeof clusterGroup.zoomToShowLayer === "function") {
      clusterGroup.zoomToShowLayer(marker, focus);
    } else {
      focus();
    }
  }

  points.forEach((point) => {
    const isRent = point.status === "aluguel";
    const icon = L.divIcon({
      html: `<span class="vdc-map-pin ${isRent ? "vdc-map-pin--aluguel" : ""}">${point.price}</span>`,
      className: "",
      iconSize: null,
      iconAnchor: [24, 36],
      popupAnchor: [0, -34],
    });
    const marker = L.marker([point.lat, point.lng], { icon });
    const specs = [point.bedrooms ? `${point.bedrooms} qts` : null, `${point.area_m2} m²`]
      .filter(Boolean)
      .join(" · ");
    marker.bindPopup(
      `<div class="vdc-map-popup">
        <strong>${point.title}</strong>
        <span>${point.neighborhood} · ${point.type_label}</span>
        <span>${specs}</span>
        <span class="vdc-map-popup__price">${point.price}</span>
        <a href="${point.url}">Ver imóvel →</a>
        <a href="#imovel-${point.id}" data-map-goto="${point.id}">Ver na lista</a>
      </div>`
    );
    // Clicar no pin também seleciona o card correspondente na lista —
    // mesmo destaque dourado, sem forçar rolagem (isso fica só pro
    // link "Ver na lista", que é um pedido explícito de ir até lá).
    marker.on("click", () => {
      markSelectedCard(point.id);
      markSelectedMarker(marker);
    });
    marker.on("popupopen", () => {
      const link = document.querySelector(`[data-map-goto="${point.id}"]`);
      if (!link) return;
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const card = document.getElementById(`imovel-${point.id}`);
        if (!card) return;
        card.scrollIntoView({ behavior: "smooth", block: "center" });
        card.classList.add("is-map-highlight");
        setTimeout(() => card.classList.remove("is-map-highlight"), 1600);
      });
    });
    markersById.set(point.id, marker);
    clusterGroup.addLayer(marker);
  });

  map.addLayer(clusterGroup);
  if (points.length > 1) {
    map.fitBounds(clusterGroup.getBounds().pad(0.2));
  }

  // Clique em qualquer lugar do card (exceto os próprios links/botões
  // — foto, título e "Ver imóvel" continuam navegando normalmente)
  // seleciona o imóvel no mapa. Delegado no container da lista pra
  // funcionar com os cards que já existem no carregamento da página.
  const cardsEl = document.querySelector(".vdc-search__cards");
  if (cardsEl) {
    cardsEl.addEventListener("click", (event) => {
      if (event.target.closest("a, button")) return;
      const card = event.target.closest('.vdc-card[id^="imovel-"]');
      if (!card) return;
      const id = Number(card.id.replace("imovel-", ""));
      selectFromList(id);
      if (markersById.has(id)) switchToMapTab();
    });

    // Navegação por teclado (Tab entre os links do card) também guia o
    // mapa, sem abrir popup — só acompanha, pra não interromper quem
    // está navegando com leitor de tela ou teclado.
    cardsEl.addEventListener("focusin", (event) => {
      const card = event.target.closest('.vdc-card[id^="imovel-"]');
      if (!card) return;
      const id = Number(card.id.replace("imovel-", ""));
      const marker = markersById.get(id);
      if (!marker) return;
      markSelectedCard(id);
      map.panTo(marker.getLatLng());
      markSelectedMarker(marker);
    });
  }

  // Alternador "Lista / Mapa", visível só no celular (ver media query
  // em style.css). No desktop os botões existem no DOM mas ficam
  // escondidos — os cliques abaixo não têm efeito visual nenhum lá,
  // porque splitEl nunca aparece sem as duas colunas visíveis.
  const tabButtons = document.querySelectorAll("[data-search-tab]");
  function switchToMapTab() {
    const mapTab = document.querySelector('[data-search-tab="map"]');
    if (mapTab) mapTab.click();
  }
  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const showMap = button.dataset.searchTab === "map";
      if (splitEl) splitEl.classList.toggle("is-mobile-tab-map", showMap);
      tabButtons.forEach((b) => {
        b.classList.toggle("is-active", b === button);
        b.setAttribute("aria-selected", b === button ? "true" : "false");
      });
      if (showMap) {
        // O mapa estava com display:none — Leaflet mediu o container
        // errado nesse momento; sem isso os tiles ficam cortados ou
        // desalinhados na primeira vez que a aba do mapa abre.
        requestAnimationFrame(() => map.invalidateSize());
      }
    });
  });
});
