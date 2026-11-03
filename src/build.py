import base64, os, re

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SRC, '..')
OUT = os.path.join(ROOT, 'build')
rd = lambda n: open(os.path.join(SRC, n), encoding='utf-8').read()

ICON = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(SRC, 'icon128.png'), 'rb').read()).decode()


def svg(body):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>')


ICONS = {
    'I_CHAT': svg('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/><path d="M8.5 12h.01M12 12h.01M15.5 12h.01"/>'),
    'I_SHIELD': svg('<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6L12 3Z"/><path d="m9 12 2 2 4-4"/>'),
    'I_CLOCK': svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    'I_USER': svg('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
    'I_SPARK': svg('<path d="M12 3c.6 4.2 2.8 6.4 7 7-4.2.6-6.4 2.8-7 7-.6-4.2-2.8-6.4-7-7 4.2-.6 6.4-2.8 7-7Z"/><path d="M19 17.5c.2 1.3.9 2 2 2.2-1.1.2-1.8.9-2 2.2-.2-1.3-.9-2-2-2.2 1.1-.2 1.8-.9 2-2.2Z"/>'),
}
SUN = svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>').replace('<svg', '<svg class="i-sun"')
MOON = svg('<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/>').replace('<svg', '<svg class="i-moon"')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700'
         '&family=Baloo+2:wght@600;700;800&display=swap">')

# Language: ?lang=vi|en in the URL wins (and is remembered), then the saved choice, then Vietnamese.
# Theme: saved choice, then the system preference, then light.
BOOT = ("<script>(function(){var d=document.documentElement,s=null;try{s=window.localStorage}catch(e){}"
        "function g(k){try{return s&&s.getItem(k)}catch(e){return null}}"
        "function p(k,v){try{s&&s.setItem(k,v)}catch(e){}}"
        "var q=null;try{q=new URLSearchParams(location.search).get('lang')}catch(e){}"
        "var l=(q==='vi'||q==='en')?q:g('kidsplay-site.lang');if(q==='vi'||q==='en')p('kidsplay-site.lang',q);"
        "var m=g('kidsplay-site.mode');"
        "if(m!=='dark'&&m!=='light'){m=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light'}"
        "l=l==='en'?'en':'vi';d.setAttribute('data-lang',l);d.setAttribute('data-mode',m);d.lang=l;})();</script>")

SUPPORT_EMAIL = 'support@koka.vn'
UPDATED = {'vi': 'Cập nhật 01/11/2026', 'en': 'Updated 01/11/2026'}

NAV = [('home', 'HOME', 'Home', 'Trang chủ'), ('support', 'SUPPORT', 'Support', 'Hỗ trợ'),
       ('privacy', 'PRIVACY', 'Privacy', 'Quyền riêng tư'), ('terms', 'TERMS', 'Terms', 'Điều khoản')]


def header(cur):
    links = '\n'.join(
        '    <a href="{{' + k + '}}"' + (' aria-current="page"' if cur == p else '')
        + f'><span class="en">{en}</span><span class="vi">{vi}</span></a>'
        for p, k, en, vi in NAV)
    return f'''<a class="skip" href="#main"><span class="en">Skip to content</span><span class="vi">Chuyển tới nội dung</span></a>
<header class="site-header"><div class="wrap">
  <a class="brand" href="{{{{HOME}}}}"><img src="{ICON}" alt="" width="34" height="34"><span>KidsPlay</span></a>
  <nav class="nav" aria-label="Pages">
{links}
  </nav>
  <div class="controls">
    <div class="seg" role="group" aria-label="Ngôn ngữ / Language">
      <button type="button" id="lang-vi" data-set-lang="vi" aria-pressed="true">VI</button>
      <button type="button" id="lang-en" data-set-lang="en" aria-pressed="false">EN</button>
    </div>
    <button type="button" id="mode-toggle" class="icon-btn" data-toggle-mode aria-label="Chuyển giao diện">{SUN}{MOON}</button>
  </div>
</div>
<nav class="wrap tabs-m" aria-label="Pages">
{links}
</nav>
</header>'''


FOOTER = '''<footer class="site-footer"><div class="wrap">
  <div class="foot-row">
    <a class="brand" href="{{HOME}}"><img src="''' + ICON + '''" alt="" width="34" height="34"><span>KidsPlay</span></a>
    <div class="foot-links">
      <a href="{{SUPPORT}}"><span class="en">Support</span><span class="vi">Hỗ trợ</span></a>
      <a href="{{PRIVACY}}"><span class="en">Privacy Policy</span><span class="vi">Chính sách quyền riêng tư</span></a>
      <a href="{{TERMS}}"><span class="en">Terms of Use</span><span class="vi">Điều khoản sử dụng</span></a>
      <a href="mailto:{{EMAIL}}"><span class="en">Contact</span><span class="vi">Liên hệ</span></a>
    </div>
  </div>
  <p class="foot-note"><span class="en">KidsPlay: no ads, no tracking, and information about your child stays on your device.</span><span class="vi">KidsPlay: không quảng cáo, không theo dõi, thông tin về Bé nằm trên máy của bạn.</span></p>
  <p class="copyright"><span class="en">© 2026 the KidsPlay team</span><span class="vi">© 2026 Nhóm phát triển KidsPlay</span></p>
</div></footer>'''

PAGES = {
    'home': dict(out='index.html', body='home.body.html', js=[],
                 t_en='KidsPlay', t_vi='KidsPlay',
                 desc='KidsPlay: a games app for children aged 2-8. Each game practises one skill and adjusts its level to each child. / Trò chơi cho trẻ 2-8 tuổi, mỗi Trò chơi luyện một Kỹ năng.'),
    'support': dict(out='support.html', body='support.body.html', js=[],
                    t_en='KidsPlay Support', t_vi='Hỗ trợ KidsPlay',
                    desc='Help, FAQ and contact for KidsPlay. / Hỗ trợ, câu hỏi thường gặp và liên hệ KidsPlay.'),
    'privacy': dict(out='privacy.html', body=None, js=['toc.js'],
                    t_en='KidsPlay Privacy Policy', t_vi='KidsPlay - Chính sách quyền riêng tư',
                    desc='How the KidsPlay app handles your data. / Cách app KidsPlay xử lý dữ liệu.'),
    'terms': dict(out='terms.html', body=None, js=['toc.js'],
                  t_en='KidsPlay Terms of Use', t_vi='KidsPlay - Điều khoản sử dụng',
                  desc='Terms of Use for the KidsPlay app. / Điều khoản sử dụng app KidsPlay.'),
    '404': dict(out='404.html', body='404.body.html', js=[],
                t_en='Page not found - KidsPlay', t_vi='Không tìm thấy trang - KidsPlay',
                desc='This page does not exist.'),
}

LEGAL_TITLE = {
    'privacy': {'en': 'Privacy Policy', 'vi': 'Chính sách quyền riêng tư'},
    'terms': {'en': 'Terms of Use', 'vi': 'Điều khoản sử dụng'},
}
TOC_TITLE = {'en': 'Contents', 'vi': 'Mục lục'}


def legal_article(key, lang):
    """Turn the copied source (content/<key>.<lang>.html) into intro + numbered sections. Text is kept verbatim."""
    src = rd(f'content/{key}.{lang}.html').strip()
    src = src.replace('href="/en/privacy"', 'href="privacy.html"').replace('href="/privacy"', 'href="privacy.html"')
    parts = re.split(r'<h2>(.*?)</h2>', src, flags=re.S)
    intro, secs = parts[0].strip(), list(zip(parts[1::2], parts[2::2]))
    toc, out = [], []
    for i, (title, html) in enumerate(secs, 1):
        title = re.sub(r'^\d+\.\s*', '', title.strip())
        n = f'{i:02d}'
        toc.append(f'        <li><a href="#{lang}-{i}"><span>{n}</span><span>{title}</span></a></li>')
        out.append(f'      <section id="{lang}-{i}">\n        <h2><span class="n">{n}</span>{title}</h2>\n{html.strip()}\n      </section>')
    return intro, '\n'.join(toc), '\n\n'.join(out)


def legal_body(key):
    head = ''
    for lang in ('vi', 'en'):
        intro, _, _ = legal_article(key, lang)
        head += (f'    <p class="lead {lang}">{re.sub(r"^<p>|</p>$", "", intro)}</p>\n')
    body = f'''<main id="main">
<section class="p-hero">
  <div class="wrap">
    <span class="eyebrow"><span class="en">Legal</span><span class="vi">Pháp lý</span></span>
    <h1><span class="en">{LEGAL_TITLE[key]['en']}</span><span class="vi">{LEGAL_TITLE[key]['vi']}</span></h1>
    <span class="updated">{{{{I_CLOCK}}}}<span class="en">{UPDATED['en']}</span><span class="vi">{UPDATED['vi']}</span></span>
{head}  </div>
</section>

<div class="p-body">'''
    for lang in ('vi', 'en'):
        _, toc, secs = legal_article(key, lang)
        body += f'''
  <div class="wrap {lang}">
    <nav class="toc" aria-label="{TOC_TITLE[lang]}">
      <div class="toc-title">{TOC_TITLE[lang]}</div>
      <ol>
{toc}
      </ol>
    </nav>
    <article class="policy">
{secs}
    </article>
  </div>
'''
    return body + '</div>\n</main>'


def render(key, links, full):
    p = PAGES[key]
    head = (f'<title data-en="{p["t_en"]}" data-vi="{p["t_vi"]}">{p["t_vi"]}</title>\n'
            f'<meta name="description" content="{p["desc"]}">\n'
            '<meta name="theme-color" content="#fff8ec">\n'
            f'<link rel="icon" href="{ICON}">\n'
            + FONTS + '\n' + BOOT + '\n<style>\n' + rd('shared.css') + '\n' + rd('page.css') + '\n</style>\n')
    main = legal_body(key) if p['body'] is None else rd(p['body'])
    body = (header(key) + '\n' + main + '\n' + FOOTER + '\n<script>\n' + rd('shared.js') + '\n'
            + ''.join(rd(j) for j in p['js']) + '</script>\n')
    for k, v in {**ICONS, 'EMAIL': SUPPORT_EMAIL, 'ICON': ICON, **links}.items():
        body = body.replace('{{' + k + '}}', v)
    assert '{{' not in body, key
    if not full:
        return head + body
    return ('<!doctype html>\n<html lang="vi" data-lang="vi" data-mode="light">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + body + '</body>\n</html>\n')


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(s)


def links(base, home):
    return {'HOME': home, 'SUPPORT': base + 'support.html', 'PRIVACY': base + 'privacy.html',
            'TERMS': base + 'terms.html', 'BASE': base}


# GitHub Pages site at the repo root. 404.html is served from any path, so it links absolutely.
for key, p in PAGES.items():
    l = links('/kidsplay-site/', '/kidsplay-site/') if key == '404' else links('', './')
    write(os.path.join(ROOT, p['out']), render(key, l, True))
# Artifact preview (build/, not committed).
art = links('', 'index.html')
write(os.path.join(OUT, 'artifact', 'home.html'), render('home', art, False))
for key in ('support', 'privacy', 'terms'):
    write(os.path.join(OUT, 'artifact', PAGES[key]['out']), render(key, art, True))
print('ok')
