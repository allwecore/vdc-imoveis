const FAVORITES_KEY = "vdc_favorites";

function getFavorites() {
  try {
    return JSON.parse(localStorage.getItem(FAVORITES_KEY) || "[]");
  } catch (err) {
    return [];
  }
}

function setFavorites(list) {
  localStorage.setItem(FAVORITES_KEY, JSON.stringify(list));
  syncFavoritesUI();
}

function isFavorited(id) {
  return getFavorites().some((item) => item.id === id);
}

function toggleFavorite(item) {
  const list = getFavorites();
  const index = list.findIndex((f) => f.id === item.id);
  if (index >= 0) {
    list.splice(index, 1);
  } else {
    list.push(item);
  }
  setFavorites(list);
}

function removeFavorite(id) {
  setFavorites(getFavorites().filter((item) => item.id !== id));
}

function syncFavoritesUI() {
  const favorites = getFavorites();
  const count = favorites.length;

  document.querySelectorAll("[data-favorites-count]").forEach((el) => {
    el.textContent = String(count);
    el.hidden = count === 0;
  });
  document.querySelectorAll("[data-favorites-toggle]").forEach((btn) => {
    if (btn.classList.contains("vdc-header__icon-btn")) {
      btn.classList.toggle("has-items", count > 0);
    }
  });

  document.querySelectorAll("[data-fav-toggle]").forEach((btn) => {
    const pressed = isFavorited(btn.dataset.favId);
    btn.setAttribute("aria-pressed", String(pressed));
  });

  const list = document.querySelector("[data-favorites-list]");
  if (!list) return;
  const empty = list.querySelector("[data-favorites-empty]");
  list.querySelectorAll(".vdc-favorites__item").forEach((el) => el.remove());

  if (count === 0) {
    if (empty) empty.hidden = false;
    return;
  }
  if (empty) empty.hidden = true;

  favorites.forEach((item) => {
    const row = document.createElement("div");
    row.className = "vdc-favorites__item";
    row.innerHTML = `
      <div class="vdc-favorites__item-body">
        <a href="${item.url}">${item.title}</a>
        <span class="vdc-caption vdc-favorites__item-meta">${item.meta}</span>
      </div>
      <button type="button" class="vdc-favorites__item-remove" aria-label="Remover dos favoritos">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    `;
    row.querySelector(".vdc-favorites__item-remove").addEventListener("click", () => removeFavorite(item.id));
    list.appendChild(row);
  });
}

function closeAllOverlays(except) {
  document.querySelectorAll("[data-nav-panel]").forEach((panel) => {
    if (panel === except) return;
    panel.closest("[data-nav-dropdown]")?.classList.remove("is-open");
    panel.closest("[data-nav-dropdown]")?.querySelector("[data-nav-trigger]")?.setAttribute("aria-expanded", "false");
  });
  if (except !== "menu") {
    const menuPanel = document.querySelector("[data-menu-panel]");
    const menuBtn = document.querySelector("[data-menu-toggle]");
    const backdrop = document.querySelector("[data-menu-backdrop]");
    menuPanel?.classList.remove("is-open");
    menuBtn?.classList.remove("is-open");
    menuBtn?.setAttribute("aria-expanded", "false");
    backdrop?.classList.remove("is-open");
  }
  if (except !== "favorites") {
    const favPanel = document.querySelector("[data-favorites-panel]");
    favPanel?.classList.remove("is-open");
    document.querySelectorAll("[data-favorites-toggle]").forEach((btn) => btn.setAttribute("aria-expanded", "false"));
  }
}

function dismissFlash(el) {
  if (el.dataset.dismissing) return;
  el.dataset.dismissing = "true";
  el.classList.add("is-leaving");
  const remove = () => el.remove();
  el.addEventListener("transitionend", remove, { once: true });
  // Fallback in case transitions are disabled (prefers-reduced-motion) or never fire.
  setTimeout(remove, 500);
}

document.addEventListener("DOMContentLoaded", () => {
  syncFavoritesUI();

  // GSAP é opcional (carregado via CDN em base.html): se falhar ao
  // carregar (offline, bloqueador) ou o visitante pediu menos
  // movimento, tudo cai pro corte seco — nunca deixa conteúdo
  // permanentemente invisível por falta da lib.
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const gsapAvailable = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";
  const motionOn = gsapAvailable && !prefersReducedMotion;
  if (motionOn) {
    gsap.registerPlugin(ScrollTrigger);
  }

  document.querySelectorAll("[data-flash]").forEach((el) => {
    const timer = setTimeout(() => dismissFlash(el), 5000);
    el.querySelector("[data-flash-close]")?.addEventListener("click", () => {
      clearTimeout(timer);
      dismissFlash(el);
    });
  });

  document.querySelectorAll("form[data-submit-feedback]").forEach((form) => {
    form.addEventListener("submit", () => {
      const btn = form.querySelector('button[type="submit"]');
      if (!btn || btn.disabled) return;
      btn.dataset.originalText = btn.textContent.trim();
      btn.disabled = true;
      btn.setAttribute("aria-busy", "true");
      btn.textContent = "Enviando...";
    });
  });

  document.querySelectorAll("[data-fav-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const wasFavorited = isFavorited(btn.dataset.favId);
      toggleFavorite({
        id: btn.dataset.favId,
        title: btn.dataset.favTitle,
        meta: btn.dataset.favMeta,
        url: btn.dataset.favUrl,
      });
      // Pulso só ao favoritar (não ao desfavoritar) — reforça a ação
      // positiva sem chamar atenção pra remover algo.
      if (!wasFavorited) {
        btn.classList.remove("is-pulsing");
        void btn.offsetWidth; // força reflow pra poder retriggar a animação em cliques seguidos
        btn.classList.add("is-pulsing");
      }
    });
  });

  document.querySelectorAll("[data-nav-dropdown]").forEach((item) => {
    const trigger = item.querySelector("[data-nav-trigger]");
    trigger?.addEventListener("click", (event) => {
      event.stopPropagation();
      const isOpen = item.classList.contains("is-open");
      closeAllOverlays();
      if (!isOpen) {
        item.classList.add("is-open");
        trigger.setAttribute("aria-expanded", "true");
      }
    });
  });

  const menuBtn = document.querySelector("[data-menu-toggle]");
  const menuPanel = document.querySelector("[data-menu-panel]");
  const backdrop = document.querySelector("[data-menu-backdrop]");
  menuBtn?.addEventListener("click", (event) => {
    event.stopPropagation();
    const isOpen = menuPanel.classList.contains("is-open");
    closeAllOverlays(isOpen ? undefined : "menu");
    menuPanel.classList.toggle("is-open", !isOpen);
    menuBtn.classList.toggle("is-open", !isOpen);
    menuBtn.setAttribute("aria-expanded", String(!isOpen));
    backdrop?.classList.toggle("is-open", !isOpen);
  });
  backdrop?.addEventListener("click", () => closeAllOverlays());

  const favPanel = document.querySelector("[data-favorites-panel]");
  document.querySelectorAll("[data-favorites-toggle]").forEach((btn) => {
    btn.addEventListener("click", (event) => {
      event.stopPropagation();
      const isOpen = favPanel.classList.contains("is-open");
      closeAllOverlays(isOpen ? undefined : "favorites");
      favPanel.classList.toggle("is-open", !isOpen);
      document.querySelectorAll("[data-favorites-toggle]").forEach((b) => b.setAttribute("aria-expanded", String(!isOpen)));
    });
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".vdc-header")) closeAllOverlays();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeAllOverlays();
  });

  document.querySelectorAll(".vdc-select").forEach((select) => {
    const sync = () => select.setAttribute("data-has-value", String(select.value !== ""));
    select.addEventListener("change", sync);
    sync();
  });

  const tabs = document.querySelectorAll("[data-hero-tab]");
  const searchPanels = document.querySelectorAll("[data-search-panel]");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => {
        t.classList.remove("is-active");
        t.setAttribute("aria-selected", "false");
      });
      tab.classList.add("is-active");
      tab.setAttribute("aria-selected", "true");

      const target = tab.dataset.searchTarget;
      if (target) {
        searchPanels.forEach((panel) => {
          panel.hidden = panel.dataset.searchPanel !== target;
        });
      }
    });
  });

  // Revelação de seção ao rolar — mesma spec do DESIGN.md (fade + 16px,
  // 400ms, uma vez). Grades (imóveis, benefícios) ganham stagger real
  // via ScrollTrigger.batch em vez de aparecer tudo junto.
  if (motionOn) {
    gsap.utils.toArray(".vdc-reveal").forEach((el) => {
      gsap.to(el, {
        opacity: 1, y: 0, duration: 0.4, ease: "power2.out",
        scrollTrigger: { trigger: el, start: "top 85%", once: true },
      });
    });

    [".vdc-card", ".vdc-wizard__type"].forEach((selector) => {
      const items = gsap.utils.toArray(selector);
      if (!items.length) return;
      ScrollTrigger.batch(selector, {
        start: "top 88%",
        once: true,
        onEnter: (batch) => gsap.to(batch, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.06 }),
      });
    });
  } else {
    document.querySelectorAll(".vdc-reveal, .vdc-card, .vdc-wizard__type").forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
    });
  }

  // Prova concreta com peso: números que a marca usa como prova
  // (PRODUCT.md) contam de 0 até o valor real, uma vez, ao entrar na tela.
  if (motionOn) {
    document.querySelectorAll(".vdc-hero__badge strong").forEach((el) => {
      const raw = el.textContent.trim();
      if (!/^\d+$/.test(raw)) return;
      const target = parseInt(raw, 10);
      const counter = { val: 0 };
      gsap.to(counter, {
        val: target, duration: 1, ease: "power1.out",
        scrollTrigger: { trigger: el, start: "top 90%", once: true },
        onUpdate: () => { el.textContent = String(Math.round(counter.val)); },
      });
    });
  }

  const slides = document.querySelectorAll(".vdc-hero__slide");
  const dots = document.querySelectorAll("[data-hero-dot]");
  if (slides.length > 1) {
    let current = 0;
    const showSlide = (index) => {
      slides[current].classList.remove("is-active");
      dots[current]?.classList.remove("is-active");
      current = index;
      slides[current].classList.add("is-active");
      dots[current]?.classList.add("is-active");
    };
    dots.forEach((dot, index) => {
      dot.addEventListener("click", () => showSlide(index));
    });
    if (!prefersReducedMotion) {
      setInterval(() => showSlide((current + 1) % slides.length), 6000);
    }
  }

  // Parallax do hero: as fotos se deslocam mais devagar que a rolagem,
  // criando profundidade — via ScrollTrigger scrub (suaviza momentum
  // sozinho, sem o rAF manual de antes). Sem GSAP, o hero fica só
  // estático — degrada bem, nunca quebra.
  const heroEl = document.querySelector(".vdc-hero");
  const heroSlidesEl = document.querySelector(".vdc-hero__slides");
  if (motionOn && heroEl && heroSlidesEl) {
    gsap.to(heroSlidesEl, {
      yPercent: 12, ease: "none",
      scrollTrigger: { trigger: heroEl, start: "top top", end: "bottom top", scrub: true },
    });
  }

  // Cabeçalho compacta ao rolar: sinaliza "você saiu do hero, está no
  // conteúdo" — estado legível, não decoração. Alterna .is-condensed
  // uma vez ao cruzar um limiar, em vez de recalcular a cada pixel.
  const headerEl = document.querySelector(".vdc-header");
  if (headerEl) {
    const CONDENSE_AT = 72;
    let headerTicking = false;
    const updateHeaderState = () => {
      headerEl.classList.toggle("is-condensed", window.scrollY > CONDENSE_AT);
      headerTicking = false;
    };
    window.addEventListener(
      "scroll",
      () => {
        if (!headerTicking) {
          requestAnimationFrame(updateHeaderState);
          headerTicking = true;
        }
      },
      { passive: true }
    );
    updateHeaderState();
  }

  // Indicador de seção ativa no menu: enquanto o visitante rola pelas
  // seções da home, o link correspondente no cabeçalho acende —
  // mesma lógica do scroll-reveal (IntersectionObserver), reaproveitada
  // pra comunicar relação/posição em vez de repetir "apareceu".
  const trackedSections = document.querySelectorAll("section[id]");
  const navLinksById = new Map();
  document.querySelectorAll(".vdc-header__navlink[href^='/#'], .vdc-header__navlink[href^='#']").forEach((link) => {
    const id = link.getAttribute("href").split("#")[1];
    if (id) navLinksById.set(id, link);
  });
  if (trackedSections.length && navLinksById.size && "IntersectionObserver" in window) {
    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const link = navLinksById.get(entry.target.id);
          if (!link) return;
          link.classList.toggle("is-current", entry.isIntersecting);
        });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    trackedSections.forEach((section) => sectionObserver.observe(section));
  }

  // Wizard de cadastro — 4 passos, validados um de cada vez (só o
  // painel visível é checado; painéis com [hidden] já ficam fora da
  // validação nativa, então "novalidate" + checagem manual aqui cobre
  // tanto o clique em "Próximo" quanto o envio final no passo 4).
  const wizardForm = document.querySelector("[data-wizard]");
  if (wizardForm) {
    const panels = Array.from(wizardForm.querySelectorAll("[data-wizard-panel]"));
    const indicators = Array.from(wizardForm.querySelectorAll("[data-wizard-indicator]"));
    const fill = wizardForm.querySelector("[data-wizard-fill]");
    const backBtn = wizardForm.querySelector("[data-wizard-back]");
    const nextBtn = wizardForm.querySelector("[data-wizard-next]");
    const submitBtn = wizardForm.querySelector("[data-wizard-submit]");
    const total = panels.length;
    let current = 1;

    const applyState = () => {
      panels.forEach((panel) => {
        panel.hidden = Number(panel.dataset.wizardPanel) !== current;
      });
      indicators.forEach((li) => {
        const step = Number(li.dataset.wizardIndicator);
        li.classList.toggle("is-current", step === current);
        li.classList.toggle("is-done", step < current);
      });
      fill.style.width = `${((current - 1) / (total - 1)) * 100}%`;
      backBtn.hidden = current === 1;
      nextBtn.hidden = current === total;
      submitBtn.hidden = current !== total;
    };

    const goToStep = (nextStep) => {
      const outgoing = panels.find((p) => Number(p.dataset.wizardPanel) === current);
      current = nextStep;
      const incoming = panels.find((p) => Number(p.dataset.wizardPanel) === current);

      if (!motionOn || !outgoing) {
        applyState();
        return;
      }
      gsap.timeline()
        .to(outgoing, { opacity: 0, y: -8, duration: 0.15, ease: "power1.in" })
        .call(applyState)
        .fromTo(incoming, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out" });
    };

    const currentPanelValid = () => {
      const panel = panels[current - 1];
      const fields = panel.querySelectorAll("[required]");
      for (const field of fields) {
        if (!field.reportValidity()) return false;
      }
      return true;
    };

    nextBtn.addEventListener("click", () => {
      if (!currentPanelValid()) return;
      if (current < total) goToStep(current + 1);
    });

    backBtn.addEventListener("click", () => {
      if (current > 1) goToStep(current - 1);
    });

    wizardForm.addEventListener("submit", (event) => {
      if (!currentPanelValid()) event.preventDefault();
    });

    applyState();

    // Feedback de seleção: o cartão escolhido (tipo de imóvel) e o
    // botão escolhido (venda/aluguel) ganham um "pop" com pequeno
    // exagero (back.out) — o :checked do CSS já garante o estado
    // final correto mesmo sem isso, essa parte é só o tempero.
    //
    // clearProps ao terminar é essencial aqui: sem isso, o GSAP deixa
    // scale/opacity como inline style (prioridade maior que a regra
    // CSS ":checked"), e quando o rádio desmarca depois, a regra CSS
    // que devolveria o selo pro estado escondido nunca vence — o selo
    // fica "grudado" visível pra sempre, em qualquer cartão já clicado
    // uma vez. Liberando a propriedade de volta pro CSS assim que a
    // animação assenta, quem manda no estado escondido volta a ser
    // só o seletor ":checked", igual antes de qualquer clique.
    if (motionOn) {
      wizardForm.querySelectorAll('input[type="radio"]').forEach((input) => {
        input.addEventListener("change", () => {
          if (!input.checked) return;
          const card = input.nextElementSibling;
          if (!card) return;
          const icon = card.querySelector(".vdc-wizard__type-icon");
          const check = card.querySelector(".vdc-wizard__type-check");
          if (icon) {
            gsap.fromTo(icon, { scale: 0.75 }, {
              scale: 1, duration: 0.4, ease: "back.out(2)",
              onComplete: () => gsap.set(icon, { clearProps: "scale" }),
            });
          }
          if (check) {
            gsap.fromTo(check, { scale: 0, autoAlpha: 0 }, {
              scale: 1, autoAlpha: 1, duration: 0.35, ease: "back.out(2.5)",
              onComplete: () => gsap.set(check, { clearProps: "scale,opacity,visibility" }),
            });
          }
          if (!icon && !check) {
            gsap.fromTo(card, { scale: 0.96 }, {
              scale: 1, duration: 0.3, ease: "back.out(2)",
              onComplete: () => gsap.set(card, { clearProps: "scale" }),
            });
          }
        });
      });
    }
  }

  // Seletor de contato da home: WhatsApp x E-mail num cartão só. A cor
  // do thumb (verde/dourado) e o painel visível trocam juntos — só
  // uma fonte de verdade (data-active no container), sem estado duplicado.
  const contactSwitch = document.querySelector("[data-contact-switch]");
  if (contactSwitch) {
    const contactTabs = Array.from(contactSwitch.querySelectorAll("[data-contact-tab]"));
    const contactPanels = Array.from(document.querySelectorAll("[data-contact-panel]"));
    contactTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const target = tab.dataset.contactTab;
        if (contactSwitch.dataset.active === target) return;
        contactSwitch.dataset.active = target;
        contactTabs.forEach((t) => {
          const active = t === tab;
          t.classList.toggle("is-active", active);
          t.setAttribute("aria-selected", String(active));
        });

        const outgoing = contactPanels.find((p) => !p.hidden);
        const incoming = contactPanels.find((p) => p.dataset.contactPanel === target);
        const applyPanels = () => {
          contactPanels.forEach((panel) => {
            panel.hidden = panel.dataset.contactPanel !== target;
          });
        };

        if (!motionOn || !outgoing || !incoming) {
          applyPanels();
          return;
        }
        gsap.timeline()
          .to(outgoing, { opacity: 0, y: -8, duration: 0.15, ease: "power1.in" })
          .call(applyPanels)
          .fromTo(incoming, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out" });
      });
    });
  }

  // Dropzone de foto (cadastro de imóvel do admin) — clique ou
  // arraste fazem a mesma coisa; a pré-visualização (arquivo novo ou
  // já salvo, na edição) substitui o rótulo com ícone.
  document.querySelectorAll("[data-dropzone]").forEach((zone) => {
    const input = zone.querySelector("[data-dropzone-input]");
    const label = zone.querySelector("[data-dropzone-label]");
    const preview = zone.querySelector("[data-dropzone-preview]");
    const previewImg = zone.querySelector("[data-dropzone-preview-img]");
    const removeBtn = zone.querySelector("[data-dropzone-remove]");
    const removeFlag = zone.querySelector("[data-dropzone-remove-flag]");
    if (!input || !label || !preview || !previewImg) return;

    const showPreview = (src) => {
      previewImg.src = src;
      label.hidden = true;
      preview.hidden = false;
      if (removeFlag) removeFlag.value = "0";
    };
    const showLabel = () => {
      label.hidden = false;
      preview.hidden = true;
      previewImg.src = "";
    };

    input.addEventListener("change", () => {
      const file = input.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => showPreview(event.target.result);
      reader.readAsDataURL(file);
    });

    removeBtn?.addEventListener("click", () => {
      input.value = "";
      if (removeFlag) removeFlag.value = "1";
      showLabel();
    });

    ["dragover", "dragenter"].forEach((evt) => {
      zone.addEventListener(evt, (event) => {
        event.preventDefault();
        zone.classList.add("is-dragover");
      });
    });
    ["dragleave", "drop"].forEach((evt) => {
      zone.addEventListener(evt, (event) => {
        event.preventDefault();
        zone.classList.remove("is-dragover");
      });
    });
    zone.addEventListener("drop", (event) => {
      const file = event.dataTransfer?.files?.[0];
      if (!file) return;
      input.files = event.dataTransfer.files;
      input.dispatchEvent(new Event("change"));
    });
  });

  // Mostrar/ocultar senha (tela de login) — o checkbox liga o mesmo
  // .vdc-toggle já usado pro "destacar na home", só trocando o
  // type do campo de senha em vez de um valor de formulário.
  document.querySelectorAll("[data-toggle-password]").forEach((checkbox) => {
    const field = document.getElementById(checkbox.dataset.togglePassword);
    if (!field) return;
    checkbox.addEventListener("change", () => {
      field.type = checkbox.checked ? "text" : "password";
    });
  });

  // Autopreenchimento de endereço a partir do CEP (ViaCEP — gratuito,
  // sem chave). Poupa a pessoa de digitar rua, bairro, cidade e UF à
  // mão, e melhora a chance de a geocodificação do backend acertar,
  // porque o nome oficial da rua vem certinho.
  //
  // Só preenche campo que ainda está vazio, pra não sobrescrever o que
  // já foi digitado. Número e complemento continuam sendo do admin: o
  // CEP não sabe qual é a casa.
  document.querySelectorAll("[data-cep-input]").forEach((cepField) => {
    const byId = (key) => document.getElementById(cepField.dataset[key] || "");
    const streetField = byId("cepTargetStreet");
    const neighborhoodField = byId("cepTargetNeighborhood");
    const cityField = byId("cepTargetCity");
    const stateField = byId("cepTargetState");
    const numberField = byId("cepTargetNumber");

    const fill = (field, value) => {
      if (field && value && !field.value.trim()) field.value = value;
    };

    cepField.addEventListener("input", () => {
      const digits = cepField.value.replace(/\D/g, "").slice(0, 8);
      cepField.value = digits.length > 5 ? `${digits.slice(0, 5)}-${digits.slice(5)}` : digits;
    });

    cepField.addEventListener("blur", () => {
      const digits = cepField.value.replace(/\D/g, "");
      if (digits.length !== 8) return;

      // ViaCEP às vezes demora ou está fora do ar; nada disso pode
      // travar o formulário, então todo erro é silenciosamente ignorado
      // e a pessoa digita o endereço normalmente.
      const abort = new AbortController();
      const timer = setTimeout(() => abort.abort(), 6000);

      fetch(`https://viacep.com.br/ws/${digits}/json/`, { signal: abort.signal })
        .then((res) => (res.ok ? res.json() : null))
        .then((data) => {
          if (!data || data.erro) return;
          fill(streetField, data.logradouro);
          fill(neighborhoodField, data.bairro);
          fill(cityField, data.localidade);
          fill(stateField, data.uf);
          // Rua veio pronta: o próximo campo a preencher é o número.
          if (numberField && !numberField.value.trim() && data.logradouro) numberField.focus();
        })
        .catch(() => {})
        .finally(() => clearTimeout(timer));
    });
  });
});
