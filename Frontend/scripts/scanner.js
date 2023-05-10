let popupBg = document.querySelector('.popup__hd-bg'); 
let popup = document.querySelector('.popup');
let openPopupButtons = document.querySelectorAll('.open-popup');
let closePopupButton = document.querySelector('.close-popup');

openPopupButtons.forEach((button) => { // Перебираем все кнопки
    button.addEventListener('click', (e) => { // Для каждой вешаем обработчик событий на клик
        e.preventDefault(); // Предотвращаем дефолтное поведение браузера
        popupBg.classList.add('active'); // Добавляем класс 'active' для фона
        popup.classList.add('active'); // И для самого окна
    })
});

closePopupButton.addEventListener('click',() => { // Вешаем обработчик на крестик
    popupBg.classList.remove('active'); // Убираем активный класс с фона
    popup.classList.remove('active'); // И с окна
});

document.addEventListener('click', (e) => { // Вешаем обработчик на весь документ
    if(e.target === popupBg) { // Если цель клика - фот, то:
        popupBg.classList.remove('active'); // Убираем активный класс с фона
        popup.classList.remove('active'); // И с окна
    }
});

async function change_use_scanner(id) {
        const btn = document.getElementById(`btn_use_${id}`);
        let using = btn.getAttribute('data-using').toLowerCase() == 'true' ? true : false;

        let url = `api/scanners/in_use/${id}`;
        let text = 'Не использовать';
        if (using == true) {
            url = `api/scanners/not_in_use/${id}`;
            text = 'Использовать';
        }

        await fetch(url=url)
            .then((resp) => resp.json())
            .then((data) => {
                if (data.status == 0) {
                    btn.textContent = text;
                    btn.setAttribute('data-using', !using);
                }
            })
            .catch(function(error) {
                console.log(error);
            })
}

async function delete_scanner(id) {
    let url = `api/scanners/${id}`;

    await fetch(url, {method: 'DELETE'})
        .then((resp) => resp.json())
        .then((data) => {
            if (data.status == 0) {

            }
        })
        .catch(function(error) {
            console.log(error);
        })
}