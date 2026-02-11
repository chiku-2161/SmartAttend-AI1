function goFaculty() {
    window.location.href = "faculty.html";
}

function goStudent() {
    window.location.href = "student.html";
}

function logout() {
    window.location.href = "index.html";
}

function searchStudent(value) {
    let filter = value.toUpperCase();
    let table = document.getElementById("attendanceTable");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            let txtValue = td.textContent || td.innerText;
            tr[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none";
        }
    }
}

const ctx = document.getElementById('attendanceChart');

if (ctx) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Rahul', 'Aman', 'Priya'],
            datasets: [{
                label: 'Attendance %',
                data: [85, 75, 95],
                backgroundColor: [
                    '#6366F1',
                    '#22D3EE',
                    '#10B981'
                ],
                borderRadius: 8
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: { color: "#F1F5F9" }
                }
            },
            scales: {
                x: {
                    ticks: { color: "#F1F5F9" }
                },
                y: {
                    ticks: { color: "#F1F5F9" }
                }
            }
        }
    });
}
function updateData() {
    const semester = document.getElementById("semesterSelect").value;
    const subject = document.getElementById("subjectSelect").value;

    const tableBody = document.querySelector("#attendanceTable tbody");

    if (semester === "sem3" && subject === "dsa") {
        tableBody.innerHTML = `
        <tr>
            <td>Rahul</td>
            <td>23CSE001</td>
            <td>34</td>
            <td>40</td>
            <td><div class="progress-bar"><div class="progress" style="width:85%;">85%</div></div></td>
        </tr>
        <tr>
            <td>Aman</td>
            <td>23CSE002</td>
            <td>30</td>
            <td>40</td>
            <td><div class="progress-bar"><div class="progress" style="width:75%;">75%</div></div></td>
        </tr>
        `;
    }

    if (semester === "sem5" && subject === "dbms") {
        tableBody.innerHTML = `
        <tr>
            <td>Sneha</td>
            <td>22CSE011</td>
            <td>36</td>
            <td>40</td>
            <td><div class="progress-bar"><div class="progress" style="width:90%;">90%</div></div></td>
        </tr>
        <tr>
            <td>Karan</td>
            <td>22CSE012</td>
            <td>28</td>
            <td>40</td>
            <td><div class="progress-bar"><div class="progress" style="width:70%;">70%</div></div></td>
        </tr>
        `;
    }
}
// Faculty login - backend ready
const facultyForm = document.getElementById("facultyLoginForm");
if(facultyForm) {
    facultyForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("facultyEmail").value;
        const password = document.getElementById("facultyPassword").value;
        const error = document.getElementById("loginError");

        error.textContent = "Loading...";

        try {
            // Replace this URL with your backend API endpoint
            const response = await fetch("https://your-backend.com/api/faculty-login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if(data.success) {
                // Save faculty info for dashboard use
                sessionStorage.setItem("facultyData", JSON.stringify(data.faculty));
                window.location.href = "faculty.html";
            } else {
                error.textContent = data.message || "Invalid credentials";
            }

        } catch(err) {
            error.textContent = "Server error. Try again later.";
            console.error(err);
        }
    });
}

