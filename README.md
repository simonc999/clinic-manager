# RehabTrack Clinic Manager

RehabTrack Clinic Manager is a command-line Python application for managing patients, rehabilitation prescriptions, and treatment assignments in a rehabilitation clinic.

The project uses SQLite as the database engine and provides separate workflows for physiatrists and physiotherapists through employee-code based access.

## Features

- employee login with role detection based on the employee code
- physiatrist workflow for:
  - viewing personal patient lists
  - checking a patient's full prescription history
  - creating new prescriptions
  - renewing existing prescriptions already signed by the logged-in physiatrist
- physiotherapist workflow for:
  - viewing assigned patients
  - checking a patient's full prescription history
  - updating treatment tracking dates for assigned prescriptions
- normalized SQLite schema with reference tables for rehabilitation types and anatomical areas
- sample dataset with patients, physiatrists, physiotherapists, prescriptions, and treatments
- ready-to-use SQL queries for reporting and analysis

## Project Structure

```text
rehabtrack-clinic-manager/
├── app.py
├── clinic/
│   ├── __init__.py
│   ├── cli.py
│   ├── database.py
│   ├── services.py
│   └── validators.py
├── data/
│   └── .gitkeep
├── sql/
│   ├── queries.sql
│   ├── schema.sql
│   └── seed.sql
├── .gitignore
└── README.md
```

## Database Model

The application is organized around the following entities:

- **Patients**: personal and demographic information for clinic patients
- **Physiatrists**: medical specialists who sign rehabilitation prescriptions
- **Physiotherapists**: professionals who deliver the treatment plan
- **Prescriptions**: rehabilitation prescriptions linked to patients, rehabilitation types, and anatomical areas
- **Treatments**: the many-to-many relationship between prescriptions and physiotherapists, including assigned sessions and treatment dates
- **Rehabilitation Types**: standardized rehabilitation categories
- **Anatomical Areas**: standardized body areas involved in treatment

Employee codes are role-based:

- codes starting with `A` identify physiatrists
- codes starting with `B` identify physiotherapists

## How to Run

1. Make sure Python 3.10 or newer is installed.
2. Open the project folder in your terminal.
3. Start the application:

```bash
python app.py
```

The SQLite database is created automatically the first time the application runs.

To rebuild the database from scratch using the SQL scripts:

```bash
python app.py --reset-db
```

## Sample Login Codes

You can use the seeded employee codes below to test the application:

### Physiatrists

- `A1001`
- `A1002`
- `A1003`

### Physiotherapists

- `B2001`
- `B2002`
- `B2003`

## Example Workflows

### Physiatrist

- view all patients linked to prescriptions signed by the logged-in physiatrist
- open the full history of a patient by entering the patient tax code
- renew one of the physiatrist's existing prescriptions with a new date and session count
- create a brand-new prescription by choosing the rehabilitation type, anatomical area, patient, and number of sessions

### Physiotherapist

- view all patients connected to the physiotherapist's assigned treatments
- inspect the prescription history of any patient already stored in the database
- update the start and end dates of a treatment only when the prescription is assigned to the logged-in physiotherapist

## SQL Reports Included

The `sql/queries.sql` file contains example reports for:

- counting unique patients who received orthopedic rehabilitation
- finding the patient linked to the highest number of prescribed sessions
- identifying repeated prescriptions grouped by patient, rehabilitation type, and anatomical area

## Technologies

- Python 3
- SQLite 3
- Standard Library only
