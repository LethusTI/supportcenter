/* Set the defaults for DataTables initialisation */
$.extend( true, $.fn.dataTable.defaults, {
	"sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
	"sPaginationType": "bootstrap",
	"oLanguage": {
		"sLengthMenu": "_MENU_ records per page"
	}
} );


/* Default class modification */
$.extend( $.fn.dataTableExt.oStdClasses, {
	"sWrapper": "dataTables_wrapper form-inline"
} );


/* API method to get paging information */
$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
	return {
		"iStart":         oSettings._iDisplayStart,
		"iEnd":           oSettings.fnDisplayEnd(),
		"iLength":        oSettings._iDisplayLength,
		"iTotal":         oSettings.fnRecordsTotal(),
		"iFilteredTotal": oSettings.fnRecordsDisplay(),
		"iPage":          Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
		"iTotalPages":    Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
	};
};


/* Bootstrap style pagination control */
$.extend( $.fn.dataTableExt.oPagination, {
	"bootstrap": {
		"fnInit": function( oSettings, nPaging, fnDraw ) {
			var oLang = oSettings.oLanguage.oPaginate;
			var fnClickHandler = function ( e ) {
				e.preventDefault();
				if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
					fnDraw( oSettings );
				}
			};

			$(nPaging).addClass('pagination').append(
				'<ul>'+
					'<li class="prev disabled"><a href="#">&larr; '+oLang.sPrevious+'</a></li>'+
					'<li class="next disabled"><a href="#">'+oLang.sNext+' &rarr; </a></li>'+
				'</ul>'
			);
			var els = $('a', nPaging);
			$(els[0]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
			$(els[1]).bind( 'click.DT', { action: "next" }, fnClickHandler );
		},

		"fnUpdate": function ( oSettings, fnDraw ) {
			var iListLength = 5;
			var oPaging = oSettings.oInstance.fnPagingInfo();
			var an = oSettings.aanFeatures.p;
			var i, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);

			if ( oPaging.iTotalPages < iListLength) {
				iStart = 1;
				iEnd = oPaging.iTotalPages;
			}
			else if ( oPaging.iPage <= iHalf ) {
				iStart = 1;
				iEnd = iListLength;
			} else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
				iStart = oPaging.iTotalPages - iListLength + 1;
				iEnd = oPaging.iTotalPages;
			} else {
				iStart = oPaging.iPage - iHalf + 1;
				iEnd = iStart + iListLength - 1;
			}

			for ( i=0, iLen=an.length ; i<iLen ; i++ ) {
				// Remove the middle elements
				$('li:gt(0)', an[i]).filter(':not(:last)').remove();

				// Add the new list items and their event handlers
				for ( j=iStart ; j<=iEnd ; j++ ) {
					sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
					$('<li '+sClass+'><a href="#">'+j+'</a></li>')
						.insertBefore( $('li:last', an[i])[0] )
						.bind('click', function (e) {
							e.preventDefault();
							oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
							fnDraw( oSettings );
						} );
				}

				// Add / remove disabled classes from the static elements
				if ( oPaging.iPage === 0 ) {
					$('li:first', an[i]).addClass('disabled');
				} else {
					$('li:first', an[i]).removeClass('disabled');
				}

				if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
					$('li:last', an[i]).addClass('disabled');
				} else {
					$('li:last', an[i]).removeClass('disabled');
				}
			}
		}
	}
} );


/*
 * TableTools Bootstrap compatibility
 * Required TableTools 2.1+
 */
if ( $.fn.DataTable.TableTools ) {
	// Set the classes that TableTools uses to something suitable for Bootstrap
	$.extend( true, $.fn.DataTable.TableTools.classes, {
		"container": "DTTT btn-group",
		"buttons": {
			"normal": "btn",
			"disabled": "disabled"
		},
		"collection": {
			"container": "DTTT_dropdown dropdown-menu",
			"buttons": {
				"normal": "",
				"disabled": "disabled"
			}
		},
		"print": {
			"info": "DTTT_print_info modal"
		},
		"select": {
			"row": "active"
		}
	} );

	// Have the collection use a bootstrap compatible dropdown
	$.extend( true, $.fn.DataTable.TableTools.DEFAULTS.oTags, {
		"collection": {
			"container": "ul",
			"button": "li",
			"liner": "a"
		}
	} );
}


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
    this.elem = $(element);
    this.list = list;
    this.actionUrl = '.'
    this._initWidgets();
}

ToolBar.prototype = {
    constructor: ToolBar,
    _initWidgets: function() {
        var me = this;
        this.aloneActions = this.elem.find('.alone-action');
        this.manyActions = this.elem.find('.many-action');
	
        this.aloneActions.hide();
        this.manyActions.hide();

	this.aloneActions.click (function (e) {
            if ($(this).is('.ignore-autoconnect'))
                return

	    e.preventDefault();
	    var url =  $(this).attr('href').replace('%d', me.list.getSeletedIds()[0]);
	    window.location.href = url;
	    
	    return false;
	});
    }
};

var ListBuilder = function(element, options)
{
    var me = this;
    this.elem = $(element);
    
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
        ajaxSource: null,
        showInfo: true,
        multipleSelect: true
    }, options || {});

    this.gaiSelected = []; //guarda os selecionados em cache

    $(this.settings['form']).submit(function (e) {
	e.preventDefault();
	me.reload();
	return false;
    });

    $(this.settings['output']).click (function (e) {

	var url = $(me.settings['form']).attr('action');

	window.location.href = url + '?'+ $(me.settings['form']).serialize()+'&format='+$(this).attr('rel');
	return false;
    });

    this.initWidgets(); // inicia o plugin
    this.toolbar = new ToolBar(this.settings.toolbar, this); // inicia o toolbar
}

ListBuilder.prototype = {
    constructor: ListBuilder,
    reload: function() {
        /*
         * Recarrega a lista
         */
        this.oTable.fnDraw();
        this.updateChecker();
    },
    buildEmail: function (email) {
        return "<a href=\"mailto:"+email+"\">"+email+"</a>";
    },
    getSeletedIds: function () {
        var me = this;
        /* funcao pública usada para coletar as rows selecionadas */
	objs = this.elem.find('tr.row_selected');
	ids = [];

        objs.each(function (i) {
	    ids[ids.length] = me.oTable.fnGetData(objs[i])[0];
	});
	return ids;
    },
    getRowSelected: function () {
        return this.getSeletedIds()[0];
    },
    _setVisAloneActions: function (vis) {
        if (this.toolbar2) {
            if (vis)
                this.toolbar2.find('.alone-action').show();
            else
                this.toolbar2.find('.alone-action').hide();
        }

        if (vis)
            this.toolbar.aloneActions.show();
        else
            this.toolbar.aloneActions.hide();
    },
    _setVisManyActions: function (vis) {
        if (this.toolbar2) {
            if (vis)
                this.toolbar2.find('.many-action').show();
            else
                this.toolbar2.find('.many-action').hide();
        }

        if (vis)
            this.toolbar.manyActions.show();
        else
            this.toolbar.manyActions.hide();
    },
    updateChecker: function () {
	// atualiza os itens do toolbar
	var len = this.getSeletedIds().length;
	if (len<1) {
            this._setVisAloneActions(false);
            this._setVisManyActions(false);
	} else if (len== 1) {
            this._setVisAloneActions(true);
            this._setVisManyActions(true);
	}
	else {
            this._setVisAloneActions(false);
            this._setVisManyActions(true);
	}
    },
    destroy: function () {
        // usada para destruir a lista
	if (this.oTable) {
	    this.oTable.fnDestroy();
	    this.oTable = null;
	}
	this.elem.find('tbody tr').empty();
    },
    onSelectOne: function (fn) {
        this.selectOneFn = fn;
    },
    onReloadCB: function (data) {
        if (data.error) {
	    $.message(data.error, 'error');
	    return;
	}
	this.reload();
    },
    clear: function () {
        this.gaiSelected = [];
        this.oTable.fnClearTable();
    },
    addRows: function (data) {
        for (var _i=0; _i<data.length; _i++) {
            this.oTable.fnAddData(data[_i]);
        }
    },
    addRow: function (data) {
        this.oTable.fnAddData(data);
    },
    _getRow: function (id) {
        var nodes = this.oTable.fnGetNodes();
        for (var _i=0; _i<nodes.length; _i++) {
            if (this.oTable.fnGetData(nodes[_i])[0] == id)
                return nodes[_i];
        }
    },
    updateRow: function (id, data) {
        var row = this._getRow(id);
        this.oTable.fnUpdate(data, row);
    },
    deleteRow: function (id) {
        var row = this._getRow(id)
        this.oTable.fnDeleteRow(row);
    },
    initWidgets: function () {
	// configura os rendering para booleans e email
        var me = this;
        var elem = this.elem;
        
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
			return '<i class="icon-ok"></i>';
		    else
			return '<i class="icon-remove"></i>';
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
		    return me.buildEmail(oObj.aData[oObj.iDataColumn]);
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
	    "sScrollY": me.settings.scrollY,
            "sPaginationType": "bootstrap",
	    "iDisplayLength": me.settings.iDisplayLength,
	    "bServerSide": me.settings.serverSide,
	    "bFilter": me.settings.filterSuport,
            "bLengthChange": me.settings.lengthChange,
            "bPaginate": me.settings.paginate,
	    "aoColumnDefs": aoColumnDefs,
	    "aaSorting": aaSorting,
            "bInfo": me.settings.showInfo,
	    "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
		// atribui a coluna de classe
		if (classColumn > -1) {
		    $(nRow).addClass(aData[classColumn]);
		}

		// busca pelo cache de linhas selecionadas
		if ( jQuery.inArray(aData[0], me.gaiSelected) != -1 )
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
        if (this.settings.serverSide) {
            params["sAjaxSource"] =  ".";
            params["fnServerData"] = function ( sSource, aoData, fnCallback ) {
		aoData.push( { "name": "format", "value": "data"});

		if (me.settings.form) { // se tiver filtro usa-o
		    aoData = $.merge(aoData, $(me.settings.form).serializeArray());
		}
                
		if (me.settings.getExtraData) { // função para pegar dados extra
		    aoData = $.merge(aoData, me.settings.getExtraData());
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
        if (this.settings.ajaxSource) {
            params["sAjaxSource"] =  this.settings.ajaxSource;   
        }
        
	me.oTable = elem.dataTable(params).fnSetFilteringDelay();

	// esconder a coluna class
	if (classColumn > -1) {
	    me.oTable.fnSetColumnVis(classColumn, false);
	}
	
	if (me.settings.hiddenId)
	    me.oTable.fnSetColumnVis(0, false); //esconde a coluna de ids

        if (linkColumns) {
            for (i in linkColumns)
                me.oTable.fnSetColumnVis(linkColumns[i], false);
        }
        

	// Função de Clicicke
	if (me.settings.selectable) {
	    elem.find('tbody tr').live('click', function (event) {
		event.preventDefault();
		var aData = me.oTable.fnGetData( this );
		if (!aData)
		    return;
		
		var iId = aData[0];
		
                me.gaiSelected = [];
                var index = jQuery.inArray(iId, me.gaiSelected);
		if (index == -1 )
		    me.gaiSelected.push(iId);
		else
                    me.gaiSelected.splice(index, 1);
		
		if (!event) { var event = window.event; }
		var target = event.target ? event.target : event.srcElement;

		if ($(target).is('a')) {
		    return;
		}

		if ((!me.settings.multipleSelect)||(!event.ctrlKey)) {
		    elem.find('tbody tr.row_selected').removeClass('row_selected');
		}
		$(this).toggleClass('row_selected');
		me.updateChecker();

                if ((me.getSeletedIds().length == 1)&&(me.selectOneFn))
                    me.selectOneFn(aData);

		return false;
	    }).live('dblclick', function (event) {
		event.preventDefault()
		$('a.dblclick').trigger('click');
		return false;
	    });
	}

	

	// append toolbar2
	//TODO: use find, refatorar os set active
	me.toolbar2 = $('.fg-toolbar').first().append($('#toolbar2').remove());
	$('#select-all').click(function(e) {
	    e.preventDefault();
	    elem.find('tbody tr').addClass('row_selected');
	    me.updateChecker();
	    return false;
	});
	
	$('#select-none').click(function(e) {
	    e.preventDefault();
	    elem.find('tbody tr.row_selected').removeClass('row_selected');
	    me.updateChecker();
	});

        me.toolbar2.find('#set-active').click (function (e) {
	    e.preventDefault();
	    ids = me.getSeletedIds();
            
	    if (ids.length == 0) {
		return
	    }
            
	    $.post('.', {'cmd': 'set_active', 'ids': ids}, 
                   function (data) {
                       me.onReloadCB(data)
                   });
	    return false;
	});
        
	me.toolbar2.find('#set-inactive').click (function (e) {
	    e.preventDefault();
	    ids = me.getSeletedIds();
            
	    if (ids.length == 0) {
		return
	    }
            
	    $.post('.', {'cmd': 'set_inactive', 'ids': ids},
                   function (data) {
                       me.onReloadCB(data)
                   });
	    return false;
	});
    }
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

