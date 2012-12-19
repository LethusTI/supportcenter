(function($) {
    var UnidadeProfileGroupView = function () {
        this._init();
    };

    UnidadeProfileGroupView.prototype = {
        constructor: UnidadeProfileGroupView,
        _init: function () {
            var _this = this;

            $('#id_grupo_flag').change(function (e) {
                var flag = $(this).val();
                
                if (flag == 'c') {
                    var grupoVal = $('#id_grupo').val()
                    _this.loadGrupo(grupoVal);
                    
                } else {
                    $('#field-permissions').slideUp();
                }
            });

            $('#id_grupo').change(function (e) {
                var val = $(this).val();

                if (val) {
                    $('#field-grupo_flag').slideDown();
                    $('#id_grupo_flag').trigger('change');
                } else {
                    $('#field-grupo_flag').slideUp();
                    $('#field-permissions').slideDown();
                    
                }
            }).trigger('change');
        },
        loadGrupo: function (val) {
            $('input[name="permissions"]').attr('checked', false);

            $.getJSON('.', {'cmd': 'get_group_perms', 'group_id': val}, function (perms) {

                for (var _i=0; _i<perms.length; _i++) {
                    $('input[name="permissions"][value="'+perms[_i]+'"]').attr('checked', true);
                }

                $('#field-permissions').slideDown(); 
            });
            
        }
    };

    $(function () {
        window.groupView = new UnidadeProfileGroupView();
    });
})(jQuery, window);