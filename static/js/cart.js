var updateBtns = document.getElementsByClassName("update-cart")

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log("USER:", user)

        //if user is a guest user then the cart item will be added as a cookie data in the browser.

		if(user == "AnonymousUser"){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log("User is authenticated, sending data...")

		var url = "/update_item/"

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body: JSON.stringify({'productId':productId, 'action':action}),
		})
		.then((response)=>{
		   return response.json();
		})
		.then((data)=>{
			console.log("Data:",data)
		    document.location.reload()
		});
}


function addCookieItem(productId, action){
	console.log('User is not authenticated')
	// var total = '{{order.get_order_total|floatformat:2}}'
    // var totalq = '{{order.get_order_quantity|floatformat:2}}'
    // console.log("Order total",total);
    // console.log("Order quantity",totalq);

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
    //after cart is modified, setting the cookie data for cart
    //(cart) will now store new cart
	console.log('CART:', cart)
	/*For checking the order quantity */
       
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	console.log(document.cookie);
	document.location.reload()
}