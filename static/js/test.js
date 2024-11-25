$('document').ready(function () {
    $('.ckd').hide()
    $('.notckd').hide()
        $('#test').submit(function(e){
            e.preventDefault();
            var data = $('form#test').serialize()
            console.log(data)
            $.ajax({
                url:'/result',
                type: 'POST',
                dataType: 'json',
                data: {msg:data},
                success: function(response){
                    $('form#test').trigger('reset')
                    if(response.data == "CKD")
                    {
                        $('.ckd').fadeIn(3000)
                    }
                    else
                    {
                        $('.notckd').fadeIn(3000)                    }
                },
                error: function(error){
                    console.log(error);
                }
            });
        });
        $('.close').click(function(){
            $('.ckd').fadeOut(1000);
            $('.notckd').fadeOut(1000);
            
        });
    })