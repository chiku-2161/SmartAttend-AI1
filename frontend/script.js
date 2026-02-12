let sessionId = null;

// ---------------- NAVIGATION ----------------

function goFaculty() {
    window.location.href = "faculty.html";
}

function goStudent() {
    window.location.href = "student.html";
}

function logout() {
    window.location.href = "index.html";
}

// ---------------- FACULTY ----------------

async function startClass() {
    setStatus("Starting class...", true);

    try {
        const response = await fetch("http://127.0.0.1:5000/teacher/start-class", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                teacher_id: 1,
                assignment_id: 1
            })
        });

        const data = await response.json();
        sessionId = data.session_id;

        setStatus("Class Started. Session ID: " + sessionId);
        enableEndButton();
    } catch (err) {
        setStatus("Error starting class.");
    }
}

function markAttendance() {
    if (!sessionId) {
        alert("Start class first!");
        return;
    }

    alert("Run camera_client.py and enter session ID: " + sessionId);
}

async function endClass() {
    if (!sessionId) {
        alert("Start class first!");
        return;
    }

    const intervals = prompt("Enter total intervals:");

    if (!intervals) return;

    setStatus("Ending class...", true);

    try {
        await fetch("http://127.0.0.1:5000/session/end", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: sessionId,
                total_intervals: parseInt(intervals)
            })
        });

        setStatus("Class Ended Successfully.");
        loadAttendance();
    } catch {
        setStatus("Error ending class.");
    }
}

async function loadAttendance() {
    const res = await fetch(
        `http://127.0.0.1:5000/debug/attendance/${sessionId}`
    );

    const data = await res.json();

    let table = `
        <h3>Attendance Results</h3>
        <table>
            <tr>
                <th>Student ID</th>
                <th>Status</th>
            </tr>
    `;

    data.forEach(row => {
        table += `
            <tr>
                <td>${row[0]}</td>
                <td>${row[1]}</td>
            </tr>
        `;
    });

    table += `</table>`;

    document.getElementById("result").innerHTML = table;
}

function setStatus(message, loading = false) {
    document.getElementById("result").innerHTML =
        loading ? `<div class="loader"></div><p>${message}</p>` :
                  `<p>${message}</p>`;
}

function enableEndButton() {
    const btn = document.getElementById("endBtn");
    if (btn) btn.disabled = false;
}

// ---------------- STUDENT ----------------

async function checkAttendance() {
    const studentId = document.getElementById("studentId").value;

    if (!studentId) return;

    document.getElementById("studentResult").innerHTML =
        `<div class="loader"></div><p>Loading...</p>`;

    const response = await fetch(
        `http://127.0.0.1:5000/analytics/student/${studentId}`
    );

    const data = await response.json();

    document.getElementById("studentResult").innerHTML =
        `
        <h3>Analytics</h3>
        <p><b>Attendance:</b> ${data.data.attendance_percentage}%</p>
        <p><b>Risk Level:</b> ${data.data.risk_level}</p>
        <p><b>Forecast (Next 5):</b> ${data.data.forecast_next_5_classes}%</p>
        `;
}
