// Функция для проверки наличия текста в поле ввода
function checkInput() {
    const messageInput = document.getElementById('message');
    const sendButton = document.getElementById('send-message');

    // Показываем кнопку, если есть текст, иначе скрываем
    if (messageInput.value.trim() !== '') {
        sendButton.style.display = 'block';
    } else {
        sendButton.style.display = 'none';
    }
}

// Добавляем обработчик события для поля ввода
document.getElementById('message').addEventListener('input', checkInput);

// Существующий код для обработки нажатия клавиши Enter
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        document.getElementById('send-message').click();
    }
}

// Добавляем обработчик события при загрузке страницы
window.onload = function() {
    document.addEventListener('keypress', handleKeyPress);
};


