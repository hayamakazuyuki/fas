// ------- grab selects, inputs and checkboxes ------- //
const item = document.getElementById('item');
const price = document.getElementById('price')
const qty = document.getElementById('qty');

const item2 = document.querySelector('item2');
const price2 = document.getElementById('price2');
const qty2 = document.getElementById('qty2');

const item3 = document.querySelector('item3');
const price3 = document.getElementById('price3');
const qty3 = document.getElementById('qty3');

const delivery = document.getElementById('delivery');
const deliveryPrice = document.getElementById('deliveryPrice')
const deliveryQty = document.getElementById('deliveryQty');

// ------------grab Modal targets --------------- //
const mItem = document.getElementById('mItem');
const mPrice = document.getElementById('mPrice')
const mQty = document.getElementById('mQty');

const mItem2 = document.getElementById('mItem2');
const mPrice2 = document.getElementById('mPrice2')
const mQty2 = document.getElementById('mQty2');

const mItem3 = document.getElementById('mItem3');
const mPrice3 = document.getElementById('mPrice3')
const mQty3 = document.getElementById('mQty3');

const mItemD = document.getElementById('mItemD');
const mPriceD = document.getElementById('mPriceD')
const mQtyD = document.getElementById('mQtyD');

// --------- copy selects, inputs and checkboxes to modal -------- //

let selectToModal = (target, value, text) => {
    valueText = value + text;
    target.textContent = valueText;
};

let inputToModal = (target, value) => {
    target.textContent = value;
};

// let checkToModal = (elem, target) => {
//     if (elem.checked) {
//         target.textContent = 'なし';
//     } else {
//         target.textContent = '';
//     };
// };

// -------- item2 inputs show/hide --------------- //
const showItem2 = document.getElementById('showItem2');
const hideItem2 = document.getElementById('hideItem2');

const inputs2 = document.getElementById('inputs2');

showItem2.addEventListener('click', () => {

    showItem2.classList.toggle('hidden');
    hideItem2.classList.toggle('hidden');

    let template = document.getElementById('templateItem2');
    let clone = template.content.cloneNode(true);

    inputs2.appendChild(clone);

}, false)

hideItem2.addEventListener('click', () => {
    mItem2.textContent = '';
    mPrice2.textContent = '';
    mQty2.textContent = '';

    hideItem2.classList.toggle('hidden');
    showItem2.classList.toggle('hidden');

    while (inputs2.firstChild){
        inputs2.removeChild(inputs2.firstChild);
    };

}, false)

// -------- item3 inputs show/hide --------------- //
const showItem3 = document.getElementById('showItem3');
const hideItem3 = document.getElementById('hideItem3');

const inputs3 = document.getElementById('inputs3');

showItem3.addEventListener('click', () => {

    showItem3.classList.toggle('hidden');
    hideItem3.classList.toggle('hidden');

    let template = document.getElementById('templateItem3');
    let clone = template.content.cloneNode(true);

    inputs3.appendChild(clone);

}, false)

hideItem3.addEventListener('click', () => {
    mItem3.textContent = '';
    mPrice3.textContent = '';
    mQty3.textContent = '';
    
    hideItem3.classList.toggle('hidden');
    showItem3.classList.toggle('hidden');

    while (inputs3.firstChild){
        inputs3.removeChild(inputs3.firstChild);
    };

}, false)

// ---------- delivery inputs show/hide -------------- //

deliveryPrice.addEventListener('change', () => {
    mItemD.textContent = '901 送料';
    let value = deliveryPrice.value;
    mPriceD.textContent = value;
});

const hideDelivery = document.getElementById('hideDelivery');
const showDelivery = document.getElementById('showDelivery');
const deliveryError = document.getElementById('deliveryError');
const inputsDelivery = document.getElementById('inputsDelivery'); // grab div divDelivery
const deliveryInputs = inputsDelivery.querySelectorAll('input'); // grab all inputs for delivery
const blockDelivery = document.getElementById('blockDelivery');

const showHideDelivery = () => {
    deliveryError.textContent = '';
    hideDelivery.classList.toggle('hidden');
    showDelivery.classList.toggle('hidden');
}

hideDelivery.addEventListener('click', () => {
    for (var i=0; i<deliveryInputs.length; i++) {
        deliveryInputs[i].value = ''
    };

    inputsDelivery.remove();
    showHideDelivery();

}, false);

showDelivery.addEventListener('click', () => {
    blockDelivery.append(inputsDelivery);
    showHideDelivery();

}, false)

// ------- calculating the total delivery qty -------- //
if(delivery){
    const deliveryQty = document.getElementById('deliveryQty');
    const qtys = document.getElementsByClassName('qty');
    let sum = 0;

    deliveryQty.addEventListener('focus', () => {
        for (var i=0; i<qtys.length; i++) {
            sum =  sum + parseInt(qtys[i].value);
        };

        deliveryQty.value = sum;
        mQtyD.textContent = sum;

    },false);
};

// ------ order form validation -------------- //
const confirmButton = document.getElementById('confirmButton'); // grab confirmButton;

confirmButton.addEventListener('click', () => {
    const selects = document.getElementsByTagName('select')
    const priceInputs = document.getElementsByClassName('price');
    const qtyInputs = document.getElementsByClassName('qty');

    const itemErrors = document.getElementsByClassName('itemError');
    const deliveryError = document.getElementById('deliveryError');

    // check if items are selected.
    for (var i=0; i<selects.length; i++) {
        selectedItem = selects[i].options[selects[i].selectedIndex].value;
        itemErrors[i].textContent = '';

        if (selects[i].options[selects[i].selectedIndex].value == '') {
            return itemErrors[i].textContent = '商品を選択してください。';
        } else if (!priceInputs[i].value || isNaN(priceInputs[i].value)) {
            return itemErrors[i].textContent = '単価を入力してください。';
        } else if (isNaN(qtyInputs[i].value) || qtyInputs[i].value == 0) {
            return itemErrors[i].textContent = '数量は 1 以上を入力してください。';
        };
    };

    if(blockDelivery.inputsDelivery){
        // check if delivery price and qty are number and more than 1
        for (var i=0; i<deliveryInputs.length; i++){
            value = deliveryInputs[i].value;
    
            if (isNaN(value) || value == ''){
                return deliveryError.textContent = '単価と数量は 1 以上を入力してください。';
            };
        };
    };

    showModal();

}, false);

const showModal = () => {
    modal = document.getElementById('modal');
    modal.classList.toggle('hidden');
}

const onlyNumbers = n => {
    return n.replace(/[０-９]/g,s => String.fromCharCode(s.charCodeAt(0) - 65248)).replace(/\D/g,'');
}
