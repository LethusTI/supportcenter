/* =============================================================
 * bootstrap-queryable-combobox.js v1.0.0
 * =============================================================
 * Copyright 2012 Wilson Pinto Júnior <wilsonpjunior@gmail.com>
 * Copyright 2012 Daniel Farrell
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================ */

!function( $ ) {

 "use strict"

  var QCombobox = function ( element, options ) {
      this.options = $.extend({}, $.fn.qcombobox.defaults, options);
      this.$container = this.setup(element);
      this.$element = this.$container.find('input');
      this.$button = this.$container.find('.dropdown-toggle');
      this.$target = this.$container.find('select');
      this.matcher = this.options.matcher || this.matcher;
      this.sorter = this.options.sorter || this.sorter;
      this.highlighter = this.options.highlighter || this.highlighter;
      this.$menu = $(this.options.menu).appendTo('body');
      this.placeholder = this.options.placeholder || this.$target.attr('data-placeholder');
      this.$element.attr('placeholder', this.placeholder);
      this.shown = false;
      this.selected = false;
      this.listen();

      var selectedVal = this.$target.val();

      if (selectedVal) {
          this.$container.addClass('combobox-selected');
          this.$element.val(this.$target.find('option[value="'+selectedVal+'"]').text());
          this.selected = true;
      }
  }

  /* NOTE: COMBOBOX EXTENDS BOOTSTRAP-TYPEAHEAD.js
     ========================================== */

  QCombobox.prototype = {
      constructor: QCombobox,
      setup: function (element) {
          var select = $(element)
          , combobox = $(this.options.template);

          select.before(combobox);
          select.detach();
          combobox.append(select);

          return combobox;
      },
      toggle: function () {
          if (this.$container.hasClass('combobox-selected')) {
              this.clearTarget()
              this.$element.val('').focus()
          } else {
              if (this.shown) {
                  this.hide()
              } else {
                  this.lookup()
              }
          }
      },
      clearTarget: function () {
          this.$target.val('')
          this.$container.removeClass('combobox-selected')
          this.selected = false
          this.$target.trigger('change')
      },
      select: function () {
          var val = this.$menu.find('.active').data('data-value');

          this.$element.val(val[1]);
          this.$container.addClass('combobox-selected');
          this.$target.val(this.map[val[1]]);
          this.$target.trigger('change');
          this.selected = true;

          return this.hide();
      },
      setItems: function (items) {
          this.$element.empty();
      },
      source: function (query, process) {
          $.getJSON(this.options.url, {term: query}, function (items) {
              process(items);
          })
      },
      matcher: function (item) {
          return ~item[1].toLowerCase().indexOf(this.query.toLowerCase())
      },
      process: function (items) {
          var that = this;

          this.$target.empty().append('<option value=""></option>');
          this.map = {};
          $.each(items, function (i, item) {
              that.$target.append('<option value="'+item[0]+'">'+item[1]+'</option>');
              that.map[item[1]] = item[0];
          });
          
          
          return $.fn.typeahead.Constructor.prototype.process.call(this, items);
      },
      sorter: function (items) {
          var beginswith = []
          , caseSensitive = []
          , caseInsensitive = []
          , item;
          
          while (item = items.shift()) {
              if (!item[1].toLowerCase().indexOf(this.query.toLowerCase())) beginswith.push(item)
              else if (~item.indexOf(this.query)) caseSensitive.push(item)
              else caseInsensitive.push(item)
          }
          
          return beginswith.concat(caseSensitive, caseInsensitive)
      },
      highlighter: function (item) {
          var query = this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, '\\$&');
          return item[1].replace(new RegExp('(' + query + ')', 'ig'), function ($1, match) {
              return '<strong>' + match + '</strong>';
          });
      },
      listen: function () {
          this.$element
              .on('blur',     $.proxy(this.blur, this))
              .on('keypress', $.proxy(this.keypress, this))
              .on('keyup',    $.proxy(this.keyup, this))
          
          if ($.browser.webkit || $.browser.msie) {
              this.$element.on('keydown', $.proxy(this.keypress, this))
          }
          
          this.$menu
              .on('click', $.proxy(this.click, this))
              .on('mouseenter', 'li', $.proxy(this.mouseenter, this))
          
          this.$button
              .on('click', $.proxy(this.toggle, this))
      },
      keyup: function (e) {
          switch(e.keyCode) {
          case 40: // down arrow
          case 39: // right arrow
          case 38: // up arrow
          case 37: // left arrow
          case 36: // home
          case 35: // end
          case 16: // shift
              break
              
          case 9: // tab
          case 13: // enter
              if (!this.shown) return
              this.select()
              break
              
          case 27: // escape
              if (!this.shown) return
              this.hide()
              break
              
          default:
              this.clearTarget()
              this.lookup()
          }
          
          e.stopPropagation()
          e.preventDefault()
      },
      blur: function (e) {
          var that = this
          e.stopPropagation()
          e.preventDefault()
          var val = this.$element.val()
          if (!this.selected && val != "" ) {
              this.$element.val("")
              this.$target.val("").trigger('change')
          }
          if (this.shown) {
              setTimeout(function () { that.hide() }, 150)
          }
      },
      lookup: function (event) {
          var items;

          this.query = this.$element.val()
          this.source(this.query, $.proxy(this.process, this));
          
          return items;
      },
      render: function (items) {
          var that = this

          items = $(items).map(function (i, item) {
              i = $(that.options.item).data('data-value', item)
              i.find('a').html(that.highlighter(item))
              return i[0];
          });
          
          items.first().addClass('active')
          this.$menu.html(items)
          return this;
      },
      show: function () {
          var pos = $.extend({}, this.$element.offset(), {
              height: this.$element[0].offsetHeight
          })

          this.$menu.css({
              top: pos.top + pos.height
              , left: pos.left
          })

          this.$menu.show()
          this.shown = true
          return this
      },
      hide: function () {
          this.$menu.hide()
          this.shown = false
          return this
      },
      keypress: function (e) {
          if (this.suppressKeyPressRepeat) return
          this.move(e)
      },
      click: function (e) {
          e.stopPropagation();
          e.preventDefault();
          this.select();
      },
      mouseenter: function (e) {
          this.$menu.find('.active').removeClass('active')
          $(e.currentTarget).addClass('active')
      },
      move: function (e) {
          if (!this.shown) return

          switch(e.keyCode) {
          case 9: // tab
          case 13: // enter
          case 27: // escape
              e.preventDefault()
              break

          case 38: // up arrow
              e.preventDefault()
              this.prev()
              break

          case 40: // down arrow
              e.preventDefault()
              this.next()
              break
          }

          e.stopPropagation()
      },
      next: function (event) {
          var active = this.$menu.find('.active').removeClass('active')
          , next = active.next()

          if (!next.length) {
              next = $(this.$menu.find('li')[0])
          }

          next.addClass('active')
      },
      prev: function (event) {
          var active = this.$menu.find('.active').removeClass('active')
          , prev = active.prev()

          if (!prev.length) {
              prev = this.$menu.find('li').last()
          }

          prev.addClass('active')
      }

  };

  $.fn.qcombobox = function ( option ) {
    return this.each(function () {
      var $this = $(this)
        , data
        , options = typeof option == 'object' && option
      $this.data('combobox', (data = new QCombobox(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.qcombobox.defaults = {
  template: '<div class="combobox-container"><input type="text" autocomplete="off" /><span class="add-on btn dropdown-toggle" data-dropdown="dropdown"><span class="caret"/><span class="combobox-clear"><i class="icon-remove"/></span></span></div>'
  , menu: '<ul class="typeahead typeahead-long dropdown-menu"></ul>'
  , item: '<li><a href="#"></a></li>'
  , placeholder: null
  }

  $.fn.qcombobox.Constructor = QCombobox

}( window.jQuery )
