from __future__ import annotations

import argparse

from clinic.database import initialize_database
from clinic.services import (
    ServiceError,
    create_prescription,
    employee_exists,
    get_anatomical_areas,
    get_patient,
    get_patient_prescription_history,
    get_rehab_types,
    get_role,
    list_physiatrist_patients,
    list_physiotherapist_patients,
    renew_prescription,
    update_treatment_dates,
)
from clinic.validators import require_positive_integer, require_valid_date


def _print_patient_rows(rows: list) -> None:
    if not rows:
        print("No patients found for this employee.")
        return

    print("\nPatients")
    print("-" * 90)
    for index, row in enumerate(rows, start=1):
        print(
            f"{index}. {row['first_name']} {row['last_name']} | "
            f"CF: {row['patient_cf']} | Birth date: {row['birth_date']} | Sex: {row['sex']}"
        )
    print()


def _show_patient_history() -> None:
    patient_cf = input("Enter the patient's tax code: ").strip().upper()
    patient = get_patient(patient_cf)

    if patient is None:
        print("Patient not found.\n")
        return

    history = get_patient_prescription_history(patient_cf)
    print(f"\nPrescription history for {patient['first_name']} {patient['last_name']} ({patient['patient_cf']})")
    print("-" * 110)

    if not history:
        print("No prescriptions found.\n")
        return

    for row in history:
        renewed_info = (
            f" | Renewed from: {row['renewed_from_prescription_id']}"
            if row['renewed_from_prescription_id']
            else ""
        )
        print(
            f"ID: {row['prescription_id']} | Date: {row['prescription_date']} | "
            f"Type: {row['rehab_type']} | Area: {row['anatomical_area']} | "
            f"Sessions: {row['sessions']} | Physiatrist: {row['physiatrist_code']}{renewed_info}"
        )
    print()


def _create_or_renew_prescription(employee_code: str) -> None:
    print("\n1. Renew an existing prescription")
    print("2. Create a new prescription")
    choice = input("Select an option: ").strip()

    try:
        if choice == "1":
            prescription_id = require_positive_integer("Enter the prescription ID to renew: ")
            new_date = require_valid_date("Enter the new prescription date (YYYY-MM-DD): ")
            sessions = require_positive_integer("Enter the number of sessions: ")
            new_id = renew_prescription(prescription_id, new_date, sessions, employee_code)
            print(f"Prescription renewed successfully. New prescription ID: {new_id}\n")
            return

        if choice == "2":
            patient_cf = input("Enter the patient's tax code: ").strip().upper()
            prescription_date = require_valid_date("Enter the prescription date (YYYY-MM-DD): ")
            print(f"Available rehabilitation types: {', '.join(get_rehab_types())}")
            rehab_type = input("Enter the rehabilitation type exactly as listed: ").strip()
            print(f"Available anatomical areas: {', '.join(get_anatomical_areas())}")
            anatomical_area = input("Enter the anatomical area exactly as listed: ").strip()
            sessions = require_positive_integer("Enter the number of sessions: ")
            new_id = create_prescription(
                patient_cf,
                prescription_date,
                rehab_type,
                anatomical_area,
                sessions,
                employee_code,
            )
            print(f"Prescription created successfully. New prescription ID: {new_id}\n")
            return

        print("Operation cancelled.\n")
    except ServiceError as error:
        print(f"{error}\n")


def _update_treatment_tracking(employee_code: str) -> None:
    try:
        prescription_id = require_positive_integer("Enter the assigned prescription ID: ")
        start_date = require_valid_date("Enter the treatment start date (YYYY-MM-DD): ")
        end_date = require_valid_date("Enter the treatment end date (YYYY-MM-DD): ")
        update_treatment_dates(prescription_id, employee_code, start_date, end_date)
        print("Treatment tracking updated successfully.\n")
    except ServiceError as error:
        print(f"{error}\n")


def _physiatrist_menu(employee_code: str) -> None:
    while True:
        print("1. View my patients")
        print("2. View a patient's prescription history")
        print("3. Create or renew a prescription")
        print("4. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            _print_patient_rows(list_physiatrist_patients(employee_code))
        elif choice == "2":
            _show_patient_history()
        elif choice == "3":
            _create_or_renew_prescription(employee_code)
        elif choice == "4":
            print("Goodbye.")
            return
        else:
            print("Invalid option.\n")


def _physiotherapist_menu(employee_code: str) -> None:
    while True:
        print("1. View my patients")
        print("2. View a patient's prescription history")
        print("3. Update treatment tracking")
        print("4. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            _print_patient_rows(list_physiotherapist_patients(employee_code))
        elif choice == "2":
            _show_patient_history()
        elif choice == "3":
            _update_treatment_tracking(employee_code)
        elif choice == "4":
            print("Goodbye.")
            return
        else:
            print("Invalid option.\n")


def run() -> None:
    parser = argparse.ArgumentParser(description="RehabTrack clinic management CLI")
    parser.add_argument(
        "--reset-db",
        action="store_true",
        help="Rebuild the SQLite database from the SQL scripts before starting the app.",
    )
    args = parser.parse_args()

    initialize_database(reset=args.reset_db)

    employee_code = input("Enter your employee code: ").strip().upper()
    if not employee_exists(employee_code):
        print("Invalid employee code.")
        return

    role = get_role(employee_code)
    print(f"Authenticated as {role.replace('_', ' ')} {employee_code}.\n")

    if role == "physiatrist":
        _physiatrist_menu(employee_code)
    else:
        _physiotherapist_menu(employee_code)
