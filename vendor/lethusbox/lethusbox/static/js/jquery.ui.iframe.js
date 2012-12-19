(function( $ ) {
    var iFrameDialog = function(element, url, options)
    {
	var elem = $(element);
	var obj = this;

	// Merge options with defaults
	this.settings = $.extend({
	}, options || {});
	elem.empty();

	elem.dialog({closeable: true,
		     //show: 'fadeIn',
		     //hide: 'fadeOut',
		     modal: true,
		     height: 600,
		     
		     width: 600}).append('<iframe id="modalIframeId" width="100%" height="100%" marginWidth="0" marginHeight="0" frameBorder="0" scrolling="auto" src="'+url+'" />');

	elem.dialog({close: function(event, ui) {
	    if (obj.settings.onClose != undefined)
		obj.settings.onClose(obj);
	}});

	// altera o titulo do dialog
	$('#modalIframeId').load(function (e) {
	    var title = $(this).contents().find("title").html();
	    elem.dialog('option', 'title', title);
	});
    }

    $.fn.ifdialog = function(url, options)
    {

	var element = $(this);
	
	// Return early if this element already has a plugin instance
	//if (element.data('ifdialog')) return;
	var ifd = new iFrameDialog(this, url, options);

        // Store plugin object in this element's data
        //element.data('ifdialog', ifd);
        return element;
    };
})( jQuery );