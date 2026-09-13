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
    labels={"guias":"Guías","comparativas":"Comparativas","agua":"Agua","humedad":"Humedad","segunda-residencia":"Segunda residencia","como-probamos":"Cómo probamos","sobre-nosotros":"Sobre nosotros","contacto":"Contacto","reviews":"Análisis"}
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


def render_comparison_products():
    ids=["aqara-water-leak-t1","shelly-flood-gen4","switchbot-water-leak","tapo-t300","seqrell-sq7024b"]
    by_id={p["id"]:p for p in PRODUCTS.get("products",[])}
    summaries={
        "aqara-water-leak-t1":("Zigbee + hub","Si ya utilizas Aqara o quieres una instalación basada en Zigbee.","Necesita hub Aqara y no es una solución móvil independiente."),
        "shelly-flood-gen4":("Wi‑Fi / local-híbrido","Si priorizas acciones locales y flexibilidad de integración.","No necesita hub Shelly en modo Wi‑Fi, pero el aviso remoto depende de la conectividad disponible."),
        "switchbot-water-leak":("Wi‑Fi directo","Si quieres una instalación sencilla sin añadir un hub para la función básica.","La comunicación remota depende de la conexión Wi‑Fi/Internet de la vivienda."),
        "tapo-t300":("Sensor + Tapo Hub","Si ya estás dentro del ecosistema Tapo o quieres centralizar varios sensores.","Requiere Tapo Hub; es una arquitectura distinta de un sensor Wi‑Fi independiente."),
        "seqrell-sq7024b":("4G / GSM","Si la prioridad es mantener una vía de comunicación móvil en una segunda residencia.","Depende de cobertura móvil y de la SIM/servicio compatible; conviene valorar el coste total.")
    }
    cards=[]
    for pid in ids:
        p=by_id.get(pid)
        if not p: continue
        typ,fit,note=summaries[pid]
        href=amazon_url(p, PRODUCTS.get("amazon_tag","TU-TAG"))
        review=p.get("review")
        cards.append(
            '<article class="compare-product-card">'
            '<div class="compare-product-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 12.5 12 5l8 7.5"></path><path d="M6.5 11.5v7h11v-7"></path><path d="M10 18.5v-4h4v4"></path></svg></div>'
            f'<span class="compare-product-type">{html.escape(typ)}</span>'
            f'<h3>{html.escape(p["name"])}</h3>'
            f'<p>{html.escape(fit)}</p>'
            f'<p class="compare-product-note">{html.escape(note)}</p>'
            '<div class="compare-product-actions">'
            + (f'<a class="button button-secondary" href="{html.escape(review)}">Leer análisis →</a>' if review else '')
            + f'<a class="button button-primary" href="{html.escape(href,quote=True)}" rel="sponsored nofollow noopener" target="_blank">Ver en Amazon ↗</a>'
            + '</div></article>'
        )
    return ('<section class="compare-products" aria-label="Detectores comparados">'
            '<div class="affiliate-disclosure"><strong>Enlaces de afiliado:</strong> algunos enlaces de esta comparativa pueden generar una comisión para Casa Bajo Control si compras a través de ellos, sin coste adicional para ti.</div>'
            '<div class="compare-products-grid">'+''.join(cards)+'</div></section>')

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


NAV=[("","Inicio"),("comparativas/","Comparativas"),("guias/","Guías"),("reviews/","Análisis"),("segunda-residencia/","Segunda residencia"),("sobre-nosotros/","Sobre nosotros")]
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
    tpl=tpl.replace("{{PRODUCTS:sin-internet}}", render_affiliate_products("sin-internet")).replace("{{PRODUCTS:fugas}}", render_affiliate_products("fugas")).replace("{{COMPARISON_PRODUCTS}}", render_comparison_products())
    tpl=re.sub(r"\{\{PRODUCT:([a-z0-9-]+)\}\}", lambda m: render_single_affiliate_product(m.group(1)), tpl)
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
redirect("contacto","/legal/aviso-legal/")
redirect("comparativas/mejores-higrometros","/comparativas/sensores-humedad/")
old=ROOT/"comparativas/seguridad/door-window"
if old.exists(): shutil.rmtree(old)

# Stubs de comparativas: URL presente, noindex, sin etiquetar nada como probado.
def stub(slug,title,eyebrow,h1,lead,crumb,image,alt,parent_label="Comparativas",parent="/comparativas/"):
    if slug in pages:
        return
    p=prefix(slug); tpl=read(ROOT/"templates/plana.html")
    extra='<p>Mientras tanto, ya puedes leer nuestros primeros análisis individuales: <a href="/reviews/shelly-flood-gen4/">Shelly Flood Gen4</a> y <a href="/reviews/aqara-water-leak-sensor-t1/">Aqara Water Leak Sensor T1</a> y <a href="/reviews/switchbot-water-leak-detector/">SwitchBot Water Leak Detector</a> y <a href="/reviews/tapo-t300/">TP-Link Tapo T300</a>.</p>' if slug=="comparativas/detectores-fugas-agua" else ''
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

stub("comparativas/sensores-humedad","Sensores de humedad | Casa Bajo Control","Humedad","Mejores sensores de humedad","Esta comparativa se publicará cuando existan resultados propios.","Sensores de humedad","/img/hero-reference.webp","Sensor de humedad en una vivienda")
stub("comparativas/sensores-temperatura","Sensores de temperatura | Casa Bajo Control","Temperatura","Mejores sensores de temperatura","Esta comparativa se publicará cuando existan resultados propios.","Sensores de temperatura","/img/hero-reference.webp","Sensor de temperatura y humedad en una vivienda")
stub("comparativas/camaras-segunda-residencia","Cámaras para segunda residencia | Casa Bajo Control","Seguridad","Mejores cámaras para segunda residencia","Esta comparativa se publicará cuando existan resultados propios.","Cámaras","/img/hero-segunda-residencia.webp","Terraza de una segunda residencia con un móvil mostrando el estado de la casa")
stub("comparativas/sensores-puertas-ventanas","Sensores de puertas y ventanas | Casa Bajo Control","Seguridad","Mejores sensores de puertas y ventanas","Esta comparativa se publicará cuando existan resultados propios.","Puertas y ventanas","/img/hero-comparativas.webp","Varios sensores domésticos sobre una mesa, listos para comparar")


# Hub y stubs de reviews: mantienen los enlaces internos sin presentar páginas pendientes como análisis publicados.
def review_stub(slug, name, profile):
    if slug in pages:
        return
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
      ("SwitchBot Water Leak Detector","/reviews/switchbot-water-leak-detector/","Análisis documental publicado."),
      ("TP-Link Tapo T300","/reviews/tapo-t300/","Análisis documental publicado."),
      ("seQrell SQ7024B","/reviews/seqrell-sq7024b/","Análisis en preparación.")
    ]
    cards_html=''.join(f'<article class="article-card"><h3><a href="{u}">{html.escape(n)}</a></h3><p>{html.escape(d)}</p></article>' for n,u,d in cards)
    body='<section class="article-content"><p>Analizamos sensores y soluciones para detectar problemas domésticos, siempre distinguiendo entre documentación y pruebas propias.</p><div class="article-grid">'+cards_html+'</div></section>'
    bc='<a href="/">Inicio</a> <span aria-hidden="true">/</span> <span aria-current="page">Análisis</span>'
    vals={"{{TITLE}}":"Análisis de productos | Casa Bajo Control","{{DESCRIPTION}}":"Análisis documentales y pruebas de sensores y soluciones para proteger una vivienda.",
          "{{CANONICAL}}":canonical,"{{JSONLD}}":json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":"Análisis de productos","url":canonical},ensure_ascii=False,separators=(",",":")),
          "{{HEADER}}":render_header(slug),"{{FOOTER}}":read(ROOT/"partials/footer.html").replace("{{ROOT}}",p),
          "{{BREADCRUMBS}}":bc,"{{EYEBROW}}":"Análisis","{{H1}}":"Análisis de productos","{{LEAD}}":"Estudios documentales y pruebas propias de sensores y soluciones para proteger una vivienda.",
          "{{META}}":"","{{HERO_MEDIA}}":hero_media(["plana","","","","","","","","","","/img/hero-analisis.webp","Suelo mojado bajo un fregadero con una fuga, junto a una planta y varios libros sobre seguridad en casa"]),"{{OG_IMAGE}}":BASE+"/img/hero-analisis.png","{{BODY}}":body}
    for a,c in vals.items(): tpl=tpl.replace(a,c)
    tpl=tpl.replace("{{ROOT}}",p)
    write(ROOT/"reviews/index.html",tpl)

reviews_hub()
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

legal_aviso="<section class=\"article-content\"><p>En cumplimiento de la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los siguientes datos.</p>\n<h2>Titular del sitio web</h2>\n<p>El sitio web <strong>casabajocontrol.es</strong> (en adelante, «el sitio») es titularidad de <strong>[Nombre y apellidos del titular]</strong>, con NIF <strong>[NIF]</strong> y domicilio a efectos de notificaciones en <strong>[dirección postal]</strong>. Correo electrónico de contacto: <a href=\"mailto:alexworksbcn1991@gmail.com\">alexworksbcn1991@gmail.com</a>.</p>\n<div class=\"callout\"><strong>Pendiente de completar:</strong> nombre, NIF y dirección postal del titular. La LSSI-CE exige identificar al responsable cuando el sitio tiene finalidad económica, como ocurre con los enlaces de afiliación.</div>\n<h2>Objeto</h2>\n<p>Casa Bajo Control es un sitio de contenido editorial sobre prevención de problemas domésticos: fugas de agua, humedad, viviendas que pasan temporadas vacías y dispositivos relacionados. Publica guías, análisis documentales y, cuando existen, pruebas propias de productos. La información tiene carácter divulgativo y no sustituye el asesoramiento de un profesional (fontanero, instalador, abogado, aseguradora) para un caso concreto.</p>\n<h2>Enlaces de afiliación</h2>\n<p>El sitio participa en el Programa de Afiliados de Amazon EU, un programa de publicidad para afiliados diseñado para ofrecer a sitios web un modo de obtener comisiones por la publicidad y la inclusión de enlaces a Amazon.es. En calidad de Afiliado de Amazon, el titular obtiene ingresos por las compras adscritas que cumplen los requisitos aplicables. Estos enlaces no suponen ningún coste adicional para el usuario ni condicionan el contenido editorial: los análisis distinguen expresamente entre productos «Analizados» (estudio documental) y «Probados» (pruebas propias), según la metodología publicada en <a href=\"/como-probamos/\">Cómo analizamos y probamos</a>.</p>\n<h2>Propiedad intelectual</h2>\n<p>Los textos, la estructura, el diseño y las imágenes propias del sitio están protegidos por la legislación sobre propiedad intelectual. Se permite citar fragmentos breves con mención de la fuente y enlace. No se permite la reproducción íntegra de contenidos sin autorización. Las marcas y nombres de productos citados pertenecen a sus respectivos titulares y se mencionan únicamente con fines informativos.</p>\n<h2>Responsabilidad</h2>\n<p>El titular procura que la información sea correcta y esté actualizada, y cita las fuentes en cada guía y análisis. No obstante, las características de los productos, la normativa y las condiciones de los servicios de terceros pueden cambiar; el usuario debe comprobar la información vigente en la fuente original antes de tomar una decisión. El titular no se responsabiliza de los contenidos de los sitios enlazados ni de los daños derivados del uso de la información con fines distintos de los meramente informativos.</p>\n<h2>Legislación aplicable</h2>\n<p>La relación entre el titular y los usuarios se rige por la legislación española. Para cualquier cuestión relativa a este aviso legal puede escribir a <a href=\"mailto:alexworksbcn1991@gmail.com\">alexworksbcn1991@gmail.com</a>.</p>\n<p><em>Última actualización: 13 de septiembre de 2026.</em></p></section>"
legal_priv="<section class=\"article-content\"><p>Esta política explica qué datos personales se tratan en <strong>casabajocontrol.es</strong>, con qué finalidad y qué derechos tiene el usuario, de acuerdo con el Reglamento (UE) 2016/679 (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD).</p>\n<h2>Responsable del tratamiento</h2>\n<p><strong>[Nombre y apellidos del titular]</strong>, con NIF <strong>[NIF]</strong> y domicilio a efectos de notificaciones en <strong>[dirección postal]</strong>. Correo electrónico: <a href=\"mailto:alexworksbcn1991@gmail.com\">alexworksbcn1991@gmail.com</a>.</p>\n<div class=\"callout\"><strong>Pendiente de completar:</strong> identidad y dirección del responsable.</div>\n<h2>Qué datos se tratan y para qué</h2>\n<h3>Contacto por correo electrónico</h3>\n<p>Si el usuario escribe a <a href=\"mailto:alexworksbcn1991@gmail.com\">alexworksbcn1991@gmail.com</a>, se tratan su dirección de correo, su nombre si lo indica y el contenido del mensaje, con la única finalidad de atender la consulta. Base jurídica: consentimiento del usuario al enviar el mensaje. Conservación: el tiempo necesario para responder y, después, el que exijan las obligaciones legales.</p>\n<h3>Datos de navegación</h3>\n<p>El sitio se aloja en GitHub Pages (GitHub, Inc.). Como cualquier servidor web, GitHub puede registrar datos técnicos de las conexiones (dirección IP, fecha, página solicitada, navegador) con fines de seguridad y funcionamiento del servicio, conforme a su propia política de privacidad. El titular no accede a datos identificativos de los visitantes ni utiliza herramientas de analítica que los identifiquen.</p>\n<h3>Fuentes tipográficas</h3>\n<p>El sitio carga la fuente Inter desde Google Fonts. Al hacerlo, el navegador del usuario se conecta a servidores de Google, que puede tratar la dirección IP conforme a su política de privacidad. No se instalan cookies por este motivo.</p>\n<h3>Enlaces a Amazon</h3>\n<p>Los enlaces de afiliación dirigen a Amazon.es. Al pulsarlos, Amazon puede instalar cookies en el navegador del usuario para atribuir la compra al programa de afiliados. Ese tratamiento lo realiza Amazon como responsable y se rige por su propia política de privacidad y cookies. Casa Bajo Control no recibe datos personales de los usuarios que compran: solo informes agregados de comisiones.</p>\n<h2>Destinatarios</h2>\n<p>No se ceden datos a terceros salvo obligación legal. Los proveedores citados (GitHub, Google, Amazon) tratan datos técnicos por cuenta propia como prestadores de servicios de la sociedad de la información. Algunos de ellos están establecidos fuera del Espacio Económico Europeo y las transferencias se amparan en las garantías previstas por el RGPD (decisiones de adecuación o cláusulas contractuales tipo).</p>\n<h2>Derechos del usuario</h2>\n<p>El usuario puede ejercer los derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad escribiendo a <a href=\"mailto:alexworksbcn1991@gmail.com\">alexworksbcn1991@gmail.com</a>, indicando el derecho que ejerce y un medio para verificar su identidad. También puede presentar una reclamación ante la Agencia Española de Protección de Datos (<a href=\"https://www.aepd.es/\" target=\"_blank\" rel=\"noopener\">aepd.es</a>) si considera que el tratamiento no es conforme a la normativa.</p>\n<h2>Menores</h2>\n<p>El sitio no se dirige a menores de 14 años ni recoge datos de ellos de forma consciente.</p>\n<h2>Cambios en esta política</h2>\n<p>Esta política puede actualizarse si cambian los servicios utilizados o la normativa. La fecha de la última revisión figura al pie.</p>\n<p><em>Última actualización: 13 de septiembre de 2026.</em></p></section>"
legal_cookies="<section class=\"article-content\"><p>Esta política explica qué cookies utiliza <strong>casabajocontrol.es</strong>, conforme al artículo 22.2 de la Ley 34/2002 (LSSI-CE) y a las guías de la Agencia Española de Protección de Datos.</p>\n<h2>Qué es una cookie</h2>\n<p>Una cookie es un pequeño archivo que un sitio web guarda en el navegador del usuario para recordar información entre visitas o durante la navegación.</p>\n<h2>Cookies que utiliza este sitio</h2>\n<p><strong>Casa Bajo Control no instala cookies propias.</strong> El sitio es estático, no tiene registro de usuarios, no utiliza herramientas de analítica ni publicidad que instalen cookies, y no requiere consentimiento previo para navegar. Por eso no muestra un banner de cookies.</p>\n<h2>Cookies de terceros al salir del sitio</h2>\n<p>Los enlaces de afiliación a Amazon.es llevan al usuario al sitio de Amazon. Es Amazon quien, en su propio dominio, puede instalar cookies para atribuir las compras al programa de afiliados y para sus propias finalidades, según su <a href=\"https://www.amazon.es/gp/help/customer/display.html?nodeId=201890250\" target=\"_blank\" rel=\"noopener\">aviso de cookies</a>. Esas cookies no se instalan mientras el usuario navega por casabajocontrol.es.</p>\n<p>La carga de la fuente tipográfica desde Google Fonts no instala cookies en el navegador.</p>\n<h2>Si en el futuro se añaden cookies</h2>\n<p>Si el sitio incorpora herramientas de analítica u otros servicios que instalen cookies no necesarias, esta política se actualizará y se solicitará el consentimiento del usuario mediante un aviso antes de instalarlas.</p>\n<h2>Cómo gestionar las cookies en el navegador</h2>\n<p>El usuario puede bloquear o eliminar cookies desde la configuración de su navegador: <a href=\"https://support.google.com/chrome/answer/95647\" target=\"_blank\" rel=\"noopener\">Chrome</a>, <a href=\"https://support.mozilla.org/es/kb/habilitar-y-deshabilitar-cookies-sitios-web-rastrear-preferencias\" target=\"_blank\" rel=\"noopener\">Firefox</a>, <a href=\"https://support.apple.com/es-es/guide/safari/sfri11471/mac\" target=\"_blank\" rel=\"noopener\">Safari</a> y <a href=\"https://support.microsoft.com/es-es/microsoft-edge/eliminar-las-cookies-en-microsoft-edge-63947406-6a3b-1ad1-fa4c-6fa06ee2dbd6\" target=\"_blank\" rel=\"noopener\">Edge</a>.</p>\n<p><em>Última actualización: 13 de septiembre de 2026.</em></p></section>"
plain_page("legal/aviso-legal","Aviso legal | Casa Bajo Control","Legal","Aviso legal","Titular, objeto, enlaces de afiliación, propiedad intelectual y responsabilidad de casabajocontrol.es.",legal_aviso,noindex=False,crumb="Aviso legal")
plain_page("legal/privacidad","Política de privacidad | Casa Bajo Control","Legal","Política de privacidad","Qué datos se tratan en casabajocontrol.es, con qué finalidad y cómo ejercer tus derechos.",legal_priv,noindex=False,crumb="Privacidad")
plain_page("legal/cookies","Política de cookies | Casa Bajo Control","Legal","Política de cookies","Casa Bajo Control no instala cookies propias; explicamos qué ocurre al pulsar un enlace de afiliación.",legal_cookies,noindex=False,crumb="Cookies")
# 404: GitHub Pages sirve /404.html desde cualquier ruta, por eso sus recursos deben ser absolutos.
plain_page("","Página no encontrada | Casa Bajo Control","404","Esta página no existe.","Puede que el enlace haya cambiado.",'<section class="article-content"><p><a class="button button-primary" href="/">Volver al inicio</a></p></section>',out_path=ROOT/"404.html",crumb="Página no encontrada")
s404=read(ROOT/"404.html").replace('href="./"','href="/"').replace('href="css/','href="/css/').replace('src="img/','src="/img/').replace('src="js/','src="/js/').replace('href="img/','href="/img/')
for path,_ in NAV: s404=s404.replace(f'href="{path}"',f'href="/{path}"')
s404=s404.replace('href="legal/','href="/legal/').replace('href="comparativas/"','href="/comparativas/"').replace('href="guias/"','href="/guias/"').replace('href="segunda-residencia/"','href="/segunda-residencia/"').replace('href="como-probamos/"','href="/como-probamos/"').replace('href="sobre-nosotros/"','href="/sobre-nosotros/"')
write(ROOT/"404.html",s404)

write(ROOT/"robots.txt",f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
excluded={"/comparativas/sensores-humedad/","/comparativas/sensores-temperatura/","/comparativas/camaras-segunda-residencia/","/comparativas/sensores-puertas-ventanas/"}
urls={"/","/reviews/","/legal/aviso-legal/","/legal/privacidad/","/legal/cookies/"}
for slug in pages:
    u="/"+slug.strip("/")+"/"
    if u not in excluded: urls.add(u)

xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sorted(urls): xml.append(f"  <url><loc>{BASE}{u}</loc></url>")
xml.append("</urlset>")
write(ROOT/"sitemap.xml","\n".join(xml)+"\n")
print("BUILD OK")
