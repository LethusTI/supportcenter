(function($){
    var ChartManager = function(elem, options)
    {
	/*
	  classe utilizada para gerenciar graficos
	*/
        var obj = $(elem);
        this.options = options
        var charts = {};
        this.info = {};
        var self = this;

        _loadDataCB = function (data) {
            obj.accordion('destroy');
            obj.empty();

            _loadContainer = function (key, container, parent) {
                var cTitle = $('<h3><a href="#">'+container.title+'</a></h3>');
                cTitle.appendTo(parent);
                
                var cElem = $('<div id="'+key+'" class="chartcontainer"></div>');
                cElem.appendTo(parent);

                for (key in container.data)
                    _loadNode(key, container.data[key], cElem);
            }
            _loadField = function (key, field, parent) {
                var id = parent.attr('id') + '_'+key;
                var cElem = $('<div id="'+id+'" title="'+field.title+'" class="chart"></div>');
                cElem.appendTo(parent);
               
                charts[id] = $(cElem).chartDrawer({'container': self});
                charts[id].load(field.values);
            }
            _loadInfo = function (key, node, parent) {
                self.info = node.data;
            }
            _loadNode = function (key, node, parent) {
                if (node.type == 'container')
                    return _loadContainer(key, node, parent);
                else if (node.type == 'field')
                    return _loadField(key, node, parent);
                else if (node.type == 'info')
                    return _loadInfo(key, node, parent);
                else
                    console.error('unknown node.type');
            }
            
            
            if (data.error != undefined) {
                $('<b>'+data.error+'</b>').appendTo('#chartinfo');
                return;
            }

            for (key in data)
                _loadNode(key, data[key], obj);

	    obj.accordion({
                autoHeight: false,
		navigation: true,
		icons: {
		    header: "ui-icon-circle-arrow-e",
		    headerSelected: "ui-icon-circle-arrow-s"
	        }
	    });
        }
        
        this.loadData = function () {
            $.getJSON('.', {cmd: 'get_data',
                            module: options.getModule()},
                      _loadDataCB);
        }
        this.loadData();
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