!(function(e) {
  "usestrict";
  e(window).on("load", function() {
    e(
      '[data-loader="circle - side"]'
    ).fadeOut(), e("#preloader").delay(350).fadeOut("slow"), e("body").delay(350).css({ overflow: "visible" });
  });
  var o = e("form#wrapped");
  o.on("submit", function() {
    o.validate(), o.valid() && e("#loader_form").fadeIn();
  }), e("#budget_slider").roundSlider({
    radius: 100,
    min: 20,
    max: 3e3,
    step: 10,
    editableTooltip: !1,
    width: 20,
    handleSize: "+16",
    handleShape: "dot",
    sliderType: "min-range",
    svgMode: !1,
    borderWidth: 1,
    borderColor: "#ededed",
    pathColor: null,
    rangeColor: null,
    tooltipColor: "#333",
    value: 1200
  }), new FloatLabels("form", { style: 1 });
  let d = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  [...d].map(e => new bootstrap.Tooltip(e)), e(
    ".products input"
  ).on("change", function() {
    var o = 0;
    e(".products").find("input:checked").each(function() {
      o += e(this).data("price");
    }), e(".final_price").val("$" + o);
  });
})(window.jQuery);
