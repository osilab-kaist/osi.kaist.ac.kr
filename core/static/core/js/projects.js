$(function() {
  // $(".collapse")
  // $(".project-summary-toggle")
  $(".project-summary").attr("style", "opacity: 0;");

  $(".project-summary").on("hide.bs.collapse", function() {
    $(this).attr("style", "opacity: 0;");
    const id = $(this).attr("id");
    const toggle = $('.project-summary-toggle[href="#' + id + '"]')
    toggle.text("See More")
  });

  $(".project-summary").on("shown.bs.collapse", function() {
    $(this).attr("style", "opacity: 1;");
  });

  $(".project-summary").on("show.bs.collapse", function() {
    const id = $(this).attr("id");
    const toggle = $('.project-summary-toggle[href="#' + id + '"]')
    toggle.text("See Less")
  })

})