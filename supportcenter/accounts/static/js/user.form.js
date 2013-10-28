(function($) {
    var UserGroupView = function () {
        var that = this;

        $('#id_group_flag').change(function (e, data) {
            var flag = $(this).val(),
            startup = false;

            if (data && data.startup)
                startup = true;
            
            if (flag == 'c') {
                var grupoVal = $('#id_group').val();
                if (grupoVal && !startup)
                    that.loadGroup(grupoVal);
                
            } else {
                $('#field-permissions').addClass('hide');
            }
        });

        $('#id_group').change(function (e, data) {
            var val = $(this).val();

            if (val) {
                $('#field-group_flag').removeClass('hide');
                $('#id_group_flag').trigger('change', data);
            } else {
                $('#field-group_flag').addClass('hide');
                $('#field-permissions').removeClass('hide');
                
            }
        }).trigger('change', {startup: true});
    };

    UserGroupView.prototype = {
        constructor: UserGroupView,
        loadGroup: function (val) {
            $('input[name="permissions"]').attr('checked', false);

            $.getJSON('.', {
                cmd: 'get_group_perms',
                group_id: val}, function (perms) {

                for (var _i=0; _i<perms.length; _i++) {
                    $('input[name="permissions"][value="'+perms[_i]+'"]').attr('checked', true);
                }

                $('#field-permissions').removeClass('hide');
            });
            
        }
    };

    $(function () {
        window.groupView = new UserGroupView();
    });
})(jQuery, window);
