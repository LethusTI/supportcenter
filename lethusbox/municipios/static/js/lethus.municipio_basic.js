(function ($) {
    var MunicipioStore = function (url) {
        this.url = url;
    }
    
    MunicipioStore.prototype = {
        constructor: MunicipioStore,
        findMunicipio: function (uf, callback) {
            $.getJSON(this.url, {cmd: 'find_municipio', uf: uf}, function (data) {
                callback(data);
            });
        }
    };
    

    var MunicipioSelect = function (ufElem, munElem, serviceUrl) {
        var that = this;

        this.store = new MunicipioStore(serviceUrl);
        this.ufSelect = $(ufElem);
        this.munSelect = $(munElem);

        this.ufSelect.change(function (e) {
            e.preventDefault();
            that.loadUf($(this).val());

            return false;
        });
    };

    MunicipioSelect.prototype = {
        constructor: MunicipioSelect,
        loadUf: function (uf) {
            var that = this;

            this.store.findMunicipio(uf, function (data) {
                var pVal = that.munSelect.val();

                that.munSelect
                    .empty()
                    .append('<option value="">----</option>');

                _.each(data, function (row) {
                    that.munSelect.append('<option value="'+row[0]+'">'+row[1]+'</option>');
                });

                if (pVal)
                    that.munSelect.val(pVal);

            });
        }
    };

    window.MunicipioSelect = MunicipioSelect;
})(jQuery); 