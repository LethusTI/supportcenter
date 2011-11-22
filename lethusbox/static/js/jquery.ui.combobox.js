/*
 * Widget de Combobox para atender as necessidades da Lethus
 * Originalmente de: http://jqueryui.com/demos/autocomplete/#combobox
 */
(function( $ ) {
    $.widget( "ui.combobox", {
	_create: function() {
	    var me = this,
	    select = this.element.hide(),
	    selected = select.children( ":selected" ),
	    value = selected.val() ? selected.text() : "";
	    var input = this.input = $( "<input type=\"text\" class=\"search-text\">" )
		.insertAfter( select )
		.val( value )
		.autocomplete({
		    delay: 0,
		    minLength: 0,
		    source: function( request, response ) {
			var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
			response( select.children( "option" ).map(function() {
			    var text = $( this ).text();
			    if ( this.value && ( !request.term || matcher.test(text) ) )
				return {
				    label: text.replace(
					new RegExp(
					    "(?![^&;]+;)(?!<[^<>]*)(" +
						$.ui.autocomplete.escapeRegex(request.term) +
						")(?![^<>]*>)(?![^&;]+;)", "gi"
					), "<strong>$1</strong>" ),
				    value: text,
				    desc: $(this).attr('title'),
				    option: this
				};
			}) );
		    },
		    select: function( event, ui ) {
			ui.item.option.selected = true;
			me._trigger( "selected", event, {
			    item: ui.item.option
			});
		    },
		    change: function( event, ui ) {
			if ( !ui.item ) {
			    var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( $(this).val() ) + "$", "i" ),
			    valid = false;
			    select.children( "option" ).each(function() {
				if ( $( this ).text().match( matcher ) ) {
				    this.selected = valid = true;
				    return false;
				}
			    });
			    if ( !valid ) {
				// remove invalid value, as it didn't match anything
				$( this ).val( "" );
				select.val( "" );
				input.data( "autocomplete" ).term = "";
                                me._trigger("cleaned", event, {
			            item: null
			        });
				return false;
			    }
			}
		    }
		})
		.addClass( "ui-widget ui-widget-content ui-corner-left" );

	    input.data( "autocomplete" )._renderItem = function( ul, item ) {
		return $( "<li></li>" )
		    .data( "item.autocomplete", item )
		    .append( "<a>" + item.label + "</a>" )
		    .appendTo( ul );
	    };

	    this.button = $( "<button type='button'>&nbsp;</button>" )
		.attr( "tabIndex", -1 )
		.attr( "title", "Mostrar todos os itens" )
		.insertAfter( input )
		.button({
		    icons: {
			primary: "ui-icon-triangle-1-s"
		    },
		    text: false
		})
		.removeClass( "ui-corner-all" )
		.addClass( "ui-corner-right ui-button-icon" )
		.click(function() {
		    // close if already visible
		    if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
			input.autocomplete( "close" );
			return;
		    }

		    // work around a bug (likely same cause as #5265)
		    $( this ).blur();

		    // pass empty string as value to search for, displaying all results
		    input.autocomplete( "search", "" );
		    input.focus();
		});
	},
        reselect: function() {
            /*
              Recheck value of combobox and redraw
             */
            var selected = this.element.children(":selected"),
	    value = selected.val() ? selected.text() : "";
            this.input.val(value);

            if (value)
                this._trigger("selected", event, {
		    item: value
		});
            else
                this._trigger("cleaned", event, {
		    item: null
	        });
        },
        clear: function() {
            this.element.val('');
            this.input.val('');
            this.element.empty();
            this._trigger("cleaned", event, {
		item: null
	    });
        },
	destroy: function() {
	    this.input.remove();
	    this.button.remove();
	    this.element.show();
	    $.Widget.prototype.destroy.call( this );
	}
    });
})( jQuery );