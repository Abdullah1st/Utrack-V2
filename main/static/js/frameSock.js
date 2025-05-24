document.addEventListener('DOMContentLoaded', () => {
    const socket = new WebSocket('ws://' + window.location.host + '/ws/clientFrames/');

    socket.onopen = () => {
        console.log("camera frames WebSocket opened");
        window.vid = document.getElementById('imgFrame');
        socket.send("Hi I am the client")       
    }
    
    socket.onmessage = (ev) => {
        vid.src = URL.createObjectURL(new Blob([ev.data], {type:'image/jpeg'}));
    };


    socket.onerror = error => console.log('WebSocket Error ' + error.message);

    window.addEventListener('beforeunload', function() {
        if (socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
    });
});