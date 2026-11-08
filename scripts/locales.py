# -*- coding: utf-8 -*-
"""locales.py — fuente UNICA de idiomas de dmc.staytick.com (preparado 2026-11-08,
D-2026-11-08-DMC-IDIOMAS-AR-RU-PT-RANKING).

Genera desde la lista LOCALES:
  * el bloque hreflang de cada pagina publicada (<link rel="alternate" ...> + x-default)
  * el selector de idiomas del pie (y de la nav, si NAV_SELECTOR=True) en todas las paginas
  * sitemap.xml con hreflang reciproco
  * los ganchos (comentados) de verificacion de Bing y Yandex en el <head>

AÑADIR UN IDIOMA (p. ej. ar):
  1. Crear ar/index.html (copia de es/index.html traducida por el equipo del cmo; para RTL:
     <html lang="ar" dir="rtl"> — el CSS [dir="rtl"] de css/site.css ya esta listo).
  2. Cambiar live=False -> True en su fila de LOCALES.
  3. python scripts/locales.py   (reescribe hreflang, selectores y sitemap; idempotente)
  4. bash scripts/check-claims.sh  &&  verificacion en navegador (Regla de oro)
  5. Tras el deploy: bash scripts/indexnow.sh
Un idioma con live=False NO se enlaza ni se anuncia en ningun sitio (sin «coming soon»).
Uso: python scripts/locales.py [--check]   (--check: falla si algo no esta al dia, no escribe)
"""
import os, re, sys

LOCALES = [
    # code, path,   native name,  dir,   live
    ('en', '/',     'EN',  'ltr', True),
    ('es', '/es/',  'ES',  'ltr', True),
    ('fr', '/fr/',  'FR',  'ltr', True),
    ('it', '/it/',  'IT',  'ltr', True),
    ('ar', '/ar/',  'AR',  'rtl', False),
    ('ru', '/ru/',  'RU',  'ltr', False),
    ('pt', '/pt/',  'PT',  'ltr', False),
]
X_DEFAULT = 'en'
HOST = 'https://dmc.staytick.com'
NAV_SELECTOR = False   # True = pinta tambien el selector en la nav (cambio visible: requiere OK CEO / Regla #0)
EXTRA_PAGES = ['legal/index.html', 'privacy/index.html']   # solo selector, sin hreflang (noindex)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
live = [l for l in LOCALES if l[4]]
pending = [l[0] for l in LOCALES if not l[4]]

def page_file(path): return os.path.join(ROOT, path.strip('/'), 'index.html') if path != '/' else os.path.join(ROOT, 'index.html')

def hreflang_block():
    lines = [f'<link rel="alternate" hreflang="{c}" href="{HOST}{p}">' for c, p, *_ in live]
    xd = [p for c, p, *_ in live if c == X_DEFAULT][0]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{HOST}{xd}">')
    return '\n'.join(lines)

def langs_html(current):
    a = ''.join(f'<a href="{p}"{" aria-current=\"page\"" if c == current else ""}>{n}</a>' for c, p, n, _, _ in live)
    note = f'<!-- locales pendientes (no se muestran hasta live=True en scripts/locales.py): {" ".join(pending)} -->' if pending else ''
    return f'<div class="langs">{a}{note}</div>'

HOOKS = ('<!-- verificacion buscadores (ganchos; descomentar con el codigo real del panel):\n'
         '<meta name="msvalidate.01" content="PENDIENTE-BING">\n'
         '<meta name="yandex-verification" content="PENDIENTE-YANDEX">\n'
         '-->')

def sitemap():
    alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{c}" href="{HOST}{p}"/>' for c, p, *_ in live)
    xd = [p for c, p, *_ in live if c == X_DEFAULT][0]
    alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{HOST}{xd}"/>'
    urls = ''.join(f'  <url><loc>{HOST}{p}</loc>\n    {alts}</url>\n' for c, p, *_ in live)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!-- generado por scripts/locales.py: no editar a mano -->\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + urls + '</urlset>\n')

def process(fname, code, with_hreflang):
    s = open(fname, encoding='utf-8').read(); o = s
    if with_hreflang:
        block = hreflang_block()
        s, n = re.subn(r'(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+', block + '\n', s, count=1)
        if n != 1: sys.exit(f'{fname}: no encuentro el bloque hreflang')
        if 'msvalidate.01' not in s:
            s = re.sub(r'(<link rel="canonical" href="[^"]+">\n)', lambda m: m.group(1) + HOOKS + '\n', s, count=1)
    s, n = re.subn(r'<div class="langs">.*?</div>', langs_html(code), s, count=1, flags=re.S)
    if n != 1: sys.exit(f'{fname}: no encuentro <div class="langs">')
    if NAV_SELECTOR and 'class="langs nav-langs"' not in s:
        s = s.replace('<a class="btn btn-gold cta"', langs_html(code).replace('class="langs"', 'class="langs nav-langs"') + '\n    <a class="btn btn-gold cta"', 1)
    return o, s

def main():
    check = '--check' in sys.argv
    changed = []
    todo = [(page_file(p), c, True) for c, p, *_ in live] + [(os.path.join(ROOT, e), None, False) for e in EXTRA_PAGES]
    for f, c, h in todo:
        if not os.path.exists(f): sys.exit(f'falta {f} (¿live=True sin pagina?)')
        o, s = process(f, c, h)
        if o != s:
            changed.append(f)
            if not check:
                with open(f + '.tmp', 'w', encoding='utf-8', newline='\n') as fh: fh.write(s)
                os.replace(f + '.tmp', f)
    sm = os.path.join(ROOT, 'sitemap.xml'); new = sitemap()
    if not os.path.exists(sm) or open(sm, encoding='utf-8').read() != new:
        changed.append(sm)
        if not check:
            with open(sm + '.tmp', 'w', encoding='utf-8', newline='\n') as fh: fh.write(new)
            os.replace(sm + '.tmp', sm)
    print(('DESACTUALIZADO: ' if check else 'escritos: ') + ', '.join(os.path.relpath(x, ROOT) for x in changed) if changed else 'locales: todo al dia')
    if check and changed: sys.exit(1)

if __name__ == '__main__':
    main()
