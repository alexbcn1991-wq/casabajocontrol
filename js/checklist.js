/* Casa Bajo Control — checklist interactivo "¿Está preparada tu segunda residencia?"
   Sin backend ni cookies: todo se calcula en el navegador. Las respuestas se codifican en el
   fragmento de la URL (#r=...) para poder volver al resultado o compartirlo. */
(function () {
  'use strict';
  var TAG = 'alex19910c-21';
  function amz(asin) { return 'https://www.amazon.es/dp/' + asin + '?tag=' + TAG; }

  var BLOCKS = {
    agua: 'Agua', humedad: 'Humedad', energia: 'Luz y conexión', seguridad: 'Seguridad', seguro: 'Seguro'
  };

  /* Cada pregunta: id, bloque, texto, opciones [{t: texto, s: puntos 0-2}], y la recomendación
     cuando la respuesta no es la mejor: título, texto, enlaces [{t, href, kind}] (kind: guia | producto). */
  var Q = [
    { id: 'q1', b: 'agua', t: '¿Cierras la llave de paso general cada vez que dejas la casa?',
      o: [{ t: 'Siempre, y compruebo que corta', s: 2 }, { t: 'A veces, o solo en invierno', s: 1 }, { t: 'No, o no sé dónde está', s: 0 }],
      r: { t: 'La llave de paso es la medida gratis que más daño evita', p: 'Una fuga en una casa cerrada puede durar semanas. Con la llave general cerrada, lo peor que puede pasar es lo que quepa en las tuberías.',
        l: [{ t: 'Cómo detectar una fuga de agua (y localizar la llave de paso)', h: '/guias/como-detectar-una-fuga-de-agua/' }, { t: 'Checklist al cerrar la casa', h: '/segunda-residencia/#sh-6' }] } },
    { id: 'q2', b: 'agua', t: '¿Tienes algún sensor que avise si hay agua en el suelo (termo, lavadora, cuarto del contador)?',
      o: [{ t: 'Sí, con aviso al móvil', s: 2 }, { t: 'Solo alarma sonora en la casa', s: 1 }, { t: 'No', s: 0 }],
      r: { t: 'Sin sensor, te enteras cuando ya hay daño', p: 'Un detector de fugas cuesta lo que una cena y avisa a las pocas horas, no a las pocas facturas. Lo importante no es el sensor sino por dónde sale el aviso.',
        l: [{ t: 'Comparativa de detectores de fugas: cuál encaja con tu casa', h: '/comparativas/detectores-fugas-agua/' }, { t: 'Shelly Flood Gen4 — nuestra selección', h: amz('B0FPG9SGLJ'), k: 'p' }, { t: 'Leer nuestro análisis del Shelly Flood Gen4', h: '/reviews/shelly-flood-gen4/' }] } },
    { id: 'q3', b: 'agua', t: 'Si un sensor avisa de una fuga mientras no estás, ¿qué pasa después?',
      o: [{ t: 'Una válvula corta el agua sola', s: 2 }, { t: 'Alguien de confianza puede ir en unas horas', s: 1 }, { t: 'Nada hasta que yo vaya', s: 0 }],
      r: { t: 'El aviso no basta si nadie puede cerrar la llave', p: 'Una válvula de corte automático cierra el suministro cuando el sensor detecta agua, sin depender de que alguien esté cerca.',
        l: [{ t: 'Válvula de cierre automático: cómo funciona y cuándo instalarla', h: '/guias/valvula-corte-automatico-agua/' }, { t: 'Aqara Valve Controller T1 (actuador sobre la llave)', h: amz('B0DB8KS8Q3'), k: 'p' }, { t: 'Leer nuestro análisis del Aqara Valve Controller T1', h: '/reviews/aqara-valve-controller-t1/' }] } },
    { id: 'q4', b: 'humedad', t: '¿Sabes qué humedad hay dentro de la casa cuando está cerrada?',
      o: [{ t: 'Sí, con higrómetro que registra o avisa', s: 2 }, { t: 'Tengo un higrómetro, pero solo lo miro al llegar', s: 1 }, { t: 'No lo sé', s: 0 }],
      r: { t: 'La humedad que no mides es la que acaba en moho', p: 'Entre 40 y 60 % es normal. Por encima, sostenido durante semanas en una casa cerrada, aparece el moho. Medir es lo primero; actuar, lo segundo.',
        l: [{ t: 'Cómo medir la humedad en casa y saber si es un problema', h: '/guias/como-medir-la-humedad-en-casa/' }] } },
    { id: 'q5', b: 'humedad', t: 'Cuando la casa está cerrada varias semanas, ¿se ventila o deshumidifica?',
      o: [{ t: 'Sí, deshumidificador o ventilación programada', s: 2 }, { t: 'Alguien la ventila de vez en cuando', s: 1 }, { t: 'Queda cerrada sin ventilar', s: 0 }],
      r: { t: 'Casa cerrada sin ventilar es la receta del moho', p: 'La condensación en una vivienda cerrada no necesita ninguna fuga: basta con aire quieto, temperatura baja y tiempo.',
        l: [{ t: 'Humedad y moho en una casa cerrada', h: '/segunda-residencia/#sh-3' }] } },
    { id: 'q6', b: 'energia', t: 'Si se va la luz en la casa, ¿te enteras?',
      o: [{ t: 'Sí, recibo un aviso', s: 2 }, { t: 'Me entero al llegar', s: 0 }],
      r: { t: 'Un corte de luz deja ciegos a tus sensores', p: 'Sin luz no hay router, y sin router la mayoría de sensores no avisan. Saber que la luz ha fallado es saber que estás a ciegas.',
        l: [{ t: '¿Qué le pasa a tu casa si se va la luz y no estás? Guía para un apagón', h: '/guias/apagon-casa-vacia/' }, { t: 'Electricidad y conectividad en una casa vacía', h: '/segunda-residencia/#sh-4' }] } },
    { id: 'q7', b: 'energia', t: 'Si falla el router o el Wi‑Fi, ¿tus avisos siguen funcionando?',
      o: [{ t: 'Sí: vía móvil, o local con batería', s: 2 }, { t: 'Solo la alarma sonora, sin aviso al móvil', s: 1 }, { t: 'No, todo depende del Wi‑Fi', s: 0 }],
      r: { t: 'Tu sistema vale lo que vale su punto más débil', p: 'La pregunta correcta no es si el sensor funciona sin Internet, sino qué parte sigue funcionando y qué parte no.',
        l: [{ t: 'Detector de fugas sin Internet: qué opciones tienes', h: '/guias/detector-de-fugas-sin-internet/' }] } },
    { id: 'q8', b: 'seguridad', t: '¿Te enterarías el mismo día si alguien entra en la casa?',
      o: [{ t: 'Sí, sensor de apertura o cámara con aviso', s: 2 }, { t: 'Un vecino pasa a menudo', s: 1 }, { t: 'No', s: 0 }],
      r: { t: 'En okupación, el tiempo lo cambia todo', p: 'La diferencia entre enterarte en horas o en semanas es la diferencia entre una llamada y un procedimiento largo.',
        l: [{ t: 'Comparativa de sensores de puertas y ventanas: cuál encaja con tu casa', h: '/comparativas/sensores-puertas-ventanas/' }, { t: 'TP-Link Tapo T110 (sensor de apertura, con hub Tapo)', h: amz('B0BF5MC9QX'), k: 'p' }, { t: 'Okupación de una segunda residencia: prevenirla, detectarla a tiempo y qué hacer', h: '/guias/okupacion-segunda-residencia/' }] } },
    { id: 'q9', b: 'seguridad', t: 'Desde fuera, ¿la casa parece habitada?',
      o: [{ t: 'Sí: buzón vaciado, luces o persianas con horario', s: 2 }, { t: 'Solo en parte', s: 1 }, { t: 'No, se nota que está vacía', s: 0 }],
      r: { t: 'El buzón lleno es la señal que buscan', p: 'Publicidad acumulada, persianas siempre igual y ninguna luz durante semanas: la casa lo cuenta todo.',
        l: [{ t: 'Prevención: lo que hacemos antes de cerrar la casa', h: '/guias/okupacion-segunda-residencia/#ok-5' }] } },
    { id: 'q10', b: 'seguro', t: '¿Has revisado la cláusula de desocupación de tu seguro de hogar?',
      o: [{ t: 'Sí, y la cumplo', s: 2 }, { t: 'Sé que existe, pero no la he mirado', s: 1 }, { t: 'No sabía que existía', s: 0 }],
      r: { t: 'Hay pólizas que excluyen la fuga si has estado ausente cierto tiempo', p: 'OCU lo cita entre las exclusiones habituales. Si tu casa pasa semanas vacía, esa cláusula decide si el seguro responde.',
        l: [{ t: 'Fuga de agua: ¿quién paga? Seguro, comunidad, vecino e inquilino', h: '/guias/fuga-de-agua-quien-paga/' }] } }
  ];

  var root = document.getElementById('ck-app');
  if (!root) return;
  var form = document.getElementById('ck-form');
  var result = document.getElementById('ck-result');

  /* ---- render del formulario ---- */
  var html = '';
  var lastBlock = '';
  Q.forEach(function (q, i) {
    if (q.b !== lastBlock) { html += '<h2 class="ck-block">' + BLOCKS[q.b] + '</h2>'; lastBlock = q.b; }
    html += '<fieldset class="ck-q" id="' + q.id + '"><legend><span class="ck-num">' + (i + 1) + '</span>' + q.t + '</legend><div class="ck-options">';
    q.o.forEach(function (o, j) {
      var oid = q.id + '_' + j;
      html += '<label class="ck-opt" for="' + oid + '"><input type="radio" name="' + q.id + '" id="' + oid + '" value="' + j + '"><span>' + o.t + '</span></label>';
    });
    html += '</div></fieldset>';
  });
  html += '<div class="ck-actions"><p class="ck-actions-lead">¿Ya has respondido las diez?</p><button type="submit" class="button button-primary ck-submit">Ver mi resultado <span aria-hidden="true">→</span></button><p class="ck-actions-note">Puntuación por bloques y qué revisar primero. Sin registro.</p><p class="ck-missing" id="ck-missing" hidden>Te faltan preguntas por responder: <span></span>.</p></div>';
  form.innerHTML = html;

  function answers() {
    return Q.map(function (q) {
      var el = form.querySelector('input[name="' + q.id + '"]:checked');
      return el ? parseInt(el.value, 10) : -1;
    });
  }

  function render(a) {
    var total = 0, max = 0, perBlock = {}, weak = [];
    Q.forEach(function (q, i) {
      var s = q.o[a[i]].s, m = 2;
      total += s; max += m;
      perBlock[q.b] = perBlock[q.b] || { s: 0, m: 0 };
      perBlock[q.b].s += s; perBlock[q.b].m += m;
      if (s < 2) weak.push({ q: q, s: s });
    });
    var pct = Math.round(total / max * 100);
    var level, cls, msg;
    if (pct >= 80) { level = 'Casa bajo control'; cls = 'ok'; msg = 'Tienes cubierto lo que más daño evita. Lo que queda abajo son ajustes, no urgencias.'; }
    else if (pct >= 50) { level = 'Hay huecos que cuestan dinero'; cls = 'mid'; msg = 'Lo básico está, pero hay fallos que en una casa vacía se convierten en semanas de daño. Empieza por los puntos de agua.'; }
    else { level = 'Riesgo alto'; cls = 'bad'; msg = 'Si hoy hubiera una fuga o una entrada, te enterarías tarde. La buena noticia: las primeras tres medidas son baratas o gratis.'; }

    var h = '<div class="ck-score ck-score-' + cls + '"><div class="ck-score-num"><strong>' + pct + '</strong><span>/100</span></div><div><p class="ck-score-level">' + level + '</p><p>' + msg + '</p></div></div>';
    h += '<ul class="ck-blocks">';
    Object.keys(BLOCKS).forEach(function (b) {
      var pb = perBlock[b]; var p = Math.round(pb.s / pb.m * 100);
      h += '<li><span>' + BLOCKS[b] + '</span><span class="ck-bar"><i style="width:' + p + '%"></i></span><b>' + p + '%</b></li>';
    });
    h += '</ul>';

    if (weak.length) {
      /* Orden: primero las respuestas peores (0), luego las parciales; dentro, el orden del cuestionario, que ya va por daño esperado. */
      weak.sort(function (x, y) { return x.s - y.s; });
      h += '<h2 class="ck-rec-title">Qué revisar, por orden</h2><div class="ck-recs">';
      weak.forEach(function (w) {
        var r = w.q.r;
        h += '<article class="ck-rec' + (w.s === 0 ? ' ck-rec-bad' : '') + '"><span class="ck-rec-tag">' + BLOCKS[w.q.b] + (w.s === 0 ? ' · sin cubrir' : ' · a medias') + '</span><h3>' + r.t + '</h3><p>' + r.p + '</p><ul>';
        r.l.forEach(function (l) {
          if (l.k === 'p') h += '<li><a class="ck-link ck-link-p" href="' + l.h + '" rel="sponsored nofollow noopener" target="_blank">' + l.t + ' <span aria-hidden="true">↗</span></a></li>';
          else h += '<li><a class="ck-link" href="' + l.h + '">' + l.t + ' →</a></li>';
        });
        h += '</ul></article>';
      });
      h += '</div><p class="ck-disclosure"><strong>Enlaces de afiliado:</strong> los enlaces marcados con ↗ llevan a Amazon.es; si compras a través de ellos, Casa Bajo Control puede obtener una comisión sin coste adicional para ti. Solo enlazamos productos que hemos analizado.</p>';
    } else {
      h += '<p class="ck-all-good">No hay ningún punto sin cubrir. Si quieres afinar, el <a href="/segunda-residencia/#sh-6">checklist al cerrar la casa</a> baja al detalle de cada visita.</p>';
    }
    h += '<div class="ck-share"><button type="button" class="button button-secondary" id="ck-copy">Copiar enlace a este resultado</button><button type="button" class="button button-secondary" id="ck-redo">Volver a empezar</button><span id="ck-copied" hidden>Copiado</span></div>';
    result.innerHTML = h;
    result.hidden = false;
    form.hidden = true;
    document.getElementById('ck-copy').addEventListener('click', function () {
      var url = location.href.split('#')[0] + '#r=' + a.join('');
      var done = function () { var c = document.getElementById('ck-copied'); c.hidden = false; setTimeout(function () { c.hidden = true; }, 2000); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function () { prompt('Copia este enlace:', url); });
      else prompt('Copia este enlace:', url);
    });
    document.getElementById('ck-redo').addEventListener('click', function () {
      form.reset(); result.hidden = true; form.hidden = false; history.replaceState(null, '', location.pathname); form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var a = answers();
    var missing = [];
    a.forEach(function (v, i) { if (v < 0) missing.push(i + 1); });
    var mEl = document.getElementById('ck-missing');
    if (missing.length) { mEl.querySelector('span').textContent = missing.join(', '); mEl.hidden = false; document.getElementById(Q[missing[0] - 1].id).scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    mEl.hidden = true;
    history.replaceState(null, '', '#r=' + a.join(''));
    render(a);
  });

  /* Restaurar desde la URL (#r=0120...) */
  var m = /#r=([0-9]{10})$/.exec(location.hash);
  if (m) {
    var a = m[1].split('').map(Number);
    var valid = a.every(function (v, i) { return v < Q[i].o.length; });
    if (valid) {
      a.forEach(function (v, i) { var el = document.getElementById(Q[i].id + '_' + v); if (el) el.checked = true; });
      render(a);
    }
  }
})();
