/**
 * EduPredict - Dashboard Interactivity & Future Score Simulator
 */

document.addEventListener("DOMContentLoaded", function () {
    // 1. Future Score Simulator Slider Logic
    const sliderInt = document.getElementById("sim-slider-internal");
    const sliderAtt = document.getElementById("sim-slider-attendance");
    const sliderAsg = document.getElementById("sim-slider-assignment");
    const sliderPrac = document.getElementById("sim-slider-practical");
    const sliderHrs = document.getElementById("sim-slider-hours");

    const labelInt = document.getElementById("val-internal");
    const labelAtt = document.getElementById("val-attendance");
    const labelAsg = document.getElementById("val-assignment");
    const labelPrac = document.getElementById("val-practical");
    const labelHrs = document.getElementById("val-hours");

    const simScoreEl = document.getElementById("sim-result-score");
    const simDeltaEl = document.getElementById("sim-result-delta");
    const simCategoryEl = document.getElementById("sim-result-category");
    const simRiskEl = document.getElementById("sim-result-risk");

    function runSimulation() {
        if (!sliderInt || !sliderAtt || !sliderAsg || !sliderPrac || !sliderHrs) return;

        const internalVal = parseFloat(sliderInt.value);
        const attVal = parseFloat(sliderAtt.value);
        const asgVal = parseFloat(sliderAsg.value);
        const pracVal = parseFloat(sliderPrac.value);
        const hrsVal = parseFloat(sliderHrs.value);

        // Update labels
        if (labelInt) labelInt.innerText = internalVal + "%";
        if (labelAtt) labelAtt.innerText = attVal + "%";
        if (labelAsg) labelAsg.innerText = asgVal + "%";
        if (labelPrac) labelPrac.innerText = pracVal + "%";
        if (labelHrs) labelHrs.innerText = hrsVal + " hrs";

        // Call backend simulation API
        fetch("/student/simulate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                internal_marks: internalVal,
                attendance: attVal,
                assignment_pct: asgVal,
                practical_marks: pracVal,
                study_hours: hrsVal
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const hypo = data.hypothetical;
                const score = hypo.predicted_percentage;
                const delta = data.score_difference;

                if (simScoreEl) simScoreEl.innerText = score.toFixed(1) + "%";
                if (simCategoryEl) simCategoryEl.innerText = hypo.performance_category;
                if (simRiskEl) {
                    simRiskEl.innerText = hypo.risk_level + " Risk";
                    simRiskEl.className = "status-badge status-" + hypo.risk_level.toLowerCase();
                }

                if (simDeltaEl) {
                    if (delta > 0) {
                        simDeltaEl.innerText = "▲ +" + delta.toFixed(1) + "% vs Current";
                        simDeltaEl.className = "score-delta-badge delta-positive";
                    } else if (delta < 0) {
                        simDeltaEl.innerText = "▼ " + delta.toFixed(1) + "% vs Current";
                        simDeltaEl.className = "score-delta-badge delta-negative";
                    } else {
                        simDeltaEl.innerText = "— No Change";
                        simDeltaEl.className = "score-delta-badge delta-neutral";
                    }
                }
            }
        })
        .catch(err => {
            console.error("Simulation error:", err);
        });
    }

    if (sliderInt) sliderInt.addEventListener("input", runSimulation);
    if (sliderAtt) sliderAtt.addEventListener("input", runSimulation);
    if (sliderAsg) sliderAsg.addEventListener("input", runSimulation);
    if (sliderPrac) sliderPrac.addEventListener("input", runSimulation);
    if (sliderHrs) sliderHrs.addEventListener("input", runSimulation);

    // Initial simulation call on page load
    if (sliderInt) runSimulation();

    // 2. Table Client-side Search Filter (Faculty & Admin)
    const tableSearchInput = document.getElementById("table-search-input");
    if (tableSearchInput) {
        tableSearchInput.addEventListener("input", function () {
            const query = this.value.toLowerCase().trim();
            const rows = document.querySelectorAll(".searchable-table tbody tr");
            rows.forEach(function (row) {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(query) ? "" : "none";
            });
        });
    }
});
