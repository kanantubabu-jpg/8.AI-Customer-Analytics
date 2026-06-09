/**
 * Dashboard Chart.js visualizations — all analytics graphs
 */
document.addEventListener('DOMContentLoaded', function () {
    const chartColors = {
        primary: '#3498db',
        success: '#2ecc71',
        danger: '#e74c3c',
        warning: '#f39c12',
        info: '#1abc9c',
        purple: '#9b59b6',
        secondary: '#95a5a6',
    };

    const palette = [
        chartColors.primary,
        chartColors.success,
        chartColors.warning,
        chartColors.danger,
        chartColors.info,
        chartColors.purple,
    ];

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: { legend: { display: true } },
    };

    function formatYAxis() {
        return {
            ticks: { callback: (v) => v.toLocaleString() },
        };
    }

    function showEmptyChart(canvasId, message) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        ctx.font = '14px Segoe UI';
        ctx.fillStyle = '#95a5a6';
        ctx.textAlign = 'center';
        ctx.fillText(message, canvas.width / 2 || 150, canvas.height / 2 || 75);
    }

    // 1. Sales Trend Line Chart
    fetch('/api/chart/sales-trend')
        .then(res => res.json())
        .then(data => {
            if (!data.labels || !data.labels.length) {
                showEmptyChart('salesTrendChart', 'No sales data available');
                return;
            }
            new Chart(document.getElementById('salesTrendChart'), {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Revenue',
                        data: data.data,
                        borderColor: chartColors.primary,
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                    }],
                },
                options: {
                    ...defaultOptions,
                    scales: { y: formatYAxis() },
                },
            });
        })
        .catch(err => console.error('Sales trend chart error:', err));

    // 2. Customer Segmentation Pie Chart
    fetch('/api/chart/segmentation')
        .then(res => res.json())
        .then(data => {
            if (!data.labels || !data.labels.length) {
                showEmptyChart('segmentationChart', 'No segmentation data');
                return;
            }
            new Chart(document.getElementById('segmentationChart'), {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.values,
                        backgroundColor: palette.slice(0, data.labels.length),
                    }],
                },
                options: {
                    ...defaultOptions,
                    plugins: { legend: { position: 'bottom' } },
                },
            });
        })
        .catch(err => console.error('Segmentation chart error:', err));

    // 3. Revenue Forecast Bar Chart
    fetch('/api/chart/forecast')
        .then(res => res.json())
        .then(data => {
            if (!data.historical_labels || !data.historical_labels.length) {
                showEmptyChart('forecastChart', 'No forecast data available');
                return;
            }
            const histLen = data.historical_labels.length;
            const allLabels = [...data.historical_labels, ...data.forecast_labels];
            const histData = [...data.historical_revenue, ...Array(data.forecast_labels.length).fill(null)];
            const forecastData = [...Array(histLen).fill(null), ...data.forecast_revenue];

            new Chart(document.getElementById('forecastChart'), {
                type: 'bar',
                data: {
                    labels: allLabels,
                    datasets: [
                        {
                            label: 'Historical Revenue',
                            data: histData,
                            backgroundColor: chartColors.primary,
                        },
                        {
                            label: 'Forecast Revenue',
                            data: forecastData,
                            backgroundColor: chartColors.warning,
                        },
                    ],
                },
                options: {
                    ...defaultOptions,
                    scales: { y: formatYAxis() },
                },
            });
        })
        .catch(err => console.error('Forecast chart error:', err));

    // 4. Churn Analysis Doughnut Chart
    fetch('/api/chart/churn')
        .then(res => res.json())
        .then(data => {
            if (!data.values || data.values.every(v => v === 0)) {
                showEmptyChart('churnChart', 'No customer data');
                return;
            }
            new Chart(document.getElementById('churnChart'), {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.values,
                        backgroundColor: [chartColors.success, chartColors.danger],
                    }],
                },
                options: {
                    ...defaultOptions,
                    plugins: { legend: { position: 'bottom' } },
                },
            });
        })
        .catch(err => console.error('Churn chart error:', err));

    // 5. Sentiment Distribution Pie Chart
    fetch('/api/chart/sentiment')
        .then(res => res.json())
        .then(data => {
            if (!data.values || data.values.every(v => v === 0)) {
                showEmptyChart('sentimentChart', 'No review data');
                return;
            }
            new Chart(document.getElementById('sentimentChart'), {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.values,
                        backgroundColor: [chartColors.success, chartColors.danger, chartColors.secondary],
                    }],
                },
                options: {
                    ...defaultOptions,
                    plugins: { legend: { position: 'bottom' } },
                },
            });
        })
        .catch(err => console.error('Sentiment chart error:', err));

    // 6. Sales by Category Bar Chart
    fetch('/api/chart/sales-category')
        .then(res => res.json())
        .then(data => {
            if (!data.labels || !data.labels.length) {
                showEmptyChart('categoryChart', 'No category data');
                return;
            }
            new Chart(document.getElementById('categoryChart'), {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Revenue',
                        data: data.values,
                        backgroundColor: palette.slice(0, data.labels.length),
                    }],
                },
                options: {
                    ...defaultOptions,
                    scales: { y: formatYAxis() },
                    plugins: { legend: { display: false } },
                },
            });
        })
        .catch(err => console.error('Category chart error:', err));

    // 7. Recent Predictions Line Chart
    fetch('/api/chart/predictions')
        .then(res => res.json())
        .then(data => {
            if (!data.labels || !data.labels.length) {
                showEmptyChart('predictionsChart', 'Run predictions to see this chart');
                return;
            }
            new Chart(document.getElementById('predictionsChart'), {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Purchase Probability (%)',
                            data: data.purchase,
                            borderColor: chartColors.success,
                            backgroundColor: 'rgba(46, 204, 113, 0.1)',
                            fill: false,
                            tension: 0.3,
                        },
                        {
                            label: 'Churn Risk (%)',
                            data: data.churn,
                            borderColor: chartColors.danger,
                            backgroundColor: 'rgba(231, 76, 60, 0.1)',
                            fill: false,
                            tension: 0.3,
                        },
                    ],
                },
                options: {
                    ...defaultOptions,
                    scales: {
                        y: {
                            min: 0,
                            max: 100,
                            ticks: { callback: (v) => v + '%' },
                        },
                    },
                },
            });
        })
        .catch(err => console.error('Predictions chart error:', err));
});
