$(document).ready(function(){
    $('.dropdown-toggle').dropdown();

    // fazendo o fixed do menu
    var menu = $('#menu'),
    pos = menu.offset();
    
    $(window).scroll(function(){
	if($(this).scrollTop() > pos.top+menu.height() && menu.hasClass('subnav')){
	    menu.addClass('subnav-fixed');
	} else if($(this).scrollTop() <= pos.top && menu.hasClass('subnav-fixed')){
	    menu.removeClass('subnav-fixed');
	}
    });

    $('form input[type="checkbox"]').parent().addClass("field-checkbox")
    
    $('[rel~=tooltip]').tooltip();

    if (typeof($.fn.mask) != 'undefined') {
        $(".cep").mask('99999-999');
        $('.tel').mask('(99) 9999-9999?9');
        $('.cpf').mask('999.999.999-99');
        $('.cnpj').mask('99.999.999/9999-99');
        $('.date').mask('99/99/9999');
    }
});
