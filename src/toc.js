(function () {
  if (!window.IntersectionObserver) return;
  var links = document.querySelectorAll('.toc a');
  var map = {};
  links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var a = map[e.target.id];
      if (!a) return;
      a.closest('ol').querySelectorAll('a').forEach(function (x) { x.classList.toggle('active', x === a); });
    });
  }, { rootMargin: '-30% 0px -60% 0px' });
  document.querySelectorAll('.policy section[id]').forEach(function (s) { io.observe(s); });
})();
