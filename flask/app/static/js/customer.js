const form = document.forms[0]; //documentの最初のフォームを指定

form.addEventListener('submit', (e) => {
    const id = document.getElementById('id').value;
    const error_id = document.getElementById('error_id'); //エラーメッセージを表示させる場所
    const regexInt = /^[1-9][0-9]*$/; //数字の1以上

    if (!(id.match(regexInt)) || !(id.length <= 5)) {
        const message = '半角数字のみ、最大５桁です。';
        error_id.textContent = message;
        e.preventDefault();
    }
}, false);
