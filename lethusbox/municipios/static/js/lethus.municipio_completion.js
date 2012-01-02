/*
 * Widget usado para autocompletar e selecionar municipio
 * escrito por Wilson Júnior 9/12/2011

 * depende de:
 * jquery.ui.combobox.js
 */

(function ($) {
    var MunicipioCompletion = function (ufElem, munElem, serviceUrl) {
        /*
          Inicia o plugin
          ufElem: elemento (select) que dos estados brasileiros
          munElem: elemento (input) para auto completar os municipios
          serviceUrl: uri usada para buscar os municipios
         */
        this._init(ufElem, munElem, serviceUrl);
    };

    MunicipioCompletion.prototype._init = function (ufElem, munElem, serviceUrl) {
        
        var me = this;

        this.ufSelect = $(ufElem);
        this.munSelect = $(munElem);

        this.ufSelect.combobox({
            selected: function (e) {
                if ($(this).val())
                    me._enableMun();
                else
                    me._disableMun();
            },
            cleaned: function (e) {
                me._disableMun();
            }
        });
        this.munSelect.autocomplete({
	    minLength: 2,
            source: function( request, response ) {
		var term = request.term;
                var uf = me.ufSelect.val();

                $.getJSON(
                    serviceUrl,
                    {cmd: 'get_autocomplete_city',
                     uf: uf, term: term},
                    function (data) {
                        if (data.error) {
                            alert(data.error);
                            response([]);
                        }
                        response(data.values);
                    });
            }
	});

        if (!this.ufSelect.val())
            this._disableMun();
    }
    MunicipioCompletion.prototype._enableMun = function () {
        this.munSelect.removeAttr('disabled').animate({opacity: 1});
    }
    
    MunicipioCompletion.prototype._disableMun = function () {
        this.munSelect
            .val('')
            .attr('disabled', true)
            .animate({opacity: 0.4});
    }
    
    $.municipioCompletion = function(ufElem, munElem, serviceUrl) {
        var obj = new MunicipioCompletion(ufElem, munElem, serviceUrl);
        return obj;
    };
})(jQuery);