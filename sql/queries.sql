-- 1) Number of unique patients who received orthopedic rehabilitation.
SELECT COUNT(*) AS orthopedic_patients
FROM (
    SELECT DISTINCT patient_cf
    FROM prescriptions
    WHERE rehab_type = 'Orthopedic'
) AS unique_orthopedic_patients;

-- 2) Patient(s) linked to the highest prescription duration in terms of sessions.
SELECT p.first_name, p.last_name, p.patient_cf, pr.sessions
FROM patients p
JOIN prescriptions pr ON pr.patient_cf = p.patient_cf
WHERE pr.sessions = (
    SELECT MAX(sessions)
    FROM prescriptions
);

-- 3) Repeated prescriptions for each patient by rehabilitation type and anatomical area.
SELECT
    p.first_name,
    p.last_name,
    pr.patient_cf,
    pr.rehab_type,
    pr.anatomical_area,
    COUNT(*) AS repeated_prescriptions
FROM patients p
JOIN prescriptions pr ON pr.patient_cf = p.patient_cf
GROUP BY
    p.first_name,
    p.last_name,
    pr.patient_cf,
    pr.rehab_type,
    pr.anatomical_area
HAVING COUNT(*) > 1
ORDER BY p.last_name, p.first_name, pr.rehab_type, pr.anatomical_area;
