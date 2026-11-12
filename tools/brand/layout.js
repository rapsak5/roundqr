  /* Skabeloner: kvadrat med logo i midten, bred med logo ved siden af, banner med logo og tekst. */
  var ORG = __ORG__;
  var TPL = { center: { shape: "square", dot: "dots", eye: "rounded", set: 0 },
              wide: { shape: "square", dot: "rounded", eye: "rounded", set: 0, mono: true },
              banner: { shape: "square", dot: "squares", eye: "square", set: 0 },
              round: { shape: "circle", dot: "dots", eye: "rounded", set: 0, fill: true, ring: true } };
  var ROUND_LAYOUT = "__ROUND__";  /* "center": logoet i midten af den runde kode, "stack": logoet under koden */
  function realLayout(v) { return v === "round" ? ROUND_LAYOUT : (v || "center"); }
  var SIDE_FONT = "";
  function sideFont() {
    if (!SIDE_FONT) SIDE_FONT = (getComputedStyle(document.documentElement).getPropertyValue("--font-display") || "").trim() || "Arial, sans-serif";
    return SIDE_FONT;
  }
  var measureCtx = document.createElement("canvas").getContext("2d");
  function wrapText(t, fs, tw) {
    measureCtx.font = "700 100px " + sideFont();
    var words = t.split(/\s+/), lines = [], cur = "", widest = 0;
    words.forEach(function (w) {
      var test = cur ? cur + " " + w : w;
      if (cur && measureCtx.measureText(test).width * fs / 100 > tw) { lines.push(cur); cur = w; } else cur = test;
    });
    if (cur) lines.push(cur);
    lines.forEach(function (l) { widest = Math.max(widest, measureCtx.measureText(l).width * fs / 100); });
    return { lines: lines, fits: widest <= tw };
  }
  function sidePanel(g, o, lg) {
    var H = g.H, x0 = g.sideX, W = g.W, P = {}, asp = lg ? lg.aspect : 0, txt = g.text;
    if (g.layout === "stack") {
      var ih = g.inner.H, area = H - ih;
      if (lg) {
        var mw = W * 0.6, mh = area * 0.62, lw = mw, lh = lw / asp;
        if (lh > mh) { lh = mh; lw = lh * asp; }
        P.logo = { x: (W - lw) / 2, y: ih + (area - lh) / 2 - area * 0.08, w: lw, h: lh };
      } else {
        P.fs = area * 0.42; P.center = true; P.tx = W / 2; P.lines = [{ t: ORG.short, y: ih + area * 0.5 }];
      }
      return P;
    }
    if (g.layout === "wide") {
      if (lg) {
        var bw = g.sideW * 0.78, bh = H * 0.46, w = bw, h = w / asp;
        if (h > bh) { h = bh; w = h * asp; }
        P.logo = { x: x0 + (g.sideW - w) / 2 - H * 0.02, y: (H - h) / 2, w: w, h: h };
      } else {
        var r0 = wrapText(ORG.short, H * 0.2, g.sideW * 0.8);
        P.fs = H * 0.2; P.tx = x0 + H * 0.04; P.lines = [{ t: ORG.short, y: H / 2 + P.fs * 0.35 }];
      }
      return P;
    }
    P.line = { x: x0 + H * 0.04, y: H * 0.18, w: H * 0.014, h: H * 0.64 };
    var tx = x0 + H * 0.14, tw = W - tx - H * 0.08, lw = 0, lh = 0, gap = H * 0.1;
    P.tx = tx;
    if (lg) { lh = H * 0.26; lw = lh * asp; if (lw > tw * 0.75) { lw = tw * 0.75; lh = lw / asp; } }
    var fs = H * 0.13, r = { lines: [] };
    if (txt) {
      for (var it = 0; it < 10; it++) {
        r = wrapText(txt, fs, tw);
        var blockH = (lg ? lh + gap : 0) + fs * 1.2 * r.lines.length;
        if (r.fits && r.lines.length <= 3 && blockH <= H * 0.72) break;
        fs *= 0.9;
      }
    }
    var block = (lg ? lh : 0) + (lg && r.lines.length ? gap : 0) + fs * 1.2 * r.lines.length - (r.lines.length ? fs * 0.2 : 0);
    var y = (H - block) / 2;
    if (lg) { P.logo = { x: tx, y: y, w: lw, h: lh }; y += lh + gap; }
    if (r.lines.length) { P.fs = fs; P.lines = r.lines.map(function (t, i) { return { t: t, y: y + fs * 0.82 + i * fs * 1.2 }; }); }
    var top = P.logo ? P.logo.y : (P.lines ? y : H * 0.18);
    P.line.y = Math.min(P.line.y, top); P.line.h = Math.max(H * 0.64, block);
    P.line.y = (H - P.line.h) / 2;
    return P;
  }
  (function () {
    var G = RQ.geometry, S = RQ.toSVG, C = RQ.toCanvas;
    RQ.geometry = function (text, o) {
      var g = G(text, o);
      if (!o.layout || o.layout === "center") return g;
      var G2 = {};
      for (var k in g) G2[k] = g[k];
      G2.inner = g; G2.layout = o.layout; G2.text = (o.sideText || "").trim();
      if (o.layout === "stack") { G2.W = g.W; G2.H = g.H * 1.3; G2.sideX = 0; G2.sideY = g.H; G2.sideW = g.W; return G2; }
      var sw = o.layout === "wide" ? g.H * 1.05 : g.H * 1.9;
      G2.W = g.W + sw; G2.H = g.H; G2.sideX = g.W; G2.sideW = sw;
      return G2;
    };
    RQ.toCanvas = function (cv, g, o, lg, px, opaque) {
      if (!g.layout) return C(cv, g, o, lg, px, opaque);
      cv.width = px; cv.height = Math.round(px * g.H / g.W);
      var ctx = cv.getContext("2d"), k = px / g.W;
      ctx.clearRect(0, 0, cv.width, cv.height);
      ctx.fillStyle = o.bg; ctx.fillRect(0, 0, cv.width, cv.height);
      var q = document.createElement("canvas");
      C(q, g.inner, o, null, Math.round(g.inner.W * k), true);
      ctx.drawImage(q, 0, 0);
      var P = sidePanel(g, o, lg);
      ctx.save(); ctx.scale(k, k);
      if (P.line) { ctx.fillStyle = o.eyec; ctx.fillRect(P.line.x, P.line.y, P.line.w, P.line.h); }
      if (P.logo) { ctx.imageSmoothingQuality = "high"; ctx.drawImage(lg.img, P.logo.x, P.logo.y, P.logo.w, P.logo.h); }
      if (P.lines) {
        ctx.fillStyle = o.fg; ctx.textBaseline = "alphabetic"; ctx.textAlign = P.center ? "center" : "left";
        ctx.font = "700 " + P.fs + "px " + sideFont();
        P.lines.forEach(function (l) { ctx.fillText(l.t, P.tx, l.y); });
      }
      ctx.restore();
    };
    function e(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
    function n(v) { return (Math.round(v * 1000) / 1000).toString(); }
    RQ.toSVG = function (g, o, lg, cm) {
      if (!g.layout) return S(g, o, lg, cm);
      var inner = S(g.inner, o, null, 0), body = inner.slice(inner.indexOf(">") + 1, inner.lastIndexOf("</svg>"));
      var W = g.W, H = g.H;
      var dims = cm ? 'width="' + n(cm) + 'cm" height="' + n(cm * H / W) + 'cm"' : 'width="' + Math.round(W * 20) + '" height="' + Math.round(H * 20) + '"';
      var s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + n(W) + " " + n(H) + '" ' + dims + '><rect width="' + n(W) + '" height="' + n(H) + '" fill="' + o.bg + '"/>' + body;
      var P = sidePanel(g, o, lg);
      if (P.line) s += '<rect x="' + n(P.line.x) + '" y="' + n(P.line.y) + '" width="' + n(P.line.w) + '" height="' + n(P.line.h) + '" fill="' + o.eyec + '"/>';
      if (P.logo) s += '<image href="' + lg.src + '" x="' + n(P.logo.x) + '" y="' + n(P.logo.y) + '" width="' + n(P.logo.w) + '" height="' + n(P.logo.h) + '"/>';
      if (P.lines) P.lines.forEach(function (l) {
        s += '<text x="' + n(P.tx) + '" y="' + n(l.y) + '" font-family="' + e(sideFont().replace(/"/g, "")) + '" font-weight="700" font-size="' + n(P.fs) + '"' + (P.center ? ' text-anchor="middle"' : '') + ' fill="' + o.fg + '">' + e(l.t) + "</text>";
      });
      return s + "</svg>";
    };
  })();
  var _optsBase = opts;
  opts = function () {
    var o = _optsBase();
    o.layout = realLayout(radio("layout")); o.sideText = $("sideText").value;
    if (o.layout !== "center") { o.logo = false; o.label = false; }
    return o;
  };
  var _renderBase = render;
  render = function () {
    _renderBase();
    var lay = realLayout(radio("layout"));
    $("stage").classList.toggle("wide", lay === "wide" || lay === "banner");
    $("sideRow").hidden = lay !== "banner";
  };
  document.querySelectorAll('input[name="layout"]').forEach(function (el) {
    el.addEventListener("change", function () {
      var T = TPL[el.value], p = PLAIN[T.set] || PLAIN[0];
      setRadio("shape", T.shape); setRadio("dot", T.dot); setRadio("eye", T.eye);
      $("fg").value = p.fg; $("eyec").value = T.mono ? p.fg : p.eyec; $("bg").value = p.bg; $("grad").checked = false;
      if (T.fill !== undefined) { $("fill").checked = T.fill; $("ring").checked = T.ring; }
      render();
    });
  });
  $("sideText").addEventListener("input", schedule);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { SIDE_FONT = ""; if (lastGeom) render(); });

