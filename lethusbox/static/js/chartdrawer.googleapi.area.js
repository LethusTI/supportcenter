(function($){
    var ChartDrawer = function(elem, options)
    {
	/*
	  classe utilizada para desenhar graficos usando o google api
	*/
        var id = $(elem).attr('id');
        var _chart = null;
        var options = options;
         
        this.draw = function (table) {
            if (!_chart)
                _chart = new google.visualization.LineChart(document.getElementById(id));

            _chart.draw(table, {width: 420, height: 240, title: $(elem).attr('title'),
                                colors: ['#cc0000',
                                         '#73d216',
                                         '#75507b',
                                         '#edd400',
                                         '#f57900',
                                         '#3465a4']});
        }
        this.load = function (data) {
            labels = [];
            for (k in data) {
                labels.push(k);
            }

            var table = new google.visualization.DataTable();
            table.addColumn('string', 'Período');

            for (var i=0; i<labels.length; i+=1) {
                table.addColumn('number', labels[i]);
            }
            var periods = options.container.info.periods;

            for (var i=0; i<periods.length; i+=1) {
                var prd = periods[i];
                var row = [];
                
                row.push(prd);
                
                for (k in data) {
                    if (data[k][i]) 
                        row.push(data[k][i]);
                    else
                        row.push(0);
                }
                table.addRow(row);
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