function moveCopyrightToBotttom() {
  const margin = window.innerHeight - $(".copyright-top").offset().top;
  if (margin > 32) {
    $(".copyright").css("padding-top", margin - 32 + "px");
  }
}

$(function () {
  moveCopyrightToBotttom();
});

$(window).resize(function () {
  moveCopyrightToBotttom();
});

$(window).on("wheel", function() {
  moveCopyrightToBotttom();
});