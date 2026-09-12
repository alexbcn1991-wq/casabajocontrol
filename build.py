from pathlib import Path
import json, html, shutil, re, urllib.parse

ROOT=Path(__file__).resolve().parent
BASE="https://casabajocontrol.es"
PRODUCTS=json.loads((ROOT/"data/products.json").read_text(encoding="utf-8")) if (ROOT/"data/products.json").exists() else {"amazon_tag":"TU-TAG","products":[]}

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
def amazon_url(product, tag):
    if product.get("asin"):
        return f"https://www.amazon.es/dp/{product['asin']}?tag={urllib.parse.quote(tag)}"
    query=urllib.parse.quote_plus(product.get("query") or product["name"])
    return f"https://www.amazon.es/s?k={query}&tag={urllib.parse.quote(tag)}"

def render_affiliate_products(key):
    groups={
        "sin-internet":["seqrell-sq7024b","shelly-flood-gen4","switchbot-water-leak","tapo-t300","aqara-water-leak-t1"],
        "fugas":["shelly-flood-gen4","switchbot-water-leak","tapo-t300","aqara-water-leak-t1"]
    }
    featured={
        "sin-internet":"seqrell-sq7024b",
        "fugas":"switchbot-water-leak"
    }
    ids=groups.get(key,[])
    by_id={p["id"]:p for p in PRODUCTS.get("products",[])}
    featured_id=featured.get(key)
    cards=[]
    featured_card=""
    if featured_id and featured_id in by_id:
        p=by_id[featured_id]
        href=amazon_url(p, PRODUCTS.get("amazon_tag","TU-TAG"))
        featured_card=(
            '<article class="affiliate-product affiliate-product-featured">'
            '<div class="affiliate-featured-badge">Nuestra selección</div>'
            '<div class="affiliate-product-copy">'
            f'<p class="affiliate-product-type">{html.escape(p["type"])}</p>'
            f'<p class="affiliate-product-name"><strong>{html.escape(p["name"])}</strong></p>'
            f'<p class="affiliate-featured-lead">{html.escape(p["fit"])}</p>'
            f'<p class="affiliate-product-note">{html.escape(p["note"])}</p>'
            '<div class="affiliate-featured-points">'
            '<span>Encaja con este escenario</span><span>Analizado por Casa Bajo Control</span>'
            '</div></div>'
            f'<div class="affiliate-actions">'+(f'<a class="button button-secondary affiliate-review-link" href="{p["review"]}">Leer nuestro análisis →</a>' if p.get("review") else '')+f'<a class="button button-primary affiliate-button affiliate-button-featured" href="{html.escape(href, quote=True)}" rel="sponsored nofollow noopener" target="_blank">Ver en Amazon <span aria-hidden="true">↗</span></a></div>'
            '</article>'
        )
    for pid in ids:
        if pid == featured_id:
            continue
        p=by_id[pid]
        href=amazon_url(p, PRODUCTS.get("amazon_tag","TU-TAG"))
        cards.append(
            '<article class="affiliate-product">'
            f'<div class="affiliate-product-copy"><p class="affiliate-product-type">{html.escape(p["type"])}</p>'
            f'<p class="affiliate-product-name"><strong>{html.escape(p["name"])}</strong></p>'
            f'<p><strong>Por qué lo incluimos:</strong> {html.escape(p["fit"])}</p>'
            f'<p class="affiliate-product-note">{html.escape(p["note"])}</p></div>'
            '<div class="affiliate-actions">'+(f'<a class="button button-secondary affiliate-review-link" href="{p["review"]}">Leer nuestro análisis →</a>' if p.get("review") else '')+f'<a class="button button-primary affiliate-button" href="{html.escape(href, quote=True)}" rel="sponsored nofollow noopener" target="_blank">Ver en Amazon</a></div>'
            '</article>'
        )
    others=(''.join(cards))
    others_block=(
        '<div class="affiliate-others-heading"><span class="eyebrow">También contemplamos</span>'
        '<h3>Otras opciones a considerar</h3></div>' + others if cards else ''
    )
    return ('<section class="affiliate-products" aria-label="Selección de productos recomendados">'
            '<div class="affiliate-disclosure"><strong>Enlaces de afiliado:</strong> si compras a través de estos enlaces, Casa Bajo Control puede obtener una comisión, sin coste adicional para ti.</div>'
            '<div class="affiliate-selection-heading"><span class="eyebrow">Nuestra selección</span>'
            '<h2>Una opción que encaja especialmente bien</h2>'
            '<p>No la presentamos como “la mejor” en términos absolutos. La destacamos porque responde especialmente bien al escenario que estamos explicando en este artículo.</p></div>'
            + featured_card + others_block + '</section>')


def render_single_affiliate_product(product_id):
    by_id={p["id"]:p for p in PRODUCTS.get("products",[])}
    p=by_id.get(product_id)
    if not p: return ""
    href=amazon_url(p, PRODUCTS.get("amazon_tag","TU-TAG"))
    desc = p.get("single_description") or p.get("fit") or ""
    return ('<section class="affiliate-product-single" aria-label="Comprar '+html.escape(p["name"],quote=True)+'">'
      '<div class="affiliate-disclosure"><strong>Enlace de afiliado:</strong> si compras a través de este enlace, Casa Bajo Control puede obtener una comisión, sin coste adicional para ti.</div>'
      '<div class="affiliate-single-inner"><div class="affiliate-single-copy">'
      '<span class="affiliate-featured-badge">Analizado por Casa Bajo Control</span>'
      f'<p class="affiliate-product-type">{html.escape(p.get("type","Sensor de fugas"))}</p><p class="affiliate-product-name"><strong>{html.escape(p["name"])}</strong></p>'
      f'<p>{html.escape(desc)}</p>'
      f'<p class="affiliate-single-note">No lo presentamos como “el mejor” ni como un producto probado: este análisis se basa en la documentación publicada por el fabricante.</p>'
      '</div><a class="button button-primary affiliate-button affiliate-button-featured" href="'+html.escape(href,quote=True)+'" rel="sponsored nofollow noopener" target="_blank">Ver en Amazon <span aria-hidden="true">↗</span></a></div></section>')
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


NAV=[("","Inicio"),("comparativas/","Comparativas"),("guias/","Guías"),("segunda-residencia/","Segunda residencia"),("sobre-nosotros/","Sobre nosotros")]
def nav_html(root,slug):
    section=slug.strip("/").split("/")[0] if slug.strip("/") else ""
    out=[]
    for path,label in NAV:
        href=(root+path) if (root or path) else "./"
        key=path.strip("/")
        active=(key==section) if key else (section=="")
        attrs=' class="active" aria-current="page"' if active else ""
        out.append(f'<a{attrs} href="{href}">{label}</a>')
    return "".join(out)
def render_header(slug):
    root=prefix(slug)
    h=read(ROOT/"partials/header.html").replace("{{NAV}}",nav_html(root,slug))
    h=h.replace('href="{{ROOT}}"','href="'+(root or "./")+'"')
    return h.replace("{{ROOT}}",root)

def build_page(slug,d):
    p=prefix(slug); canonical=BASE+"/"+slug.strip("/")+"/"
    tpl=read(ROOT/"templates"/(d[0]+".html"))
    header=render_header(slug)
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
    tpl=tpl.replace("{{PRODUCTS:sin-internet}}", render_affiliate_products("sin-internet")).replace("{{PRODUCTS:fugas}}", render_affiliate_products("fugas")).replace("{{PRODUCT:shelly-flood-gen4}}", render_single_affiliate_product("shelly-flood-gen4")).replace("{{PRODUCT:aqara-water-leak-t1}}", render_single_affiliate_product("aqara-water-leak-t1"))
    tpl=tpl.replace("{{ROOT}}",p)
    write(ROOT/slug/"index.html",tpl)

def redirect(slug,target):
    canonical=BASE+target
    s='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="'+canonical+'"><meta http-equiv="refresh" content="0;url='+canonical+'"><title>Redirigiendo | Casa Bajo Control</title></head><body><p>Esta página se ha movido a <a href="'+canonical+'">'+canonical+'</a>.</p><script>location.replace('+json.dumps(canonical)+');</script></body></html>'
    write(ROOT/slug/"index.html",s)

# Home: se regenera desde la copia maestra sustituyendo solo la cabecera por la común.
def build_home():
    src=read(ROOT/"content/home/index.html")
    hdr=render_header("")
    hdr_only=hdr[hdr.index('<header class="site-header">'):hdr.index('</header>')+len('</header>')]
    out=re.sub(r'<header class="site-header">.*?</header>',lambda m: hdr_only,src,count=1,flags=re.S)
    write(ROOT/"index.html",out)
build_home()

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
    extra='<p>Mientras tanto, ya puedes leer nuestros primeros análisis individuales: <a href="/reviews/shelly-flood-gen4/">Shelly Flood Gen4</a> y <a href="/reviews/aqara-water-leak-sensor-t1/">Aqara Water Leak Sensor T1</a>.</p>' if slug=="comparativas/detectores-fugas-agua" else ''
    body='<section class="article-content"><div class="callout"><strong>En preparación:</strong> no etiquetamos productos como probados hasta completar nuestro protocolo.</div>'+extra+'<p><a class="button button-primary" href="/como-probamos/">Ver cómo probamos</a></p></section>'
    data=["plana",title,lead,eyebrow,h1,lead,body,"2026-09-11","2026-09-11",crumb,image,alt]
    canonical=BASE+"/"+slug+"/"
    vals={"{{TITLE}}":html.escape(title),"{{DESCRIPTION}}":html.escape(lead),"{{CANONICAL}}":canonical,
          "{{JSONLD}}":json.dumps({"@context":"https://schema.org","@type":"Article","headline":h1,"url":canonical,"image":[BASE+image]},ensure_ascii=False,separators=(",",":")),
          "{{HEADER}}":render_header(slug),"{{FOOTER}}":read(ROOT/"partials/footer.html").replace("{{ROOT}}",p),
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


# Hub y stubs de reviews: mantienen los enlaces internos sin presentar páginas pendientes como análisis publicados.
def review_stub(slug, name, profile):
    p=prefix(slug)
    tpl=read(ROOT/"templates/plana.html")
    canonical=BASE+"/"+slug.strip("/")+"/"
    body=('<section class="article-content"><div class="callout"><strong>En preparación.</strong> Este análisis todavía no está publicado. '
          'No etiquetamos un producto como probado hasta completar nuestro protocolo.</div>'
          '<p><a class="button button-primary" href="/comparativas/detectores-fugas-agua/">Ver la comparativa de detectores de fugas →</a></p></section>')
    bc=read(ROOT/"partials/breadcrumbs.html").replace("{{BREADCRUMBS}}",
        f'<a href="/">Inicio</a> <span aria-hidden="true">/</span> <a href="/reviews/">Análisis</a> <span aria-hidden="true">/</span> <span aria-current="page">{html.escape(name)}</span>')
    vals={"{{TITLE}}":html.escape(name+" | Casa Bajo Control"),"{{DESCRIPTION}}":html.escape("Análisis de producto en preparación en Casa Bajo Control."),
          "{{CANONICAL}}":canonical,"{{JSONLD}}":json.dumps({"@context":"https://schema.org","@type":"WebPage","name":name,"url":canonical},ensure_ascii=False,separators=(",",":")),
          "{{HEADER}}":render_header(slug),"{{FOOTER}}":read(ROOT/"partials/footer.html").replace("{{ROOT}}",p),
          "{{BREADCRUMBS}}":bc,"{{EYEBROW}}":"Análisis","{{H1}}":html.escape(name),"{{LEAD}}":html.escape(profile),
          "{{META}}":"","{{HERO_MEDIA}}":"","{{OG_IMAGE}}":BASE+"/img/og-default.png","{{BODY}}":body}
    for a,c in vals.items(): tpl=tpl.replace(a,c)
    tpl=tpl.replace("{{ROOT}}",p).replace("<head>","<head><meta name=\"robots\" content=\"noindex,follow\">",1)
    write(ROOT/slug/"index.html",tpl)

def reviews_hub():
    slug="reviews"; p=prefix(slug); tpl=read(ROOT/"templates/plana.html")
    canonical=BASE+"/reviews/"
    cards=[
      ("Shelly Flood Gen4","/reviews/shelly-flood-gen4/","Análisis documental publicado."),
      ("Aqara Water Leak Sensor T1","/reviews/aqara-water-leak-sensor-t1/","Análisis documental publicado."),
      ("SwitchBot Water Leak Detector","/reviews/switchbot-water-leak-detector/","Análisis en preparación."),
      ("TP-Link Tapo T300","/reviews/tapo-t300/","Análisis en preparación."),
      ("seQrell SQ7024B","/reviews/seqrell-sq7024b/","Análisis en preparación.")
    ]
    cards_html=''.join(f'<article class="article-card"><h3><a href="{u}">{html.escape(n)}</a></h3><p>{html.escape(d)}</p></article>' for n,u,d in cards)
    body='<section class="article-content"><p>Analizamos sensores y soluciones para detectar problemas domésticos, siempre distinguiendo entre documentación y pruebas propias.</p><div class="article-grid">'+cards_html+'</div></section>'
    bc='<a href="/">Inicio</a> <span aria-hidden="true">/</span> <span aria-current="page">Análisis</span>'
    vals={"{{TITLE}}":"Análisis de productos | Casa Bajo Control","{{DESCRIPTION}}":"Análisis documentales y pruebas de sensores y soluciones para proteger una vivienda.",
          "{{CANONICAL}}":canonical,"{{JSONLD}}":json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":"Análisis de productos","url":canonical},ensure_ascii=False,separators=(",",":")),
          "{{HEADER}}":render_header(slug),"{{FOOTER}}":read(ROOT/"partials/footer.html").replace("{{ROOT}}",p),
          "{{BREADCRUMBS}}":bc,"{{EYEBROW}}":"Análisis","{{H1}}":"Análisis de productos","{{LEAD}}":"Estudios documentales y pruebas propias de sensores y soluciones para proteger una vivienda.",
          "{{META}}":"","{{HERO_MEDIA}}":"","{{OG_IMAGE}}":BASE+"/img/og-default.png","{{BODY}}":body}
    for a,c in vals.items(): tpl=tpl.replace(a,c)
    tpl=tpl.replace("{{ROOT}}",p)
    write(ROOT/"reviews/index.html",tpl)

reviews_hub()
review_stub("reviews/switchbot-water-leak-detector","SwitchBot Water Leak Detector","Análisis documental de un detector de fugas con conexión Wi-Fi.")
review_stub("reviews/tapo-t300","TP-Link Tapo T300","Análisis documental de un sensor de fugas del ecosistema Tapo.")
review_stub("reviews/seqrell-sq7024b","seQrell SQ7024B","Análisis documental de una solución con comunicación móvil.")
# Páginas planas fuera de pages.json (legales en borrador y 404): misma cabecera común, noindex, fuera del sitemap.
def plain_page(slug,title,eyebrow,h1,lead,body,noindex=True,out_path=None,crumb=None):
    p=prefix(slug) if slug else ""
    tpl=read(ROOT/"templates/plana.html")
    canonical=BASE+("/"+slug.strip("/")+"/" if slug else "/")
    bc='<a href="/">Inicio</a> <span aria-hidden="true">/</span> <span aria-current="page">'+html.escape(crumb or h1)+'</span>'
    vals={"{{TITLE}}":html.escape(title),"{{DESCRIPTION}}":html.escape(lead),"{{CANONICAL}}":canonical,
          "{{JSONLD}}":json.dumps({"@context":"https://schema.org","@type":"WebPage","name":h1,"url":canonical},ensure_ascii=False,separators=(",",":")),
          "{{HEADER}}":render_header(slug),"{{FOOTER}}":read(ROOT/"partials/footer.html").replace("{{ROOT}}",p),
          "{{BREADCRUMBS}}":read(ROOT/"partials/breadcrumbs.html").replace("{{BREADCRUMBS}}",bc),
          "{{EYEBROW}}":eyebrow,"{{H1}}":html.escape(h1),"{{LEAD}}":html.escape(lead),"{{META}}":"","{{HERO_MEDIA}}":"","{{OG_IMAGE}}":BASE+"/img/og-default.png","{{BODY}}":body}
    for a,c in vals.items(): tpl=tpl.replace(a,c)
    tpl=tpl.replace("{{ROOT}}",p)
    if noindex: tpl=tpl.replace("<head>","<head><meta name=\"robots\" content=\"noindex,follow\">",1)
    write(out_path or (ROOT/slug/"index.html"),tpl)

legal_body='<section class="article-content"><div class="callout"><strong>NO PUBLICAR TODAVÍA.</strong> Esta página queda preparada para incorporar el texto legal definitivo.</div></section>'
plain_page("legal/aviso-legal","Aviso legal | Casa Bajo Control","Legal","Aviso legal","Borrador estructural. Completar con los datos reales antes del lanzamiento.",legal_body)
plain_page("legal/privacidad","Política de privacidad | Casa Bajo Control","Legal","Política de privacidad","Borrador estructural. Completar con los datos reales antes del lanzamiento.",legal_body)
plain_page("legal/cookies","Política de cookies | Casa Bajo Control","Legal","Política de cookies","Borrador estructural. Completar con los datos reales antes del lanzamiento.",legal_body)
# 404: GitHub Pages sirve /404.html desde cualquier ruta, por eso sus recursos deben ser absolutos.
plain_page("","Página no encontrada | Casa Bajo Control","404","Esta página no existe.","Puede que el enlace haya cambiado.",'<section class="article-content"><p><a class="button button-primary" href="/">Volver al inicio</a></p></section>',out_path=ROOT/"404.html",crumb="Página no encontrada")
s404=read(ROOT/"404.html").replace('href="./"','href="/"').replace('href="css/','href="/css/').replace('src="img/','src="/img/').replace('src="js/','src="/js/').replace('href="img/','href="/img/')
for path,_ in NAV: s404=s404.replace(f'href="{path}"',f'href="/{path}"')
s404=s404.replace('href="legal/','href="/legal/').replace('href="comparativas/"','href="/comparativas/"').replace('href="guias/"','href="/guias/"').replace('href="segunda-residencia/"','href="/segunda-residencia/"').replace('href="como-probamos/"','href="/como-probamos/"').replace('href="sobre-nosotros/"','href="/sobre-nosotros/"').replace('href="contacto/"','href="/contacto/"')
write(ROOT/"404.html",s404)

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
