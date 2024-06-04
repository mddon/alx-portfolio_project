function displayError(message) {
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = message;
    setTimeout(() => errorMessage.textContent = "", 5000);
}

function fetchStudents() {
    fetch('/students')
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch students');
        }
        return response.json();
    })
    .then(data => {
        const studentList = data.students;
        const tableBody = document.getElementById("studentList");
        tableBody.innerHTML = "";
        studentList.forEach(student => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${student.registration_number}</td>
                <td>${student.name}</td>
                <td>${student.department}</td>
                <td>${student.age}</td>
                <td>
                    <button onclick="editStudent(${student.registration_number})">Edit</button>
                    <button onclick="confirmDeleteStudent(${student.registration_number})">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => displayError(`Error: ${error.message}`));
}

function addStudent() {
    var name = document.getElementById("name").value;
    var department = document.getElementById("department").value;
    var age = document.getElementById("age").value;

    fetch('/students', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name, department: department, age: age })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add student');
        }
        document.getElementById("name").value = "";
        document.getElementById("department").value = "";
        document.getElementById("age").value = "";
        fetchStudents();
    })
    .catch(error => displayError(`Error: ${error.message}`));
}

function confirmDeleteStudent(regNo) {
    if (confirm('Are you sure you want to delete this student?')) {
        deleteStudent(regNo);
    }
}

function deleteStudent(regNo) {
    fetch(`/students/${regNo}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete student');
        }
        fetchStudents();
    })
    .catch(error => displayError(`Error: ${error.message}`));
}

function editStudent(regNo) {
    var newName = prompt("Enter the new name:");
    if (newName === null) return;

    var newDepartment = prompt("Enter the new department:");
    if (newDepartment === null) return;

    var newAge = prompt("Enter the new age:");
    if (newAge === null) return;

    fetch(`/students/${regNo}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newName, department: newDepartment, age: newAge })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update student');
        }
        fetchStudents();
    })
    .catch(error => displayError(`Error: ${error.message}`));
}

fetchStudents();

function toggleMenu() {
    var navLinks = document.getElementById("navLinks");
    var menuIcon = document.querySelector(".menu-icon");
    if (navLinks.style.display === "block") {
        navLinks.style.display = "none";
        menuIcon.classList.remove("active");
    } else {
        navLinks.style.display = "block";
        menuIcon.classList.add("active");
    }
}