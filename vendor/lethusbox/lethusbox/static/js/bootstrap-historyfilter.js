
// Objeto para manusear o filtro de historico

(function($){
    var HFilter = function(element)
    {
        
	var elem = $(element);
	var obj = this;

        var dates = $( "#id_from_date, #id_to_date" ).datepicker();
        function setActions (mod) {
            if (!mod) {
                $("#action").slideUp();
                return;
            }
            $("#action").slideDown();

            $.getJSON('.', {cmd: 'get_action_list',
                            module: mod},
                      function (data) {
                          $('#id_action').empty();

                          for (i=0; i<data.length; i+=1) {
                              var obj = data[i];
                              $('<option value="'+obj[0]+'">'+obj[1]+'</option>').appendTo('#id_action');
                          }
                      });
        }

	setActions($("#id_module").val());

	$("#id_module").change(function (e) {
	    var mod = $("#id_module").val();
	    setActions(mod);
	    elem.trigger('submit');
	});
	
	$("#id_action").change(function (e) {
	    elem.trigger('submit');
	});

	elem.change(function (e) {
	    elem.trigger('submit');
	});

    }
    $.fn.hfilter= function(options)
    {
	var element = $(this);
	
	// Return early if this element already has a plugin instance
	if (element.data('hfilter')) return;
	var hfilter = new HFilter(this, options);

        // Store plugin object in this element's data
        element.data('hfilter', hfilter);
        return hfilter;
    };
})(jQuery);
