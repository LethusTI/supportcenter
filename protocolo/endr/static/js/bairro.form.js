(function ($) {
    var BairroForm = function () {
        $.fx.off = true;
        var that = this;
        
        $('#id_mun').change(function (e) {
            var munId = $(this).val();

            if (munId) {
                $('#field-distrito').slideDown()
                that.loadMunicipio(munId);
            } else {
                $('#field-distrito').slideUp()
            }

        }).trigger('change');

        $('#id_uf').change(function (e) {
            var uf = $(this).val();
            
            if (uf) {
                $('#field-mun').slideDown()
                that.loadUf(uf);
            } else {
                $('#field-mun').slideUp()
                that.cleanMuninicipios();
            }
        }).trigger('change');

        this.municipioComboBox = $('#id_mun').combobox().data('combobox');
        this.ufComboBox = $('#id_uf').combobox().data('combobox');
        this.distritoRelationBox = $('#id_distrito_select').relationbox({input: '#id_distrito_nome'}).data('relationbox');
        $.fx.off = false;
    };

    BairroForm.prototype = {
        constructor: BairroForm,
        loadUf: function (uf) {
            var that = this;

            $.getJSON('.', {cmd: 'get_municipios', uf: uf}, function (municipios) {
                var e = $('#id_mun');
                var oldVal = e.val();

                e.empty().append('<option></option>');

                
                _.each(municipios, function (m) {
                    e.append('<option value="'+m[0]+'">'+m[1]+'</option>')
                });

                if (oldVal)
                    e.val(oldVal)

                that.municipioComboBox.refresh();
            });
        },
        cleanMuninicipios: function () {
            $('#id_mun').empty();
        },
        loadMunicipio: function (munId) {
            var that = this;

            $.getJSON('.', {cmd: 'get_distritos', mun_id: munId}, function (distritos) {
                var e = $('#id_distrito_select');
                var oldVal = e.val();

                e.empty().append('<option></option>');

                
                _.each(distritos, function (d) {
                    e.append('<option value="'+d[0]+'">'+d[1]+'</option>');
                });

                if (oldVal)
                    e.val(oldVal);

                that.distritoRelationBox.refresh();
            });
        }
    };

    $(document).ready(function (e) {
        window.bairroForm = new BairroForm();
    });
    
})(jQuery);