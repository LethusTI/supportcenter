/*
  folder.uploadfiles.bootstrap.js
  AUTOR: Wilson Júnior <wilsonpjunior@gmail.com>

  Utilizado para gerenciar arquivos anexados em documentos (usando bootstrap).
  Depende de:
  bootstrap.js
  plupload.full.js
  jquery.dataTables.js
  lethus.listBuilder-bootstrap.js
*/

(function($){
    var FileManager = function (elem, options) {
        this.elem = $(elem);
        this.options = options;

        this._initToolbar();
        this._initList();
        this._initUploaderList();
        this._initUploader();
    };

    FileManager.prototype = {
        constructor: FileManager,
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
            var that = this;
            $('a#add-file')
                .click(function (e) {
                    e.preventDefault();
                    that.uploadDialog.modal('show');
                    return false;
                });

            $('a#delete-file')
                .click(function (e) {
                    e.preventDefault();
                    that.removeSelectedFile();
                    return false;
                });
            $('a#download-file')
                .click(function (e) {
                    e.preventDefault();
                    that.downloadSelectedFile();
                    return false;
                });
        },
        _initUploaderList: function () {
            var that = this;
            
            $('a.remove').live('click', function (e) {
                var file = $(this).parents('tr').data('file');
                that.uploader.removeFile(file);
            });
        },
        _initUploader: function () {
            var that = this;

            this.uploadDialog = $("#upload-container").modal({
                show: false
            });

            $('a#sendfiles').click(function () {
                that.uploader.start();
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
                               '</td><td><div class="progress">'+
                               '<div class="bar" style="width: 0%;"></div>'+
                               '</div>'+
                               '</td><td class="remove"><a class="remove" href="#">'+
                               '<i class="icon-trash"></i>'+
                               '</a></td>'+
		               '</tr>');

                    tr.data('file', file);
                    tr.appendTo('#upload-table tbody');
	        });

	        up.refresh(); // Reposition Flash/Silverlight
            });

            this.uploader.bind('FilesRemoved', function (up, files) {
                $.each(files, function(i, file) {
                    $('tr[id="'+file.id+'"]').remove()
                });
            });

            this.uploader.bind('UploadProgress', function(up, file) {
                $('tr[id="'+file.id+'"] .progress .bar').css('width', file.percent);
            });

            this.uploader.bind('UploadComplete', function(up, files) {
                $('#upload-table tbody').empty();
                that.uploadDialog.modal('hide');
            });

            this.uploader.bind('FileUploaded', function(up, file, resp) {
                var data = $.parseJSON(resp.response);
                
                if (data.error) {
                    $.message(data.error, 'error');
                    return;
                }

                that.addFile(data);
            });
        },
        addFile: function (data) {
            this.list.addRow([data.pk, data.filename, data.human_size]);
        },
        removeSelectedFile: function () {
            var that = this,
            pk = this.list.getRowSelected();

            if (confirm('Apagando este arquivo ele será '+
                         'permanentemente removido, tem '+
                         'certeza que deseja continuar ?')) {
                
                $.post('.', {'delete_file': pk},
                       function (data) {
                           if (data.error) {
                               alert(data.error);
                               return;
                           }
                           if (data.deleted)
                               that.list.deleteRow(pk);
                       });
            }
        },
        downloadSelectedFile: function() {
            var pk = this.list.getRowSelected();
            window.location = './?get_file='+pk;
        }
        
    }

    $.fn.fileManager = function (options) {
        if (this.data('fileManager'))
            return;

        var obj = new FileManager(this, options);
        this.data('fileManager', obj);

        return obj;
    };
})(jQuery);
