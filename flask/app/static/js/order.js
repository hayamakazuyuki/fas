// appends order inputs;
const appendInputs = document.getElementById('appendInputs');

// appendInputs.addEventListener('click', (e) => {
//     const divItem = document.getElementById('divItem'); // grab div for item;
//     const item2 = document.getElementById('item2'); // grab div for item2;
//     const item3 = document.getElementById('item3'); // grab div for item3;

//     if (!item2.hasChildNodes()){
//         // clone divItem nodes to divItem2;
//         let divItem2 = divItem.cloneNode(true);
//         // change divItem2 id from divItem to divItem2;
//         divItem2.id = 'divItem2';

//         let labels2 = divItem2.getElementsByTagName('label'); // grab labels in divItem2;
//         let selects2 = divItem2.getElementsByTagName('select'); // grab selects in divItem2;
//         let inputs2 = divItem2.getElementsByTagName('input'); // grab inputs in divItem2;

//         // change labels
//         labels2[0].htmlFor = 'item2';
//         labels2[1].htmlFor = 'price2';
//         labels2[2].htmlFor = 'qty2';
//         labels2[3].htmlFor = 'noDelivery2';

//         // change ids and names of selects2;
//         selects2[0].setAttribute('id', 'item2');
//         selects2[0].setAttribute('name', 'item2');
        
//         // change ids and names of inputs2;
//         inputs2[0].setAttribute('id','price2');
//         inputs2[0].setAttribute('name','price2');
//         inputs2[0].value = '';
//         inputs2[1].setAttribute('id','qty2');
//         inputs2[1].setAttribute('name','qty2');
//         inputs2[1].value = '';
//         inputs2[2].setAttribute('id','noDelivery2');
//         inputs2[2].setAttribute('name','noDelivery2');

//         return item2.appendChild(divItem2);
//     };

//     if (!item3.hasChildNodes()){
//         // clone divItem nodes to divItem2;
//         let divItem3 = divItem.cloneNode(true);
//         // change divItem2 id from divItem to divItem2;
//         divItem3.id = 'divItem3';

//         let labels3 = divItem3.getElementsByTagName('label'); // grab labels in divItem2;
//         let selects3 = divItem3.getElementsByTagName('select'); // grab selects in divItem2;
//         let inputs3 = divItem3.getElementsByTagName('input'); // grab inputs in divItem2;

//         // change labels
//         labels3[0].htmlFor = 'item3';
//         labels3[1].htmlFor = 'price3';
//         labels3[2].htmlFor = 'qty3';
//         labels3[3].htmlFor = 'noDelivery3';

//         // change ids and names of selects2;
//         selects3[0].setAttribute('id', 'item3');
//         selects3[0].setAttribute('name', 'item3');
        
//         // change ids and names of inputs2;
//         inputs3[0].setAttribute('id','price3');
//         inputs3[0].setAttribute('name','price3');
//         inputs3[0].value = '';
//         inputs3[1].setAttribute('id','qty3');
//         inputs3[1].setAttribute('name','qty3');
//         inputs3[1].value = '';
//         inputs3[2].setAttribute('id','noDelivery3');
//         inputs3[2].setAttribute('name','noDelivery3');

//         return item3.appendChild(divItem3);
//     };



// }, false);


// reducing item inputs;
// const removeInputs = document.getElementById('removeInputs');

// removeInputs.addEventListener('click', (e) => {
//     const item2 = document.getElementById('item2'); // grab div for item2;
//     const item3 = document.getElementById('item3'); // grab div for item3;

//     if (item3.hasChildNodes()){
//         divItem3.remove();
//         return;
//     };
//     if (item2.hasChildNodes()){
//         divItem2.remove();
//         return;
//     };
// }, false)

// item 2 inputs show and hide
const showItem2 = document.getElementById('showItem2');
const hideItem2 = document.getElementById('hideItem2');
const divInputs2 = document.getElementById('divInputs2');

showItem2.addEventListener('click', () => {
    const inputsItem1 = document.getElementById('inputsItem1')

    showItem2.classList.toggle('hidden');
    hideItem2.classList.toggle('hidden');

    let inputsItem2 = inputsItem1.cloneNode(true);
    inputsItem2.id = 'inputsItem2'
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

showItem3.addEventListener('click', () => {
    showItem3.classList.toggle('hidden');
    hideItem3.classList.toggle('hidden');

}, false)

hideItem3.addEventListener('click', () => {
    hideItem3.classList.toggle('hidden');
    showItem3.classList.toggle('hidden');

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

if(deliveryInputs[1]){

    const item2 = document.getElementById('item2'); // grab div for item2;
    const item3 = document.getElementById('item3'); // grab div for item3;

    deliveryInputs[2].addEventListener('focus', (e) => {
        let qty = parseInt(document.getElementById('qty').value);
        let qty2 = '';
        let qty3 = '';
        if(item2.hasChildNodes()){
            qty2 = parseInt(document.getElementById('qty2').value);
            }
        if(item3.hasChildNodes()){
            qty3 = parseInt(document.getElementById('qty3').value);
            }
        deliveryInputs[2].value = qty + qty2 + qty3;
        },false);
    }


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
}, false);
