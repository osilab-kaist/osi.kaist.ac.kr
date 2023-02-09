const $grid = $('.grid').packery({
  itemSelector: '.grid-item',
  columnWidth: '.grid-sizer',
  // percentPosition: true,
  // horizontalOrder: false,
  // fitWidth: true
});

setInterval(function() {
  $('.grid').packery();
}, 2000, 10);