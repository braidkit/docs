/* Braid Docs — search affordances.
 *
 * Two jobs Material does not do for us:
 *
 *   1. Cmd/Ctrl-K opens search. Material binds "s", "f" and "/", but the
 *      command-palette shortcut is what people reach for.
 *   2. The header search trigger is a <label> (Material's overlay is driven by
 *      the #__search checkbox). Labels are not activated by Enter or Space, so
 *      the button semantics we advertise have to be implemented.
 *
 * Toggling the checkbox in script does not fire `change`, and Material's
 * overlay listens for exactly that — so every toggle here dispatches one.
 */
(function () {
  "use strict";

  var IS_APPLE = /mac|iphone|ipad|ipod/i.test(navigator.platform || navigator.userAgent);

  function setToggle(id, value) {
    var toggle = document.getElementById(id);
    if (!toggle || toggle.checked === value) return null;

    toggle.checked = value;
    toggle.dispatchEvent(new Event("change", { bubbles: true }));
    return toggle;
  }

  function openSearch() {
    if (!setToggle("__search", true)) return;

    // The overlay is revealed by CSS reacting to the checkbox, so the input is
    // not focusable until style and layout have settled. One frame is not
    // always enough; two is, because the second runs after the first paint.
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () {
        var input = document.querySelector("[data-md-component='search-query']");
        if (input) input.focus();
      });
    });
  }

  /* The shortcut hint is authored as "Ctrl K" and corrected on Apple hardware,
     so the pre-JS render is right for the majority platform. */
  function localizeShortcutHint() {
    if (!IS_APPLE) return;
    document.querySelectorAll("[data-braid-shortcut]").forEach(function (el) {
      el.textContent = "⌘ K";
    });
  }

  function syncDrawerButton() {
    var drawer = document.getElementById("__drawer");
    if (!drawer) return;

    document.querySelectorAll(".braid-header__menu").forEach(function (button) {
      button.setAttribute("aria-expanded", String(drawer.checked));
      button.setAttribute("aria-label", drawer.checked ? "Close navigation" : "Open navigation");
    });
  }

  function toggleDrawer() {
    var drawer = document.getElementById("__drawer");
    if (!drawer) return;

    setToggle("__drawer", !drawer.checked);
    syncDrawerButton();
  }

  function onKeydown(event) {
    if (typeof event.key !== "string") return;

    /* The drawer trigger is a <label>, so a pointer toggles #__drawer natively
       and nothing here needs to handle click. Keyboard is the gap: labels are
       not activated by Enter or Space, so the button semantics the markup
       advertises have to be implemented. Because activation is not native
       there is no synthetic click to collide with, and this toggles once. */
    var target = event.target;
    var menuButton = target && target.closest
      ? target.closest(".braid-header__menu")
      : null;

    if (menuButton && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      toggleDrawer();
      return;
    }

    if (event.defaultPrevented) return;

    // Enter/Space on the search label we have given button semantics.
    var trigger = target && target.closest
      ? target.closest(".braid-search-trigger")
      : null;

    if (trigger && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      openSearch();
      return;
    }

    // Cmd/Ctrl-K from anywhere.
    if (!(event.metaKey || event.ctrlKey) || event.altKey) return;
    if (event.key.toLowerCase() !== "k") return;

    event.preventDefault();
    openSearch();
  }

  document.addEventListener("keydown", onKeydown);
  document.addEventListener("change", function (event) {
    if (event.target && event.target.id === "__drawer") syncDrawerButton();
  });

  localizeShortcutHint();
  syncDrawerButton();

  // Material re-renders the header on instant navigation; re-apply after each.
  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(function () {
      localizeShortcutHint();
      syncDrawerButton();
    });
  }
})();
