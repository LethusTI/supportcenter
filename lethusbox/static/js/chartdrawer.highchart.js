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
        var labelMap = {};
        
        this.draw = function (table) {
            console.info(table);
        }
        this.load = function (data) {
            var newData = [];
            var total = 0.0;
            
            for (var _i=0; _i<data.length; _i++) {
                total += data[_i][1];
                labelMap[data[_i][0]] = data[_i][1];
            }

            for (var _i=0; _i<data.length; _i++) {
                newData.push([data[_i][0], total / data[_i][1]]);
            }

            console.info(total);

            var chart = new Highcharts.Chart({
		chart: {
		    renderTo: document.getElementById(id),
		    plotBackgroundColor: null,
		    plotBorderWidth: null,
		    plotShadow: false,
                    width: 420
		},
		title: {
		    text: $(elem).attr('title')
		},
		tooltip: {
		    formatter: function() {
			return '<b>'+ this.point.name +'</b>: '+ labelMap[this.point.name];
		    }
		},
		plotOptions: {
		    pie: {
			allowPointSelect: true,
			cursor: 'pointer',
			dataLabels: {
			    enabled: true,
			    color: '#000000',
			    connectorColor: '#000000',
			    formatter: function() {
				return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
			    }
			}
		    }
		},
		series: [{
		    type: 'pie',
		    name: 'Browser share',
		    data: newData
		}]
	    });
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