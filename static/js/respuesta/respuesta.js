(function ($) {
    var self,base,
        form = {
            init: function () {
                self = this;
                base = $('body');
                self.bindEvents();
            },

            bindEvents: function () {
                base.on('click', '#id_correcta', self.respuestacorrecta);
            },

            respuestacorrecta : function () {
                var value = $(this).attr('data-value');
                swal({
                    buttons: {
                        catch: {
                          text: "Si",
                          value: value,
                        },
                        cancel: true
                    },
                    closeOnClickOutside: false,
                    icon: "warning",
                    text: '¿Está seguro que es la respuesta correcta?'
                }).then(value => {
                    value = value === null ? 0 : parseInt(value);
                    if (parseInt(value) !== 0)
                        return fetch('/pregunta/respuesta_correcta/'+value+'/')
                }).then(results => {
                    return results.json();
                }).then(json => {

                    console.log('json' + json.data);
                    if (json.success) {
                        swal({
                            title: "Tarea Finalizada",
                            text: "éxito esa respuesta será la correcta!",
                            icon: "success",
                            catch: {
                                text: "Aceptar",
                                value: "catch"
                            },
                            cancel: false
                        }).then(value1 => {
                            location.reload();
                        });
                    }

                }).catch(err => {
                      if (err) {
                        swal("Oh noes!", "Error al realizar la solucitud!", "error");
                      } else {
                        swal.stopLoading();
                        swal.close();
                      }
                });
            },
            
        };
    form.init();
})(jQuery);

