(() => {
  const customLayouts = ["THEME01-025", "THEME01-047", "THEME01-058", "THEME01-028", "THEME01-057"];

  function getSlideModel(dataLayout) {
    const api = window.__deckViewModel;
    const vm = api?.model;
    const slide = vm?.slides?.find(item => item.dataLayout === dataLayout);
    if (!slide) return null;
    const liveProps = api.peek?.("props")?.[slide.id] || {};
    return { slide, props: { ...(slide.props || {}), ...liveProps } };
  }

  function makeEditable(tag, className, id, text) {
    const el = document.createElement(tag);
    el.className = className;
    el.dataset.editableId = id;
    el.textContent = text || "";
    return el;
  }

  function createShell(section, className) {
    section.classList.add("opc-customized");
    const shell = document.createElement("div");
    shell.className = `opc-green-slide ${className}`;
    section.appendChild(shell);
    return shell;
  }

  function addHeader(shell, slideKey, props) {
    shell.appendChild(makeEditable("div", "opc-section-title", `text:${slideKey}:custom-section`, props.kicker));
    shell.appendChild(makeEditable("div", "opc-main-title", `text:${slideKey}:custom-title`, props.title));
    if (props.cn) shell.appendChild(makeEditable("div", "opc-subtitle", `text:${slideKey}:custom-subtitle`, props.cn));
  }

  function buildTable() {
    const dataLayout = "THEME01-025";
    const section = document.querySelector(`.slide[data-layout="${dataLayout}"]`);
    if (!section || section.querySelector(".opc-green-slide")) return false;
    const model = getSlideModel(dataLayout);
    if (!model) return false;
    const { slide, props } = model;
    const shell = createShell(section, "opc-table-slide");
    addHeader(shell, slide.key, props);

    const table = document.createElement("div");
    table.className = "opc-table";
    table.appendChild(makeEditable("div", "opc-table-cell opc-table-head", `text:${slide.key}:table-corner`, "对比维度"));
    (props.companies || []).slice(0, 3).forEach((company, index) => {
      table.appendChild(makeEditable(
        "div",
        "opc-table-cell opc-table-head",
        `text:${slide.key}:table-company-${index}`,
        `${company.name}｜${company.role}`,
      ));
    });
    (props.attributes || []).slice(0, 4).forEach((row, rowIndex) => {
      table.appendChild(makeEditable("div", "opc-table-cell opc-table-row-label", `text:${slide.key}:table-row-${rowIndex}`, row.label));
      (row.values || []).slice(0, 3).forEach((value, colIndex) => {
        table.appendChild(makeEditable("div", "opc-table-cell", `text:${slide.key}:table-${rowIndex}-${colIndex}`, value));
      });
    });
    shell.appendChild(table);
    window.__initEditableText?.(shell);
    return true;
  }

  function buildStatement() {
    const dataLayout = "THEME01-047";
    const section = document.querySelector(`.slide[data-layout="${dataLayout}"]`);
    if (!section || section.querySelector(".opc-green-slide")) return false;
    const model = getSlideModel(dataLayout);
    if (!model) return false;
    const { slide, props } = model;
    const shell = createShell(section, "opc-statement-slide");
    shell.appendChild(makeEditable("div", "opc-section-title", `text:${slide.key}:custom-section`, props.kicker));
    shell.appendChild(makeEditable("div", "opc-statement", `text:${slide.key}:custom-statement`, props.quote));
    window.__initEditableText?.(shell);
    return true;
  }

  function buildFunnel(dataLayout, mapEvent) {
    const section = document.querySelector(`.slide[data-layout="${dataLayout}"]`);
    if (!section || section.querySelector(".opc-green-slide")) return false;
    const model = getSlideModel(dataLayout);
    if (!model) return false;
    const { slide, props } = model;
    const shell = createShell(section, "opc-funnel-slide");
    addHeader(shell, slide.key, props);

    const funnel = document.createElement("div");
    funnel.className = "opc-funnel";
    (props.events || []).slice(0, 5).forEach((event, index) => {
      const content = mapEvent(event);
      const stage = document.createElement("div");
      stage.className = "opc-funnel-stage";
      stage.appendChild(makeEditable("div", "opc-stage-name", `text:${slide.key}:funnel-${index}-name`, content.name));
      stage.appendChild(makeEditable("div", "opc-stage-action", `text:${slide.key}:funnel-${index}-action`, content.action));
      stage.appendChild(makeEditable("div", "opc-stage-note", `text:${slide.key}:funnel-${index}-note`, content.note));
      funnel.appendChild(stage);
    });
    shell.appendChild(funnel);
    window.__initEditableText?.(shell);
    return true;
  }

  function buildClosing() {
    const dataLayout = "THEME01-057";
    const section = document.querySelector(`.slide[data-layout="${dataLayout}"]`);
    if (!section || section.querySelector(".opc-green-slide")) return false;
    const model = getSlideModel(dataLayout);
    if (!model) return false;
    const { slide, props } = model;
    const shell = createShell(section, "opc-closing-slide");

    const title = makeEditable("h2", "opc-closing-title", `text:${slide.key}:custom-title`, props.title);
    shell.appendChild(title);

    const qr = document.createElement("div");
    qr.className = "opc-closing-qr";
    const image = document.createElement("img");
    image.src = props.images?.[0] || "";
    image.alt = "微信二维码";
    qr.appendChild(image);
    shell.appendChild(qr);

    window.__initEditableText?.(shell);
    return true;
  }

  function initialize() {
    if (!window.__deckViewModel || !window.__initEditableText) return false;
    const results = [
      buildTable(),
      buildStatement(),
      buildFunnel("THEME01-058", event => ({ name: event.date, action: event.title, note: event.desc })),
      buildFunnel("THEME01-028", event => ({ name: event.date, action: event.round, note: event.note })),
      buildClosing(),
    ];
    document.querySelectorAll(".opc-green-slide").forEach(node => window.__initEditableText?.(node));
    return customLayouts.every(layout => document.querySelector(`.slide[data-layout="${layout}"] .opc-green-slide`));
  }

  let attempts = 0;
  const timer = window.setInterval(() => {
    attempts += 1;
    if (initialize() || attempts > 50) window.clearInterval(timer);
  }, 100);
})();
