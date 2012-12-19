$(document).ready(function (e) {
    $("#filter-form").hfilter();

    $("table.display").listbuilder({
	form: "#filter-form",
	output: ".output",
	selectable: false,
	filterSuport: false
    });
});