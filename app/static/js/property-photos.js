// Gerenciador de fotos do imóvel (cadastro/edição no admin) — tudo
// acontece no navegador (adicionar, remover, reordenar, escolher a
// principal); nada disso fala com o servidor até o formulário inteiro
// ser enviado. No submit, 3 campos ocultos são montados com o estado
// final e o <input type="file"> é reconstruído só com os arquivos
// novos, na ordem visual final — o backend (_apply_property_photos em
// app.py) lê esse pacote e aplica tudo de uma vez.
document.addEventListener("DOMContentLoaded", () => {
  const manager = document.querySelector("[data-photos-manager]");
  if (!manager) return;

  const form = manager.closest("form");
  const grid = manager.querySelector("[data-photos-grid]");
  const dropzone = manager.querySelector("[data-photos-dropzone]");
  const input = manager.querySelector("[data-photos-input]");
  const template = manager.querySelector("[data-photo-item-template]");
  const emptyHint = manager.querySelector("[data-photos-empty-hint]");
  const orderField = manager.querySelector("[data-photos-order]");
  const primaryField = manager.querySelector("[data-photos-primary]");
  const deletedField = manager.querySelector("[data-photos-deleted]");
  if (!form || !grid || !template) return;

  const deletedIds = []; // ids de fotos já salvas, marcadas pra excluir
  const pendingFiles = new Map(); // ref temporária ("pending:N") -> File
  let pendingCounter = 0;
  let primaryRef = null; // ref (existing:<id> ou pending:<n>) da foto principal atual

  const itemsInOrder = () => Array.from(grid.querySelectorAll("[data-photo-item]"));

  function updateEmptyState() {
    if (emptyHint) emptyHint.hidden = itemsInOrder().length > 0;
  }

  function setPrimary(ref) {
    primaryRef = ref;
    itemsInOrder().forEach((el) => {
      const isThis = el.dataset.photoRef === ref;
      const star = el.querySelector("[data-photo-star]");
      const badge = el.querySelector("[data-photo-primary-badge]");
      star.setAttribute("aria-pressed", String(isThis));
      star.querySelector("svg").setAttribute("fill", isThis ? "currentColor" : "none");
      if (badge) badge.hidden = !isThis;
    });
  }

  // Garante que sempre exista uma principal enquanto houver pelo menos
  // 1 foto — chamada depois de adicionar ou remover.
  function ensurePrimary() {
    const items = itemsInOrder();
    if (!items.length) {
      primaryRef = null;
      return;
    }
    if (items.some((el) => el.dataset.photoRef === primaryRef)) return;
    setPrimary(items[0].dataset.photoRef);
  }

  function removeItem(el) {
    const ref = el.dataset.photoRef;
    if (ref.startsWith("existing:")) {
      deletedIds.push(Number(ref.split(":")[1]));
    } else {
      pendingFiles.delete(ref);
    }
    el.remove();
    ensurePrimary();
    updateEmptyState();
  }

  function moveItem(el, direction) {
    if (direction === "left" && el.previousElementSibling) {
      grid.insertBefore(el, el.previousElementSibling);
    } else if (direction === "right" && el.nextElementSibling) {
      grid.insertBefore(el.nextElementSibling, el);
    }
  }

  function wireItem(el) {
    el.querySelector("[data-photo-star]").addEventListener("click", () => setPrimary(el.dataset.photoRef));
    el.querySelector("[data-photo-remove]").addEventListener("click", () => removeItem(el));
    el.querySelector("[data-photo-move-left]")?.addEventListener("click", () => moveItem(el, "left"));
    el.querySelector("[data-photo-move-right]")?.addEventListener("click", () => moveItem(el, "right"));

    // Arrastar e soltar é bônus de desktop (mouse) — as setas ◂ ▸
    // acima já resolvem reordenar em qualquer dispositivo, incluindo
    // tablet/touch, onde o HTML5 drag-and-drop nativo não funciona
    // direito sem biblioteca extra.
    el.addEventListener("dragstart", (event) => {
      el.classList.add("is-dragging");
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("text/plain", el.dataset.photoRef);
    });
    el.addEventListener("dragend", () => el.classList.remove("is-dragging"));
  }

  grid.addEventListener("dragover", (event) => {
    const dragging = grid.querySelector(".is-dragging");
    if (!dragging) return;
    event.preventDefault();
    // Acha o item mais próximo do ponteiro (comparando o centro
    // horizontal de cada card) e solta antes dele — simples e
    // suficiente pra uma grade que quebra linha, sem precisar de
    // matemática 2D completa.
    const proximo = itemsInOrder()
      .filter((el) => el !== dragging)
      .find((el) => {
        const box = el.getBoundingClientRect();
        return event.clientX < box.left + box.width / 2;
      });
    grid.insertBefore(dragging, proximo || null);
  });
  grid.addEventListener("drop", (event) => event.preventDefault());

  // Fotos já existentes (renderizadas pelo servidor no carregamento
  // da página) — descobre a principal atual entre elas.
  itemsInOrder().forEach((el) => {
    wireItem(el);
    if (el.querySelector("[data-photo-star]")?.getAttribute("aria-pressed") === "true") {
      primaryRef = el.dataset.photoRef;
    }
  });
  ensurePrimary();
  updateEmptyState();

  function addFiles(fileList) {
    Array.from(fileList).forEach((file) => {
      if (!file.type.startsWith("image/")) return;
      const ref = `pending:${pendingCounter++}`;
      pendingFiles.set(ref, file);

      const node = template.content.firstElementChild.cloneNode(true);
      node.dataset.photoRef = ref;
      wireItem(node);
      grid.appendChild(node);

      const reader = new FileReader();
      reader.onload = (event) => {
        node.querySelector(".vdc-photos__thumb").src = event.target.result;
      };
      reader.readAsDataURL(file);
    });
    ensurePrimary();
    updateEmptyState();
  }

  input.addEventListener("change", () => {
    addFiles(input.files);
    input.value = ""; // permite selecionar o mesmo arquivo de novo depois de removê-lo
  });

  ["dragover", "dragenter"].forEach((evt) => {
    dropzone.addEventListener(evt, (event) => {
      event.preventDefault();
      dropzone.classList.add("is-dragover");
    });
  });
  ["dragleave", "drop"].forEach((evt) => {
    dropzone.addEventListener(evt, (event) => {
      event.preventDefault();
      dropzone.classList.remove("is-dragover");
    });
  });
  dropzone.addEventListener("drop", (event) => {
    if (event.dataTransfer?.files?.length) addFiles(event.dataTransfer.files);
  });

  // No envio do formulário: monta a ordem final, decide quem é a
  // principal e reconstrói o <input type="file"> só com os arquivos
  // novos — na mesma sequência em que aparecem na grade, porque o
  // backend associa "new:0", "new:1"... à posição de cada arquivo em
  // request.files.getlist('photos').
  form.addEventListener("submit", () => {
    const order = [];
    const dataTransfer = new DataTransfer();
    let novoIndice = 0;
    let principalFinal = "";

    itemsInOrder().forEach((el) => {
      const ref = el.dataset.photoRef;
      if (ref.startsWith("existing:")) {
        order.push(ref);
        if (ref === primaryRef) principalFinal = ref;
        return;
      }
      const file = pendingFiles.get(ref);
      if (!file) return; // não deveria acontecer, mas não trava o envio
      dataTransfer.items.add(file);
      const refFinal = `new:${novoIndice++}`;
      order.push(refFinal);
      if (ref === primaryRef) principalFinal = refFinal;
    });

    input.files = dataTransfer.files;
    orderField.value = JSON.stringify(order);
    primaryField.value = principalFinal;
    deletedField.value = JSON.stringify(deletedIds);
  });
});
