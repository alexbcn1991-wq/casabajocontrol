# Casa Bajo Control — v2.10

La home de v1.6 queda congelada como diseño maestro.

## Infraestructura añadida
- build.py
- templates: guía, comparativa, review y página plana
- partials: header, footer y breadcrumbs
- content/pages.json
- data/products.json como fuente única de productos
- CNAME para casabajocontrol.es
- 404.html
- robots.txt y sitemap.xml generables
- redirecciones de URLs antiguas
- estructura legal noindex pendiente de texto definitivo

## Flujo
Editar fuentes y ejecutar:

    python build.py

La home se conserva como `content/home/index.html` y se restaura sin rediseñarla.

## Importante
No marcar productos como Probado hasta tener pruebas propias.
No publicar las páginas legales de borrador hasta completar los datos reales.

## v2.9 — hero interior según mockup
- La foto llena toda la altura de la tarjeta (antes tenía 325 px fijos y dejaba un hueco verde debajo) y se funde con el fondo por la izquierda mediante un degradado (`.standard-page-hero-media::after`).
- Columna de texto más compacta (H1 34–46 px, entradilla 16,5 px) para que la tarjeta quede en torno a 350 px de alto con Inter cargada.
- Recorte por imagen: `build.py` ya añade la clase `hero-media-<archivo>`; en CSS se fija `--hero-pos` para cada foto (`hero-metodologia`, `hero-fugas`, `hero-comparativas`, `hero-reference`). Para una foto nueva: añadir `.hero-media-<archivo>{--hero-pos:X% 50%}` si el centro no es el encuadre adecuado; si no se define, se usa `center`.
- Móvil/tablet (≤900 px): texto arriba, foto debajo a 260 px (220 px en ≤560 px) con degradado superior.
- `hero-fugas.png/.webp`: eliminada una flecha suelta en la esquina superior derecha (resto del recorte del hero de la home).
- Nada de esto toca la home. Para añadir una página interior: entrada en `pages.json` con imagen y alt; `python build.py`.

## v2.10 — cierre responsive y OG
- ≤900 px: cada foto del hero conserva su proporción completa (sin `object-fit: cover`); el degradado solo existe en dos columnas.
- `og:image` sale del mismo dato que el hero (`pages.json`): el build usa el PNG hermano de la WebP (WhatsApp/Facebook no siempre aceptan WebP). Sin imagen de hero, `og-default.png`.
- `build.py` lee las dimensiones reales de la imagen con Pillow (sin tabla fija).
- Nuevas fotos: `hero-fuga-lavadora` (guía de fugas), `hero-alerta-fuga` (/agua/), `hero-lavadora-sensor` (/guias/), `hero-segunda-residencia` (recorte apaisado 690×430 del hero original; el PNG vertical anterior se ha sustituido).
- Pendiente de decisión: hero específico para /humedad/ (sigue con `hero-reference`).
- Las tres fotos nuevas las aportó el propietario: comprobar que se dispone de derechos de uso antes de publicar (parecen fotografías de fabricante).

## v2.11 — nuevas fotos y checklist en la home
- Home: la tarjeta oscura "¿Está preparada tu segunda residencia?" se sustituye por la imagen `img/home-checklist` (enlaza a la misma URL) en pantallas ≥701 px. En móvil se mantiene la tarjeta, porque el texto incrustado en la foto no es legible a 390 px. Es el único cambio en la home; `content/home/index.html` sincronizada.
- Guía de fugas y hub /guias/: `hero-fuga-lavadora` (lavadora + sensor sobre el charco). Hub /agua/: `hero-alerta-fuga` (fuga bajo fregadero + móvil con la app).
- Las fotos de terceros de v2.10 se retiran del sitio y quedan en `_assets/banco-imagenes/` con los mockups de referencia. Las carpetas que empiezan por `_` no se publican en GitHub Pages.
- `_assets/banco-imagenes/README.md` lista qué imagen falta para cada página según el collage de referencia.
