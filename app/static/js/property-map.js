// Mapa da página de um imóvel (/imovel/<id>) — Leaflet + tiles do
// OpenStreetMap, ambos gratuitos e sem chave de API.
//
// Regra que vale a pena não esquecer: aqui NÃO existe geocodificação.
// As coordenadas já vêm prontas do banco, nos data-attributes do
// elemento. Uma página de imóvel com muita visita não gera nenhuma
// requisição ao serviço de geocodificação — só os tiles do mapa, que
// o navegador ainda cacheia.
document.addEventListener("DOMContentLoaded", () => {
  const el = document.querySelector("[data-property-map]");
  if (!el || typeof L === "undefined") return;

  const lat = parseFloat(el.dataset.lat);
  const lng = parseFloat(el.dataset.lng);
  // Coordenada inválida (banco sujo, atributo faltando): esconde o
  // bloco em vez de renderizar um mapa no meio do oceano.
  if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
    el.hidden = true;
    return;
  }

  const raio = parseFloat(el.dataset.radius) || 0;
  const precisao = el.dataset.precision || "aproximado";
  const titulo = el.dataset.title || "Imóvel";

  // Quanto mais grosseira a precisão, mais longe o mapa começa — abrir
  // no zoom máximo em cima de um ponto que só representa o bairro
  // passaria uma exatidão que o dado não tem.
  const zoomPorPrecisao = { exato: 17, rua: 16, bairro: 15, cidade: 13, aproximado: 15 };
  const zoom = zoomPorPrecisao[precisao] || 15;

  const map = L.map(el, {
    scrollWheelZoom: false, // não sequestra o scroll de quem está só passando
    zoomControl: true,
  }).setView([lat, lng], zoom);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  // Círculo de imprecisão: quando o serviço gratuito só achou a rua ou
  // o bairro, a área desenhada diz isso visualmente, em vez de um pin
  // seco fingindo ser a porta da casa.
  if (raio > 0) {
    L.circle([lat, lng], {
      radius: raio,
      color: "#283B62",
      weight: 1.5,
      opacity: 0.55,
      fillColor: "#5272B2",
      fillOpacity: 0.15,
    }).addTo(map);
  }

  const marker = L.marker([lat, lng], {
    icon: L.divIcon({
      html: '<span class="vdc-propmap__pin" aria-hidden="true"></span>',
      className: "",
      iconSize: [26, 26],
      iconAnchor: [13, 26],
      popupAnchor: [0, -24],
    }),
    keyboard: false,
    title: titulo,
  }).addTo(map);

  if (raio > 0) {
    marker.bindPopup(
      '<div class="vdc-map-popup"><strong>Localização aproximada</strong>' +
        "<span>O serviço gratuito de mapas não localizou o número exato.</span></div>"
    );
  }

  // Mesmo comportamento do mapa da busca: roda do mouse só dá zoom
  // depois de um clique dentro do mapa.
  map.on("click", () => map.scrollWheelZoom.enable());
  el.addEventListener("mouseleave", () => map.scrollWheelZoom.disable());

  // Leaflet mede o container só na criação; sem isso, girar o celular
  // ou redimensionar deixa os tiles desalinhados.
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => map.invalidateSize(), 150);
  });
});
