document.addEventListener('DOMContentLoaded', () => {
    window.socket = new WebSocket('ws://' + window.location.host + '/ws/dashFrames/');
    window.showAlert = showAlert;
    window.showNot = showNotifications;
    window.vCounter = document.getElementById('violations-counter');
    window.sCounter = document.getElementById('students-counter');
    let doneNotified = true;
    const host = window.location.origin;
    const notificationContainer = document.getElementById('notification-container');
    const dropdownMenu = document.getElementById('notificationDropdown');

    dropdownMenu.addEventListener('click', (event) => {
        event.stopPropagation();
    });

    function showAlert(violator) {

        const alertContainer = document.getElementById('alert-container');
        const alertImage = document.getElementById('alert-image');
        socket.send(JSON.stringify({
            'acknowledgement': violator.id
        }))

        setTimeout(() => {
            // Clear previous image and set new one
            alertImage.innerHTML = `<img src="${host}/images/alerts/${violator.imageID}/" style="width: 100%; height: 100%; object-fit: contain;">`;
        }, 50);

        document.getElementById('confirmm-btn').onclick = function () {
            handleAlertResponse(violator.id, true);
            alertContainer.style.display = 'none';
            if (vCounter) {
                vCounter.innerHTML = parseInt(vCounter.innerHTML) + 1;
                updateGraph(vCounter.innerHTML, violator.date);
            }
        };

        document.getElementById('ignoree-btn').onclick = function () {
            handleAlertResponse(violator.id, false);
            alertContainer.style.display = 'none';
        };

        alertContainer.style.display = 'block';

        //Auto hide
        setTimeout(() => {
            alertContainer.style.display = 'none';
            showNotifications(violator);
        }, 10000);
    }
    function handleAlertResponse(violatorID, confirmed) {
        socket.send(JSON.stringify({
            'rmNotification': {
                'violatorID': violatorID,
                'isConfirmed': confirmed
            }
        }));
    }
    function timeAgo(dateString) {
        // Parse the date string
        const date = new Date(dateString);
        const now = new Date();

        // Calculate the time difference in milliseconds
        const diffMs = now - date;

        // Convert milliseconds to seconds
        const diffSec = Math.floor(diffMs / 1000);

        // Define time intervals in seconds
        const minute = 60;
        const hour = minute * 60;
        const day = hour * 24;

        // Determine the appropriate time unit and value
        if (diffSec < minute) {
            return { 'timeAgo': `${diffSec} seconds ago`, 'isToday': true };

        } else if (diffSec < hour) {
            const minutes = Math.floor(diffSec / minute);
            return {
                'timeAgo': `${minutes} ${minutes === 1 ? 'minute' : 'minutes'} ago`,
                'isToday': true
            };
        } else if (diffSec < day) {
            const hours = Math.floor(diffSec / hour);
            return  {'timeAgo': `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`, 'isToday': true};
           
        } else {
            const days = Math.floor(diffSec / day);
            return { 'timeAgo': `${days} ${days === 1 ? 'day' : 'days'} ago`, 'isToday': false};
        }
    }
    handleNotification = function (id, isConfirmed, date) {
        handleAlertResponse(id, isConfirmed);
        document.getElementById(id).style.display = 'none';
        if (vCounter){
            vCounter.innerHTML = parseInt(vCounter.innerHTML) + 1;
        }
    }

    function showNotifications(notification) {
        if (doneNotified) document.querySelector('.notification-bell').className += ' unread';
        doneNotified = false;
        notificationContainer.innerHTML += `
        <div class="row align-items-center" id=${notification.id}>
                  <div class="col-auto" id='avatarContainer'>
                    <!-- Avatar -->
                    <img src="${host}/images/alerts/${notification.imageID}/" style="width: 100px; height: 100%; object-fit: contain;">
                  </div>
                  <div class="col ps-0 ms-2">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h4 class="h6 mb-0" style="color:rgb(219, 118, 118);">Pending</h4>
                        <i class="bi bi-exclamation-octagon-fill"
                          style="margin-left: 30%; font-size: 1.2rem; color:rgb(255, 130, 130);"></i>
                      </div>
                      <div class="text-end" style="margin-right: 15px; margin-bottom: 14%;">
                        <small id="timeAgo">${timeAgo(notification.date).timeAgo}</small>
                      </div>
                    </div>
                    <p class="font-small mt-3">
                      <button id="confirm-btn" onclick="handleNotification(${notification.id}, true)"
                        style="flex: 1; padding: 15px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                        <i class="bi bi-check-circle-fill"></i>
                      </button>
                      <button id="ignore-btn" onclick="handleNotification(${notification.id}, false)"
                        style="flex: 1; padding: 15px; background-color: #f44336; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                        <i class="bi bi-x-circle-fill"></i>
                      </button>
                    </p>
                  </div>
                </div><br>
        `;
        
    }
});