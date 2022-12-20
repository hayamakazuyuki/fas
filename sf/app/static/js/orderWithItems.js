

// ------- calculating the total delivery qty -------- //
// const sumQty = () => {
//     const deliveryQty = document.getElementById('deliveryQty');
//     const qtys = document.getElementsByClassName('qty');
//     let sum = 0;

//     for (var i=0; i<qtys.length - 1; i++) {
//         sum =  sum + parseInt(qtys[i].value);
//     };

//     deliveryQty.value = sum;
// };

// ------ order form validation -------------- //



const confirmButton = document.getElementById('confirmButton'); // grab confirmButton;

confirmButton.addEventListener('click', () => {
    const products = document.getElementsByClassName('product');
    const prices = document.getElementsByClassName('price');
    const qtys = document.getElementsByClassName('qty');

    const itemErrors = document.getElementsByClassName('itemError');

    // check if items are selected.
    for (var i=0; i<products.length; i++) {
        itemErrors[i].textContent = '';

        if (!prices[i].value || isNaN(prices[i].value)) {
            return itemErrors[i].textContent = '単価を入力してください。';
        } else if (isNaN(qtys[i].value) || qtys[i].value == 0) {
            return itemErrors[i].textContent = '数量は 1 以上を入力してください。';
        };
    };

    prepareModal(products, prices, qtys);

    showModal();

}, false);

const prepareModal = (products, prices, qtys) => {

    let productList = {
        602: "FUROSHIKI 45L （半透明）",
        603: "FUROSHIKI 70L （半透明）",
        604: "FUROSHIKI 90L （半透明）",
        605: "FUROSHIKI 120L （半透明）",
        606: "FUROSHIKI 45L （青色）",
        607: "FUROSHIKI 70L （青色）",
        608: "FUROSHIKI 90L （青色）",
        609: "FUROSHIKI 45L （黄色）",
        610: "FUROSHIKI 70L （黄色）",
        611: "FUROSHIKI 90L （黄色）",
        615: "FUROSHIKI 200L（半透明）",
        622: "FUROSHIKI 45L(半透明)200枚",
        623: "FUROSHIKI 150L(半透明)",
        624: "FUROSHIKI 45L（青）200枚",
        625: "FUROSHIKI 45L（黄）200枚",
        626: "FUROSHIKI 90L(半透明) 0.05",
        627: "FUROSHIKI 70L(半透明) 0.05",
        628: "パレットカバー",
        629: "FUROSHIKI 45L（半透明、0.03、50枚x10箱）",
        630: "FUROSHIKI 45L（半透明50枚）",
        651: "FUROSHIKI 70L（半透明、0.03、100枚x5箱）",
        680: "再生材ごみ袋（1500x2000）",
        901: "ごみ袋送料"
    };

    const modalTbody = document.getElementById('modalTbody');

    if (modalTbody.childNodes) {
        while (modalTbody.firstChild) {
            modalTbody.removeChild(modalTbody.firstChild);
        };
    };

    for (var j=0; j<products.length; j++) {
        let row = [];
        row.push(products[j].value + productList[products[j].value]);
        row.push(prices[j].value);
        row.push(qtys[j].value);
        let tr = document.createElement('tr');

        for (var k=0; k<3; k++) {
            let td = document.createElement('td');
            td.textContent = row[k];
            tr.appendChild(td);
        };

        modalTbody.appendChild(tr);
    };
};

const showModal = () => {
    modal = document.getElementById('modal');
    modal.classList.toggle('hidden');
};
