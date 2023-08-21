$(function(){
    $("#addCategoryForm").on("click", ".btnSave", function(){
        $.ajax({
            url: "{% url 'addCategory' %}",
            type: "POST",
            dataType: "JSON",
            data: $("#addCategoryForm").serialize(),

            success: function(response) {
                console.log(response);
            }
        })
    });
});