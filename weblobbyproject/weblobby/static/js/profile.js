$('#profileTabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
})

function changeField(name, hide) {
    var name1 = "#" + name
    if (hide)
        $(name1).parent().parent().hide()
    else
        $(name1).parent().parent().show()
}

function changeAllWifi(hide) {
    changeField("id_funcionario_contato_nome", hide)
    changeField("id_setor_contato", hide)
    changeField("id_observacao", hide)
}

function showOrHideFields() {
    if ($("#id_entrada").is(":checked")) {
        changeAllWifi(false)
    } else {
        changeAllWifi(true)
    }
}

$(function() {
    $("#id_entrada").change(function() {
        showOrHideFields()
    });
});

showOrHideFields()

$('.date_time_input').datetimepicker({
    dateFormat: "yy-mm-dd",
    timeFormat: "HH:mm:ss"
});

// Guarda a matricula do funcionario num campo hidden, assim o usuario da aplicacao so ve o nome, mas a matricula e' enviada.
$('#id_funcionario_contato_nome').bind('selectChoice', function(e, choice, autocomplete) {
    document.getElementById('id_funcionario_matricula').value = choice.data().value;
});