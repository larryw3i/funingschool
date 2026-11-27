$(document).ready(function () {
  $('.canteen-navigation a').each(function (index, element) {
    console.log($(element).attr('href'))
    console.log(window.location.pathname, window.location.search)

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
