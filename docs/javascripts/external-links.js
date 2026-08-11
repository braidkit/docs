/* Tag nav links that leave the site.
 *
 * This can't be done in CSS: `navigation.instant` rewrites every nav href to an
 * absolute URL when it hydrates, so an [href^="http"] selector matches internal
 * links too. Comparing the anchor's resolved hostname is unambiguous.
 *
 * Re-runs on each instant navigation via Material's document$ observable, with
 * a plain listener as the fallback when that isn't available.
 */
(function () {
  function tagExternalNavLinks() {
    var links = document.querySelectorAll('.md-nav--primary .md-nav__link[href]');
    Array.prototype.forEach.call(links, function (link) {
      var external = link.hostname && link.hostname !== window.location.hostname;
      link.classList.toggle('braid-external', !!external);
      if (external) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener');
      }
    });
  }

  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(tagExternalNavLinks);
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tagExternalNavLinks);
  } else {
    tagExternalNavLinks();
  }
})();
