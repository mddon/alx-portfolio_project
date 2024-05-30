MIMZ ACADEMY STUDENT MANAGEMENT SYSTEM

Welcome to the Mimz Academy Student Management System, a comprehensive web application designed to streamline student registration, admission, and record management. This README provides an overview of the project, setup instructions, and details on its usage and features.

TABLE OF CONTENT
1.  Project Overview
2.  Features
3.  Technologies Used
4.  Setup Instructions
5.  Usage
6.  Areas of improvement
7.  Contributors
8.  Author
9.  Contact


PROJECT OVERVIEW
The Mimz Academy Student Management System is a web application designed to streamline the process of managing student admissions, registrations, and records. The system provides an efficient and user-friendly interface for school administrators to handle student data, improving overall administrative operations.

FEATURES
1.  User Authentication: Secure login system for administrators.
2.  Student Registration: Allows administrators to add new students.
3.  Admission Management: Facilitates the admission process for prospective students.
4.  Student Record Management: Enables viewing, adding, updating, and deleting student details.
5.  Responsive Design: Accessible on various devices.

TECHNOLOGIES USED
1.  Backend: Flask (Python)
2.  Database: SQLite
3.  Frontend: HTML, CSS, JavaScript


SETUP INSTRUCTIONS
To set up the Mimz Academy Student Management System locally, follow these steps:

1.  Clone the Repository
    git clone https://github.com/yourusername/mimz-academy.git
    cd mimz-academy

2.  Create a Virtual Environment
    python3 -m venv venv
    source venv/bin/activate

3.  Install Dependencies
    pip install -r requirements.txt

4.  Set Up the Database
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    Run the Application
    flask run

5.  Access the Application
    Open your web browser and navigate to http://127.0.0.1:5000/.

USAGE:
User Authentication:
    1.  Login: Access the login page at /login, enter your credentials, and log in.
    2.  Logout: Log out by navigating to /logout.

Student Management:
    1.  View Students: Access the list of students at /students.
    2.  Add Student: Use the form at /student-manager to add a new student.
    3.  Update Student: Send a PUT request to /students/<registration_number> with the updated data.
    4.  Delete Student: Send a DELETE request to /students/<registration_number> to remove a student.

Admission Management:
    1.  View Prospective Students: Access the admission page at /admission to see prospective students who have signed up.
    2   API Endpoints:
        * GET /students: Retrieve a list of all students.
        * POST /students: Add a new student.
        * PUT /students/<registration_number>: Update a student's details.
        * DELETE /students/<registration_number>: Delete a student.

AREAS FROM IMPROVEMENT:
1.  Frontend design
2.  Admission Status on the admission db
3.  Customized login for individual data base administrator
4.  More sophisticated frameworks for both the frontend and backend
5.  Admitted students to automatically be added into the student management database

CONTRIBUTIONS:
Contributions are welcome! Please follow these steps:
    1.  Fork the repository.
    2.  Create a new branch (git checkout -b feature/YourFeature).
    3.  Commit your changes (git commit -m 'Add some feature').
    4.  Push to the branch (git push origin feature/YourFeature).
    5.  Open a pull request.

AUTHOR:
    [Miracle Obinna Okafor] <miracle.okafor14@gmail.com>

CONTACT:
    For questions or inquiries, please contact Me.