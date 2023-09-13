var id = 'af2a17d6-7dbb-4dc0-aa0d-469867001b63'

var Socket = new WebSocket('ws://'+window.location.host+'/wc/OrderTrack/' + id);

Socket.onopen = function () {
    console.log("connected....")
}

Socket.onmessage = function (event) {
    var data = JSON.parse(event.data)
    var value = data.payload.progress
    console.log("new....", data.payload.status)

    increaseStatusProgress(value, data.payload.status)

};

Socket.onclose = function (e) {
    console.log('Connection closed');
}

function increaseStatusProgress(value, status) {

    var progress = document.querySelector('.progress-bar')
    var status_html = document.querySelector('#status')

    if (value == 100) {
        console.log("ss")
        progress.classList.add('bg-success')
    }
    if (value == 80) {
        progress.classList.add('bg-primary')
    }

    if (status === 'Order Recieved') {
        status_html.classList.add('bg-info');
    }
    else if (status == 'Baking') {
        status_html.classList.add('bg-primary');
    }
    else if (status === 'Baked') {
        status_html.classList.add('bg-warning');
    }
    else if (status === 'Out for delivery') {
        status_html.classList.add('bg-danger');
    }
    else {
        status_html.classList.add('bg-success');
    }


    status_html.innerHTML = status
    progress.style.width = value + "%"

}