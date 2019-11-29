function get(){
    var val_city = document.getElementById("city").value;

    $.ajax({
        type : 'GET',
        url : "",
        data: {
            "city": val_city,
            "country": val_country,


            "w-main": val_wmain,
            "w-desc": val_wdesc,
            "temp": val_temp, 
            "wind": val_wind
        },
        dataType: "json"
    }).done(function () {
        // $('#modal-1').modal('hide');
        table.row.data([val_no, val_name, val_address, val_phone, val_car, val_penalty, UserIndex_CreateEditButton(val_no, val_name, val_address, val_phone, val_car, val_penalty), UserIndex_CreateDeleteButton(val_no)], $('#' + tempUpdate));
    }
} 