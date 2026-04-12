// State tracking variables
let currentTimeframe = "Last 10 Min";

// Apply colors from CSS Variables so they update with themes dynamically
function getCSSVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }

// Theme Logic
function setTheme(mode) {
    const root = document.documentElement;
    if(mode === 'default') {
        root.style.setProperty('--color-primary', '#4ade80');
        root.style.setProperty('--color-secondary', '#3b82f6');
        root.style.setProperty('--color-tertiary', '#eab308');
        root.style.setProperty('--color-danger', '#ef4444');
    } else if (mode === 'red') {
        root.style.setProperty('--color-primary', '#ef4444');
        root.style.setProperty('--color-secondary', '#f97316');
        root.style.setProperty('--color-tertiary', '#f59e0b');
        root.style.setProperty('--color-danger', '#991b1b');
    } else if (mode === 'blue') {
        root.style.setProperty('--color-primary', '#3b82f6');
        root.style.setProperty('--color-secondary', '#6366f1');
        root.style.setProperty('--color-tertiary', '#EC4899');
        root.style.setProperty('--color-danger', '#eab308');
    }
    closeSettings();
    forceChartRedraw(); // Re-apply colors to existing charts
}

function getSharedLayout() {
    return {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#8b949e', family: 'Roboto' },
        margin: { t: 20, r: 20, l: 40, b: 20 },
        xaxis: { showgrid: true, gridcolor: '#30363d', zeroline: false },
        yaxis: { showgrid: true, gridcolor: '#30363d', zeroline: false },
        showlegend: true,
        legend: { orientation: "h", y: -0.2, x: 0.5, xanchor: 'center' }
    };
}

// Initialization of charts uses dummy data first
Plotly.newPlot('chart-sales', [], getSharedLayout(), {displayModeBar: false, responsive: true});
Plotly.newPlot('chart-health', [{ type: "indicator", mode: "gauge+number", value: 0 }], getSharedLayout(), {displayModeBar: false, responsive: true});
Plotly.newPlot('chart-inventory', [{ type: "indicator", mode: "gauge+number", value: 0 }], getSharedLayout(), {displayModeBar: false, responsive: true});
Plotly.newPlot('chart-polarity', [], getSharedLayout(), {displayModeBar: false, responsive: true});
Plotly.newPlot('chart-roas', [], getSharedLayout(), {displayModeBar: false, responsive: true});
Plotly.newPlot('chart-latency', [], getSharedLayout(), {displayModeBar: false, responsive: true});

// Fetch Data Loop
async function fetchState() {
    try {
        const res = await fetch(`/api/state?timeframe=${encodeURIComponent(currentTimeframe)}`);
        const d = await res.json();
        renderData(d);
    } catch(e) { console.error("Poll Error:", e); }
}

function renderData(d) {
    const layout = getSharedLayout();
    const c1 = getCSSVar('--color-primary');
    const c2 = getCSSVar('--color-secondary');
    const c3 = getCSSVar('--color-tertiary');
    const cRed = getCSSVar('--color-danger');

    // 1. Update Sales
    const salesTraces = [
        { x: d.sales_trend.x, y: d.sales_trend.hourly, name: 'Hourly Revenue ($)', marker: {color: c1} },
        { x: d.sales_trend.x, y: d.sales_trend.daily, name: 'Daily Revenue', marker: {color: c3} },
        { x: d.sales_trend.x, y: d.sales_trend.anomaly, name: 'Anomaly Detected', marker: {color: c2} }
    ];
    Plotly.react('chart-sales', salesTraces, { ...layout, margin: { t: 10, r: 10, l: 50, b: 40 }, yaxis: { tickprefix: '$', gridcolor: '#30363d'}});

    // 2 & 3. Update Gauges
    Plotly.react('chart-health', [{
        type: "indicator", mode: "gauge+number", value: d.health_score,
        number: { suffix: "%", font: { color: c1, size: 50 } },
        gauge: {
            axis: { range: [0, 100], visible: true, tickcolor: "#fff" },
            bar: { color: "transparent" }, bgcolor: "#1e2126", borderwidth: 0,
            steps: [ { range: [0, 100], color: c1 }, { range: [90, 100], color: cRed } ],
            threshold: { line: { color: "transparent", width: 4 }, thickness: 0.75, value: 0 }
        }
    }], { ...layout, margin: { t: 10, r: 30, l: 30, b: 10 } });

    Plotly.react('chart-inventory', [{
        type: "indicator", mode: "gauge+number", value: d.inventory_days,
        number: { suffix: " Days", font: { color: c3, size: 40 } },
        gauge: { axis: { range: [0, 30], visible: false }, bar: { color: c3 }, bgcolor: "#1e2126", borderwidth: 0, shape: "angular" }
    }], { ...layout, margin: { t: 10, r: 30, l: 30, b: 10 } });

    // 4. Update Sentiment Text
    document.getElementById('sentiment-text').innerText = d.sentiment_text;
    document.getElementById('sentiment-text').style.color = c1;
    document.getElementById('sentiment-score').innerText = `(${d.sentiment_score.toFixed(1)}/5)`;

    // 5. Polarity
    Plotly.react('chart-polarity', [{
        x: d.sentiment_polarity.x, y: d.sentiment_polarity.y, name: 'Sentiment Polarity (RAG)', marker: {color: c1}
    }], { ...layout, showlegend: true, margin: { t: 10, r: 10, l: 30, b: 40 }});

    // 6. ROAS
    Plotly.react('chart-roas', [
        { x: ['Facebook ROAS'], y: [d.roas_fb], type: 'bar', name: 'Facebook ROAS', marker: {color: c1} },
        { x: ['Google ROAS'], y: [d.roas_google], type: 'bar', name: 'Google ROAS', marker: {color: c2} }
    ], { ...layout, margin: { t: 10, r: 10, l: 40, b: 40 }});

    // 7. Latency
    Plotly.react('chart-latency', [
        { x: d.latency.nodes, y: d.latency.fetch, name: 'Data Fetch', type: 'bar', marker: {color: c1} },
        { x: d.latency.nodes, y: d.latency.reason, name: 'Reasoning', type: 'bar', marker: {color: c3} },
        { x: d.latency.nodes, y: d.latency.action, name: 'Action', type: 'bar', marker: {color: cRed} }
    ], { ...layout, barmode: 'stack', margin: { t: 10, r: 10, l: 30, b: 40 }});

    // 8. Logs
    document.getElementById('agent-logs').innerHTML = d.logs.map(log => `<div>${log}</div>`).join('');
}

function forceChartRedraw() { fetchState(); } // Next tick paints new colors

// --- UI Controls --- //
function downloadReport() {
    window.location.href = `/api/export_report?timeframe=${encodeURIComponent(currentTimeframe)}`;
}

function openSettings() { document.getElementById("settingsModal").style.display = "block"; }
function closeSettings() { document.getElementById("settingsModal").style.display = "none"; }

function selectTime(timeStr) {
    currentTimeframe = timeStr;
    document.getElementById('timeLabel').innerText = timeStr;
    // Trigger immediate fetch to show data scale jump
    fetchState();
}

// Window click close modal
window.onclick = function(event) {
    var modal = document.getElementById("settingsModal");
    if (event.target == modal) { modal.style.display = "none"; }
}

setInterval(fetchState, 1500);
fetchState();
