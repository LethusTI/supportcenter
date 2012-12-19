/*
 *  Copyright (C) 2011-2012 Lethus Tecnologia da Informação
 *  <www.lethus.com.br>
 *
 *  Escrito por
 *  Wilson Pinto Júnior (20/12/2011) <wpjunior@lethus.com.br>
 * 
 *  Gerênciador de gráficos
 *
 *  Depênde de:
 *  jquery.js
 *  jquery-ui.js
 *  Algum CharDrawer.js
 */

(function($){
    var ChartManager = function(elem, options)
    {
        this._init(elem, options);
    };

    ChartManager.prototype = {
        constructor: ChartManager,
        _init: function (elem, options) {
            this.elem = $(elem);
            this.options = options;
            this.onLoadInfo = null;
            this.charts = {};
        },
        _loadDataCB: function (data) {
            /*
             * Callback quando os dados são recebidos via ajax
             */

            this.elem.accordion('destroy');
            this.elem.empty();

            if (data.error) {
                $('<b>'+data.error+'</b>').appendTo('#chartinfo');
                return;
            }

            for (key in data)
                this._loadNode(key, data[key], this.elem);

	    this.elem.accordion({
                autoHeight: false,
		navigation: true,
		icons: {
		    header: "ui-icon-circle-arrow-e",
		    headerSelected: "ui-icon-circle-arrow-s"
	        }
	    });
        },
        _loadContainer: function (key, container, parent) {
            /*
             * Desenha e carrega um container
             */
            var cTitle = $('<h3><a href="#">'+container.title+'</a></h3>');
            cTitle.appendTo(parent);
            
            var cElem = $('<div id="'+key+'" class="chartcontainer"></div>');
            cElem.appendTo(parent);

            for (key in container.data)
                this._loadNode(key, container.data[key], cElem);
        },
        _loadField: function (key, field, parent) {
            /*
             * Carrega e desenha um campo
             */
            var id = parent.attr('id') + '_'+key;
            var cElem = $('<div id="'+id+'" title="'+field.title+'" class="chart"></div>');
            cElem.appendTo(parent);
            
            this.charts[id] = $(cElem).chartDrawer({'container': this});
            this.charts[id].load(field.values);
        },
        _loadInfo: function (key, node, parent) {
            this.info = node.data;

            if (this.onLoadInfo) {
                this.onLoadInfo(this.info);
            }
        },
        _loadNode: function (key, node, parent) {
            if (node.type == 'container')
                return this._loadContainer(key, node, parent);
            else if (node.type == 'field')
                return this._loadField(key, node, parent);
            else if (node.type == 'info')
                return this._loadInfo(key, node, parent);
            else
                console.error('unknown node.type');
        },
        load: function (mod, params) {
            var me = this;

            if (params) {
                var vars = {};
                for (var i in params) {
                    vars[i] = params[i];
                }
            } else {
                var vars = {};
            }

            vars.cmd = 'get_data';
            vars.module = mod;

            $.getJSON('.', vars,
                      function (data) {
                          me._loadDataCB(data);
                      });
        }
    };

    $.fn.chartManager = function(options)
    {
        var element = $(this);
	if (element.data('chartManager')) return;
	var manager = new ChartManager(this, options);

        // Store plugin object in this element's data
        element.data('chartManager', manager);
        return manager;
    };
})(jQuery);