$("#username-input").mousemove(function () {
    $.ajax({
        type: "GET",
        url: "/ajax/check-name/",

        data: {
            "username": $("#username-input").val()
        },

        dataType:"text",
        cache:false,

        success: function(data){
          if(data == 'no'){
                console.log(data)
              $(".username_check_alert").attr("style","display: none")
              return false
          }
          else if(data == 'yes')
          {
              console.log("it ex")
            $(".username_check_alert").attr("style","display: block")
              return true
          }
        }
    });
})
