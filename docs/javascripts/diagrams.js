(function () {
  const minScale = 0.75;
  const maxScale = 3;
  const step = 0.25;
  const minimumDiagramWidth = 2400;

  function clamp(value) {
    return Math.max(minScale, Math.min(maxScale, value));
  }

  function enhanceDiagram(diagram, index) {
    if (diagram.dataset.diagramEnhanced === "true" || diagram.closest(".diagram-stage")) {
      return;
    }

    diagram.dataset.diagramEnhanced = "true";

    const stage = document.createElement("div");
    stage.className = "diagram-stage";

    const toolbar = document.createElement("div");
    toolbar.className = "diagram-toolbar";

    const zoomOut = document.createElement("button");
    zoomOut.type = "button";
    zoomOut.className = "diagram-control";
    zoomOut.textContent = "-";
    zoomOut.title = "Zoom out";
    zoomOut.setAttribute("aria-label", "Zoom diagram out");

    const zoomValue = document.createElement("span");
    zoomValue.className = "diagram-zoom-value";

    const zoomIn = document.createElement("button");
    zoomIn.type = "button";
    zoomIn.className = "diagram-control";
    zoomIn.textContent = "+";
    zoomIn.title = "Zoom in";
    zoomIn.setAttribute("aria-label", "Zoom diagram in");

    const reset = document.createElement("button");
    reset.type = "button";
    reset.className = "diagram-reset";
    reset.textContent = "100%";
    reset.title = "Reset zoom";
    reset.setAttribute("aria-label", "Reset diagram zoom");

    toolbar.append(zoomOut, zoomValue, zoomIn, reset);

    const viewport = document.createElement("div");
    viewport.className = "diagram-viewport";
    viewport.tabIndex = 0;
    viewport.setAttribute("aria-label", `Diagram ${index + 1}`);

    diagram.parentNode.insertBefore(stage, diagram);
    viewport.appendChild(diagram);
    stage.append(toolbar, viewport);

    let scale = 1;
    let baseWidth = minimumDiagramWidth;

    function applyScale() {
      const percent = `${Math.round(scale * 100)}%`;
      const width = Math.round(baseWidth * scale);

      diagram.style.setProperty("--diagram-width", `${width}px`);
      zoomValue.textContent = percent;
      zoomOut.disabled = scale <= minScale;
      zoomIn.disabled = scale >= maxScale;

      const svg = diagram.querySelector("svg");
      if (svg) {
        svg.style.width = `${width}px`;
        svg.style.maxWidth = "none";
        svg.style.height = "auto";
      }
    }

    function setScale(nextScale) {
      scale = clamp(nextScale);
      applyScale();
    }

    zoomOut.addEventListener("click", () => setScale(scale - step));
    zoomIn.addEventListener("click", () => setScale(scale + step));
    reset.addEventListener("click", () => setScale(1));
    viewport.addEventListener(
      "wheel",
      (event) => {
        if (!event.ctrlKey && !event.metaKey) {
          return;
        }

        event.preventDefault();
        setScale(scale + (event.deltaY < 0 ? step : -step));
      },
      { passive: false },
    );

    function syncRenderedSize() {
      const svg = diagram.querySelector("svg");
      if (svg) {
        const viewBoxWidth = svg.viewBox && svg.viewBox.baseVal ? svg.viewBox.baseVal.width : 0;
        const attrWidth = parseFloat(svg.getAttribute("width") || "0");
        baseWidth = Math.max(minimumDiagramWidth, viewBoxWidth, attrWidth);
      }

      applyScale();
    }

    const observer = new MutationObserver(syncRenderedSize);
    observer.observe(diagram, { childList: true, subtree: true });

    requestAnimationFrame(syncRenderedSize);
  }

  function initDiagrams() {
    document.querySelectorAll(".mermaid").forEach(enhanceDiagram);
  }

  if (window.document$) {
    window.document$.subscribe(initDiagrams);
  } else {
    document.addEventListener("DOMContentLoaded", initDiagrams);
  }

  const pageObserver = new MutationObserver(initDiagrams);
  pageObserver.observe(document.documentElement, { childList: true, subtree: true });
})();
