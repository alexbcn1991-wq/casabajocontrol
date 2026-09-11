# Casa Bajo Control — v0.3

Construcción estática siguiendo el mockup visual de referencia aportado para Casa Bajo Control.

## Qué incluye
- Home con header, hero, cuatro categorías, cinco comparativas destacadas, segunda residencia, checklist y metodología.
- Imagen de referencia del hero y recursos de producto incluidos en `/img/`.
- Menú móvil funcional.
- Navegación interna sin `href="#"`.
- `robots.txt` y `sitemap.xml`.
- Cuatro primeras páginas de contenido: detectores de fugas, sensores de humedad, segunda residencia y metodología.
- Páginas puente para evitar enlaces rotos mientras se amplía el contenido.

## Antes de publicar
1. Sustituir el favicon de ejemplo y crear `og-default.jpg`.
2. Decidir si la foto del hero de referencia se mantiene como recurso provisional o se sustituye por una fotografía propia.
3. Revisar cada afirmación y etiqueta de producto antes de publicar. “Probado” debe reservarse para productos realmente probados.
4. Añadir enlaces de Amazon solo cuando el producto y su ASIN hayan sido verificados.
5. Publicar contenido suficiente en las páginas puente o retirar temporalmente sus enlaces del menú.
6. Configurar Search Console y comprobar sitemap, canonical y móviles.
7. Considerar autoalojar Inter en `/fonts/` antes del lanzamiento final.

## GitHub
Sube el contenido de esta carpeta al repositorio que sirva `casabajocontrol.es` desde la raíz. Las rutas absolutas `/css/`, `/js/` e `/img/` presuponen dominio en la raíz.


## GitHub Pages
Esta versión usa rutas relativas para funcionar correctamente dentro del subdirectorio `/casabajocontrol/` de GitHub Pages. No cambiar las rutas a `/css/`, `/img/` o `/js/` salvo que el sitio pase a servirse desde la raíz del dominio.


## v0.9 — ajuste visual
- Home ajustada contra el mockup maestro.
- Logo vectorial SVG para evitar pixelación.
- Hero en alta resolución y `srcset` 1x/2x.
- Composición del hero centrada mediante contenedor de hasta 1440 px.
- Iconos de beneficios en SVG.
- Mantener el mockup como referencia visual; no usar etiquetas “Probado” hasta tener pruebas reales.

## v1.0 — auditoría estructural (sin cambios de diseño)
- Hero: la imagen ahora se posiciona dentro del contenedor (`.hero-inner`), no respecto a la ventana. Termina en el mismo margen derecho que el resto de la web (50 px en escritorio).
- Hero: eliminados los restos de texto del mockup ("vivienda / residencia") en el borde izquierdo de la imagen. Añadida versión WebP (56 KB frente a 620 KB PNG) con fallback PNG.
- Imágenes de las comparativas: eliminadas las etiquetas "Probado/Analizado" que venían incrustadas en los PNG y se duplicaban con las etiquetas HTML.
- Iconos SVG de categorías y beneficios: faltaban tamaño y trazo (se veían en negro o no se veían).
- Menú móvil: se mostraban los dos iconos (abrir y cerrar) a la vez.
- Móvil: la foto del hero se solapaba con "Cómo funciona"; ahora fluye debajo del texto.
- `/comparativas/` no existía (enlace roto en el menú de todas las páginas). Creada como página hub con enlaces a las cinco comparativas.
- `/comparativas/seguridad/door-window/` duplicaba `/comparativas/sensores-puertas-ventanas/`: convertida en redirección y retirada del sitemap. La tarjeta "Seguridad" de la home enlaza ahora a la URL en español.
- Páginas "en construcción" (10): `noindex,follow` hasta que tengan contenido. Quitar la meta al publicarlas y añadirlas al sitemap.
- `sitemap.xml` solo con las 6 URLs con contenido real.

### Pendiente (no se ha tocado)
- Etiquetas "Probado" en la home: solo cuando haya pruebas reales (regla editorial propia).
- `img/og-default.jpg` no existe; crearlo (1200×630) o quitar la meta `og:image`.
- `img/hero-home.webp` y `hero-home@2x.webp` no se usan (recorte peor que `hero-reference`). Se pueden borrar.
- El botón de búsqueda sigue oculto (`hidden`) hasta que exista un buscador real.

## v1.1 — hero a tamaño completo y menú centrado
- Menú de navegación centrado entre el logo y el buscador.
- A partir de 1300 px de ancho la foto del hero se muestra a tamaño real (992×430), ocupando toda la altura del bloque, del header a las tarjetas. Su borde derecho sigue alineado con el margen del contenedor; por la izquierda se extiende bajo el texto con un degradado blanco (composición del mockup).
- Por debajo de 1300 px no cabe sin recortar: se mantiene la composición v1.0 (foto entera sin degradado).
- Opción: si prefieres que la foto llegue hasta el borde de la ventana como en el mockup, cambia en la regla v1.1 `.hero-image{right:0}` por `right:-50px`.
