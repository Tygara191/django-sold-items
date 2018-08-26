/**
 * Created by Admin on 8.5.2017 г..
 */

function toggleIdInInput(field, id, action) {
    string_ids = field.val();
    list_ids = string_ids.split(",");
    id = id.toString();

    index = list_ids.indexOf(id);
    if(index >= 0){
        list_ids.splice(index, 1);
    }else{
        list_ids.push(id);
    }

    if(list_ids.length > 0){
        if(list_ids[0].length <= 0){
            list_ids.splice(0, 1);
        }
    }

    field.val(list_ids.join(","));
}

$(function () {
    $('form').submit(function(e){
	    var emptyinputs = $(this).find('input').filter(function(){
	        return !$.trim(this.value).length;  // get all empty fields
	    }).prop('disabled',true);
	    var form_id = $(this).attr('id');
	    var emptyinputs_by_form_attr = $('[form='+form_id+']').filter(function(){
	        return !$.trim(this.value).length;  // get all empty fields
	    }).prop('disabled',true);
	});

    var inputs = {
        'ecc': $('#ecc'),
        'ecw': $('#ecw'),
        'ps': $('#ps'),
        'gp': $('#gp'),
        'man': $('#man'),
        'pws': $('#pws')
    };

    var tickboxes = $('.checkbox-filter');

    tickboxes.on('change', function (event) {
        var this_box = $(this);
        var field = inputs[this_box.attr('data-filter-field-id')];
        var id = this_box.attr('data-id');

        toggleIdInInput(field, id, this_box.is(":checked"));
        $('#search-form').submit();
    });

    $('#ordering').on('change', function () {
        $('#search-form').submit();
    })
});