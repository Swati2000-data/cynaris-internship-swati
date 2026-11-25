import Plotly from "plotly.js-dist-min";
import * as echarts from "echarts";

// ----------------------------------
// PLOTLY BAR CHART
// ----------------------------------

export function createPlotlyChart() {

    const chartElement = document.getElementById("plotlyChart");

    if (!chartElement) {
        console.error("Plotly chart container not found");
        return;
    }

    const months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June"
    ];

    const sales = [
        25000,
        32000,
        28000,
        45000,
        39000,
        56000
    ];

    const data = [{
        x: months,
        y: sales,
        type: "bar",
        name: "Monthly Sales",

        marker: {
            color: "#818cf8"
        },

        hovertemplate:
            "%{x}<br>Sales: ₹%{y:,}<extra></extra>"
    }];

    const layout = {
        title: {
            text: "Monthly Sales Performance"
        },

        autosize: true,

        paper_bgcolor: "#151f32",
        plot_bgcolor: "#151f32",

        font: {
            color: "#ffffff"
        },

        xaxis: {
            title: "Month",
            gridcolor: "#293449"
        },

        yaxis: {
            title: "Sales (₹)",
            gridcolor: "#293449"
        },

        margin: {
            t: 55,
            r: 20,
            b: 60,
            l: 65
        }
    };

    Plotly.newPlot(
        chartElement,
        data,
        layout,
        {
            responsive: true,
            displayModeBar: true
        }
    ).catch(error => {
        console.error("Plotly error:", error);
    });
}


// ----------------------------------
// ECHARTS PIE CHART
// ----------------------------------

export function createEChartsChart() {

    const chartElement = document.getElementById("echartsChart");

    if (!chartElement) {
        console.error("ECharts container not found");
        return;
    }

    const chart = echarts.init(chartElement);

    const options = {

        backgroundColor: "transparent",

        tooltip: {
            trigger: "item",
            formatter: "{b}: ₹{c} ({d}%)"
        },

        legend: {
            bottom: "2%",
            textStyle: {
                color: "#ffffff"
            }
        },

        series: [{
            name: "Product Sales",
            type: "pie",

            radius: ["40%", "70%"],
            center: ["50%", "45%"],

            avoidLabelOverlap: true,

            itemStyle: {
                borderRadius: 8,
                borderColor: "#151f32",
                borderWidth: 3
            },

            label: {
                color: "#ffffff",
                formatter: "{b}\n{d}%"
            },

            data: [
                {
                    value: 45000,
                    name: "Electronics"
                },
                {
                    value: 32000,
                    name: "Clothing"
                },
                {
                    value: 25000,
                    name: "Furniture"
                },
                {
                    value: 18000,
                    name: "Accessories"
                }
            ]
        }]
    };

    chart.setOption(options);

    return chart;
}

// Resize Plotly chart when the browser window changes
export function resizePlotlyChart() {
    const element = document.getElementById("plotlyChart");

    if (element) {
        Plotly.Plots.resize(element);
    }
}