var Script = function () {
  // body...
  function to_follow(obj) {
    // body...
    var type_id = $( ".follow" ).attr("data-id");
    $.ajax({
      type: 'POST',
      url: '/accounts/follows/',
      dataType: 'json',
      data: 'type_id=' + type_id,

      success: function (data) {
        // body...
      }

    });
  }


  function un_follow(obj) {
    // body...
    var type_id = $( ".follow" ).attr("data-id");
    $.ajax({
      type: 'POST',
      url: '/accounts/unfollow/',
      dataType: 'json',
      data: 'type_id=' + type_id,

      success: function (data) {
        // body...
      }

    });
  }


  $(document).ready(function () {
    // body...
    $('label.to_follow').click(function () {
      // body...
      to_follow($(this));
    })

    $('label.un_follow').click(function () {
      // body...
      un_follow($(this));
    })

  });

}();
