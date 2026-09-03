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

  function onKeydown(event) {
    if (event.defaultPrevented || typeof event.key !== "string") return;

    // Enter/Space on a label we have given button semantics.
    var target = event.target;
    var trigger = target && target.closest
      ? target.closest(".braid-search-trigger, .braid-header__menu")
      : null;

    if (trigger && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      if (trigger.classList.contains("braid-search-trigger")) {
        openSearch();
      } else {
        setToggle(trigger.htmlFor, true);
      }
      return;
    }

    // Cmd/Ctrl-K from anywhere.
    if (!(event.metaKey || event.ctrlKey) || event.altKey) return;
    if (event.key.toLowerCase() !== "k") return;

    event.preventDefault();
    openSearch();
  }

  document.addEventListener("keydown", onKeydown);

  localizeShortcutHint();

  // Material re-renders the header on instant navigation; re-apply after each.
  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(localizeShortcutHint);
  }
})();
