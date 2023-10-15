const socket_noti = new WebSocket(`ws://127.0.0.1:8000/ws/noti/`)
const socket_chat = new WebSocket(`ws://127.0.0.1:8000/ws/chat/`)
const socket_message = new WebSocket(`ws://127.0.0.1:8000/ws/message/`)

function connect_noti() {
    socket_noti.onopen = function () {
        console.log("Websocket noti is connected")
    }
    socket_noti.onclose = function () {
        console.log("Websocket noti is disconnected")
        setInterval(function () {
            console.log("Websocket noti reconnecting...")
            connect_noti()
        }, 2000)
    }
}

function connect_chat() {
    socket_chat.onopen = function () {
        console.log("Websocket chat is connected")
    }
    socket_chat.onclose = function () {
        console.log("Websocket chat is disconnected")
        setInterval(function () {
            console.log("Websocket chat reconnecting...")
            connect_chat()
        }, 2000)
    }
}

function connect_message() {
    socket_message.onopen = function () {
        console.log("Websocket message is connected")
    }
    socket_message.onclose = function () {
        console.log("Websocket message is disconnected")
        setInterval(function () {
            console.log("Websocket message reconnecting...")
            connect_message()
        }, 2000)
    }
}

export {
    socket_noti, connect_noti, socket_chat, connect_chat, socket_message, connect_message
}