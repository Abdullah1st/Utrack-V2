document.addEventListener('DOMContentLoaded', () => {
    socket.onopen = () => {
        console.log("dashboard WebSocket opened");
        if (vCounter){
            createGraph();
        }
    }

    socket.onmessage = (ev) => {
        const data = JSON.parse(ev.data)
        if (data.notification){
            showNot(data.notification); 
        }
        else if (data.violator){
            if (vCounter){
                sCounter.innerHTML = parseInt(sCounter.innerHTML) + 1;
            }
            showAlert(data.violator);
        }
    }

    socket.onerror = error => console.log('WebSocket Error ' + error.message);

    window.addEventListener('beforeunload', function() {
        if (socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
    });
});