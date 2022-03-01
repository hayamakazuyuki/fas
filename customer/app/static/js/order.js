// ------- grab selects, inputs and checkboxes ------- //
const item = document.getElementById('item');

// ------------grab Modal targets --------------- //
const mItem = document.getElementById('mItem');

// --------- copy selects, inputs and checkboxes to modal -------- //

let selectToModal = (target, text) => {
    target.textContent = text;
};

