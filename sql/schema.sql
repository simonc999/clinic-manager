PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS rehabilitation_types;
DROP TABLE IF EXISTS anatomical_areas;
DROP TABLE IF EXISTS physiotherapists;
DROP TABLE IF EXISTS physiatrists;
DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    patient_cf TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    sex TEXT NOT NULL CHECK (sex IN ('M', 'F', 'X')),
    birth_date TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE physiatrists (
    employee_code TEXT PRIMARY KEY CHECK (employee_code LIKE 'A%'),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE physiotherapists (
    employee_code TEXT PRIMARY KEY CHECK (employee_code LIKE 'B%'),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE rehabilitation_types (
    rehab_type_name TEXT PRIMARY KEY
);

CREATE TABLE anatomical_areas (
    area_name TEXT PRIMARY KEY
);

CREATE TABLE prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescription_date TEXT NOT NULL,
    sessions INTEGER NOT NULL CHECK (sessions > 0),
    physiatrist_code TEXT NOT NULL,
    patient_cf TEXT NOT NULL,
    rehab_type TEXT NOT NULL,
    anatomical_area TEXT NOT NULL,
    renewed_from_prescription_id INTEGER,
    FOREIGN KEY (physiatrist_code) REFERENCES physiatrists(employee_code) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (patient_cf) REFERENCES patients(patient_cf) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (rehab_type) REFERENCES rehabilitation_types(rehab_type_name) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (anatomical_area) REFERENCES anatomical_areas(area_name) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (renewed_from_prescription_id) REFERENCES prescriptions(prescription_id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE treatments (
    prescription_id INTEGER NOT NULL,
    physiotherapist_code TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    assigned_sessions INTEGER NOT NULL CHECK (assigned_sessions > 0),
    PRIMARY KEY (prescription_id, physiotherapist_code),
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (physiotherapist_code) REFERENCES physiotherapists(employee_code) ON UPDATE CASCADE ON DELETE RESTRICT
);
