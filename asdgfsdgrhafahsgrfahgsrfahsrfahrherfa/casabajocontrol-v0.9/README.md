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
