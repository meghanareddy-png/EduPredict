/**
 * EduPredict - Chart.js Data Visualizations
 * Palette:
 *   Primary Purple: #7C3AED
 *   Dark Purple:    #4C1D95
 *   Accent Purple:  #A78BFA
 *   Soft Purple:    rgba(124, 58, 237, 0.15)
 *   Success Green:  #16A34A
 *   Warning Orange: #F59E0B
 *   Danger Red:     #DC2626
 */

window.EduCharts = {
    // 1. Subject-Wise Performance Bar Chart
    renderSubjectBarChart: function (canvasId, subjects, scores) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: subjects,
                datasets: [{
                    label: 'Score Percentage (%)',
                    data: scores,
                    backgroundColor: 'rgba(124, 58, 237, 0.85)',
                    borderColor: '#7C3AED',
                    borderWidth: 1.5,
                    borderRadius: 8,
                    hoverBackgroundColor: '#6D28D9'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1E1B4B',
                        titleFont: { family: 'Plus Jakarta Sans', weight: 'bold' },
                        bodyFont: { family: 'Inter' },
                        padding: 10,
                        cornerRadius: 8
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: 'rgba(226, 232, 240, 0.6)' },
                        ticks: { font: { family: 'Inter' } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Inter', weight: '600' } }
                    }
                }
            }
        });
    },

    // 2. Monthly Attendance Line Chart
    renderAttendanceLineChart: function (canvasId, months, attendancePcts) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Attendance %',
                    data: attendancePcts,
                    borderColor: '#7C3AED',
                    backgroundColor: 'rgba(124, 58, 237, 0.12)',
                    fill: true,
                    tension: 0.35,
                    borderWidth: 2.5,
                    pointBackgroundColor: '#7C3AED',
                    pointBorderColor: '#FFFFFF',
                    pointBorderWidth: 2,
                    pointRadius: 5
                }, {
                    label: '75% Threshold',
                    data: Array(months.length).fill(75),
                    borderColor: '#DC2626',
                    borderWidth: 1.5,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top', labels: { font: { family: 'Inter', size: 11 } } },
                    tooltip: { backgroundColor: '#1E1B4B', cornerRadius: 8 }
                },
                scales: {
                    y: {
                        min: 40,
                        max: 100,
                        grid: { color: 'rgba(226, 232, 240, 0.6)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    },

    // 3. Assignment Completion Doughnut Chart
    renderAssignmentDoughnutChart: function (canvasId, completed, pending) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Pending'],
                datasets: [{
                    data: [completed, pending],
                    backgroundColor: ['#7C3AED', '#E2E8F0'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '72%',
                plugins: {
                    legend: { position: 'bottom', labels: { font: { family: 'Inter', weight: '600' } } }
                }
            }
        });
    },

    // 4. Class Performance Distribution (Faculty Dashboard)
    renderClassPerformanceChart: function (canvasId, names, internalMarks, predictedMarks) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: names,
                datasets: [
                    {
                        label: 'Current Internal Marks (%)',
                        data: internalMarks,
                        backgroundColor: 'rgba(167, 139, 250, 0.7)',
                        borderRadius: 6
                    },
                    {
                        label: 'Predicted Final Score (%)',
                        data: predictedMarks,
                        backgroundColor: '#7C3AED',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top', labels: { font: { family: 'Inter', weight: '600' } } },
                    tooltip: { backgroundColor: '#1E1B4B', cornerRadius: 8 }
                },
                scales: {
                    y: { beginAtZero: true, max: 100 }
                }
            }
        });
    }
};
