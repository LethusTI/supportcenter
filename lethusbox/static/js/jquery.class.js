/*
  Biblioteca para criação de classes
  Autor: Wilson Pinto Júnior <wilsonpjunior@gmail.com>
  18 de setembro de 2011
*/

$.classes = {};

$.registerClass = function (name, cls) {
    /*
      Registra a classe no registro
    */
    $.classes[name] = cls;
}

$.superClass = function (obj) {
    /*
      funciona como o super do python
      retornando os prototype da classe superior
    */
    return obj._parentClass.prototype;
}

$.registerInitClass = function (cls, attr) {
    /*
      registra a classe como plugin
      cls: classe em si
      attr: como ela será armazenada no elemento
     */
    $.fn[attr] = function (options) {
        var element = $(this);
        var p = element.data(attr);

        if (p) return p;

	p = new cls(this, options);
        element.data(attr, p);
        return p;
    }
}

$.inherits = function (child, parent, options) {
    /*
      Gera herança de um objeto
      child: classe filha
      parent: classe pai ou nome (se estiver registrada)
      options: opções que serão rescritas na classe filha
    */

    if (parent.constructor == String)
        parent = $.classes[parent];
    
    var _super = parent.prototype;
    child.prototype = {};
    
    //copia os attributos da classe pai para a filha
    for (var k in _super) {
        child.prototype[k] = _super[k];
    }

    for (var k in options||{}) {
        if (_super[k] && typeof(_super[k] == 'function')) {
            child.prototype[k] = (function(name, fn){
                return function() {
                    var tmp = this._super;
            
                    // Add a new ._super() method that is the same method
                    // but on the super-class
                    this._super = _super[name];
                    
                    // The method only need to be bound temporarily, so we
                    // remove it when we're done executing
                    var ret = fn.apply(this, arguments);        
                    this._super = tmp;
            
                    return ret;
                };
            })(k, options[k]);
        } else {
            child.prototype[k] = options[k];
        }
    }

    child.prototype._parentClass = parent;

    //super method for constructor
    child.prototype._super = function () {
        var tmp = this._super;
        
        if (parent.prototype._super)
            this._super = parent.prototype._super;
        else
            this._super = null;

        var ret = parent.apply(this, arguments)

        this._super = tmp;
        return ret;
    }
    child.prototype.constructor = child;
}