document.addEventListener('DOMContentLoaded', function() {
    // Sample data for demonstration
    const data = {
        dates: ['2024-06-01', '2024-06-02', '2024-06-03', '2024-06-04', '2024-06-05'],
        open: [100, 110, 105, 115, 112],
        high: [120, 125, 118, 130, 118],
        low: [95, 105, 100, 110, 105],
        close: [115, 120, 112, 125, 110]
    };

    // Plot candlestick chart
    plotCandlestickChart(data);
});

function plotCandlestickChart(data) {
    var trace = {
        x: data.dates,
        close: data.close,
        decreasing: {line: {color: 'red'}},
        high: data.high,
        increasing: {line: {color: 'green'}},
        low: data.low,
        open: data.open,
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y'
    };

    var layout = {
        dragmode: 'zoom',
        margin: {
            r: 10,
            t: 25,
            b: 40,
            l: 60
        },
        showlegend: false,
        xaxis: {
            autorange: true,
            title: 'Date',
        },
        yaxis: {
            autorange: true,
            title: 'Price',
            type: 'linear'
        }
    };

    var config = {responsive: true};

    Plotly.newPlot('candlestick-chart', [trace], layout, config);

    // Display cursor position on hover
    var cursorInfo = document.getElementById('cursor-position');
    var candlestickChart = document.getElementById('candlestick-chart');

    candlestickChart.on('plotly_hover', function(data) {
        var point = data.points[0];
        if (point) {
            var xVal = point.x;
            var yVal = point.y;

            cursorInfo.textContent = `X: ${xVal}, Y: ${yVal}`;
        }
    });
}
