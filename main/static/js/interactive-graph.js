document.addEventListener('DOMContentLoaded', () => {
    window.createGraph = createGraph;
    window.updateGraph = updateGraph;
    window.isAfter6AM = isAfter6AM;
    function createGraph() {
        let data = [{
            x: [],
            y: [],
            type: 'scatter',
        }];

        let layout = {
            title: 'Violations Graph',
            xaxis: {
                title: 'Time',
                // range: ['06:00', '23:59'],
                // type: 'date', 
                // tickformat: '%H:%M',
                // tickmode: 'linear',
                // tick0: '06:00',
                // dtick: 'M05'
            },
            yaxis: {
                title: 'Count'
            }
        };

        Plotly.newPlot('graph', data, layout);

        fetch(`${window.location.origin}/detector/api/dashboard/all/obj/`)
            .then(res => res.json())
            .then(data => {
                let counter = 1;
                data.violation_objects.reverse();
                console.log(data.violation_objects[0].date)
                data.violation_objects.forEach(element => {
                    if (element.state == 'confirmed' && isAfter6AM(element.date)) {
                        updateGraph(counter++, element.date.slice(11,19))
                    }
                });
            })

        // Sat May 24 2025 06:00:00 GMT+0200 (Central European Summer Time)

    }

    function isAfter6AM(date) {
        const inputDate = new Date(date.replace(' ', 'T'));
        const now = new Date();
        const today6AM = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 6, 0, 0, 0)
        return inputDate > today6AM;
    }

    function updateGraph(dateData, countData) {
        Plotly.extendTraces('graph', {
            x: [[countData]],
            y: [[dateData]]
        }, [0], 90);
    }

});