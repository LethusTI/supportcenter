/*
 * Widget usado para autocompletar e selecionar municipio
 * escrito por Wilson Júnior 3/10/2012

 * depende de:
 * bootstrap.combobox.js
 */

(function ($) {
    var MunicipioFullCompletion = function (ufElem, munElem, serviceUrl) {
        /*
          Inicia o plugin
          ufElem: elemento (select) que dos estados brasileiros
          munElem: elemento (input) para auto completar os municipios
          serviceUrl: uri usada para buscar os municipios
         */
        var that = this;

        this.ufSelect = $(ufElem);
        this.munSelect = $(munElem);
        this.serviceUrl = serviceUrl;
        this.ufSelect.change(function (e) {
            var val = $(this).val();

            if (val) {
                that.loadMunicipios(val);
            } else {
                that._disableMun();
            }
        });

        this.ufCombobox = this.ufSelect.combobox().data('combobox');
        this.munCombobox = this.munSelect.combobox().data('combobox');
    };

    MunicipioFullCompletion.prototype = {
        constructor: MunicipioFullCompletion,
        _disableMun: function () {
            this.munSelect.val('');
            this.munCombobox.refresh();
        },
        loadMunicipios: function (uf) {
            var _this = this;
            this.munSelect.empty();

            $.getJSON(this.serviceUrl, {cmd: 'get_municipios', uf: uf}, function (data) {
                $('<option value=""></option>').appendTo(_this.munSelect);

                $.each(data, function (i, mun) {
                    $('<option value="'+mun[0]+'">'+mun[1]+'</option>').appendTo(_this.munSelect);
                });

                _this.munCombobox.refresh();
            });
        }
    }

    $.municipioFullCompletion = function (ufElem, munElem, serviceUrl) {
        var obj = new MunicipioFullCompletion(ufElem, munElem, serviceUrl);
        return obj;
    };
})(jQuery);