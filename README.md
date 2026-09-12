# Casa Bajo Control — v2.22

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

## v2.12 — heroes de comparativas/guías/segunda residencia/sobre nosotros y auditoría de enlaces
- Nuevas fotos: `hero-comparativas`, `hero-guias`, `hero-segunda-residencia`, `hero-sobre-nosotros` (todas 1774×887, WebP + PNG para OG).
- Corregido: la tarjeta "Mejores sensores de humedad" de la home llevaba a una redirección cuyo destino (`/comparativas/sensores-humedad/`) no existía → 404. Ahora existe como stub (noindex) y la home enlaza directo.
- Home: "Preparar mi casa", el banner del checklist y su tarjeta móvil enlazan directamente a `/segunda-residencia/` (antes pasaban por la redirección `proteger-segunda-residencia`). Retirado "Consejos" del menú de la home (era una redirección a Guías; las interiores no lo tenían). No cambia nada visual salvo ese elemento del menú.
- Los cinco stubs de comparativas se generan ahora desde `build.py` (función `stub`): misma cabecera estándar, `noindex`, fuera del sitemap. Desaparecen las tres páginas antiguas con menú y cabecera de v1.

## v2.13 — navegación unificada
- Cabecera única: `build.py` genera el menú (`NAV` en build.py) para TODAS las páginas, incluida la home (se regenera desde `content/home/index.html` sustituyendo solo el bloque `<header>`), los stubs, las legales y `404.html`. No queda ningún header escrito a mano.
- Menú: Inicio · Comparativas · Guías · Segunda residencia · Sobre nosotros. Estado activo por sección (`/guias/…` → Guías, etc.).
- "Consejos" eliminado de todos los menús. `/consejos/` se mantiene solo como redirección heredada (noindex) a `/guias/`.
- `404.html` con recursos y enlaces absolutos (GitHub Pages lo sirve desde cualquier ruta).
- Para cambiar el menú en el futuro: editar la lista `NAV` en `build.py` y ejecutar el build.

## v2.14
- Buscador y lupa eliminados por decisión editorial (se valorará más adelante). Desaparecen `/buscar/`, `js/search.js` y `data/search-index.json`. El menú queda: Inicio · Comparativas · Guías · Segunda residencia · Sobre nosotros.

## v2.15 — guía "Detector de fugas sin Internet" sobre la base v2.14
- La guía llegó construida sobre v2.9 (sin los cambios v2.10–v2.14). Se ha portado a v2.14: entrada en `pages.json`, `hero-sin-internet` (WebP + PNG para OG), enlace desde la guía de fugas y tarjeta en `/guias/`, sitemap.
- Ajustes mínimos en el texto: voz de equipo ("utilizaríamos"), ancla y entrada de sumario para la opción 4, enlaces de vuelta a la guía de fugas y al hub de agua, sección "Dónde colocarlo" resumida para no duplicar la guía de fugas, título acortado.

## v2.17
- La guía "Detector de fugas sin Internet" aparece en el hub `/agua/` (tarjeta) y en el pilar `/segunda-residencia/` (enlaces en "Agua" y "Conectividad"). Home sin cambios.

## v2.20 — /segunda-residencia/ con la maquetación editorial del boceto
- Solo cambian `content/pages.json` (cuerpo de la página), `css/styles.css` (bloque `.second-home-*`, reescrito limpio; sustituye al de v2.19) y `segunda-residencia/index.html` regenerado. Hero, cabecera, footer y resto de páginas: byte a byte iguales.
- Estructura: índice bajo el hero (3 columnas) → intro → 1 riesgos (4 tarjetas + cita de la tesis en columna lateral) → 2 agua en 3 tarjetas con checks (cerrar / vigilar + contador / corte automático con secuencia y caja "sirena") → 3 humedad con tarjeta lateral → 4 electricidad con flujo vertical "si se va la luz" → 5 personas (dos tarjetas) + "Y si alguien entra" → 6 checklist numerada (20 filas) con "Al volver a la casa" en columna lateral → 7 FAQ en `<details>` → 8 metodología con tres escenarios y botón.
- Sin fotos nuevas (el boceto las tiene; se ha priorizado componentes, como indica el brief). Sin productos ni marcas en esta página.

## v2.21
- Botón "Volver arriba" en todas las páginas interiores (plantillas guía, comparativa, review y plana): fijo abajo a la derecha, aparece tras 600 px de scroll, respeta `prefers-reduced-motion`, accesible por teclado. La home no lo lleva.
- Corregido el botón "Cómo analizamos y probamos" de /segunda-residencia/: el color de enlace de la página pisaba el texto blanco del botón.


## v2.22 — Review Shelly Flood Gen4
- Añadido `/reviews/shelly-flood-gen4/` como análisis documental.
- Añadido bloque de afiliación con ASIN real y tag `alex19910c-21`.
- Añadido hub `/reviews/` y stubs noindex para futuras reviews.
- Diseño específico de review añadido sin modificar Home ni Hero de páginas existentes.

## v2.23 — review Shelly Flood Gen4 contrastada con la ficha oficial
- Corregido: Matter y Zigbee son firmwares alternativos (no simultáneos); hub necesario solo con firmware Zigbee.
- Añadido desde kb.shelly.cloud (S4SN-0071A): modo Económico pensado por Shelly para casas de vacaciones (zumbador y aviso acústico de batería baja desactivados); comprobación del cable cada 5 s; causas documentadas de falsas alarmas y ajuste "State hold time"; condiciones de trabajo (–20 a 40 °C, 30–70 % HR); acciones locales reales (webhooks, MQTT, UDP; sin scripting); cómo lo expone cada ecosistema; mención al Shelly Flood S Gen4 para evitar confusiones.
- Retirada la fila de garantía (sin fuente). URLs de soporte codificadas. Fuente añadida: Knowledge Base oficial.
- Jerarquía: el nombre del producto en los bloques de afiliación deja de ser H3 (duplicaba el H1); el cierre de metodología deja de ser H3.

## v2.24 — la review es alcanzable desde la web
- Bloques de producto: cuando un producto tiene análisis propio (`review` en products.json), aparece "Leer nuestro análisis →" junto a "Ver en Amazon". Shelly Flood Gen4 entra también en el bloque de la guía de detección de fugas.
- Tarjeta del análisis en `/agua/`; enlace desde `/comparativas/`, desde el stub de la comparativa de detectores y desde la mención a Shelly en la guía sin Internet. Seis páginas enlazan ya a la review.
- Corregido un desbordamiento horizontal en móvil de la guía sin Internet (tablas de 5 columnas): ahora desplazan dentro de su caja. Las 28 páginas comprobadas a 390 px sin overflow.
