function resizeProjectImages() {
  $(".project-image").css("height", $(".project-image").width() / 16 * 9);
}

$(function() {
  resizeProjectImages();
});

$(window).resize(function () {
  resizeProjectImages();
});