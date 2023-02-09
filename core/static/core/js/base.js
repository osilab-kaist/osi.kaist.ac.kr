let $content = null

function adjustContentHeight() {
  // Makes content fill up any remaining space in viewport
  $content.css("padding-bottom", 0);
  // const contentHeight = $content.height();
  const targetPadding = Math.max(0, $(window).innerHeight() - $("body").height());
  $content.css("padding-bottom", targetPadding);
}

$(function () {
  $content = $(".content")
  adjustContentHeight();
  setInterval(adjustContentHeight, 1000, 5);
})

$(window).resize(adjustContentHeight)

