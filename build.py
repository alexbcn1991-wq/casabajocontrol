from pathlib import Path
import json, html, shutil

ROOT=Path(__file__).resolve().parent
BASE="https://casabajocontrol.es"

def read(p): return p.read_text(encoding="utf-8")
def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding="utf-8")
def prefix(slug): return "../"*len([x for x in slug.split("/") if x])
def crumbs(slug):
    labels={"guias":"Guías","comparativas":"Comparativas","agua":"Agua","humedad":"Humedad","segunda-residencia":"Segunda residencia","como-probamos":"Cómo probamos","sobre-nosotros":"Sobre nosotros","contacto":"Contacto"}
    bits=[x for x in slug.strip("/").split("/") if x]
    out=['<a href="/">Inicio</a>']; acc=""
    for i,b in enumerate(bits):
        acc+="/"+b
        label=labels.get(b,b.replace("-"," ").title())
        if i==len(bits)-1: out.append(f'<span aria-current="page">{html.escape(label)}</span>')
        else: out.append(f'<a href="{acc}/">{html.escape(label)}</a>')
    return ' <span aria-hidden="true">/</span> '.join(out)
def build_page(slug,d):
    p=prefix(slug); canonical=BASE+"/"+slug.strip("/")+"/"
    tpl=read(ROOT/"templates"/(d[0]+".html"))
    header=read(ROOT/"partials/header.html").replace("{{ROOT}}",p)
    footer=read(ROOT/"partials/footer.html").replace("{{ROOT}}",p)
    bc=read(ROOT/"partials/breadcrumbs.html").replace("{{BREADCRUMBS}}",crumbs(slug))
    date_published = d[7] if len(d)>7 and d[7] else "11 de septiembre de 2026"
    date_modified = d[8] if len(d)>8 and d[8] else date_published
    schema=json.dumps({"@context":"https://schema.org","@type":"Article","headline":d[4],"description":d[2],"url":canonical,"datePublished":date_published,"dateModified":date_modified,"author":{"@type":"Organization","name":"Casa Bajo Control","url":BASE+"/sobre-nosotros/"},"publisher":{"@type":"Organization","name":"Casa Bajo Control","url":BASE+"/"},"image":[BASE+"/img/og-default.png"]},ensure_ascii=False,separators=(",",":"))
    vals={"{{TITLE}}":html.escape(d[1]),"{{DESCRIPTION}}":html.escape(d[2]),"{{CANONICAL}}":canonical,"{{JSONLD}}":schema,"{{HEADER}}":header,"{{FOOTER}}":footer,"{{BREADCRUMBS}}":bc,"{{EYEBROW}}":html.escape(d[3]),"{{H1}}":html.escape(d[4]),"{{LEAD}}":html.escape(d[5]),"{{META}}":f'<p class="article-meta">Actualizado: {d[8] if len(d)>8 and d[8] else (d[7] if len(d)>7 and d[7] else "11 de septiembre de 2026")}</p>',"{{BODY}}":d[6]}
    for a,b in vals.items(): tpl=tpl.replace(a,b)
    tpl=tpl.replace("{{ROOT}}",p)
    write(ROOT/slug/"index.html",tpl)

def redirect(slug,target):
    canonical=BASE+target
    s='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="'+canonical+'"><meta http-equiv="refresh" content="0;url='+canonical+'"><title>Redirigiendo | Casa Bajo Control</title></head><body><p>Esta página se ha movido a <a href="'+canonical+'">'+canonical+'</a>.</p><script>location.replace('+json.dumps(canonical)+');</script></body></html>'
    write(ROOT/slug/"index.html",s)

pages=json.loads(read(ROOT/"content/pages.json"))
for slug,d in pages.items():
    while len(d)<9: d.append(None)
    d[7]=d[7] or "11 de septiembre de 2026"
    d[8]=d[8] or d[7]
    build_page(slug,d)
redirect("proteger-segunda-residencia","/segunda-residencia/")
redirect("consejos","/guias/")
redirect("comparativas/mejores-higrometros","/comparativas/sensores-humedad/")
old=ROOT/"comparativas/seguridad/door-window"
if old.exists(): shutil.rmtree(old)

# Keep the first commercial URL structurally present, but explicitly unproven.
slug="comparativas/detectores-fugas-agua"; p=prefix(slug)
tpl=read(ROOT/"templates/plana.html")
vals={"{{TITLE}}":"Detectores de fugas de agua | Casa Bajo Control","{{DESCRIPTION}}":"Comparativa de detectores de fugas de agua basada en pruebas reales.","{{CANONICAL}}":BASE+"/comparativas/detectores-fugas-agua/","{{JSONLD}}":json.dumps({"@context":"https://schema.org","@type":"Article","headline":"Mejores detectores de fugas de agua","url":BASE+"/comparativas/detectores-fugas-agua/"}),"{{HEADER}}":read(ROOT/"partials/header.html").replace("{{ROOT}}",p),"{{FOOTER}}":read(ROOT/"partials/footer.html").replace("{{ROOT}}",p),"{{BREADCRUMBS}}":read(ROOT/"partials/breadcrumbs.html").replace("{{BREADCRUMBS}}",'<a href="/">Inicio</a> / <a href="/comparativas/">Comparativas</a> / <span aria-current="page">Detectores de fugas</span>'),"{{EYEBROW}}":"Agua","{{H1}}":"Mejores detectores de fugas de agua","{{LEAD}}":"Esta comparativa se publicará cuando existan resultados propios.","{{META}}":'<p class="article-meta">Pendiente de pruebas reales</p>','{{BODY}}':'<section class="article-content"><div class="callout"><strong>En preparación:</strong> no etiquetamos productos como probados hasta completar nuestro protocolo.</div><p><a class="button button-primary" href="/como-probamos/">Ver cómo probamos</a></p></section>'}
for a,b in vals.items(): tpl=tpl.replace(a,b)
tpl=tpl.replace("{{ROOT}}",p)
tpl=tpl.replace("<head>","<head><meta name=\"robots\" content=\"noindex,follow\">",1)
write(ROOT/slug/"index.html",tpl)

write(ROOT/"robots.txt",f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
excluded={"/comparativas/detectores-fugas-agua/","/legal/aviso-legal/","/legal/privacidad/","/legal/cookies/"}
urls={"/"}
for slug in pages:
    u="/"+slug.strip("/")+"/"
    if u not in excluded: urls.add(u)

xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sorted(urls): xml.append(f"  <url><loc>{BASE}{u}</loc></url>")
xml.append("</urlset>")
write(ROOT/"sitemap.xml","\n".join(xml)+"\n")
print("BUILD OK")
