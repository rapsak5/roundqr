  // Levende miniaturer af de tre skabeloner med det aktuelle link
  var thumbTimer = null, thumbCv = document.createElement("canvas");
  function drawThumbs() {
    if (!lastText) return;
    ["center", "wide", "banner", "round"].forEach(function (key) {
      var T = TPL[key], p = PLAIN[T.set] || PLAIN[0], o = _optsBase();
      o.shape = T.shape; o.dot = T.dot; o.eye = T.eye; o.fg = p.fg; o.eyec = T.mono ? p.fg : p.eyec; o.bg = p.bg; o.grad = false;
      o.layout = realLayout(key); o.sideText = $("sideText").value; o.label = false; o.fill = !!T.fill; o.ring = !!T.ring;
      if (o.layout !== "center") o.logo = false;
      try {
        var g = RQ.geometry(lastText, o);
        RQ.toCanvas(thumbCv, g, o, logo, (key === "wide" || key === "banner") ? 720 : 360);
        $("th-" + key).src = thumbCv.toDataURL("image/png");
      } catch (e) {}
    });
  }
  var _renderThumbs = render;
  render = function () { _renderThumbs(); clearTimeout(thumbTimer); thumbTimer = setTimeout(drawThumbs, 150); };
