// -------- item2 inputs show/hide --------------- //
const showItem2 = document.getElementById('showItem2');
const hideItem2 = document.getElementById('hideItem2');

const inputs2 = document.getElementById('inputs2');

const showHideItem2 = () => {
    showItem2.classList.toggle('hidden');
    hideItem2.classList.toggle('hidden');
};

showItem2.addEventListener('click', () => {

    showHideItem2();

    let template = document.getElementById('templateItem2');
    let clone = template.content.cloneNode(true);

    inputs2.appendChild(clone);

}, false)

hideItem2.addEventListener('click', () => {

    showHideItem2();

    while (inputs2.firstChild){
        inputs2.removeChild(inputs2.firstChild);
    };

}, false)

// -------- item3 inputs show/hide --------------- //
const showItem3 = document.getElementById('showItem3');
const hideItem3 = document.getElementById('hideItem3');

const inputs3 = document.getElementById('inputs3');

const showHideItem3 = () => {
    showItem3.classList.toggle('hidden');
    hideItem3.classList.toggle('hidden');
};

showItem3.addEventListener('click', () => {
    showHideItem3();

    let template = document.getElementById('templateItem3');
    let clone = template.content.cloneNode(true);

    inputs3.appendChild(clone);

}, false)

hideItem3.addEventListener('click', () => {
    showHideItem3();

    while (inputs3.firstChild){
        inputs3.removeChild(inputs3.firstChild);
    };

}, false)

// ---------- delivery inputs show/hide -------------- //
const showDelivery = document.getElementById('showDelivery');
const hideDelivery = document.getElementById('hideDelivery');
const deliveryError = document.getElementById('deliveryError');

const inputsDelivery = document.getElementById('inputsDelivery'); 

const showHideDelivery = () => {
    if(deliveryError) {
        deliveryError.textContent = '';
    };
    showDelivery.classList.toggle('hidden');
    hideDelivery.classList.toggle('hidden');
};

showDelivery.addEventListener('click', () => {
    showHideDelivery();
    let template = document.getElementById('templateDelivery');
    let clone = template.content.cloneNode(true);

    inputsDelivery.appendChild(clone);

}, false);

hideDelivery.addEventListener('click', () => {
    showHideDelivery();

    while (inputsDelivery.firstChild){
        inputsDelivery.removeChild(inputsDelivery.firstChild);
    };

}, false);

// ------- calculating the total delivery qty -------- //
const sumQty = () => {
    const deliveryQty = document.getElementById('deliveryQty');
    const qtys = document.getElementsByClassName('qty');
    let sum = 0;

    for (var i=0; i<qtys.length; i++) {
        sum =  sum + parseInt(qtys[i].value);
    };

    deliveryQty.value = sum;
    mQtyD.textContent = sum;
};

// ------ order form validation -------------- //
const confirmButton = document.getElementById('confirmButton'); // grab confirmButton;

confirmButton.addEventListener('click', () => {
    const selects = document.getElementsByTagName('select')
    const priceInputs = document.getElementsByClassName('price');
    const qtyInputs = document.getElementsByClassName('qty');

    const itemErrors = document.getElementsByClassName('itemError');

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

    const delivery = document.getElementById('delivery');

    if(delivery){
        const deliveryError = document.getElementById('deliveryError');
        const deliveryInputs = inputsDelivery.querySelectorAll('input'); // grab inputs in deliveryInputs div

        // check if delivery price and qty are number and more than 1
        for (var i=0; i<deliveryInputs.length; i++){
            value = deliveryInputs[i].value;
    
            if (value < 1){
                return deliveryError.textContent = '単価と数量は 1 以上を入力してください。';
            } else {
            };
        };
    };

    showModal();

}, false);

const showModal = () => {
    modal = document.getElementById('modal');
    modal.classList.toggle('hidden');
};

const onlyNumbers = n => {
    return n.replace(/[０-９]/g,s => String.fromCharCode(s.charCodeAt(0) - 65248)).replace(/\D/g,'');
};
