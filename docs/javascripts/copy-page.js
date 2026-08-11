/* "Copy page" — puts the page's raw Markdown on the clipboard, so a page can be
 * pasted into an editor or an agent prompt without hand-stripping the chrome.
 *
 * The source is embedded at build time by overrides/main.html; nothing is
 * fetched. Listening on the document rather than the button means the handler
 * survives Material's instant navigation, which swaps the content in place.
 */
(function () {
  var RESET_MS = 2000;

  function label(button, text) {
    var span = button.querySelector('[data-braid-copy-label]');
    if (span) span.textContent = text;
  }

  function source(button) {
    var holder = button.parentNode.querySelector('[data-braid-page-markdown]');
    if (!holder) return null;
    try {
      return JSON.parse(holder.textContent);
    } catch (err) {
      return null;
    }
  }

  function flash(button, text, copied) {
    if (copied) button.classList.add('is-copied');
    label(button, text);
    setTimeout(function () {
      button.classList.remove('is-copied');
      label(button, 'Copy page');
    }, RESET_MS);
  }

  /* execCommand is deprecated but still the only path when the async clipboard
   * is unavailable — an insecure origin, or a denied permission. */
  function legacyCopy(text) {
    var area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.cssText = 'position:fixed;top:0;left:-9999px;opacity:0';
    document.body.appendChild(area);
    area.select();
    var ok = false;
    try {
      ok = document.execCommand('copy');
    } catch (err) {
      ok = false;
    }
    document.body.removeChild(area);
    return ok;
  }

  document.addEventListener('click', function (event) {
    var button = event.target.closest('[data-braid-copy]');
    if (!button) return;

    var markdown = source(button);
    if (markdown === null) {
      flash(button, 'Unavailable', false);
      return;
    }

    function fallback() {
      if (legacyCopy(markdown)) flash(button, 'Copied', true);
      else flash(button, 'Copy failed', false);
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(markdown).then(function () {
        flash(button, 'Copied', true);
      }, fallback);
    } else {
      fallback();
    }
  });
})();
