const close_alert = document.querySelectorAll('.close_alert');

close_alert.forEach((x) =>
    x.addEventListener('click', (e) => {
    x.parentElement.classList.add('hidden');
    })
)
