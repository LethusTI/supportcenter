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

        this._init(element, list)
    }

    ToolBar.prototype = {
        "_init": function (element, list) {
	    this.elem = $(element);
	    this.list = list;
            this.actionUrl = '.'
            this._initWidgets();
        },
        
        "_initWidgets": function() {
            var me = this;
            this.aloneActions = this.elem.find('.alone-action')
            this.manyActions = this.elem.find('.many-action')

            // busca por todos buttons que possuem o attributo rev para setar como icone
            this.elem.find(".button-icon").each(function (idx, obj) {
                var icon = $(obj).attr('rev');
                $(obj).button({ icons: {primary: icon}});
            });
	
            this.aloneActions.hide();
            this.manyActions.hide();

	    this.aloneActions.click (function (e) {
                if ($(this).is('.ignore-autoconnect'))
                    return

	        e.preventDefault();
	        var url =  $(this).attr('href').replace('%d', me.list.getSeletedIds()[0]);

                
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

            this.elem.find('#post-delete').click(function (e) {
	        ids = me.list.getSeletedIds();
	        
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
			    $.post(me.actionUrl,
                                   {'cmd': 'mass_delete', 'ids': ids},
                                   function (data) {
                                       me.list.onReloadCB(data)
                                   });
		        }
		    }
	        });
	    });
            
	    
        }
    }

    var ListBuilder = function(element, options)
    {
        this._init(element, options)
    }

    ListBuilder.prototype = {
        "_init": function (elem, options) {
            var me = this;
            this.elem = $(elem);
            
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
	        var params = $(me.settings['form']).serializeJSON();
	        var url = $(me.settings['form']).attr('action');

	        params['format'] = $(this).attr('rel');
                
	        // TODO: pegar sorting and filter do datatable
	        window.location.href = url + '?'+ $.param(params);
	        return false;
	    });

	    this.initWidgets(); // inicia o plugin
	    this.toolbar = new ToolBar(this.settings.toolbar, this); // inicia o toolbar
        },
	"reload": function() {
            this.oTable.fnDraw();
            this.updateChecker();
        },
        "getSeletedIds": function () {
            var me = this;
            /* funcao pública usada para coletar as rows selecionadas */
	    objs = this.elem.find('tr.row_selected');
	    ids = [];

            objs.each(function (i) {
		ids[ids.length] = me.oTable.fnGetData(objs[i])[0];
	    });
	    return ids;
	},
        "getRowSelected": function () {
            return this.getSeletedIds()[0];
        },
        "_setVisAloneActions": function (vis) {
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
        "_setVisManyActions": function (vis) {
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
        "updateChecker": function () {
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
	"destroy": function () {
            // usada para destruir a lista
	    if (this.oTable) {
		this.oTable.fnDestroy();
		this.oTable = null;
	    }
	    this.elem.find('tbody tr').empty();
	},
        "onSelectOne": function (fn) {
            this.selectOneFn = fn;
        },
        "onReloadCB": function (data) {
            if (data.error) {
		$.message(data.error, 'error');
		return;
	    }
	    this.reload();
        },
        "clear": function () {
            this.gaiSelected = [];
            this.oTable.fnClearTable();
        },
        "addRows": function (data) {
            for (var _i=0; _i<data.length; _i++) {
                this.oTable.fnAddData(data[_i]);
            }
        },
        "addRow": function (data) {
            this.oTable.fnAddData(data);
        },
        "_getRow": function (id) {
            var nodes = this.oTable.fnGetNodes();
            for (var _i=0; _i<nodes.length; _i++) {
                if (this.oTable.fnGetData(nodes[_i])[0] == id)
                    return nodes[_i];
            }
        },
        "updateRow": function (id, data) {
            row = this._getRow(id);
            this.oTable.fnUpdate(data, row);
        },
        "initWidgets": function () {
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
		"sScrollY": me.settings.scrollY,
		"sPaginationType": "full_numbers",
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
})(jQuery);
