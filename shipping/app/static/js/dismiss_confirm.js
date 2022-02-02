const confirm_submit = () => {
    // grab the form in the document;
    const form = document.forms[0];
    // grab the checkboxes(name=dismiss) in the form;
    const checkbox = document.querySelectorAll('input[type="checkbox"]');

    for (let i=0; i<checkbox.length; i++) {
        if (checkbox[i].checked) {
            confirmation = window.confirm('非表示にして良いですか？');

            if (confirmation) {
                form.submit();
            }
        }
    }
}
