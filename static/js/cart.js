$(".update-cart").click(function(){

  product_id=$(this).data("product");
  product_action=$(this).data("action")

  if (user =='AnonymousUser')
  {
    addCookieItem(product_id,product_action)
  }
  else{
    console.log('Authorize User..!!!')

    $.ajax({
      headers: {
          'X-CSRFToken':csrftoken
      },
      url:'/updateItem/',
      type:'POST',
      data:{'product_id':product_id,'product_action':product_action},
      success:function(data){
        // alert(data.success)
        location.reload()
        localStorage.setItem("cart_count",data.cart_count);
        $('#cart_total').text(localStorage.getItem('cart_count'))

      }
    });
  }
});

function addCookieItem(proId,proAction)
{
  // alert('Un Authorize User..!!!');
  if(proAction == 'add')
  {
    if(cart[proId] == undefined)
    {
      cart[proId]={'quantity':1}
    }
    else{
      cart[proId]['quantity'] += 1;
    }
  }

  if(proAction == 'remove')
  {
    cart[proId]['quantity'] -= 1;
    if(cart[proId]['quantity'] <= 0)
    {
      console.log('product is deleted!!!')
      delete cart[proId]
    }
  }
  setCookie('cart', cart, 3)
  console.log("cart:",cart)
  location.reload()
  var total_cart_count=0;
  for (c in cart) {
    total_cart_count += cart[c]['quantity']
  }
  console.log(total_cart_count)
  localStorage.setItem("cart_count",total_cart_count);
  $('#cart_total').text(localStorage.getItem('cart_count'))

}
