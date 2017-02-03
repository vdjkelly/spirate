
  var posts = {
    add_puntos: function (puntos) {
      // body..
      var id = $( ".btn-group" ).attr("data-id");

      $.ajax({
        type: 'POST',
        url: '/posts/puntuar/',
        data:'post_id=' + id + '&puntos=' + puntos,
        dataType: 'json',
      }).done(function (data) {
        // body...
        console.log(data);

      }).fail(function (jqXHR, textStatus, errorThrown) {
        // body...
        var responseText = jQuery.parseJSON(jqXHR.responseText)

        swal({
            title: '<small>Error al dar puntos</small>',
            text: '<span style="color:#F8BB86">' + responseText.message + '<span>',
            html: true
        });
      })
    }
  }
