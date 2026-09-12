document.addEventListener("DOMContentLoaded",()=>{const menu=document.querySelector(".mobile-menu"),nav=document.querySelector("#main-nav");if(!menu||!nav)return;const setOpen=o=>{nav.classList.toggle("is-open",o);menu.setAttribute("aria-expanded",String(o));menu.setAttribute("aria-label",o?"Cerrar menú":"Abrir menú")};menu.addEventListener("click",()=>setOpen(!nav.classList.contains("is-open")));nav.addEventListener("click",e=>{if(e.target.closest("a"))setOpen(false)});document.addEventListener("keydown",e=>{if(e.key==="Escape")setOpen(false)});document.addEventListener("click",e=>{if(!e.target.closest(".site-header"))setOpen(false)});});
// Botón "Volver arriba" (solo páginas interiores; aparece tras desplazarse).
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector(".back-to-top");
  if (!btn) return;
  const toggle = () => { btn.hidden = window.scrollY < 600; };
  toggle();
  window.addEventListener("scroll", toggle, { passive: true });
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    const smooth = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({ top: 0, behavior: smooth ? "smooth" : "auto" });
    const main = document.getElementById("contenido"); if (main) main.focus({ preventScroll: true });
  });
});
