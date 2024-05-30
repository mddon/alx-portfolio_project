from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a random secret key for production

# Dummy data for demonstration purposes
users = {
    'admin': generate_password_hash('password123')
}

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('students.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS students (
                        reg_no INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        department TEXT NOT NULL,
                        age INTEGER NOT NULL)''')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_students_reg_no ON students (reg_no)')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_connection2():
    conn2 = None
    try:
        conn2 = sqlite3.connect('prospective_students.db')
        conn2.execute('''CREATE TABLE IF NOT EXISTS prospective_students (
                        id INTEGER PRIMARY KEY,
                        surname TEXT NOT NULL,
                        other_names TEXT NOT NULL,
                        email TEXT NOT NULL,
                        academic TEXT NOT NULL,
                        date_of_birth INTEGER NOT NULL,
                        guardian_name TEXT NOT NULL,
                        guardian_phone TEXT NOT NULL)''')
        conn2.execute('CREATE INDEX IF NOT EXISTS idx_prospective_students_id ON prospective_students (id)')
    except sqlite3.Error as e:
        print(e)
    return conn2

def get_db(db_name):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_hash = users.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session['username'] = username
            return redirect(url_for('student_manager'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/student-manager')
def student_manager():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('student-manager.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        surname = request.form['surname']
        other_names = request.form['other_names']
        email = request.form['email']
        academic_level = request.form['academic_level']
        date_of_birth = request.form['date_of_birth']
        guardian_name = request.form['guardian_name']
        guardian_phone = request.form['guardian_phone']
        
        conn2 = create_connection2()
        if conn2 is None:
            abort(500, description="Database connection error")
        
        cursor2 = conn2.cursor()
        cursor2.execute('INSERT INTO prospective_students (surname, other_names, email, academic, date_of_birth, guardian_name, guardian_phone) VALUES (?, ?, ?, ?, ?, ?, ?)', (surname, other_names, email, academic_level, date_of_birth, guardian_name, guardian_phone))
        conn2.commit()
        conn2.close()
        
        return redirect(url_for('signup_success'))
    return render_template('signup.html')

@app.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if 'username' not in session:
        abort(401)
    
    conn = create_connection()
    if conn is None:
        abort(500, description="Database connection error")
    
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        rows = cursor.fetchall()
        students = [{'registration_number': row[0], 'name': row[1], 'department': row[2], 'age': row[3]} for row in rows]
        conn.close()
        return jsonify({'students': students})
    
    elif request.method == 'POST':
        data = request.json
        if not data or not all(k in data for k in ('name', 'department', 'age')):
            abort(400, description="Missing student data.")
        
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, department, age) VALUES (?, ?, ?)', (data['name'], data['department'], data['age']))
        conn.commit()
        new_student_id = cursor.lastrowid
        conn.close()
        
        student = {'registration_number': new_student_id, 'name': data['name'], 'department': data['department'], 'age': data['age']}
        return jsonify(student), 201

@app.route('/students/<int:registration_number>', methods=['DELETE'])
def delete_student(registration_number):
    if 'username' not in session:
        abort(401)
    
    conn = create_connection()
    if conn is None:
        abort(500, description="Database connection error")
    
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE reg_no = ?', (registration_number,))
    conn.commit()
    conn.close()
    
    return '', 204

@app.route('/students/<int:registration_number>', methods=['PUT'])
def update_student(registration_number):
    if 'username' not in session:
        abort(401)
    
    data = request.json
    name = data.get('name')
    department = data.get('department')
    age = data.get('age')
    
    if name and department and age:
        conn = create_connection()
        if conn is None:
            abort(500, description="Database connection error")
        
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET name = ?, department = ?, age = ? WHERE reg_no = ?', 
                       (name, department, age, registration_number))
        conn.commit()
        conn.close()
        return '', 204
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/admission')
def admission():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn2 = get_db('prospective_students.db')
    cursor = conn2.cursor()
    cursor.execute('SELECT * FROM prospective_students')
    rows = cursor.fetchall()
    prospective_students = [{'id': row[0], 'surname': row[1], 'other_names': row[2], 'email': row[3], 'academic': row[4], 'date_of_birth': row[5], 'guardian_name': row[6], 'guardian_phone': row[7]} for row in rows]
    
    return render_template('admission.html', prospective_students=prospective_students)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
