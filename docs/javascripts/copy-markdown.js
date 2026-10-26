/*
  The Markdown split button: copy the page's source, or open the menu for both
  actions. A page with an agent guide copies the guide from the face instead,
  and offers the page's source in the menu.

  `page_markdown.py` publishes every page's source beside its HTML, and each
  agent guide beside that, so copying only has to fetch the button's file. Fetching rather than reading the DOM
  means the reader gets the authored Markdown, not a reconstruction of the
  rendered page.

  Everything listens on the document rather than on the elements, which
  survives Material's instant navigation swapping the content out from under
  us.
*/
(function () {
  "use strict";

  var RESET_MS = 2000;
  var resetTimer = null;

  function labelsFor(url) {
    // Every control that copies the same file reports back, so a copy from the
    // menu also shows on the face.
    var nodes = [];
    document.querySelectorAll("[data-braid-copy-markdown]").forEach(function (button) {
      var label = button.querySelector("[data-braid-copy-label]");
      if (label && button.getAttribute("data-markdown-url") === url) {
        nodes.push(label);
      }
    });
    return nodes;
  }

  function setLabels(nodes, text) {
    // The face and the menu items can have different labels, so each one
    // remembers its own.
    nodes.forEach(function (node) {
      if (!node.hasAttribute("data-braid-copy-original")) {
        node.setAttribute("data-braid-copy-original", node.textContent);
      }
      node.textContent = text;
    });
  }

  function resetLabels() {
    document.querySelectorAll("[data-braid-copy-original]").forEach(function (node) {
      node.textContent = node.getAttribute("data-braid-copy-original");
    });
  }

  function closeMenu() {
    var toggle = document.querySelector("[data-braid-menu-toggle]");
    var menu = document.querySelector("[data-braid-menu]");
    if (toggle && menu) {
      toggle.setAttribute("aria-expanded", "false");
      menu.hidden = true;
    }
  }

  async function copy(button) {
    var url = button.getAttribute("data-markdown-url");
    if (!url) {
      return;
    }

    window.clearTimeout(resetTimer);
    resetLabels();
    var nodes = labelsFor(url);

    try {
      var response = await fetch(url, { headers: { Accept: "text/markdown" } });
      if (!response.ok) {
        throw new Error("markdown request failed: " + response.status);
      }
      await navigator.clipboard.writeText(await response.text());
      setLabels(nodes, "Copied");
    } catch (error) {
      // The clipboard API needs a secure context and a permission the reader
      // can refuse, and the fetch can fail on its own. Say so rather than
      // leaving the button looking like it worked.
      setLabels(nodes, "Copy failed");
      console.error("Braid: copy as Markdown failed", error);
    }

    resetTimer = window.setTimeout(resetLabels, RESET_MS);
  }

  document.addEventListener("click", function (event) {
    var toggle = event.target.closest("[data-braid-menu-toggle]");
    if (toggle) {
      var menu = document.querySelector("[data-braid-menu]");
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
      menu.hidden = open;
      return;
    }

    var button = event.target.closest("[data-braid-copy-markdown]");
    if (button) {
      copy(button);
      closeMenu();
      return;
    }

    // Any click that is not on the control dismisses it, including one on the
    // menu's own link, which is navigating away regardless.
    if (!event.target.closest("[data-braid-pageactions]")) {
      closeMenu();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") {
      return;
    }
    var toggle = document.querySelector('[data-braid-menu-toggle][aria-expanded="true"]');
    if (toggle) {
      closeMenu();
      toggle.focus();
    }
  });

  // Instant navigation reuses the document, so a menu left open on one page
  // would still be open on the next.
  document.addEventListener("DOMContentLoaded", closeMenu);
})();
