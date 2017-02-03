/**
 * Created by vdjke on 16/10/2015.
 */


var Script = function () {
  function Mayusculas(string) {
    var len = string.length,strip = string.replace(/([A-Z])+/g, '').length, strip2 = string.replace(/([a-zA-Z])+/g, '').length,percent = (len  - strip) / (len - strip2) * 100;
    return percent

  }

    $(document).ready(function() {

        $('#postsForm')

            .find('[name="tags"]')
            // Revalidate the tags field when it is changed
            .change(function (e) {
                $('#postsForm').formValidation('revalidateField', 'tags');
            })
            .end()
            .find('[name="cuerpo"]')
            // Revalidate the content field when it is changed
            .change(function (e) {
                $('#postsForm').formValidation('revalidateField', 'cuerpo');
            })
            .end()
            .formValidation({
            framework: 'bootstrap',
                excluded: ':disabled',
            icon: {
                valid: 'fa fa-check',
                invalid: 'fa fa-times',
                validating: 'fa fa-refresh'
            },
                button:{
                    selector: '#prev',
                    disabled: 'disabled'
                },
            fields: {
                titulo: {

                    validators:{
                        notEmpty:{
                            message: 'El campo titulo es obligatorio'
                        },
                        stringLength: {
                            min: 18,
                            max: 180,
                            message: 'The title must be more than 8 and less than 20 characters long'
                        },
                        callback: {
                          message: 'El t&iacute;tulo no debe estar en may&uacute;sculas',
                          callback: function(value, validator, $field) {
                              if (Mayusculas(value) > 90) {
                                return false;
                              }
                              return true;
                          }
                      }

                    },

                },

                categoria: {
                    validators:{
                        notEmpty:{
                            message: 'El campo categoria es obligatorio'
                        }
                    }
                },
                tags: {
                    validators: {
                        notEmpty: {
                            message: 'El campo tags es obligatorio'
                        },

                        stringLength: {
                            min: 8,
                            max: 100,
                            message: 'El tags debe ser más de 8 y menos de 100 caracteres de longitud'
                        },


                    }
                },
                cuerpo: {
                    validators: {
                        notEmpty: {
                            message: 'El campo contenido del posts es obligatorio'
                        }
                    }
                },

            }
        }).on('success.form.fv', function(e){
                e.preventDefault();
                var $form = $(e.target);
                var fv = $form.data('formValidation');

                fv.disableSubmitButtons(false);

                var params = 'titulo=' + encodeURIComponent(this[name="titulo"].value);
                  params += '&cuerpo=' + encodeURIComponent(this['cuerpo'].value);
                  params += '&categoria=' + encodeURIComponent(this['categoria'].value);
                  params += '&permitir_comentarios=' + encodeURIComponent(this['permitir_comentarios'].value);
                  params += '&tags=' + encodeURIComponent(this['tags'].value);
                  params += '&img_file=' + encodeURIComponent($( "#foto_upload" ).attr( "data-id" ));

                var preview = $("#preview");
                var edicion = $("#edicion");

                $.ajax({
                    url: '/posts/previsualizar/',
                    type: 'POST',
                    data: params,
                    dataType: 'json'
                }).done(function(data){
                    e.preventDefault();
                    bootbox.dialog({
                      size: 'large',
                      title: data.message,
                      message: data.cuerpo
                     });

                }).fail(function(jqXHR, textStatus, errorThrown) {
                    e.preventDefault();
                    
                    var responseText = jQuery.parseJSON(jqXHR.responseText)
                    swal({
                        title: '<small>Error en el posts</small>',
                        text: '<span style="color:#F8BB86">' + responseText + '<span>',
                        html: true
                    });
                    //console.log(responseText);
                })
            })
    });

$(document).ready(function() {
        $('#noticiasEditForm')
            .find('[name="tags"]')
            // Revalidate the tags field when it is changed
            .change(function (e) {
                $('#noticiasForm').formValidation('revalidateField', 'tags');
            })
            .end()
            .find('[name="contenido"]')
            // Revalidate the content field when it is changed
            .change(function (e) {
                $('#noticiasForm').formValidation('revalidateField', 'contenido');
            })
            .end()
            .formValidation({
            framework: 'bootstrap',
                excluded: ':disabled',
            icon: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                titulo: {
                    validators:{
                        notEmpty:{
                            message: 'El campo titulo es obligatorio'
                        },
                        stringLength: {
                            min: 18,
                            max: 180,
                            message: 'The title must be more than 8 and less than 20 characters long'
                        }
                    },

                },
                id: {
                    validators:{
                        notEmpty:{
                            message: 'El campo categoria es obligatorio'
                        }
                    }
                },
                tags: {
                    validators: {
                        notEmpty: {
                            message: 'El campo tags es obligatorio'
                        }
                    }
                },
                contenido: {
                    validators: {
                        notEmpty: {
                            message: 'El campo contenido de la noticia es obligatorio'
                        }
                    }
                },

            }
        })
    });

    $(document).ready(function() {
        $('#CatForm')
            .formValidation({
            framework: 'bootstrap',
                excluded: ':disabled',
            icon: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                name: {
                    validators:{
                        notEmpty:{
                            message: 'El campo nombre es obligatorio'
                        },
                        stringLength: {
                            min: 4,
                            max: 35,
                            message: 'The title must be more than 8 and less than 20 characters long'
                        }
                    },

                }

            }
        })
    });
}();
