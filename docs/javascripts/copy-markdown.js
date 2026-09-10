/*
  The Markdown split button: copy the page's source, or open the menu for both
  actions.

  `page_markdown.py` publishes every page's source beside its HTML, so copying
  only has to fetch its own `.md` twin. Fetching rather than reading the DOM
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

  function labels(root) {
    return root.querySelectorAll("[data-braid-copy-label]");
  }

  function setLabel(text) {
    // The face and the menu item share a label, so a copy from either place
    // reports back in both.
    labels(document).forEach(function (node) {
      node.textContent = text;
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

    var original = document.body.getAttribute("data-braid-copy-original");
    if (original === null) {
      var first = labels(document)[0];
      original = first ? first.textContent : "Copy page";
      document.body.setAttribute("data-braid-copy-original", original);
    }

    window.clearTimeout(resetTimer);

    try {
      var response = await fetch(url, { headers: { Accept: "text/markdown" } });
      if (!response.ok) {
        throw new Error("markdown request failed: " + response.status);
      }
      await navigator.clipboard.writeText(await response.text());
      setLabel("Copied");
    } catch (error) {
      // The clipboard API needs a secure context and a permission the reader
      // can refuse, and the fetch can fail on its own. Say so rather than
      // leaving the button looking like it worked.
      setLabel("Copy failed");
      console.error("Braid: copy as Markdown failed", error);
    }

    resetTimer = window.setTimeout(function () {
      setLabel(document.body.getAttribute("data-braid-copy-original"));
    }, RESET_MS);
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
