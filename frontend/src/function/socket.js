const socket_noti = new WebSocket(`ws://127.0.0.1:8000/ws/noti/`)

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
    socket_noti.onmessage = function (e) {
        var data = JSON.parse(e.data)
        console.log(data)
    }
}

export {
    socket_noti, connect_noti
}