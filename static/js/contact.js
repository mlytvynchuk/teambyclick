$("#sub-btn").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/ajax/create-contact/",

        data: {
            "name": $("#name_id").val(),
            "email": $("#email_id").val(),
            "message": $("#message_id").val(),
        },

        dataType:"text",
        cache:false,

        success: function(data){
          if(data == 'no'){
              return false
          }
          else if(data == 'yes')
          {
            $("#alert-success").attr("style","display: block")
              return true
          }
        }
    });

})

