// appends order inputs;
const appendInputs = document.getElementById('appendInputs');

appendInputs.addEventListener('click', (e) => {
    const divItem = document.getElementById('divItem'); // grab div for item;
    const item2 = document.getElementById('item2'); // grab div for item2;
    const item3 = document.getElementById('item3'); // grab div for item3;

    if (!item2.hasChildNodes()){
        // clone divItem nodes to divItem2;
        let divItem2 = divItem.cloneNode(true);
        // change divItem2 id from divItem to divItem2;
        divItem2.id = 'divItem2';

        let labels2 = divItem2.getElementsByTagName('label'); // grab labels in divItem2;
        let selects2 = divItem2.getElementsByTagName('select'); // grab selects in divItem2;
        let inputs2 = divItem2.getElementsByTagName('input'); // grab inputs in divItem2;

        // change labels
        labels2[0].htmlFor = 'item2';
        labels2[1].htmlFor = 'price2';
        labels2[2].htmlFor = 'qty2';
        labels2[3].htmlFor = 'noDelivery2';

        // change ids and names of selects2;
        selects2[0].setAttribute('id', 'item2');
        selects2[0].setAttribute('name', 'item2');
        
        // change ids and names of inputs2;
        inputs2[0].setAttribute('id','price2');
        inputs2[0].setAttribute('name','price2');
        inputs2[0].value = '';
        inputs2[1].setAttribute('id','qty2');
        inputs2[1].setAttribute('name','qty2');
        inputs2[1].value = '';
        inputs2[2].setAttribute('id','noDelivery2');
        inputs2[2].setAttribute('name','noDelivery2');

        return item2.appendChild(divItem2);
    };

    if (!item3.hasChildNodes()){
        // clone divItem nodes to divItem2;
        let divItem3 = divItem.cloneNode(true);
        // change divItem2 id from divItem to divItem2;
        divItem3.id = 'divItem3';

        let labels3 = divItem3.getElementsByTagName('label'); // grab labels in divItem2;
        let selects3 = divItem3.getElementsByTagName('select'); // grab selects in divItem2;
        let inputs3 = divItem3.getElementsByTagName('input'); // grab inputs in divItem2;

        // change labels
        labels3[0].htmlFor = 'item3';
        labels3[1].htmlFor = 'price3';
        labels3[2].htmlFor = 'qty3';
        labels3[3].htmlFor = 'noDelivery3';

        // change ids and names of selects2;
        selects3[0].setAttribute('id', 'item3');
        selects3[0].setAttribute('name', 'item3');
        
        // change ids and names of inputs2;
        inputs3[0].setAttribute('id','price3');
        inputs3[0].setAttribute('name','price3');
        inputs3[0].value = '';
        inputs3[1].setAttribute('id','qty3');
        inputs3[1].setAttribute('name','qty3');
        inputs3[1].value = '';
        inputs3[2].setAttribute('id','noDelivery3');
        inputs3[2].setAttribute('name','noDelivery3');

        return item3.appendChild(divItem3);
    };



}, false);

//     if (!area_item2.hasChildNodes()) {


//         } else if (!area_item3.hasChildNodes()) {
//             div_item3 = div_item1.cloneNode(true);
//             div_item3.id = 'div_item3';
//             let labels3 = div_item3.getElementsByTagName('label');
//             let select3 = div_item3.getElementsByTagName('select');
//             let inputs3 = div_item3.getElementsByTagName('input');
//             // 各labelのforを変更する
//             labels3[0].htmlFor = 'item3';
//             labels3[1].htmlFor = 'item3_price';
//             labels3[2].htmlFor = 'item3_qty';
//             labels3[3].htmlFor = 'no_delivery3';
//             // selectのidとnameを変更
//             select3[0].setAttribute('id','item3');
//             select3[0].setAttribute('name','item3');
//             // inputの各idとnameを変更
//             inputs3[0].setAttribute('id','item3_price');
//             inputs3[0].setAttribute('name','item3_price');
//             inputs3[0].value = '';
//             inputs3[1].setAttribute('id','item3_qty');
//             inputs3[1].setAttribute('name','item3_qty');
//             inputs3[1].value = '';
//             inputs3[2].setAttribute('id','no_delivery3');
//             inputs3[2].setAttribute('name','no_delivery3');
//             // area_item3にアペンドする
//             return area_item3.appendChild(div_item3);
//         } else {
//             return;
//         };
//     }, false);

// reducing item inputs;
const removeInputs = document.getElementById('removeInputs');

removeInputs.addEventListener('click', (e) => {
    const item2 = document.getElementById('item2'); // grab div for item2;
    const item3 = document.getElementById('item3'); // grab div for item3;

    if (item3.hasChildNodes()){
        divItem3.remove();
        return;
    };
    if (item2.hasChildNodes()){
        divItem2.remove();
        return;
    };
}, false)

//商品入力欄を削除（減らす）
//     if (area_item3.hasChildNodes()) {
//         div_item3.remove();
//         return;
//     } else if (area_item2.hasChildNodes()) {
//         div_item2.remove();
//         return;
//     } else {
//         return;
//         };//     }, false);



// removing and appending delivery fee inputs;
const deliveryInclude = document.getElementById('deliveryInclude'); // grab deliveryInclude checkbox
const divDelivery = document.getElementById('divDelivery'); // grab div divDelivery
const inputs = divDelivery.querySelectorAll('input'); // grab all inputs for delivery

deliveryInclude.addEventListener('change', (e) => {
    const deliveryError = document.getElementById('deliveryError');

    if(deliveryInclude.checked){
        for (var i=0; i<3; i++){
            inputs[i].value = '';
            divDelivery.removeChild(inputs[i]);
        };

    if(deliveryError.textContent){
        deliveryError.textContent = '';
    };

    } else {
        for (var i=0; i<3; i++){
            divDelivery.appendChild(inputs[i]);
        };
    };
}, false);


// order form validation;
const confirmButton = document.getElementById('confirmButton'); // grab confirmButton;

confirmButton.addEventListener('click', (e) => {
    const deliveryInclude = document.getElementById('deliveryInclude');
    const deliveryError = document.getElementById('deliveryError');
    const deliveryInputs = document.getElementById('divDelivery').querySelectorAll('input');

    const reGreater1 = /^[1-9]\d*$/; //半角数字1以上の正規表現

    const msgGreater1 = '数量は1以上を入力してください。';
    
    if(!deliveryInclude.checked){
        for (var i=0; i<3; i++){
            if(!deliveryInputs[i].value.match(reGreater1)){
                return deliveryError.textContent = '送料単価と数量は 1 以上を入力してください。';
            };
        };
    };
}, false);


// 注文フォームのバリデーション
// const regexNumOnly = /^[0-9]+$/; //半角数字（空文字NG）の正規表現。0はオッケー

// const error_order = document.getElementById('error_order'); //商品のエラーメッセージを表示させる場所
// const area_items = document.getElementById('area_items'); //商品入力エリア

// let item_inputs = area_items.getElementsByTagName('input'); //商品入力エリア内のinputタグ

// to_confirm.addEventListener('click', function(e){
//     const msg_select_item = '商品を選択してください。'
//     const msg_number_only = '単価と数量は半角数字で入力してください。';
//     const msg_greater1 = '数量は1以上を入力してください。';

//     if(item.options[item.selectedIndex].value == ''){
//         return error_order.textContent = msg_select_item
//         }

//     if(area_item2.hasChildNodes()){
//         if(item2.options[item2.selectedIndex].value == ''){
//             return error_order.textContent = msg_select_item
//             }
//         }

//     if(area_item3.hasChildNodes()){
//         if(item3.options[item3.selectedIndex].value == ''){
//             return error_order.textContent = msg_select_item
//             }
//         }

//     for(let j=0; j<item_inputs.length; j++){
//             let item_value = item_inputs[j].value;
//             if(!item_value.match(regexNumOnly)){
//                 return error_order.textContent = msg_number_only;
//             } else if(!item_inputs[1].value.match(regexGreater1)){
//                 return error_order.textContent = msg_greater1;
//             }
//         }

//     if(item_inputs.length == 9){
//        if(!item_inputs[7].value.match(regexGreater1)){
//             return error_order.textContent = msg_greater1;
//        }
//     }

//     if(item_inputs.length == 6){
//        if(!item_inputs[4].value.match(regexGreater1)){
//             return error_order.textContent = msg_greater1;
//        }
//     }


//     modal();
// }, false);
