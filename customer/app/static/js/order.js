// ------- grab selects, inputs and checkboxes ------- //
const item = document.getElementById('item');
const qty = document.getElementById('qty');

// ------------grab Modal targets --------------- //
const mItem = document.getElementById('mItem');
const mQty = document.getElementById('mQty');

// --------- copy selects, inputs and checkboxes to modal -------- //

let selectToModal = (target, value, text) => {
    target.textContent = text;
};

