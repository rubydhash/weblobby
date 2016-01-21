function refresh() {
    $.ajax({
        url : "/weblobby/panel",
        type : "POST",
        dataType: "json",
        data : {
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success : function(visitante) {
            $('#id_username').html(sprintf("%011d", parseInt(visitante[0].fields.cpf)));
            $('#id_senha').html(visitante[0].fields.senha);
            $('#result').show();
            $('#logo').hide();
            //setTimeout(refresh, 5000);
        },
        error : function(xhr,errmsg,err) {
            $('#result').hide();
            $('#logo').show();
            //setTimeout(refresh, 2000);
        }
    });
}

//setTimeout(refresh, 2000);