let products = document.getElementsByClassName('update-basket')

for (let i = 0; i < products.length; i++) {
    products[i].addEventListener('click', function () {
        let product_id = this.dataset.product
        let action = this.dataset.action

        if (user != 'AnonymousUser') {
            UpdateUserOrder(product_id, action)

        } else {
            addCookieItem(product_id, action)
        }

    })
}

function UpdateUserOrder(product_id, action) {

    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'product_id': product_id, 'action': action })
    })

        .then((response) => {
            return response.json()
        })

        .then((response) => {
            location.reload()
        })

}

function addCookieItem(product_id, action) {

    if (action == 'add') {
        if (basket[product_id] == undefined) {
            basket[product_id] = { 'quantity': 1 }
        } else {
            basket[product_id]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        basket[product_id]['quantity'] -= 1
        if (basket[product_id]['quantity'] <= 0) {
            delete basket[product_id]
        }
    }

    document.cookie = 'basket=' + JSON.stringify(basket) + ";domain=;path=/"
    location.reload()
}