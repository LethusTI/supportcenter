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


    var MunicipioFullCompletion = function (ufElem, munElem, serviceUrl) {
        /*
          Inicia o plugin
          ufElem: elemento (select) que dos estados brasileiros
          munElem: elemento (input) para auto completar os municipios
          serviceUrl: uri usada para buscar os municipios
         */
        this._init(ufElem, munElem, serviceUrl);
    };

    MunicipioFullCompletion.prototype._init = function (ufElem, munElem, serviceUrl) {
        /*
         *
         * Plugin de auto-completion para todas as cidades do brasil.
         */
        
        var _this = this;

        this.ufSelect = $(ufElem);
        this.munSelect = $(munElem);
        this.serviceUrl = serviceUrl;
        this.ufSelect.combobox({
            selected: function (e) {
                var val = $(this).val();

                if (val) {
                    _this._enableMun();
                    _this.loadMunicipios(val)
                } else {
                    _this._disableMun();
                }
            },
            cleaned: function (e) {
                _this._disableMun();
            }
        }).trigger('selected');

        this.munSelect.combobox({
            selected: function (e) {
            },
            cleaned: function (e) {
            }
        });
    };
    

    MunicipioFullCompletion.prototype.loadMunicipios = function (uf) {
        var _this = this;

        this.munSelect.empty();
        this.munSelect.trigger('change')
            .combobox('reselect');
        $.getJSON(
            this.serviceUrl,
            {cmd: 'get_cities_brasil',
             id: uf},
            function (data) {
                for (var _i=0; _i < data.length; _i++) {
                    var mun = data[_i];

                    $('<option value="'+mun[0]+'">'+mun[1]+'</option>').appendTo(_this.munSelect);
                }
            });
    };

    MunicipioFullCompletion.prototype._disableMun = function () {
        this.munSelect
            .val('')
            .attr('disabled', true)
            .animate({opacity: 0.4});
    };

    MunicipioFullCompletion.prototype._enableMun = function () {
        this.munSelect.removeAttr('disabled').animate({opacity: 1});
    };

    $.municipioCompletion = function(ufElem, munElem, serviceUrl) {
        var obj = new MunicipioCompletion(ufElem, munElem, serviceUrl);
        return obj;
    };

    $.municipioFullCompletion = function (ufElem, munElem, serviceUrl) {
        var obj = new MunicipioFullCompletion(ufElem, munElem, serviceUrl);
        return obj;
    };
})(jQuery);