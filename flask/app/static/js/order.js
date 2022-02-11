// item 2 inputs show and hide
const showItem2 = document.getElementById('showItem2');
const hideItem2 = document.getElementById('hideItem2');
const divInputs2 = document.getElementById('divInputs2');
const inputsItem1 = document.getElementById('inputsItem1')

showItem2.addEventListener('click', () => {

    showItem2.classList.toggle('hidden');
    hideItem2.classList.toggle('hidden');

    const inputsItem2 = inputsItem1.cloneNode(true);
    inputsItem2.id = 'inputsItem2';

    const labels = inputsItem2.getElementsByTagName('label');
    const selects = inputsItem2.getElementsByTagName('select');
    const inputs = inputsItem2.getElementsByTagName('input');

    // change labels
    labels[0].htmlFor = 'item2';
    labels[1].htmlFor = 'price2';
    labels[2].htmlFor = 'qty2';
    labels[3].htmlFor = 'noDelivery2';

    // change ID and name of selects2;
    selects[0].setAttribute('id', 'item2');
    selects[0].setAttribute('name', 'item2');

    // change IDs and names of inputs2
    inputs[0].setAttribute('id', 'price2');
    inputs[0].setAttribute('name', 'price2');
    inputs[0].value = '';

    inputs[1].setAttribute('id', 'qty2')
    inputs[1].setAttribute('name', 'qty2')
    inputs[1].value = '';

    inputs[2].setAttribute('id', 'noDelivery2')
    inputs[2].setAttribute('name', 'noDelivery2')

    return divInputs2.appendChild(inputsItem2);

}, false)

hideItem2.addEventListener('click', () => {
    hideItem2.classList.toggle('hidden');
    showItem2.classList.toggle('hidden');

    return inputsItem2.remove();

}, false)

// item3 inputs show and hide
const showItem3 = document.getElementById('showItem3');
const hideItem3 = document.getElementById('hideItem3');
const divInputs3 = document.getElementById('divInputs3');

showItem3.addEventListener('click', () => {
    showItem3.classList.toggle('hidden');
    hideItem3.classList.toggle('hidden');

    let inputsItem3 = inputsItem1.cloneNode(true);
    inputsItem3.id = 'inputsItem3'

    const labels = inputsItem3.getElementsByTagName('label');
    const selects = inputsItem3.getElementsByTagName('select');
    const inputs = inputsItem3.getElementsByTagName('input');

    // change labels
    labels[0].htmlFor = 'item3';
    labels[1].htmlFor = 'price3';
    labels[2].htmlFor = 'qty3';
    labels[3].htmlFor = 'noDelivery3';

    // change ID and name of selects2;
    selects[0].setAttribute('id', 'item3');
    selects[0].setAttribute('name', 'item3');

    // change IDs and names of inputs2
    inputs[0].setAttribute('id', 'price3');
    inputs[0].setAttribute('name', 'price3');
    inputs[0].value = '';

    inputs[1].setAttribute('id', 'qty3')
    inputs[1].setAttribute('name', 'qty3')
    inputs[1].value = '';

    inputs[2].setAttribute('id', 'noDelivery3')
    inputs[2].setAttribute('name', 'noDelivery3')

    return divInputs3.appendChild(inputsItem3);

}, false)

hideItem3.addEventListener('click', () => {
    hideItem3.classList.toggle('hidden');
    showItem3.classList.toggle('hidden');

    return inputsItem3.remove();

}, false)

// delivery fee inputs 
const hideDelivery = document.getElementById('hideDelivery');
const showDelivery = document.getElementById('showDelivery');
const deliveryError = document.getElementById('deliveryError');
const divDelivery = document.getElementById('divDelivery'); // grab div divDelivery
const deliveryInputs = divDelivery.querySelectorAll('input'); // grab all inputs for delivery

const toggleHidden = () => {
    deliveryError.textContent = '';
    hideDelivery.classList.toggle('hidden');
    showDelivery.classList.toggle('hidden');
}

hideDelivery.addEventListener('click', () => {
    for (var i=0; i<deliveryInputs.length; i++) {
        deliveryInputs[i].value = '';
        divDelivery.removeChild(deliveryInputs[i]);
    };

    toggleHidden();

}, false);

showDelivery.addEventListener('click', () => {
    for (var i=0; i<deliveryInputs.length; i++) {
        divDelivery.appendChild(deliveryInputs[i]);
    };

    toggleHidden();

}, false)


// calculating the total delivery quantity
const delivery = document.getElementById('delivery');

if(delivery){
    const deliveryQty = document.getElementById('deliveryQty');
    const qtys = document.getElementsByClassName('qty');
    let sum = 0;

    deliveryQty.addEventListener('focus', () => {
        for (var i=0; i<qtys.length; i++) {
            sum =  sum + parseInt(qtys[i].value);
        };

        deliveryQty.value = sum;

    },false);
};

// order form validation;
const confirmButton = document.getElementById('confirmButton'); // grab confirmButton;

confirmButton.addEventListener('click', (e) => {
    const selects = document.getElementsByTagName('select')
    const priceInputs = document.getElementsByClassName('price');
    const qtyInputs = document.getElementsByClassName('qty');

    const deliveryInputs = document.getElementById('divDelivery').querySelectorAll('input');

    const itemErrors = document.getElementsByClassName('itemError');
    const deliveryError = document.getElementById('deliveryError');

    // clear error messages.
    deliveryError.textContent = '';

    // check if items are selected.
    for (var i=0; i<selects.length; i++) {
        itemErrors[i].textContent = '';

        if (selects[i].options[selects[i].selectedIndex].value == '') {
            return itemErrors[i].textContent = '商品を選択してください。';
        } else if (!priceInputs[i].value || isNaN(priceInputs[i].value)) {
            return itemErrors[i].textContent = '単価を入力してください。';
        } else if (isNaN(qtyInputs[i].value) || qtyInputs[i].value == 0) {
            return itemErrors[i].textContent = '数量は 1 以上を入力してください。';
        }
    };

    // check if delivery price and qty are number and more than 1 
    if(deliveryInputs){
        for (var i=0; i<deliveryInputs.length; i++){
            value = deliveryInputs[i].value;
            if (isNaN(value) || value == ''){
                return deliveryError.textContent = '単価と数量は 1 以上を入力してください。';
            };
        };
    };
    modal();
}, false);

const modal = () => {
    const delivery = document.getElementById('delivery')
    const mItem1 = document.getElementById('mItem1');
    const mItem2 = document.getElementById('mItem2');
    const mItem3 = document.getElementById('mItem3');
    const mItemD = document.getElementById('mItemD');

    alert(mItem1.id)
    
}