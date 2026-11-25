
import "../css/style.css";

import {
    createPlotlyChart,
    createEChartsChart,
    resizePlotlyChart
} from "./charts.js";

console.log("CIA Chart Generation started");

let echartsInstance = null;

// Initialize dashboard charts
function initializeDashboard() {
    try {
        createPlotlyChart();
        echartsInstance = createEChartsChart();

        console.log("Both charts initialized successfully");
    } catch (error) {
        console.error("Dashboard initialization error:", error);
    }
}

// Wait until HTML is ready
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeDashboard);
} else {
    initializeDashboard();
}

// Resize charts when the browser window changes
window.addEventListener("resize", () => {
    resizePlotlyChart();

    if (echartsInstance) {
        echartsInstance.resize();
    }
});
