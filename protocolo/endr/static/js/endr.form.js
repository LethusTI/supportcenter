(function ($) {
    var EndrStore = function () {};
    
    EndrStore._instance = null;
    EndrStore.getInstance = function () {
        if (!EndrStore._instance)
            EndrStore._instance = new EndrStore();

        return EndrStore._instance;
    };

    EndrStore.prototype = {
        constructor: EndrStore,
        getMunicipios: function (uf, callback) {
            var that = this;

            $.getJSON('.', {cmd: 'get_municipios', uf: uf}, function (municipios) {
                callback.call(that, municipios);
            });
        },
        getDistritos: function (munId, callback) {
            var that = this;

            $.getJSON('.', {cmd: 'get_distritos', mun_id: munId}, function (distritos) {
                callback.call(that, distritos);
            });
        },
        getBairros: function (munId, callback) {
            var that = this;

            $.getJSON('.', {cmd: 'get_bairros', mun_id: munId}, function (bairros) {
                callback.call(that, bairros);
            });
        },
        getDistritoBairros: function (dstId, callback) {
            var that = this;

            $.getJSON('.', {cmd: 'get_distrito_bairros', dst_id: dstId}, function (bairros) {
                callback.call(that, bairros);
            });
        }
    };

    var EndrForm = function (elem) {
        $.fx.off = true;
        var that = this;
        
        this.store = EndrStore.getInstance();
        this.$elem = $(elem);
        this.$selectUf = this.$('#field-uf select');
        this.$selectMun = this.$('#field-mun select');
        this.$selectDistrito = this.$('#field-distrito select');
        this.$selectBairro = this.$('#field-bairro select');

        this.$selectDistrito.change(function (e) {
            var dstId = $(this).val();

            if (dstId) {
                that._loadDistritoBairros(dstId)
            } else {
                var munId = that.$selectMun.val();

                if (munId)
                    that._loadBairros(munId);
                else
                    that._hideBairros();
            }
        });

        this.$selectMun.change(function (e) {
            var munId = $(this).val();

            if (munId) {
                that._loadBairros(munId);
                that._loadDistritos(munId);
            } else {
                that._hideBairros();
                that._hideDistritos();
            }

        });
        
        this.$selectUf.change(function (e) {
            var uf = $(this).val();
            
            if (uf)
                that._loadMunicipios(uf);
            else
                that._hideMuninicipios();

        }).trigger('change');

        this.municipioComboBox = this.$selectMun.combobox().data('combobox');
        this.ufComboBox = this.$selectUf.combobox().data('combobox');
        this.distritoComboBox = this.$selectDistrito.combobox().data('combobox');
        this.bairroComboBox = this.$selectBairro.combobox().data('combobox');
        $.fx.off = false;
    };

    EndrForm.prototype = {
        constructor: EndrForm,
        $: function (name) {
            return this.$elem.find(name);
        },
        _loadMunicipios: function (uf, fn) {
            var that = this;
            
            this.store.getMunicipios(uf, function (municipios) {
                var e = that.$selectMun;
                var oldVal = e.val();

                that.$('#field-mun').removeClass('hide');
                e.empty().append('<option></option>');
                
                _.each(municipios, function (m) {
                    e.append('<option value="'+m[0]+'">'+m[1]+'</option>')
                });

                if (oldVal)
                    e.val(oldVal)

                e.trigger('change');
                that.municipioComboBox.refresh();

                if (fn) {
                    fn.call(that);
                }
            });
        },

        _loadBairros: function (munId, fn) {
            var that = this;

            this.store.getBairros(munId, function (bairros) {
                var e = that.$selectBairro;
                var oldVal = e.val();

                e.empty().append('<option></option>');
                
                _.each(bairros, function (b) {
                    e.append('<option value="'+b[0]+'">'+b[1]+'</option>');
                });

                if (oldVal)
                    e.val(oldVal);

                if (bairros.length > 0)
                    that.$('#field-bairro').removeClass('hide');
                else
                    that.$('#field-bairro').addClass('hide');

                e.trigger('change');
                that.bairroComboBox.refresh();

                if (fn)
                    fn.call(that);
            });
        },
        
        _loadDistritos: function (munId, fn) {
            var that = this;

            this.store.getDistritos(munId, function (distritos) {
                var e = that.$selectDistrito;
                var oldVal = e.val();

                e.empty().append('<option></option>');
                
                _.each(distritos, function (d) {
                    e.append('<option value="'+d[0]+'">'+d[1]+'</option>');
                });

                if (oldVal)
                    e.val(oldVal);

                if (distritos.length > 0)
                    that.$('#field-distrito').removeClass('hide');
                else
                    that.$('#field-distrito').addClass('hide');

                e.trigger('change')
                that.distritoComboBox.refresh();

                if (fn)
                    fn.call(that);
            });
        },
        _loadDistritoBairros: function (dstId, fn) {
            var that = this;

            this.store.getDistritoBairros(dstId, function (bairros) {
                var e = that.$selectBairro;
                var oldVal = e.val();

                e.empty().append('<option></option>');
                
                _.each(bairros, function (b) {
                    e.append('<option value="'+b[0]+'">'+b[1]+'</option>');
                });

                if (oldVal)
                    e.val(oldVal);

                if (bairros.length > 0)
                    that.$('#field-bairro').removeClass('hide');
                else
                    that.$('#field-bairro').addClass('hide');

                e.trigger('change')
                that.bairroComboBox.refresh();
                
                if (fn)
                    fn.call(that);
            });
        },
        _hideBairros: function () {
            this.$selectBairro.empty();
            this.$('#field-bairro').addClass('hide');
        },
        _hideDistritos: function () {
            this.$selectDistrito.empty();
            this.$('#field-distrito').addClass('hide');
        },
        _hideMuninicipios: function () {
            this.$('#field-mun').addClass('hide');
            this.$selectMun.empty().trigger('change');
        },
        fill: function (uf, mun, distrito, bairro) {
            var that = this;
            var selectBairro = function () {
                if (bairro) {
                    that.$selectBairro.val(bairro);
                    that.bairroComboBox.refresh();
                }
            };

            var selectDistrito = function () {
                if (distrito) {
                    that.$selectDistrito.val(distrito);
                    that.distritoComboBox.refresh();

                    that._loadDistritoBairros(distrito, selectBairro);
                } else {
                    that._hideBairros();
                }
            };

            var selectMunicipio = function () {
                if (mun) {
                    that.$selectMun.val(mun);
                    that.municipioComboBox.refresh();
                    
                    that._loadBairros(mun, selectBairro);
                    that._loadDistritos(mun, selectDistrito);
                } else {
                    that._hideBairros();
                    that._hideDistritos();
                }
            };

            if (uf) {
                this.$selectUf.val(uf);
                this.ufComboBox.refresh();
                
                this._loadMunicipios(uf, selectMunicipio);
            }

        }
    };

    $(document).ready(function (e) {
        $('.endr-form').each(function (i, e) {
            var obj = new EndrForm(e);
            $(e).data('endr-form', obj);
        });
    });

})(jQuery);
