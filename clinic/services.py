from __future__ import annotations

import sqlite3
from typing import Iterable

from clinic.database import get_connection


class ServiceError(Exception):
    """Raised when a business rule is violated."""


def employee_exists(employee_code: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT employee_code FROM physiatrists WHERE employee_code = ?
            UNION
            SELECT employee_code FROM physiotherapists WHERE employee_code = ?
            """,
            (employee_code, employee_code),
        ).fetchone()
    return row is not None


def get_role(employee_code: str) -> str:
    if employee_code.startswith("A"):
        return "physiatrist"
    if employee_code.startswith("B"):
        return "physiotherapist"
    raise ServiceError("Unknown employee code format.")


def patient_exists(patient_cf: str) -> bool:
    with get_connection() as conn:
        row = conn.execute("SELECT 1 FROM patients WHERE patient_cf = ?", (patient_cf,)).fetchone()
    return row is not None


def get_patient(patient_cf: str) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT patient_cf, first_name, last_name, sex, birth_date, address
            FROM patients
            WHERE patient_cf = ?
            """,
            (patient_cf,),
        ).fetchone()


def list_physiatrist_patients(employee_code: str) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT DISTINCT p.first_name, p.last_name, p.patient_cf, p.birth_date, p.sex
            FROM patients p
            JOIN prescriptions pr ON pr.patient_cf = p.patient_cf
            WHERE pr.physiatrist_code = ?
            ORDER BY p.last_name, p.first_name
            """,
            (employee_code,),
        ).fetchall()


def list_physiotherapist_patients(employee_code: str) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT DISTINCT p.first_name, p.last_name, p.patient_cf, p.birth_date, p.sex
            FROM patients p
            JOIN prescriptions pr ON pr.patient_cf = p.patient_cf
            JOIN treatments t ON t.prescription_id = pr.prescription_id
            WHERE t.physiotherapist_code = ?
            ORDER BY p.last_name, p.first_name
            """,
            (employee_code,),
        ).fetchall()


def get_patient_prescription_history(patient_cf: str) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT
                pr.prescription_id,
                pr.prescription_date,
                pr.rehab_type,
                pr.anatomical_area,
                pr.sessions,
                pr.physiatrist_code,
                pr.renewed_from_prescription_id
            FROM prescriptions pr
            WHERE pr.patient_cf = ?
            ORDER BY pr.prescription_date DESC, pr.prescription_id DESC
            """,
            (patient_cf,),
        ).fetchall()


def get_rehab_types() -> list[str]:
    with get_connection() as conn:
        rows = conn.execute("SELECT rehab_type_name FROM rehabilitation_types ORDER BY rehab_type_name").fetchall()
    return [row[0] for row in rows]


def get_anatomical_areas() -> list[str]:
    with get_connection() as conn:
        rows = conn.execute("SELECT area_name FROM anatomical_areas ORDER BY area_name").fetchall()
    return [row[0] for row in rows]


def _ensure_value_in_catalog(value: str, catalog: Iterable[str], label: str) -> None:
    if value not in catalog:
        allowed = ", ".join(catalog)
        raise ServiceError(f"Invalid {label}. Allowed values: {allowed}")


def create_prescription(
    patient_cf: str,
    prescription_date: str,
    rehab_type: str,
    anatomical_area: str,
    sessions: int,
    physiatrist_code: str,
) -> int:
    if not patient_exists(patient_cf):
        raise ServiceError("The patient code was not found.")

    rehab_types = get_rehab_types()
    anatomical_areas = get_anatomical_areas()
    _ensure_value_in_catalog(rehab_type, rehab_types, "rehabilitation type")
    _ensure_value_in_catalog(anatomical_area, anatomical_areas, "anatomical area")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO prescriptions (
                prescription_date,
                sessions,
                physiatrist_code,
                patient_cf,
                rehab_type,
                anatomical_area,
                renewed_from_prescription_id
            ) VALUES (?, ?, ?, ?, ?, ?, NULL)
            """,
            (
                prescription_date,
                sessions,
                physiatrist_code,
                patient_cf,
                rehab_type,
                anatomical_area,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def renew_prescription(
    original_prescription_id: int,
    new_prescription_date: str,
    sessions: int,
    physiatrist_code: str,
) -> int:
    with get_connection() as conn:
        original = conn.execute(
            """
            SELECT prescription_id, rehab_type, anatomical_area, patient_cf, physiatrist_code
            FROM prescriptions
            WHERE prescription_id = ?
            """,
            (original_prescription_id,),
        ).fetchone()

        if original is None:
            raise ServiceError("Prescription not found.")

        if original["physiatrist_code"] != physiatrist_code:
            raise ServiceError("You can only renew prescriptions signed by you.")

        cursor = conn.execute(
            """
            INSERT INTO prescriptions (
                prescription_date,
                sessions,
                physiatrist_code,
                patient_cf,
                rehab_type,
                anatomical_area,
                renewed_from_prescription_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_prescription_date,
                sessions,
                physiatrist_code,
                original["patient_cf"],
                original["rehab_type"],
                original["anatomical_area"],
                original["prescription_id"],
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def update_treatment_dates(
    prescription_id: int,
    physiotherapist_code: str,
    start_date: str,
    end_date: str,
) -> None:
    with get_connection() as conn:
        assigned_treatment = conn.execute(
            """
            SELECT prescription_id, physiotherapist_code
            FROM treatments
            WHERE prescription_id = ? AND physiotherapist_code = ?
            """,
            (prescription_id, physiotherapist_code),
        ).fetchone()

        if assigned_treatment is None:
            raise ServiceError("This prescription is not assigned to you.")

        conn.execute(
            """
            UPDATE treatments
            SET start_date = ?, end_date = ?
            WHERE prescription_id = ? AND physiotherapist_code = ?
            """,
            (start_date, end_date, prescription_id, physiotherapist_code),
        )
        conn.commit()
