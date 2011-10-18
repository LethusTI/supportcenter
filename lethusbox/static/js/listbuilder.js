/*
  Builder de listas em ajax
  com suporte para paginação, ajax, pdf e csv
*/

//Object Oriented via jQuery



(function($){
    jQuery.fn.dataTableExt.oApi.fnSetFilteringDelay = function ( oSettings, iDelay ) {
	/*
	 * Inputs:      object:oSettings - dataTables settings object - automatically given
	 *              integer:iDelay - delay in milliseconds
	 * Usage:       $('#example').dataTable().fnSetFilteringDelay(250);
	 * Author:      Zygimantas Berziunas (www.zygimantas.com) and Allan Jardine
	 * License:     GPL v2 or BSD 3 point style
	 * Contact:     zygimantas.berziunas /AT\ hotmail.com
	 */
	
	var
	_that = this,
	iDelay = (typeof iDelay == 'undefined') ? 1000 : iDelay;
	
	$(this).each( function ( i ) {
	    $.fn.dataTableExt.iApiIndex = i;
	    var
	    $this = this, 
	    oTimerId = null, 
	    sPreviousSearch = null,
	    anControl = $( 'input', _that.fnSettings().aanFeatures.f );
	    
	    anControl.unbind( 'keyup' ).bind( 'keyup', function() {
		var $$this = $this;

		if (sPreviousSearch === null || sPreviousSearch != anControl.val()) {
		    window.clearTimeout(oTimerId);
		    sPreviousSearch = anControl.val();	
		    oTimerId = window.setTimeout(function() {
			$.fn.dataTableExt.iApiIndex = i;
			_that.fnFilter( anControl.val() );
		    }, iDelay);
		}
	    });
	    
	    return this;
	} );
	return this;
   
    }

    var ToolBar = function(element, list)
    {
	/*
	  classe utilizada para gerenciar a barra de tarefas de uma lista
	*/
	var elem = $(element);
	var obj = this;
	var list = list;

	var actionUrl = '.';

	// busca por todos buttons que possuem o attributo rev para setar como icone
        elem.find(".button-icon").each(function (idx, obj) {
            var icon = $(obj).attr('rev');
            $(obj).button({ icons: {primary: icon}});
        });
	
        $('.alone-action, .many-action').hide();

	$("a.alone-action").click (function (e) {
	    e.preventDefault();
	    var url =  $(this).attr('href').replace('%d', list.getSeletedIds()[0]);

	    if ($(this).hasClass('modal')) {
		$("#dialog").ifdialog(url, {
		    onClose: function (obj) {
			list.reload();
		    }
		});
	    } else {
		window.location.href = url;
	    }
	    return false;
	});

	function onReloadCB(data) {
	    if (data.error) {
		$.message(data.error, 'error');
		return;
	    }
	    list.reload();
	}
	
        $('#post-delete').click(function (e) {
	    ids = list.getSeletedIds();
	    
	    if (ids.length == 0) {
		return
	    }

	    if (ids.length == 1) {
		var msg = "Tem certeza que deseja apagar esse registro ?"
	    } else {
		var msg = "Tem certeza que deseja apagar esses "+ids.length+" registros ?";
	    }
	    
	    $('#dialog-confirm').attr('title', "Aviso");
	    $('#dialog-confirm #message').text(msg);
	    $( "#dialog-confirm" ).dialog({
		resizable: false,
		height:160,
		modal: true,
		buttons: {
		    "Cancelar": function() {
			$( this ).dialog( "close" );
		    },
		    "Apagar": function() {
			$( this ).dialog( "close" );
			$.post(actionUrl,
                               {'cmd': 'mass_delete', 'ids': ids},
                               onReloadCB);
		    }
		}
	    });
	});

	$('#set-active').click (function (e) {
	    e.preventDefault();
	    ids = list.getSeletedIds();

	    if (ids.length == 0) {
		return
	    }

	    $.post(actionUrl, {'cmd': 'set_active', 'ids': ids}, onReloadCB);
	    return false;
	});

	$('#set-inactive').click (function (e) {
	    e.preventDefault();
	    ids = list.getSeletedIds();

	    if (ids.length == 0) {
		return
	    }

	    $.post(actionUrl, {'cmd': 'set_inactive', 'ids': ids}, onReloadCB);
	    return false;
	});
    }

    var ListBuilder = function(element, options)
    {
	/*
	  Gerador de Lista
	  com paginação, toolbar e seachfilter
	*/
	var elem = $(element);
	var obj = this;

	// Merge options with defaults
	this.settings = $.extend({
            form: null,
            listFormat: [],
            toolbar: "#toolbar",
	    selectable: true,
	    hiddenId: true,
	    serverSide: true,
	    filterSuport: true,
            scrollY: 500,
            iDisplayLength: 10,
            paginate: true,
            lengthChange: true,
	}, options || {});

	var gaiSelected =  []; //guarda os selecionados em cache
        
	this.reload = function () {
	    obj.oTable.fnDraw();
	    updateChecker();
	}

        this.getSeletedIds = function () {
            /* funcao pública usada para coletar as rows selecionadas */
	    objs = elem.find('tr.row_selected');
	    ids = [];

            objs.each(function (i) {
		ids[ids.length] = obj.oTable.fnGetData(objs[i])[0];
	    });
	    return ids;
	}

	function updateChecker() {
	    // atualiza os itens do toolbar
	    var len = obj.getSeletedIds().length;
	    if (len<1) {
		$('.alone-action').hide();
		$('.many-action').hide();
	    } else if (len== 1) {
		$('.alone-action').show();
		$('.many-action').show();
	    }
	    else {
		$('.alone-action').hide();
		$('.many-action').show();
	    }
	}

	this.init = function () {
	    // configura os rendering para booleans e email
	    var aoColumnDefs = [];
	    var aaSorting = [];
            var linkColumns = {};
	    var classColumn = -1;
	    ths = elem.find("thead th"); // todas colunas
	    data = elem.find('thead th.boolean'); // colunas que sao do tipo boolean

	    if (data) {
		var cols = [];
		
		data.each(function (i, col) {
		    // preenche uma list com todas essas colunas
		    cols[cols.length] = ths.index(col);
		});

		aoColumnDefs.push({
		    "fnRender": function ( oObj ) {
			if (oObj.aData[oObj.iDataColumn]) 
			    return '<span class="ui-icon ui-icon-check" />';
			else
			    return '<span class="ui-icon ui-icon-close" />';
		    },
		    "aTargets": cols
		});
	    }

            data = elem.find('thead th.right');
            if (data) {
                var cols = [];
		
		data.each(function (i, col) {
		    // preenche uma list com todas essas colunas
		    cols[cols.length] = ths.index(col);
		});

		aoColumnDefs.push({
                    "sClass": "right",
		    "aTargets": cols
		});
            }

	    data = elem.find('thead th.email');
	    if (data) {
		var cols = [];
		data.each(function (i, col) {
		    cols[cols.length] = ths.index(col);
		});
		aoColumnDefs.push({
		    "fnRender": function ( oObj ) {
			return $.buildEmail(oObj.aData[oObj.iDataColumn]);
		    },
		    "aTargets": cols
		});
	    }

	    data = elem.find('thead th.sort-desc');
	    if (data) {
		data.each(function (i, col) {
		    aaSorting.push([ths.index(col), 'desc']);
		});
	    }
	    
	    data = elem.find('thead th.sort-asc');
	    if (data) {
		data.each(function (i, col) {
		    aaSorting.push([ths.index(col), 'asc']);
		});
	    }

	    data = elem.find('thead th.class');
	    if (data) {
		classColumn = ths.index(data.first());
	    }

            data = elem.find('thead th.link');
	    if (data) {
                var cols = [];
		data.each(function (i, col) {
                    var index= ths.index(col);
                    var rel = parseInt($(col).attr('rel'));

                    cols.push(rel);
                    linkColumns[rel] = index;
		});

                aoColumnDefs.push({
		    "fnRender": function ( oObj ) {
                        var linkColumn = linkColumns[oObj.iDataColumn];
                        var linkData = oObj.aData[linkColumn];
                        var colData = oObj.aData[oObj.iDataColumn];

                        if (linkData)
                            return '<a href="'+linkData+'">'+colData+'</a>';
                        
                        return colData;
		    },
		    "aTargets": cols
		});
	    }

	    // configura o datatable
	    var params = {
		"bJQueryUI": true,
		"sScrollY": obj.settings.scrollY,
		"sPaginationType": "full_numbers",
		"iDisplayLength": obj.settings.iDisplayLength,
		"bServerSide": obj.settings.serverSide,
		"bFilter": obj.settings.filterSuport,
                "bLengthChange": obj.settings.lengthChange,
                "bPaginate": obj.settings.paginate,
		"aoColumnDefs": aoColumnDefs,
		"aaSorting": aaSorting,
		"fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
		    // atribui a coluna de classe
		    if (classColumn > -1) {
			$(nRow).addClass(aData[classColumn]);
		    }

		    // busca pelo cache de linhas selecionadas
		    if ( jQuery.inArray(aData[0], gaiSelected) != -1 )
		    {
			$(nRow).addClass('row_selected');
		    }
		    return nRow;
		    
		},
		
		"oLanguage": {
		    "sProcessing":   "Processando...",
		    "sLengthMenu":   "Mostrar _MENU_ registros",
		    "sZeroRecords":  "Não foram encontrados resultados",
		    "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
		    "sInfoEmpty":    "Mostrando de 0 até 0 de 0 registros",
		    "sInfoFiltered": "(filtrado de _MAX_ registros no total)",
		    "sInfoPostFix":  "",
		    "sSearch":       "Buscar:",
		    "sUrl":          "",
		    "oPaginate": {
			"sFirst":    "Primeiro",
			"sPrevious": "Anterior",
			"sNext":     "Seguinte",
			"sLast":     "Último"
		    }
		}
	    };
            if (obj.settings.serverSide) {
                params["sAjaxSource"] =  ".";
                params["fnServerData"] = function ( sSource, aoData, fnCallback ) {
		    aoData.push( { "name": "format", "value": "data"});

		    if (obj.settings.form) { // se tiver filtro usa-o
		        aoData = $.merge(aoData, $(obj.settings.form).serializeArray());
		    }

		    if (obj.settings.getExtraData) { // função para pegar dados extra
		        aoData = $.merge(aoData, obj.settings.getExtraData());
		    }

		    $.getJSON( sSource, aoData, function (json) {
		        // Busca Mensagens do Django
		        if ((json.messages) && (json.messages.length>0)) {
			    for (i=0; i<json.messages.length; i=i+1) {
			        msg = json.messages[i];
			        $.message(msg.message, msg.tags);
			    }
		        }

		        fnCallback(json);
		    });
	        };
            };
	    obj.oTable = elem.dataTable(params).fnSetFilteringDelay();

	    // esconder a coluna class
	    if (classColumn > -1) {
		obj.oTable.fnSetColumnVis(classColumn, false);
	    }
	    
	    if (obj.settings.hiddenId)
		obj.oTable.fnSetColumnVis(0, false); //esconde a coluna de ids

            if (linkColumns) {
                for (i in linkColumns)
                    obj.oTable.fnSetColumnVis(linkColumns[i], false);
            }
            

	    // Função de Clicicke
	    if (obj.settings.selectable) {
		elem.find('tbody tr').live('click', function (event) {
		    event.preventDefault();
		    var aData = obj.oTable.fnGetData( this );
		    if (!aData)
			return;
		    
		    var iId = aData[0];
		    
                    var index = jQuery.inArray(iId, gaiSelected);
		    if (index == -1 )
			gaiSelected.push(iId);
		    else
                        gaiSelected.splice(index, 1);
		    
		    if (!event) { var event = window.event; }
		    var target = event.target ? event.target : event.srcElement;

		    if ($(target).is('a')) {
			return;
		    }

		    if (!event.ctrlKey) {
			elem.find('tbody tr.row_selected').removeClass('row_selected');
		    }
		    $(this).toggleClass('row_selected');
		    updateChecker();
		    return false;
		}).live('dblclick', function (event) {
		    event.preventDefault()
		    $('a.dblclick').trigger('click');
		    return false;
		});
	    }

	    // usada para destruir a lista
	    obj.destroy = function () {
		if (obj.oTable) {
		    obj.oTable.fnDestroy();
		    obj.oTable = null;
		}
		elem.find('tbody tr').empty();
	    }

	    // append toolbar2
	    
	    $('.fg-toolbar').first().append($('#toolbar2').remove());
	    $('#select-all').click(function(e) {
		e.preventDefault();
		elem.find('tbody tr').addClass('row_selected');
		updateChecker();
		return false;
	    });
	    
	    $('#select-none').click(function(e) {
		e.preventDefault();
		elem.find('tbody tr.row_selected').removeClass('row_selected');
		updateChecker();
	    });
	}

	$(obj.settings['form']).submit(function (e) {
	    e.preventDefault();
	    obj.reload();
	    return false;
	});

	$(obj.settings['output']).click (function (e) {

	    var params = $(obj.settings['form']).serializeJSON();
	    var url = $(obj.settings['form']).attr('action');

	    params['format'] = $(this).attr('rel');

	    // TODO: pegar sorting and filter do datatable
	    window.location.href = url + '?'+ $.param(params);
	    return false;
	});

	obj.init(); // inicia o plugin
	var toolbar = new ToolBar(obj.settings.toolbar, obj); // inicia o toolbar

    };

    $.fn.listbuilder = function(options)
    {

	var element = $(this);
	
	// Return early if this element already has a plugin instance
	if (element.data('listbuilder')) return;
	var listbuilder = new ListBuilder(this, options);

        // Store plugin object in this element's data
        element.data('listbuilder', listbuilder);
        return listbuilder;
    };
})(jQuery);
