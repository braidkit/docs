(function () {
  function enhanceSearch() {
    var searchInput = document.querySelector("[data-md-component='search-query']");
    if (searchInput) searchInput.placeholder = "Search documentation…";
  }

  function openSearch() {
    var searchToggle = document.getElementById("__search");
    if (!searchToggle) return;

    searchToggle.checked = true;
    window.setTimeout(function () {
      var searchInput = document.querySelector("[data-md-component='search-query']");
      if (searchInput) searchInput.focus();
    }, 0);
  }

  document.addEventListener("keydown", function (event) {
    var trigger = event.target.closest && event.target.closest(".braid-search-trigger, .braid-header__menu");
    if (trigger && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      var toggle = document.getElementById(trigger.htmlFor);
      if (toggle) toggle.checked = true;
      if (trigger.classList.contains("braid-search-trigger")) openSearch();
      return;
    }

    if (!(event.metaKey || event.ctrlKey) || event.key.toLowerCase() !== "k") {
      return;
    }

    event.preventDefault();
    openSearch();
  });

  enhanceSearch();
  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(enhanceSearch);
  }
})();
