$(function () {
  $(".photos").magnificPopup({
    delegate: "a.photo-image-link", // child items selector, by clicking on it popup will open
    type: "image",
  });

  $(".photo-image").css("height", $(".photo-image").width());
})

$(window).resize(function () {
  $(".photo-image").css("height", $(".photo-image").width());

})