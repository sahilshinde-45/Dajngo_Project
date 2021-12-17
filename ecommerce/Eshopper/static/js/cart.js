var updateBtns = document.getElementsByClassName('update-cart')


for(var i = 0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){

        var productId = this.dataset.product
        var action = this.dataset.action

        console.log('productId:', productId, 'action:', action)

        console.log('user:',user)

        if(user == "AnonymousUser")
        {
            console.log("NOT LOGGED IN");
            alert('Hello User to use this functionality login is required.. PLEASE LOGIN.');
        }
        else
        {
            UpdateUserOrder(productId,action)
        }
    })
}


function UpdateUserOrder(productId,action)
{
    console.log("logged in successfully sending data...")

    var url = '/cart/updateitem/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type' : 'application/json',
            'X-CSRFToken'  : csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data', data)
        location.reload()
    })
}

let quantityField = document.getElementsByClassName('quantity-update')

console.log('hi')

for(let i = 0; i< quantityField.length; i++)
{
    
    quantityField[i] = addEventListener('change',function(){
        let quantityFieldvalue = quantityField[i].value
        let quantityFieldProduct = quantityField[i].parentElement.parentElement.children[1].children[0].innerText
        

        console.log('quantityFieldProduct',quantityFieldProduct,'quantityFieldvalue' ,quantityFieldvalue) 

        
        let url = '/cart/updatequantity/'
        fetch(url, {
            method:'POST',
            headers:{
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,            
        },
        body:JSON.stringify({'qfp': quantityFieldProduct, 'qfv':quantityFieldvalue})
        })
        .then(response => response.json())
        .then(data => console.log(data))
        location.reload()

    })
   
}







