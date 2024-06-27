


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


data2 = [
    {
    type: 'scatterpolar',
    r: [39, 28, 8, 7, 28, 39],
    theta: ['A','B','C', 'D', 'E', 'A'],
    fill: 'toself',
    name: 'Group A',
    line: {shape:'spline'}
    },
    {
    type: 'scatterpolar',
    r: [1.5, 10, 39, 31, 15, 1.5],
    theta: ['A','B','C', 'D', 'E', 'A'],
    fill: 'toself',
    name: 'Group B',
    line: {shape:'spline'}
    }
  ]
  
  layout = {
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 50]
      }
    },
    showlegend: false,
    paper_bgcolor: 'transparent',
    margin: {l:20, r:20, t:30, b:20}
  }
  Plotly.newPlot("radial-chart", data2, layout)
  




//Timeseries plot
var data = [
    {
      x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
      y: [1, 3, 6],
      type: 'scatter'
    }
  ];
  layout = {
    margin: {
      r: 10,
      t: 25,
      b: 40,
      l: 60
  },
  }
  
  Plotly.newPlot('radar-comparison', data, layout);


  //Donut chart
  var data = [{
    values: [16, 15, 12, 6, 5, 4, 42],
    labels: ['US', 'China', 'European Union', 'Russian Federation', 'Brazil', 'India', 'Rest of World' ],
    domain: {column: 0},
    name: 'GHG Emissions',
    hoverinfo: 'label+percent+name',
    hole: .4,
    type: 'pie'
  }];
  
  var layout = {
    title: 'Indian Market Participants',
    paper_bgcolor: 'transparent',
    margin: {
      r: 20,
      t: 40,
      b: 20,
      l: 100
    },
    annotations: [
      {
        font: {
          size: 15
        },
        showarrow: false,
        text: 'INDIA',
        x: 0.19,
        y: 0.5
      }    
    ],
    height: 400,
    width: 600,
    showlegend: false,
    grid: {rows: 1, columns: 2}
  };
  
  Plotly.newPlot('donut_chart', data, layout);
  




//Timeseries for market share
var data = [
  {
    x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
    y: [1, 3, 6],
    type: 'scatter'
  },
  {
    x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
    y: [3, 2, 4],
    type: 'scatter'
  }
];

layout = {
  margin: {
    r: 10,
    t: 25,
    b: 40,
    l: 60
},
}

Plotly.newPlot('market_share_timeline', data, layout);