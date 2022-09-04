const btn = document.querySelector('button.mobile-menu-button');
const menu = document.querySelector('.mobile-menu');

//add event listener;
if (btn) {
    btn.addEventListener('click', () => {
        menu.classList.toggle("hidden");
        }
        )
    }
