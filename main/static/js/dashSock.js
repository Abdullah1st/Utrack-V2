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
            showAlert(data.violator);
        }
        else if (data == 'new_entry'){
            console.log('new entry ! ! ! !!  ! ! ! !');
            sCounter.innerHTML = parseInt(sCounter.innerHTML) + 1;
        }
    }

    socket.onerror = error => console.log('WebSocket Error ' + error.message);

    window.addEventListener('beforeunload', function() {
        if (socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
    });
});