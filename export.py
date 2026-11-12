#!/usr/bin/env python3
"""Exports dist/ as single-file HTML pages (CSS and JS inlined).
html/open-on-computer : double-click index.html, every link works offline between the files.
html/paste-into-wordpress : one fragment per page for an Elementor HTML widget (Canvas template); links use the live site paths."""
import re, os, shutil
D='dist'; OUT='html'
css=open(f'{D}/assets/site.css',encoding='utf-8').read()
js={n:open(f'{D}/assets/{n}',encoding='utf-8').read() for n in ('site.js','planner.js')}
pages={'':'index'}
for d in sorted(os.listdir(D)):
    if os.path.isfile(f'{D}/{d}/index.html'): pages[d]=d
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(f'{OUT}/open-on-computer'); os.makedirs(f'{OUT}/paste-into-wordpress')
def inline(s):
    s=s.replace('<link rel="stylesheet" href="/assets/site.css">','<style>'+css+'</style>')
    return re.sub(r'<script src="/assets/([a-z.]+)" defer></script>',lambda m:'<script>'+js[m.group(1)]+'</script>',s)
def local(m):
    path,frag=m.group(1),m.group(2) or ''
    slug=path.strip('/')
    return 'href="%s.html%s"'%(pages[slug],frag) if slug in pages else m.group(0)
for slug,name in pages.items():
    src=open(os.path.join(D,slug,'index.html'),encoding='utf-8').read()
    full=inline(src)
    open(f'{OUT}/open-on-computer/{name}.html','w',encoding='utf-8').write(re.sub(r'href="(/[a-z0-9\-/]*)(#[a-z\-]+)?"',local,full))
    fonts=re.search(r'<link rel="stylesheet" href="https://fonts[^>]+>',src).group(0)
    ld=re.search(r'<script type="application/ld\+json">.*?</script>',src,re.S).group(0)
    battr,body=re.search(r'<body ?([^>]*)>(.*)</body>',full,re.S).groups()
    frag=(f'<!-- Demoski Digital: {name}. Paste into an Elementor HTML widget on a page using the "Elementor Canvas" template. -->\n'
          f'{fonts}\n<style>{css}\n#demoski-root{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55;padding-bottom:88px}}</style>\n{ld}\n'
          f'<div id="demoski-root" {battr}>{body}</div>\n')
    open(f'{OUT}/paste-into-wordpress/{name}.html','w',encoding='utf-8').write(frag)
print('exported',len(pages),'pages')
