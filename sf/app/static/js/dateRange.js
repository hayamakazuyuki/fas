const date_from = document.getElementById('date_from');
const date_to = document.getElementById('date_to');

date_from.addEventListener('change', () => {

    let from_date_value = date_from.value;
    date_to.setAttribute('min', from_date_value);

    }, false);
