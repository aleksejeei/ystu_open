const scrollableElement = document.getElementById('chat-container');

function listener() {
    let posLeft = window.pageYOffset;
    console.log(posLeft)
}

scrollableElement.addEventListener('scroll', listener);

// Инициализация позиции скролла при загрузке страницы
listener();