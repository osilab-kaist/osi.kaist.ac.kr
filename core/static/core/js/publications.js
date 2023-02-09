let selectedYears = [];
let selectedTypes = [];
let selectedAreaIds = [];

function applySelections() {
  $("#filter-reset").hide();

  if (selectedYears.length) {
    $("#filter-year-toggle").addClass("active")
    $("#filter-reset").show();
  } else {
    $("#filter-year-toggle").removeClass("active")
  }

  if (selectedTypes.length) {
    $("#filter-type-toggle").addClass("active")
    $("#filter-reset").show();
  } else {
    $("#filter-type-toggle").removeClass("active")
  }

  if (selectedAreaIds.length) {
    $("#filter-area-toggle").addClass("active")
    $("#filter-reset").show();
  } else {
    $("#filter-area-toggle").removeClass("active")
  }

  $(".section").each(function () {
    $(this).show();
  });

  $(".publication").each(function () {
    $(this).show();
    if (selectedYears.length) {
      const year = $(this).attr("data-year");
      if (!selectedYears.includes(year)) {
        $(this).hide();
      }
    }

    if (selectedTypes.length) {
      const type = $(this).attr("data-type");
      if (!selectedTypes.includes(type)) {
        $(this).hide();
      }
    }

    if (selectedAreaIds.length) {
      $(this).hide();
      const areaIds = $(this).attr("data-area-ids").split(" ");
      for (const i in areaIds) {
        if (selectedAreaIds.includes(areaIds[i])) {
          $(this).show();
        }
      }
    }
  });

  $(".section").each(function () {
    if ($(this).find(".publication:visible").length === 0) {
      $(this).hide();
    }
  });
}

function resetSelections() {
  $("input.filter-year").prop("checked", false);
  $("input.filter-area").prop("checked", false);
  $("input.filter-type").prop("checked", false);

  selectedYears = [];
  selectedTypes = [];
  selectedAreaIds = [];
}

$(function () {
  $("input.filter-year").change(function () {
    const year = $(this).attr("data-year");
    if (this.checked) {
      if (!selectedYears.includes(year)) {
        selectedYears.push(year)
      }
    } else {
      const index = selectedYears.indexOf(year);
      if (index > -1) {
        selectedYears.splice(index, 1); // 2nd parameter means remove one item only
      }
    }
    applySelections();
  });

  $("input.filter-type").change(function () {
    const type = $(this).attr("data-type");
    if (this.checked) {
      if (!selectedTypes.includes(type)) {
        selectedTypes.push(type)
      }
    } else {
      const index = selectedTypes.indexOf(type);
      if (index > -1) {
        selectedTypes.splice(index, 1); // 2nd parameter means remove one item only
      }
    }
    applySelections();
  });

  $("input.filter-area").change(function () {
    const areaId = $(this).attr("data-area-id");
    if (this.checked) {
      if (!selectedAreaIds.includes(areaId)) {
        selectedAreaIds.push(areaId)
      }
    } else {
      const index = selectedAreaIds.indexOf(areaId);
      if (index > -1) {
        selectedAreaIds.splice(index, 1); // 2nd parameter means remove one item only
      }
    }
    applySelections();
  });

  $("#filter-reset").click(function () {
    resetSelections();
    applySelections();
  });

})