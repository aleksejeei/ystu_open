const socket = new WebSocket(`ws://${window.location.host}/messenger/updates/`);


socket.onopen = function(event) {
    console.log('Connected');
    get_messages();
    //socket.send(JSON.stringify({ 'message': 'Привет, сервер!' }));
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    //console.log(event);
    if (JSON.parse(event.data).all_messages) {
    reload_page(JSON.parse(event.data))
    }
    //console.log('Сообщение от сервера:', data.message);
};

socket.onclose = function(event) {
    console.log('Соединение закрыто');
};

socket.onerror = function(error) {
    console.error('Ошибка WebSocket:', error);
};

function send_message() {
    if (socket.readyState === WebSocket.OPEN) {
        const input=document.getElementById("message");
        message = input.value;
        const url = new URL(window.location.href);
        const chat_id = url.searchParams.get('id');
        const info = {
        type: 'send_message',
        message: message,
        chat_id: chat_id,
        }
        socket.send(JSON.stringify(info));
        input.value = '';
    } else {
        console.log('Соединение еще не установлено. Попробуйте позже.');
    }
}


function reload_page(messages) {
    const parentElement = document.getElementById('chat-container');
    const list_m = messages.all_messages;
    while (parentElement.firstChild) {
        parentElement.removeChild(parentElement.firstChild);
        }
    //console.log(list_m)
    list_m.forEach((element) => {
        //console.log(element[0])
        const divmes = document.createElement('div');
        if (element[3] === 'current') divmes.className = 'message my-message';
        else divmes.className = 'message other-message';

        parentElement.appendChild(divmes);

        const sendmes = document.createElement('div');
        sendmes.className = 'sender';
        if (element[3] !== 'current') sendmes.textContent = element[4]
        divmes.appendChild(sendmes);

        const text = document.createElement('div');
        text.textContent = element[1];
        divmes.appendChild(text);

        const time = document.createElement('div');
        time.className = 'timestamp';
        time.textContent = element[2];
        divmes.appendChild(time);

    })

    //document.getElementById("scroll").scrollTop = document.getElementById("scroll").scrollHeight;
    //console.log(parentElement.scrollTop)
}

function get_messages() {
    if (socket.readyState === WebSocket.OPEN) {
        const url = new URL(window.location.href);
        const chat_id = url.searchParams.get('id');
        const info = {
        type: 'get_messages',
        chat_id
        }
        socket.send(JSON.stringify(info));
    }
    else {
        console.log('Соединение еще не установлено. Попробуйте позже.');
    }
}




setInterval(() => {get_messages()}, 1000)