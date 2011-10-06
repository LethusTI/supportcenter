(function($){
    var TANGO_COLORS = ['#a40000',
                        '#8f5902', '#4e9a06', '#204a87', '#5c3566',
                        '#75507b', '#cc0000', '#c4a000', '#ce5c00',
                        '#f57900', '#c17d11', '#73d216', '#3465a4',
                        '#729fcf', '#ad7fa8', '#ef2929', '#edd400',
                        '#fce94f', '#fcaf3e', '#e9b96e', '#8ae234',
                        ]

    var ChartDrawer = function(elem, options)
    {
	/*
	  classe utilizada para desenhar graficos usando o google api
	*/
        var id = $(elem).attr('id');
        var _chart = null;
        
         
        this.draw = function (table) {
            if (!_chart)
                _chart = new google.visualization.PieChart(document.getElementById(id));

            _chart.draw(table, {width: 420, height: 240, title: $(elem).attr('title'),
                              colors: TANGO_COLORS});
        }
        this.load = function (data) {
            var table = new google.visualization.DataTable();
            table.addColumn('string', 'Name');
            table.addColumn('number', 'Value');
            for (i=0; i<data.length; i+=1) {
                table.addRow(data[i]);
            }
            this.draw(table);
        }
    };
    $.fn.chartDrawer = function(options)
    {

	var element = $(this);
	
	// Return early if this element already has a plugin instance
	if (element.data('chartDrawer')) return;
	var drawer = new ChartDrawer(this, options);

        // Store plugin object in this element's data
        element.data('chartDrawer', drawer);
        return drawer;
    };
})(jQuery);