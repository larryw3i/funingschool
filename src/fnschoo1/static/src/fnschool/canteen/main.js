$(document).ready(function () {
  $('.canteen-navigation a').each(function (index, element) {
    if (
      $(element).attr('href') ===
      window.location.pathname + window.location.search
    ) {
      $(element).addClass('bg-danger')
    } else {
      $(element).addClass('bg-primary')
    }
  })
})

// The end.
