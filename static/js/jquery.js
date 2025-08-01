$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
       
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if(response.status == 'Login required!'){
                    swal(response.message, '', 'info').then(function(){
                        window.location= '/accounts/login';
                    })
                }else if(response.status=='failure'){
                    swal(response.message, '', 'error')


                }else if(response.status=='success'){
                    swal(response.message, '', 'success')
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                }
            
            }
        })
     })

     //place the cart item quantity on load

     $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
     })

     //decrease cart
     $('.decrease_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
    
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if(response.status == 'Login required!'){
                    swal(response.message, '', 'info').then(function(){
                        window.location= '/accounts/login';
                    })
                }else if(response.status='failure'){
                    swal(response.message, '', 'error')


                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty)

                }
                
            
            }
        })
     })

});



$(document).ready(function () {
    $('#alertButton').click(function () {
        alert('Button was clicked!');
    });
});

