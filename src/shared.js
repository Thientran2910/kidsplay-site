(function () {
  var root = document.documentElement;
  var KEY_LANG = 'kidsplay-site.lang', KEY_MODE = 'kidsplay-site.mode';
  function save(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function setLang(lang) {
    root.setAttribute('data-lang', lang);
    root.lang = lang;
    var t = document.querySelector('title[data-en]');
    if (t) document.title = t.getAttribute('data-' + lang);
    document.querySelectorAll('[data-set-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-set-lang') === lang));
    });
  }
  function setMode(mode) {
    root.setAttribute('data-mode', mode);
    var btn = document.querySelector('[data-toggle-mode]');
    if (btn) {
      var en = mode === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';
      var vi = mode === 'dark' ? 'Chuyển sang giao diện sáng' : 'Chuyển sang giao diện tối';
      btn.setAttribute('aria-label', root.getAttribute('data-lang') === 'en' ? en : vi);
    }
  }

  document.querySelectorAll('[data-set-lang]').forEach(function (b) {
    b.addEventListener('click', function () {
      var l = b.getAttribute('data-set-lang');
      setLang(l); save(KEY_LANG, l);
      setMode(root.getAttribute('data-mode') || 'light');
    });
  });
  var modeBtn = document.querySelector('[data-toggle-mode]');
  if (modeBtn) modeBtn.addEventListener('click', function () {
    var m = root.getAttribute('data-mode') === 'dark' ? 'light' : 'dark';
    setMode(m); save(KEY_MODE, m);
  });

  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var el = document.getElementById(b.getAttribute('data-copy'));
      var done = function () { b.classList.add('done'); setTimeout(function () { b.classList.remove('done'); }, 1500); };
      var select = function () { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); };
      if (navigator.clipboard) navigator.clipboard.writeText(el.textContent).then(done, select); else select();
    });
  });

  setLang(root.getAttribute('data-lang') === 'en' ? 'en' : 'vi');
  setMode(root.getAttribute('data-mode') === 'dark' ? 'dark' : 'light');
})();
