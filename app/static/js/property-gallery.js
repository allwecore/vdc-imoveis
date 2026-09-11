// Galeria da página do imóvel: foto principal + tira de miniaturas
// (troca de foto sem recarregar a página) e o lightbox em tela cheia.
// A lista completa de fotos vem de data-photos no elemento raiz — a
// tira de miniaturas só renderiza as 4 primeiras + "ver todas" (ver
// imovel.html), mas as setas e o lightbox navegam pela galeria
// inteira, sem limite de quantidade.
document.addEventListener("DOMContentLoaded", () => {
  const gallery = document.querySelector("[data-gallery]");
  if (!gallery) return;

  let photos = [];
  try {
    photos = JSON.parse(gallery.dataset.photos || "[]");
  } catch (err) {
    photos = [];
  }
  if (!photos.length) return;

  const title = gallery.dataset.galleryTitle || "";
  const mainImg = gallery.querySelector("[data-gallery-main-img]");
  const counterEl = gallery.querySelector("[data-gallery-counter]");
  const prevBtn = gallery.querySelector("[data-gallery-prev]");
  const nextBtn = gallery.querySelector("[data-gallery-next]");
  const thumbs = Array.from(gallery.querySelectorAll("[data-gallery-thumb]"));

  let current = 0;

  function showMain(index) {
    current = (index + photos.length) % photos.length;
    if (mainImg) {
      mainImg.src = photos[current];
      mainImg.alt = `${title} — foto ${current + 1} de ${photos.length}`;
    }
    if (counterEl) counterEl.textContent = `${current + 1} / ${photos.length}`;
    thumbs.forEach((thumb) => {
      thumb.classList.toggle("is-active", Number(thumb.dataset.index) === current);
    });
  }

  prevBtn?.addEventListener("click", () => showMain(current - 1));
  nextBtn?.addEventListener("click", () => showMain(current + 1));
  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => showMain(Number(thumb.dataset.index)));
  });

  // --- Lightbox (tela cheia) ---
  const lightbox = document.querySelector("[data-lightbox]");
  const lightboxImg = lightbox?.querySelector("[data-lightbox-img]");
  const lightboxCounter = lightbox?.querySelector("[data-lightbox-counter]");
  let triggerEl = null; // elemento que abriu o lightbox — recebe o foco de volta ao fechar

  function updateLightbox() {
    if (!lightboxImg) return;
    lightboxImg.src = photos[current];
    lightboxImg.alt = `${title} — foto ${current + 1} de ${photos.length}`;
    if (lightboxCounter) lightboxCounter.textContent = `${current + 1} / ${photos.length} fotos`;
  }

  function openLightbox(index, fromEl) {
    if (!lightbox) return;
    triggerEl = fromEl || document.activeElement;
    showMain(index);
    updateLightbox();
    lightbox.hidden = false;
    document.body.classList.add("vdc-no-scroll");
    lightbox.querySelector("[data-lightbox-close]")?.focus();
  }

  function closeLightbox() {
    if (!lightbox || lightbox.hidden) return;
    lightbox.hidden = true;
    document.body.classList.remove("vdc-no-scroll");
    triggerEl?.focus?.();
  }

  function lightboxStep(delta) {
    showMain(current + delta);
    updateLightbox();
  }

  gallery.querySelectorAll("[data-gallery-open]").forEach((btn) => {
    btn.addEventListener("click", () => openLightbox(Number(btn.dataset.index ?? current), btn));
  });
  if (mainImg) {
    mainImg.style.cursor = "zoom-in";
    mainImg.addEventListener("click", () => openLightbox(current, mainImg));
    // A foto tem tabindex/role=button (ver imovel.html) porque é um
    // gatilho de verdade, não só uma imagem — Enter/Espaço precisam
    // funcionar como um clique pra quem navega só com teclado.
    mainImg.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openLightbox(current, mainImg);
      }
    });
  }

  lightbox?.querySelectorAll("[data-lightbox-close]").forEach((el) => {
    el.addEventListener("click", closeLightbox);
  });
  lightbox?.querySelector("[data-lightbox-prev]")?.addEventListener("click", () => lightboxStep(-1));
  lightbox?.querySelector("[data-lightbox-next]")?.addEventListener("click", () => lightboxStep(1));

  document.addEventListener("keydown", (event) => {
    if (!lightbox || lightbox.hidden) return;
    if (event.key === "Escape") closeLightbox();
    else if (event.key === "ArrowLeft") lightboxStep(-1);
    else if (event.key === "ArrowRight") lightboxStep(1);
  });

  // Swipe (celular) — vale tanto pra foto grande quanto pro lightbox,
  // já que os dois têm a mesma necessidade de "passar a próxima foto"
  // sem exigir mirar num botão pequeno na tela.
  function enableSwipe(el, onSwipeLeft, onSwipeRight) {
    let startX = null;
    el.addEventListener(
      "touchstart",
      (event) => {
        startX = event.touches[0].clientX;
      },
      { passive: true }
    );
    el.addEventListener(
      "touchend",
      (event) => {
        if (startX === null) return;
        const deltaX = event.changedTouches[0].clientX - startX;
        startX = null;
        const LIMIAR = 40; // px — abaixo disso é só um toque, não um swipe
        if (deltaX <= -LIMIAR) onSwipeLeft();
        else if (deltaX >= LIMIAR) onSwipeRight();
      },
      { passive: true }
    );
  }

  const mainEl = gallery.querySelector(".vdc-gallery__main");
  if (mainEl) enableSwipe(mainEl, () => showMain(current + 1), () => showMain(current - 1));
  if (lightbox) enableSwipe(lightbox, () => lightboxStep(1), () => lightboxStep(-1));

  showMain(0);
});
