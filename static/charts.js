const plotCandlestickChart = function(id_, data, layout_= {}) {
  /*Data format has to be object as below !important*****
  {
    dates: ['2024-06-01', '2024-06-02', '2024-06-03', '2024-06-04', '2024-06-05'],
    open: [100, 110, 105, 115, 112],
    high: [120, 125, 118, 130, 118],
    low: [95, 105, 100, 110, 105],
    close: [115, 120, 112, 125, 110]
  }
  */

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

  Object.assign(layout, layout_);

  Plotly.newPlot(id_, [trace], layout, config);

}
 
//Radar chart
const plotRadarChart = function(id_, data_, layout_ = {}, name_= "radar", line = true){
  /*
  [
    {
    r: [39, 28, 8, 7, 28, 39],
    theta: ['A','B','C', 'D', 'E', 'A'],
    }
  ]
  name_ = ['group a', 'group b']
  */

  for(let i = 0; i< data_.length; i++){
    data_[i].type = 'scatterpolar'
    data_[i].fill = 'toself'
    data_[i].name = name_[i]
    if(line === true){
      data_[i].line = {shape:'spline'}
    }
  }

  const layout = {
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 50]
      }
    },
    showlegend: false,
    paper_bgcolor: 'transparent',
    margin: {l:20, r:20, t:40, b:20}
  }
  Object.assign(layout, layout_);
  const config = {
    displaylogo:false,
    displayModeBar: false
  }

  Plotly.newPlot(id_, data_, layout, config);
}

//Donut chart
const plotDonutChart = function(id_, data_, name_,  layout_ = {}){
  /*REQUIRED DATA FORMAT...
  [{
    values: [16, 15, 12, 6, 5, 4, 42],    //Sum up to 100
    labels: ['US', 'China', 'European Union', 'Russian Federation', 'Brazil', 'India', 'Rest of World' ]
  }]
  */
  try {
    for(let i=0; i<data_.length; i++){
      data_[i].type = 'pie'
      data_[i].hole = 0.4
      data_[i].hoverinfo = 'label+percent'
      data_[i].name = name_
      data_[i].domain = {column:0}
      data_[i].marker = {
        colors: ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
      };
    }
  
    var layout = {
      title: 'Set title in layout',
      paper_bgcolor: 'transparent',
      margin: {
        r: 20,
        t: 40,
        b: 20,
        l: 100
      },
      height: 400,
      width: 600,
      showlegend: false,
      grid: {rows: 1, columns: 1}
    };
  
    Object.assign(layout, layout_);

    const config = {
      displaylogo: false,
      displayModeBar: false
    }
    
    Plotly.newPlot(id_, data_, layout, config)

  } catch (error) {
    console.log(error)
  }

}

const plotTimeSeriesChat = function(id_, data_, layout_ = {}){
  /* DATA FORMAT
  [
    {
      x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
      y: [1, 3, 6],
    },
    {
      x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
      y: [3, 2, 4],
    }
  ]*/
  for(let i=0; i<data_.length; i++){
    data_[i].type = 'scatter'
  };

  const layout = {
    margin: {l:20, r:20, t:30, b:20},
  };

  Object.assign(layout, layout_);

  Plotly.newPlot(id_, data_, layout);
}

const plotHeatMap = function (id_, data_, layout_ = {}){
  /*
  Required Data format
  [{
    z: [[1, 4, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
    x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    y: ['Morning', 'Afternoon', 'Evening'],

  }]
   */
  //Data can be array also
  for(let i=0; i<data_.length; i++){
    data_[i].type ='heatmap'
    data_[i].colorscale = 'Viridis'
    data_[i].hoverongaps = false
  }

  const layout = {
    margin: {l:20, r:20, t:30, b:20},
    paper_bgcolor:'transparent'
  };

  Object.assign(layout, layout_);
  
  const config = {
    displaylogo: false
  }

  Plotly.newPlot(id_, data_, layout,config);

}



export {
  plotHeatMap,
  plotTimeSeriesChat,
  plotDonutChart,
  plotRadarChart,
  plotCandlestickChart
}