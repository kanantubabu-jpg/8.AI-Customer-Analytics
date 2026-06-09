/**
 * Single-chart renderer for advanced analytics modules
 */
(function () {
    const meta = document.getElementById('chartMeta');
    if (!meta) return;

    const apiUrl = meta.dataset.api;
    const chartType = meta.dataset.type;
    const isLive = meta.dataset.live === 'true';
    const canvas = document.getElementById('analyticsChart');
    let chartInstance = null;

    const colors = {
        primary: '#3498db', success: '#2ecc71', danger: '#e74c3c',
        warning: '#f39c12', info: '#1abc9c', purple: '#9b59b6', secondary: '#95a5a6',
    };
    const palette = [colors.primary, colors.success, colors.warning, colors.danger, colors.info, colors.purple];

    function buildConfig(type, data) {
        const base = { responsive: true, plugins: { legend: { display: true } } };

        switch (type) {
            case 'bar':
                return {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{ label: 'Value', data: data.values, backgroundColor: colors.primary }],
                    },
                    options: { ...base, scales: { y: { ticks: { callback: v => v.toLocaleString() } } } },
                };

            case 'horizontal_bar':
                return {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{ label: 'Target Score', data: data.values, backgroundColor: colors.success }],
                    },
                    options: { ...base, indexAxis: 'y' },
                };

            case 'line':
                if (data.actual) {
                    return {
                        type: 'line',
                        data: {
                            labels: data.labels,
                            datasets: [
                                { label: 'Actual ROI %', data: data.actual, borderColor: colors.primary, tension: 0.3 },
                                { label: 'Predicted ROI %', data: data.predicted, borderColor: colors.warning, tension: 0.3 },
                            ],
                        },
                        options: base,
                    };
                }
                return {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Live Sales', data: data.values,
                            borderColor: colors.danger, backgroundColor: 'rgba(231,76,60,0.1)', fill: true, tension: 0.3,
                        }],
                    },
                    options: base,
                };

            case 'grouped_bar':
                return {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [
                            { label: 'Sent', data: data.sent, backgroundColor: colors.secondary },
                            { label: 'Opens', data: data.opens, backgroundColor: colors.primary },
                            { label: 'Clicks', data: data.clicks, backgroundColor: colors.info },
                            { label: 'Conversions', data: data.conversions, backgroundColor: colors.success },
                        ],
                    },
                    options: base,
                };

            case 'stacked_bar':
                return {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [
                            { label: 'Purchase Frequency', data: data.frequency, backgroundColor: colors.primary },
                            { label: 'Avg Spending', data: data.spending, backgroundColor: colors.success },
                            { label: 'Review Sentiment', data: data.sentiment, backgroundColor: colors.warning },
                        ],
                    },
                    options: { ...base, scales: { x: { stacked: true }, y: { stacked: true, max: 100 } } },
                };

            case 'doughnut':
                return {
                    type: 'doughnut',
                    data: {
                        labels: data.labels,
                        datasets: [{ data: data.values, backgroundColor: [colors.success, colors.warning, colors.danger] }],
                    },
                    options: { ...base, plugins: { legend: { position: 'bottom' } } },
                };

            case 'funnel_bar':
                return {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Customers', data: data.values,
                            backgroundColor: [colors.primary, colors.info, colors.warning, colors.success],
                        }],
                    },
                    options: base,
                };

            case 'multi_line':
                return {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [
                            { label: 'Collaborative Filtering', data: data.cf, borderColor: colors.primary, tension: 0.3 },
                            { label: 'Content-Based', data: data.content, borderColor: colors.success, tension: 0.3 },
                            { label: 'Hybrid', data: data.hybrid, borderColor: colors.danger, tension: 0.3 },
                        ],
                    },
                    options: base,
                };

            default:
                return {
                    type: 'bar',
                    data: {
                        labels: data.labels || [],
                        datasets: [{
                            label: 'Recommendation Score',
                            data: data.scores || data.values || [],
                            backgroundColor: palette,
                        }],
                    },
                    options: base,
                };
        }
    }

    function loadChart() {
        fetch(apiUrl)
            .then(r => r.json())
            .then(data => {
                const config = buildConfig(chartType, data);
                if (chartInstance) {
                    chartInstance.destroy();
                }
                chartInstance = new Chart(canvas, config);
            })
            .catch(err => console.error('Chart load error:', err));
    }

    loadChart();
    if (isLive) {
        setInterval(loadChart, 10000);
    }
})();
