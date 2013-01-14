/*
  folder.uploadfiles.jqueryui.js
  AUTOR: Wilson Júnior <wilsonpjunior@gmail.com>

  Utilizado para gerenciar arquivos anexados em documentos (JqueryUI)
  Depende de:
  plupload.full.js
  jquery.dataTables.js
  lethus.listBuilder.js
*/

(function ($) {
    var FileManager = function (elem, options) {
        this._init(elem, options);
    };

    FileManager.prototype = {
        constructor: FileManager,
        _init: function (elem, options) {
            this.elem = $(elem);
            this.options = options;
            

            this._initToolbar();
            this._initList();
            this._initUploaderList();
            this._initUploader();
        },
        _initList: function () {
            this.list = $("table#result").listbuilder({
                serverSide: false,
                scrollY: 250,
                filterSuport: false,
                paginate: false,
                lengthChange: false
            });
        },
        _initToolbar: function () {
            var me = this;
            $('a#add-file')
                .click(function (e) {
                    e.preventDefault();
                    me.uploadDialog.dialog('open');
                    return false;
                });

            $('a#delete-file')
                .click(function (e) {
                    e.preventDefault();
                    me.removeSelectedFile();
                    return false;
                });
            $('a#download-file')
                .click(function (e) {
                    e.preventDefault();
                    me.downloadSelectedFile();
                    return false;
                });
        },
        _initUploaderList: function () {
            var me = this;
            
            $('a.remove').live('click', function (e) {
                var file = $(this).parents('tr').data('file');
                me.uploader.removeFile(file);
            });
        },
        _initUploader: function () {
            var me = this;

           

            this.uploadDialog = $("#upload-container")
                .dialog({
                    modal: true,
                    autoOpen: false,
                    buttons: [
                        {
                            id:"pickfiles",
                            text: "Selecionar",
                            click: function(e) {
                                e.preventDefault();

                                //nao sei porque so funciona com isso
                                $(this).dialog('close');
                                $(this).dialog('open');

                                return false;
                            }
                        },
                        {
                            id: "sendfiles",
                            text: "Enviar",
                            click: function() {
                                me.uploader.start();
                            }
                        }]
                });
            this.uploader = new plupload.Uploader({
		runtimes : 'html5,flash,silverlight,browserplus',
		browse_button : 'pickfiles',
		container : 'result',
                url: '.',
		max_file_size : '10mb',
                multipart_params: {'cmd': 'post_file'},
		flash_swf_url : '/static/js/plupload.flash.swf',
		silverlight_xap_url : '/static/js/plupload.silverlight.xap',
                headers : {'X-Requested-With' : 'XMLHttpRequest', 'X-CSRFToken' : this.options.token},
            });

            this.uploader.init();
            this.uploader.bind('FilesAdded', function (up, files) {
                $('#upload-container').fadeIn();
                $.each(files, function(i, file) {
                    var tr = $('<tr id="' + file.id + '"><td>' + file.name +
                               '</td><td>' + plupload.formatSize(file.size) +
                               '</td><td><div class="progress"></div>'+
                               '</td><td class="remove"><a class="remove" href="#"></a></td>'+
		               '</tr>');

                    tr.data('file', file);
                    tr.appendTo('#upload-table tbody');
                    tr.find('.progress').progressbar();
	        });

	        up.refresh(); // Reposition Flash/Silverlight
            });

            this.uploader.bind('FilesRemoved', function (up, files) {
                $.each(files, function(i, file) {
                    $('tr[id="'+file.id+'"]').remove()
                });
            });

            this.uploader.bind('UploadProgress', function(up, file) {
                $('tr[id="'+file.id+'"] .progress').progressbar({value: file.percent});
            });

            this.uploader.bind('UploadComplete', function(up, files) {
                $('#upload-table tbody').empty();
                me.uploadDialog.dialog('close');
            });

            this.uploader.bind('FileUploaded', function(up, file, resp) {
                var data = $.parseJSON(resp.response);
                
                if (data.error) {
                    $.message(data.error, 'error');
                    return;
                }

                me.addFile(data);
            });
        },
        addFile: function (data) {
            this.list.addRow([data.pk, data.filename, data.human_size]);
        },
        removeSelectedFile: function () {
            var me = this;
            var pk = this.list.getRowSelected();
            $("#file-delete-confirm").dialog({
		resizable: false,
		height:160,
		modal: true,
                buttons: {
                    "Apagar": function() {
                        $.post('.', {'delete_file': pk},
                               function (data) {
                                   if (data.error) {
                                       $.message(data.error, 'error');
                                       return;
                                   }
                                   if (data.deleted)
                                       me.list.deleteRow(pk);
                               });
                        $(this).dialog("close");
		    },
                    "Cancelar": function() {
                        $(this).dialog("close");
                    }
                }
            });
        },
        downloadSelectedFile: function() {
            var pk = this.list.getRowSelected();
            window.location = './?get_file='+pk;
        }
        
    }
    $.fn.fileManager = function (options) {
        var element = $(this);
        var p = element.data('fileManager');

        if (p) return p;

	p = new FileManager(this, options);
        element.data('fileManager', p);
        return p;
    };
})(jQuery);
