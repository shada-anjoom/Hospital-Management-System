-- Drop existing tables if needed (for reset)
DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS Doctors;

-- Create Doctors table
CREATE TABLE Doctors (
    DoctorID SERIAL PRIMARY KEY,
    Name TEXT NOT NULL,
    Specialization TEXT
);

-- Create Patients table
CREATE TABLE Patients (
    PatientID SERIAL PRIMARY KEY,
    Name TEXT NOT NULL,
    DOB DATE,
    Phone TEXT UNIQUE
);

-- Create Appointments table
CREATE TABLE Appointments (
    AppointmentID SERIAL PRIMARY KEY,
    PatientID INTEGER NOT NULL REFERENCES Patients(PatientID) ON DELETE CASCADE,
    DoctorID INTEGER NOT NULL REFERENCES Doctors(DoctorID) ON DELETE CASCADE,
    AppointmentDate DATE NOT NULL,
    Status TEXT DEFAULT 'Scheduled' CHECK (Status IN ('Scheduled', 'Completed', 'Cancelled'))
);

-- Optional: Insert sample data

-- Insert Doctors
INSERT INTO Doctors (Name, Specialization) VALUES
('Dr. Alice Smith', 'Cardiology'),
('Dr. Bob Johnson', 'Neurology');

-- Insert Patients
INSERT INTO Patients (Name, DOB, Phone) VALUES
('John Doe', '1990-05-15', '1234567890'),
('Jane Roe', '1985-09-22', '0987654321');

-- Insert Appointments
INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, Status) VALUES
(1, 1, '2025-10-20', 'Scheduled'),
(2, 2, '2025-10-21', 'Scheduled');
