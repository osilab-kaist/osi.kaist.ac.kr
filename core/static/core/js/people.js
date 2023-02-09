$(function () {
  $(".member-image").each(function () {
    $(this).css("height", $(this).width());
  });
})

$(window).resize(function () {
  $(".member-image").each(function () {
    $(this).css("height", $(this).width());
  });
})