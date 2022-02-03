const form = document.forms[0]; //documentの最初のフォームを指定

form.addEventListener('submit', (e) => {

    // regular expressions;
    const reNumOnly = /^[0-9]+$/; //半角数字（空白OK）の正規表現
    const reId = /^[1-9][0-9]*/;
    const reTel = /\d{2,4}-\d{2,4}-\d{2,4}$/; //数字（2〜4桁）-数字（2〜4桁）-数字（2〜4桁）
    const reTelNumOnly = /^0[1-9][0-9]{8,}/; //0から始まり1~9、そして数字のみ８つ以上

    // values for validation;
    let id = document.getElementById('id').value; //事業所ID
    let zip = document.getElementById('zip').value; //郵便番号
    let telephone = document.getElementById('telephone').value; //電話番号
    let tel_num = telephone.replace(/-/g,'');

    // elements to display error messages;
    const error_id = document.getElementById('error_id'); // 事業所ID
    const error_zip = document.getElementById('error_zip'); // 郵便番号
    const error_tel = document.getElementById('error_tel'); // 電話番号

    // error messages;
    const errorNumOnly = '半角数字のみです';
    const errorTel = '有効な電話番号ではありません';

    e.preventDefault();

    if (!id.match(reId)) {
        return error_id.textContent = errorNumOnly;
    } else if (!zip.match(reNumOnly)) {
        return error_zip.textContent = errorNumOnly;
    } else if (!telephone.match(reTel)) {
        return error_tel.textContent = errorTel;
    } else if (!tel_num.match(reTelNumOnly)) {
        return error_tel.textContent = errorTel;
    } else {
        document.forms[0].submit();
    }
}, false);
