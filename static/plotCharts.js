import {plotCandlestickChart,plotHeatMap,plotTimeSeriesChat,plotRadarChart,plotDonutChart} from '../static/charts.js'



const donut_layout = {
    margin: {
        r: 10,
        t: 50,
        b: 10,
        l: 10
      },
      title: 'Share holding res',
      height:300,
      width:300

}
const donutChartData= [{
    values: [16, 15, 12, 6, 5, 4, 42],    //Sum up to 100
    labels: ['US', 'China', 'European Union', 'Russian Federation', 'Brazil', 'India', 'Rest of World' ]
}]

plotDonutChart('pie_chart',  donutChartData,'Donut chart' , donut_layout)

const radar_data = [
    {
    r: [39, 28, 18, 20, 28, 39],
    theta: ['A','B','C', 'D', 'E', 'A'],
    }
];
const radar_layout = {
    height: 400,
    showlegend:true,
    legend: {
        x:3,
        y:2,
        orientation:"h"
    }
}

plotRadarChart("comparison_radar",radar_data,radar_layout)