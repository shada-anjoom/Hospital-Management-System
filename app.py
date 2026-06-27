from flask import Flask, render_template, request, redirect
import psycopg2

# Flask app setup
app = Flask(__name__)


# Function to connect to the database
def get_connection():
    return psycopg2.connect(
        dbname='hospital_db',
        user='postgres',
        password='shada',
        host='localhost',
        port=5432
    )

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Add patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        phone = request.form['phone']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Patients (Name, DOB, Phone) VALUES (%s, %s, %s)", (name, dob, phone))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_patient.html')

# Add doctor
@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Doctors (Name, Specialization) VALUES (%s, %s)", (name, specialization))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_doctor.html')

# Book appointment
@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT PatientID, Name FROM Patients")
    patients = cur.fetchall()
    cur.execute("SELECT DoctorID, Name FROM Doctors")
    doctors = cur.fetchall()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        cur.execute("INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate) VALUES (%s, %s, %s)",
                    (patient_id, doctor_id, date))
        conn.commit()
        conn.close()
        return redirect('/')
    conn.close()
    return render_template('book_appointment.html', patients=patients, doctors=doctors)

# View all appointments
@app.route('/view_appointments')
def view_appointments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT A.AppointmentID, P.Name, D.Name, A.AppointmentDate, A.Status
        FROM Appointments A
        JOIN Patients P ON A.PatientID = P.PatientID
        JOIN Doctors D ON A.DoctorID = D.DoctorID
        ORDER BY A.AppointmentDate
    """)
    appointments = cur.fetchall()
    conn.close()
    return render_template('view_appointments.html', appointments=appointments)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
