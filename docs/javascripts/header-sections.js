/* The header's section links have to recompute their own active state.

   Material's instant navigation swaps the page title and the components it
   owns; a custom nav living in the header is not among them. The class the
   template rendered for the first page visited would otherwise stay put for the
   rest of the visit, so clicking Changelog left Documentation highlighted.

   The rule here mirrors the template's: a section is current when its own URL is
   the page being viewed, and the first section is the fallback for every page
   that is not a section root of its own. Nothing is hardcoded, so the two stay
   in step if a section is added. */
(function () {
  "use strict";

  var ACTIVE = "braid-header__section--active";

  function sync() {
    var links = document.querySelectorAll(".braid-header__section");
    if (!links.length) return;

    var current = null;
    links.forEach(function (link) {
      if (new URL(link.href).pathname === window.location.pathname) current = link;
    });
    current = current || links[0];

    links.forEach(function (link) {
      var active = link === current;
      link.classList.toggle(ACTIVE, active);
      if (active) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }

  sync();
  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(sync);
  }
})();
