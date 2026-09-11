from pathlib import Path
import json, html, shutil

ROOT=Path(__file__).resolve().parent
BASE="https://casabajocontrol.es"

def read(p): return p.read_text(encoding="utf-8")
def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding="utf-8")
def prefix(slug): return "../"*len([x for x in slug.split("/") if x])
def crumbs(slug,d=None):
    labels={"guias":"Guías","comparativas":"Comparativas","agua":"Agua","humedad":"Humedad","segunda-residencia":"Segunda residencia","como-probamos":"Cómo probamos","sobre-nosotros":"Sobre nosotros","contacto":"Contacto"}
    bits=[x for x in slug.strip("/").split("/") if x]
    out=['<a href="/">Inicio</a>']; acc=""
    for i,b in enumerate(bits):
        acc+="/"+b
        label=(d[9] if d is not None and i==len(bits)-1 and len(d)>9 and d[9] else labels.get(b,b.replace("-"," ").title()))
        if i==len(bits)-1: out.append(f'<span aria-current="page">{html.escape(label)}</span>')
        else: out.append(f'<a href="{acc}/">{html.escape(label)}</a>')
    return ' <span aria-hidden="true">/</span> '.join(out)
def format_date(iso):
    months=["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    try:
        y,m,day=iso.split("-")
        return f"{int(day)} de {months[int(m)-1]} de {y}"
    except Exception:
        return iso

def hero_media(d):
    image = d[10] if len(d)>10 and d[10] else None
    alt = d[11] if len(d)>11 and d[11] else None
    if not image:
        return ""
    if not alt:
        raise ValueError("Falta hero_alt para una página con hero_image")
    image_path = ROOT / image.lstrip("/")
    if not image_path.exists():
        raise FileNotFoundError(f"Hero no encontrado: {image}")
    stem = image_path.stem
    try:
        from PIL import Image
        with Image.open(image_path) as im:
            width, height = im.size
    except Exception:
        width, height = (1200, 675)
    return (f'<div class="standard-page-hero-media hero-media-{html.escape(stem)}">'
            f'<img src="{html.escape(image)}" alt="{html.escape(alt)}" width="{width}" height="{height}" '
            f'fetchpriority="high" decoding="async"></div>')

def build_page(slug,d):
    p=prefix(slug); canonical=BASE+"/"+slug.strip("/")+"/"
    tpl=read(ROOT/"templates"/(d[0]+".html"))
    header=read(ROOT/"partials/header.html").replace("{{ROOT}}",p)
    footer=read(ROOT/"partials/footer.html").replace("{{ROOT}}",p)
    bc=read(ROOT/"partials/breadcrumbs.html").replace("{{BREADCRUMBS}}",crumbs(slug,d))
    date_published = d[7] if len(d)>7 and d[7] else "2026-09-11"
    date_modified = d[8] if len(d)>8 and d[8] else date_published
    image = d[10] if len(d)>10 and d[10] else "/img/og-default.png"
    og_image = image
    if image.endswith(".webp") and (ROOT / (image[:-5] + ".png").lstrip("/")).exists():
        og_image = image[:-5] + ".png"
    schema=json.dumps({"@context":"https://schema.org","@type":"Article","headline":d[4],"description":d[2],"url":canonical,"datePublished":date_published,"dateModified":date_modified,"author":{"@type":"Organization","name":"Casa Bajo Control","url":BASE+"/sobre-nosotros/"},"publisher":{"@type":"Organization","name":"Casa Bajo Control","url":BASE+"/"},"image":[BASE+image]},ensure_ascii=False,separators=(",",":"))
    vals={"{{TITLE}}":html.escape(d[1]),"{{DESCRIPTION}}":html.escape(d[2]),"{{CANONICAL}}":canonical,"{{JSONLD}}":schema,"{{HEADER}}":header,"{{FOOTER}}":footer,"{{BREADCRUMBS}}":bc,"{{EYEBROW}}":html.escape(d[3]),"{{H1}}":html.escape(d[4]),"{{LEAD}}":html.escape(d[5]),"{{META}}":f'<p class="article-meta">Actualizado: {format_date(date_modified)}</p>',"{{HERO_MEDIA}}":hero_media(d),"{{OG_IMAGE}}":BASE+og_image,"{{BODY}}":d[6]}
    for a,b in vals.items(): tpl=tpl.replace(a,b)
    tpl=tpl.replace("{{ROOT}}",p)
    write(ROOT/slug/"index.html",tpl)

def redirect(slug,target):
    canonical=BASE+target
    s='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="'+canonical+'"><meta http-equiv="refresh" content="0;url='+canonical+'"><title>Redirigiendo | Casa Bajo Control</title></head><body><p>Esta página se ha movido a <a href="'+canonical+'">'+canonical+'</a>.</p><script>location.replace('+json.dumps(canonical)+');</script></body></html>'
    write(ROOT/slug/"index.html",s)

pages=json.loads(read(ROOT/"content/pages.json"))
for slug,d in pages.items():
    while len(d)<11: d.append(None)
    d[7]=d[7] or "2026-09-11"
    d[8]=d[8] or d[7]
    build_page(slug,d)
redirect("proteger-segunda-residencia","/segunda-residencia/")
redirect("consejos","/guias/")
redirect("comparativas/mejores-higrometros","/comparativas/sensores-humedad/")
old=ROOT/"comparativas/seguridad/door-window"
if old.exists(): shutil.rmtree(old)

# Stubs de comparativas: URL presente, noindex, sin etiquetar nada como probado.
def stub(slug,title,eyebrow,h1,lead,crumb,image,alt,parent_label="Comparativas",parent="/comparativas/"):
    p=prefix(slug); tpl=read(ROOT/"templates/plana.html")
    body='<section class="article-content"><div class="callout"><strong>En preparación:</strong> no etiquetamos productos como probados hasta completar nuestro protocolo.</div><p><a class="button button-primary" href="/como-probamos/">Ver cómo probamos</a></p></section>'
    data=["plana",title,lead,eyebrow,h1,lead,body,"2026-09-11","2026-09-11",crumb,image,alt]
    canonical=BASE+"/"+slug+"/"
    vals={"{{TITLE}}":html.escape(title),"{{DESCRIPTION}}":html.escape(lead),"{{CANONICAL}}":canonical,
          "{{JSONLD}}":json.dumps({"@context":"https://schema.org","@type":"Article","headline":h1,"url":canonical,"image":[BASE+image]},ensure_ascii=False,separators=(",",":")),
          "{{HEADER}}":read(ROOT/"partials/header.html").replace("{{ROOT}}",p),"{{FOOTER}}":read(ROOT/"partials/footer.html").replace("{{ROOT}}",p),
          "{{BREADCRUMBS}}":read(ROOT/"partials/breadcrumbs.html").replace("{{BREADCRUMBS}}",f'<a href="/">Inicio</a> <span aria-hidden="true">/</span> <a href="{parent}">{parent_label}</a> <span aria-hidden="true">/</span> <span aria-current="page">{html.escape(crumb)}</span>'),
          "{{EYEBROW}}":eyebrow,"{{H1}}":html.escape(h1),"{{LEAD}}":html.escape(lead),"{{META}}":'<p class="article-meta">Pendiente de pruebas reales</p>',
          "{{HERO_MEDIA}}":hero_media(data),"{{OG_IMAGE}}":BASE+(image[:-5]+".png" if image.endswith(".webp") and (ROOT/(image[:-5]+".png").lstrip("/")).exists() else image),"{{BODY}}":body}
    for a,c in vals.items(): tpl=tpl.replace(a,c)
    tpl=tpl.replace("{{ROOT}}",p).replace("<head>","<head><meta name=\"robots\" content=\"noindex,follow\">",1)
    write(ROOT/slug/"index.html",tpl)

stub("comparativas/detectores-fugas-agua","Detectores de fugas de agua | Casa Bajo Control","Agua","Mejores detectores de fugas de agua","Esta comparativa se publicará cuando existan resultados propios.","Detectores de fugas","/img/hero-comparativas.webp","Varios detectores de fugas de agua de distintas marcas sobre una mesa")
stub("comparativas/sensores-humedad","Sensores de humedad | Casa Bajo Control","Humedad","Mejores sensores de humedad","Esta comparativa se publicará cuando existan resultados propios.","Sensores de humedad","/img/hero-reference.webp","Sensor de humedad en una vivienda")
stub("comparativas/sensores-temperatura","Sensores de temperatura | Casa Bajo Control","Temperatura","Mejores sensores de temperatura","Esta comparativa se publicará cuando existan resultados propios.","Sensores de temperatura","/img/hero-reference.webp","Sensor de temperatura y humedad en una vivienda")
stub("comparativas/camaras-segunda-residencia","Cámaras para segunda residencia | Casa Bajo Control","Seguridad","Mejores cámaras para segunda residencia","Esta comparativa se publicará cuando existan resultados propios.","Cámaras","/img/hero-segunda-residencia.webp","Terraza de una segunda residencia con un móvil mostrando el estado de la casa")
stub("comparativas/sensores-puertas-ventanas","Sensores de puertas y ventanas | Casa Bajo Control","Seguridad","Mejores sensores de puertas y ventanas","Esta comparativa se publicará cuando existan resultados propios.","Puertas y ventanas","/img/hero-comparativas.webp","Varios sensores domésticos sobre una mesa, listos para comparar")

write(ROOT/"robots.txt",f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
excluded={"/comparativas/detectores-fugas-agua/","/comparativas/sensores-humedad/","/comparativas/sensores-temperatura/","/comparativas/camaras-segunda-residencia/","/comparativas/sensores-puertas-ventanas/","/legal/aviso-legal/","/legal/privacidad/","/legal/cookies/"}
urls={"/"}
for slug in pages:
    u="/"+slug.strip("/")+"/"
    if u not in excluded: urls.add(u)

xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sorted(urls): xml.append(f"  <url><loc>{BASE}{u}</loc></url>")
xml.append("</urlset>")
write(ROOT/"sitemap.xml","\n".join(xml)+"\n")
print("BUILD OK")
