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

## v2.26 — review Aqara T1 contrastada con la documentación de Aqara
- Corregido: la temperatura –10 a 55 °C era del sensor anterior (sin T1); la ficha del T1 (WL-S02D) dice 0–55 °C, 0–100 % HR sin condensación, 13 dBm. Añadida la advertencia de no confundir ambos modelos.
- Ecosistemas según la ficha del T1 (Apple Home, Google Home, Alexa, IFTTT, Matter, siempre vía hub); Home Assistant no documentado por Aqara.
- Alarma local: es el hub el que suena; depende de que tenga altavoz (E1 no).
- Sin Internet: ya no "no especificado": Aqara documenta que el Hub M3 ejecuta automatizaciones y sirena en local sin Internet y que las notificaciones push necesitan la nube; hubs anteriores, automatizaciones en la nube salvo con M3.
- Añadido el Valve Controller T1 (cierre automático documentado por Aqara) como puente al clúster de corte de agua.
- Title alineado con el H1 ("opinión" implicaba uso). Fuentes: Hub M3 y página del Valve Controller; ficha europea etiquetada como del modelo anterior.

## v2.27
- ASIN del Aqara Water Leak Sensor T1 (B0DWXHMFQS) en products.json: el botón pasa de búsqueda a ficha. Enlace "Leer nuestro análisis" activo en los bloques de producto de las dos guías.

## v2.28
- El análisis del Aqara T1 enlazado desde /agua/, /comparativas/, el stub de la comparativa, los bloques de producto de ambas guías y las alternativas del Shelly.

## v2.29 — review SwitchBot Water Leak Detector (sobre la base v2.28)
- La review llegó construida sobre v2.24; portada a v2.28 (Aqara con ASIN y enlaces de hubs conservados).
- Contrastada con el Help Center y la página de producto de SwitchBot; añadido lo documentado que faltaba: alarma de 60 s por defecto que sigue intentando enviar el aviso; latencia documentada (Wi‑Fi apagado en reposo, 30–120 s de conexión + ~20 s hasta la notificación); advertencia del fabricante de que una salpicadura breve puede sonar sin generar notificación; un hub cercano acelera el aviso; Alexa.
- Title/H1 sin "opinión" (implica uso). Enlazada desde /agua/, /comparativas/, el stub de la comparativa, ambas guías y las otras dos reviews. Hub /reviews/ la marca como publicada.
- ASIN pendiente: el botón sigue en búsqueda hasta confirmarlo en Amazon.es.

## v2.30 — menú "Análisis", hub indexable, home con la selección de análisis
- Menú: Inicio · Comparativas · Guías · Análisis · Segunda residencia · Sobre nosotros (lista NAV en build.py). /reviews/ en el sitemap.
- Home: en el bloque de comparativas solo cambia el rótulo ("Nuestra selección · Analizados por Casa Bajo Control"). Las cinco tarjetas y su enlace se mantienen como estaban, por decisión del propietario.
- ASIN SwitchBot Water Leak Detector (B0CRRL9DNN): botón a ficha.

## v2.32
- Corregido: la caja de producto (Amazon) no aparecía en la review del SwitchBot porque el build solo sustituía los marcadores {{PRODUCT:…}} de Shelly y Aqara. Ahora sustituye cualquier {{PRODUCT:id}}.
- Alternativas de las reviews: la tarjeta entera es clicable y resalta al pasar el ratón (borde, sombra, elevación); foco visible por teclado.
- Botón "Ver cómo probamos" del bloque final de metodología: ya no se parte en tres líneas; tamaño y padding iguales al resto de botones del sitio. Mismo ajuste para los botones dentro del cuerpo de artículos (stubs de comparativas, hubs). En móvil ocupa todo el ancho.

## v2.33 — estados hover/focus unificados en todo el sitio
- Mismo lenguaje en todo lo pulsable: tarjetas-enlace de hubs (`.link-grid a`), tarjetas con título enlazado (`.article-card`, ahora clicables enteras), categorías y comparativas de la home (borde y título verdes al pasar), alternativas de reviews, índice del pilar, botones (primario y secundario), enlaces de texto en artículos (subrayado), resúmenes de FAQ y enlaces del footer. Foco visible por teclado en las tarjetas. Sin movimiento si el sistema tiene reducido el movimiento.

## v2.34 — bloque "Nuestra selección" de la home (idea A)
- Mismo diseño y mismas imágenes; cambian etiquetas, títulos, textos, botones y destinos: 1) Detector de fugas: nuestra elección → análisis del Shelly Flood Gen4 (Analizado); 2) Sensores de humedad → /humedad/ (En análisis); 3) Frío y heladas → pilar de segunda residencia (Guía); 4) Y si alguien entra → pilar, sección de intrusión (Guía); 5) Detector de fugas sin Internet → guía (Guía). Enlace de sección: "Ver todos los análisis →".
- Desaparecen de la home las etiquetas "Probado" y "Recomendado" sin respaldo.

## v2.36 — review Tapo T300 contrastada con el datasheet oficial
- Añadido el datasheet EU/US 1.0 de TP-Link como fuente. De él: zumbador 0–90 dB con cuatro niveles y silencio con una pulsación; condiciones de trabajo 0–40 °C y 0–99 % HR; dimensiones; hasta 64 sensores por hub; y una tercera cifra de autonomía («1 año o más») que contradice la página de producto (3 años) y la FAQ (1,5): se muestran las tres, atribuidas.
- ASIN pendiente (botón en búsqueda).

## v2.37
- ASIN del Tapo T300 (B0CHZ83LQD): botón a ficha. Cuatro análisis con enlace a ficha de Amazon; solo el seQrell queda en búsqueda.

## v2.38 — auditoría de las cuatro reviews
- Migas de pan de las reviews: "Análisis" (antes "Reviews", que no coincidía con el menú); etiqueta corta de SwitchBot y Tapo corregidas (antes se generaban desde el slug).
- El análisis del Tapo T300 enlazado desde /agua/, /comparativas/ y el stub de la comparativa, como los otros tres. Fecha de publicación del Tapo: 13 de septiembre.
- Shelly: la arquitectura del veredicto usa los nombres de la guía sin Internet ("sensor + Wi‑Fi con lógica local"), coherente con las otras tres.

## v2.39
- FAQ unificadas en todo el sitio (reviews, pilar y cualquier `.faq-list` futura): mismo estilo con botón redondo "+ / –", hover y foco visible.
- Hub /reviews/: imagen de cabecera propia (`hero-analisis`, recorte de la imagen aportada sin el texto incrustado) y OG específico. El mockup completo queda en `_assets/banco-imagenes/`.

## v2.41 — guía de okupación auditada
- Añadido en "Qué hacer si descubres que han entrado" el efecto de la reforma de 2025 (LO 1/2025, art. 795 LECrim; Circular FGE 1/2025): allanamiento y usurpación con violencia por juicio rápido; la ocupación sin violencia de un inmueble que no es morada (245.2) sigue por delitos leves. Las fuentes ya estaban citadas pero el texto no lo explicaba.
- Enlaces que faltaban: desde el H3 "Y si alguien entra" del pilar, desde el hub de guías y desde la tarjeta "Y si alguien entra" de la home (solo cambia el destino).
- PNG de la imagen de cabecera para el OG (solo existía WebP).

## v2.42 — /guias/okupacion-segunda-residencia/ con la maquetación editorial
- El ZIP recibido tenía la maquetación en el campo equivocado de `pages.json` (índice 8, el de la fecha de modificación), lo que generaba eyebrow y H1 cambiados, fecha vacía y JSON-LD con HTML dentro; además revertía el enlace de la home a la guía. Reconstruido sobre v2.41: cuerpo maquetado en su campo, títulos, fechas y enlaces correctos.
- Ajustes sobre la maquetación: índice antes de la introducción (como en el pilar); iconos de check con la clase del sistema (se veían como círculos negros); prevención en tres tarjetas con título propio en vez de cuatro "Antes de cerrar"; checklist con la tabla editorial numerada del pilar.
- CSS: bloque `.ok-*` añadido; nada global cambia.

## v2.43 — bloque de preguntas frecuentes en la home (antes del footer)
- 18 preguntas en tres columnas: "Agua y casa vacía" (6), "Okupación y vigilancia" (6) y "Alarmas, cerraduras y cámaras" (6). Mismo componente de FAQ que el resto del sitio; enlaces a las guías donde existen.
- No incluidas, por no poder responderse sin inventar precios o marcas: "cuánto cuesta instalar videovigilancia" y "qué marcas de puertas acorazadas". Las demás preguntas de seguridad se responden con criterios y normativa (EN 50131, UNE-EN 1303, AEPD, Código Penal), sin marcas.
- Sección nueva `.home-faq`; el resto de la home no cambia.

## v2.44 — páginas legales y contacto
- Aviso legal, política de privacidad y política de cookies redactados (LSSI-CE, RGPD/LOPDGDD, criterio AEPD): sin cookies propias ni banner (no hay analítica), enlaces de afiliación explicados, GitHub Pages y Google Fonts declarados. Indexables y en el sitemap.
- PENDIENTE DEL TITULAR: nombre y apellidos, NIF y dirección postal en el aviso legal y en la privacidad (marcado con un aviso en ambas páginas). La LSSI-CE lo exige.
- Contacto: correo alexworksbcn1991@gmail.com, qué enviar y qué no hacemos.
- Si algún día se añade analítica (GA4, etc.), hay que crear banner de consentimiento y actualizar la política de cookies.

## v2.45
- Página de contacto retirada (decisión del propietario): fuera del footer, del sitemap y de pages.json; `/contacto/` queda como redirección (noindex) al aviso legal para no dejar un 404. El correo de contacto sigue en el aviso legal y en la política de privacidad, donde la ley lo exige.

## v2.46
- "Sobre nosotros" redactada (antes 25 palabras): qué es la web, quiénes (Equipo Casa Bajo Control, sin credenciales inventadas), cómo trabajamos (Analizado/Probado), cómo se financia (afiliación Amazon), lo que no hacemos, y remisión al aviso legal para contacto.

## v2.48 — comparativa de detectores de fugas auditada
- Voz de equipo en las cinco tarjetas de escenario ("Miraríamos", antes "Miraría") y sus líneas de recomendación envueltas en párrafo (se veían con dos tamaños de letra).
- Tabla: la autonomía del Tapo T300 refleja las tres cifras que publica TP-Link, como en su análisis.
- H2 "Los cinco modelos de esta comparativa" (antes "que hemos analizado": el seQrell no tiene análisis).
- Eliminada del build la llamada al stub de esta comparativa, que quedaba en conflicto con la página real.

## v2.49
- Home: la tarjeta "Detector de fugas: nuestra elección" lleva ahora a la comparativa (texto y botón ajustados: "Ver la comparativa →"). Nada más cambia.

## v2.50 — comparativa: correcciones finales aprobadas
- Tabla: fila "Qué ocurre sin Internet"; columna seQrell con "Sin documentación verificada" donde no hay fuente (se conserva "Vía móvil (SIM)").
- Párrafo sobre genéricos (Tuya/Smart Life, GoveeLife), packs y coste por sensor al final de "¿Cuál elegir según tu casa?".
- FAQ nueva en primer lugar: "¿Cuál es el mejor detector de fugas para una segunda residencia?".
- Enlace a /agua/ en la conclusión. "Acciones locales" en lugar de "automatizaciones locales" (Shelly). Title con sufijo "| Casa Bajo Control".
- Sin cambios en hero, diseño, menú, Amazon ni otras páginas.

## v2.52 — guía de válvulas de corte automático, correcciones antes de publicar
- Slug acortado a `/guias/valvula-corte-automatico-agua/` (la guía no se había publicado); title de 108 a 87 caracteres.
- Sección 3: bloque "Qué tipos de solución existen" (actuador sobre la llave, motorizada de bola, electroválvula de solenoide, sistemas de caudal), con qué hace cada tipo sin corriente, medidas habituales (1/2", 3/4", 1"), presión y sentido de flujo; regla del contador (nunca antes del contador, siempre tras la llave general del abonado).
- Sección 5 y FAQ "si se va la luz": respondidas según el tipo de válvula en vez de dejarlas como preguntas abiertas.
- Fuentes consultadas (Aqara Valve Controller T1, CTE DB-HS4, análisis propios).
- Enlaces entrantes: comparativa (sección 7 y FAQ), pilar (corte automático), hubs de agua y guías, análisis del Aqara.

## v2.53 — análisis del Aqara Valve Controller T1 y bloque de producto en la guía de válvulas
- Nuevo `/reviews/aqara-valve-controller-t1/` (2.200 palabras), redactado y contrastado con la ficha de especificaciones, la página de producto y el manual de Aqara (VC-X01D/E: DN15–25, maneta de palanca o mariposa, 3,6 N·m, 5–20 s, 4×AA hasta 2 años, hub Aqara obligatorio, –10 a 50 °C, no apto para exterior). Etiqueta Analizado; ASIN B0DB8KS8Q3 en products.json.
- Bloque de producto en la guía de válvulas (tras el tipo A) y en la propia review; enlaces desde la guía, el análisis del sensor Aqara T1, la comparativa (sección 7) y el hub de análisis (5 publicados).
- Imagen `hero-valvula` (aportada) en la guía y en el análisis. Nota: la foto muestra una válvula motorizada en línea, no el actuador de Aqara; el alt lo describe como tal y el texto explica la diferencia.

## v2.54
- Corregido el botón "Ver en Amazon" en la guía de válvulas: la regla de color de enlace de la página (`.water-valve-guide a`) pisaba el texto blanco del botón. Regla general para que ningún botón herede el color de enlace de su página.
- Análisis del Valve Controller T1: accionamiento manual descrito como en el manual (embrague «PUSH», girar el brazo, reenganchar); "qué ocurre sin corriente" marcado como no especificado por Aqara, con la deducción explícita; fuentes ampliadas con el manual en PDF, la ficha europea y el soporte de Aqara (fuera la ficha de Amazon).
