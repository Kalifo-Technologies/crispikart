function group_edit(group_id,group_name,group_start,group_end){
    $('#g-name').val(group_name)
    $('#g-id').val(group_id)
    $('#g-start').val(group_start)
    $('#g-end').val(group_end)
}

function group_delete(group_id){
    $('#gd-id').val(group_id)
}