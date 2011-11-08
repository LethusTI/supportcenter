/*
  Utilizado para gerenciar formulários via Ajax
  
  Escrito por Wilson Pinto Júnior (8 de dezembro de 2011)
 */

(function($){
    var FormBase = function (options) {
        this._init(options);
    };

    FormBase.prototype = {
        "_init": function (options) {
            this._initWidgets();
        },
        "_initWidgets": function () {
            console.error("this method is abstract");
        },
        "show": function () {
            this.elem.show();
        }
    };

    $.registerClass('FormBase', FormBase);
})(jQuery);