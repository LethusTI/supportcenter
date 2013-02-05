$(document).ready(function (e) {
    $("#filter-form").hfilter();

    $("table.display").listbuilder({
	form: "#filter-form",
	output: ".output",
	selectable: false,
	filterSuport: false
    });
    $('#id_from_date').attr('placeholder', "De").addClass('input-small');
    $('#id_to_date').attr('placeholder', "Até").addClass('input-small');
});
