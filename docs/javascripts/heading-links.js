/* Heading links update the URL and copy it, so a reader can paste the exact
   section into a review or support thread. The link remains an ordinary anchor
   when JavaScript is unavailable. */
(function () {
  "use strict";

  var toast;
  var toastTimer;

  function updateUrl(url) {
    window.history.pushState(null, "", url);
  }

  function legacyCopy(text) {
    var input = document.createElement("textarea");
    input.value = text;
    input.setAttribute("readonly", "");
    input.style.cssText = "left:-9999px;position:fixed;top:0";
    document.body.appendChild(input);
    input.select();
    var copied = document.execCommand("copy");
    input.remove();
    if (!copied) throw new Error("The browser did not copy the link");
  }

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () {
        legacyCopy(text);
      });
    }

    legacyCopy(text);
    return Promise.resolve();
  }

  function announce(message) {
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "braid-link-toast";
      toast.setAttribute("aria-live", "polite");
      toast.setAttribute("role", "status");
      document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.dataset.visible = "true";
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () {
      toast.dataset.visible = "false";
    }, 1800);
  }

  function decorate() {
    document.querySelectorAll(".md-typeset .headerlink").forEach(function (link) {
      if (link.dataset.braidHeadingLink) return;
      link.dataset.braidHeadingLink = "true";
      link.setAttribute("aria-label", "Copy link to this section");
      link.setAttribute("title", "Copy link to this section");
    });
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest(".md-typeset .headerlink");
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

    event.preventDefault();
    var url = new URL(link.getAttribute("href"), window.location.href).href;
    updateUrl(url);
    link.blur();

    copy(url).then(function () {
      announce("Link copied");
    }).catch(function () {
      announce("Link ready to copy");
    });
  });

  decorate();
  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(decorate);
  }
})();
