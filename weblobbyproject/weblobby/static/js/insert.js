jQuery(function($) {
	$("#id_telefone").mask("(99) 9?99999999");
	$("#id_telefone_comercial").mask("(99) 9?99999999");
	$("#id_cpf").mask("999.999.999-99");
});

function changeField(name, hide) {
	var name1 = "#" + name
	if (hide)
		$(name1).parent().parent().hide();
	else
		$(name1).parent().parent().show();
}

function changeAllWifi(hide) {
	changeField("id_cpf", hide);
	changeField("id_telefone", hide);
	changeField("id_telefone_comercial", hide);
	changeField("id_email", hide);
}

function changeAllPassaporte(show) {
    changeField("id_emissor", show);
    changeField("id_uf", show);
}

function showOrHideFields() {
	if ($("#id_wifi").is(":checked")) {
		changeAllWifi(false);
	} else {
		changeAllWifi(true);
	}

	if ($("#id_passaporte").is(":checked")) {
	    changeAllPassaporte(true);

	} else {
	    changeAllPassaporte(false);
	}
}

$(function() {
	$("#id_wifi").change(function() {
		showOrHideFields();
	});
	$("#id_passaporte").change(function() {
        showOrHideFields();
	});
});

showOrHideFields();