INSERT INTO rehabilitation_types (rehab_type_name) VALUES
('Orthopedic'),
('Neurological - acute post-stroke'),
('Neurological - medium-term post-stroke'),
('Neurological - long-term post-stroke'),
('Respiratory');

INSERT INTO anatomical_areas (area_name) VALUES
('Upper limbs'),
('Lower limbs'),
('Right side'),
('Left side'),
('Right upper limb'),
('Left upper limb'),
('Right lower limb'),
('Left lower limb'),
('Lumbar spine'),
('Cervical spine');

INSERT INTO patients (patient_cf, first_name, last_name, sex, birth_date, address) VALUES
('FRRMRA85A41F205Z', 'Marta', 'Ferri', 'F', '1985-01-01', '12 Via delle Azalee, 20121 Milan'),
('BLLLCU90C10H501K', 'Luca', 'Bellini', 'M', '1990-03-10', '8 Via dei Tigli, 00184 Rome'),
('RVAGLI78M52D612T', 'Giulia', 'Riva', 'F', '1978-08-12', '21 Piazza Verdi, 40121 Bologna'),
('VNTRND67R18F839P', 'Andrea', 'Venturi', 'M', '1967-10-18', '5 Corso Libertà, 50123 Florence'),
('MRNLNE92T44L219B', 'Elena', 'Marino', 'F', '1992-12-04', '16 Via Manzoni, 80121 Naples'),
('GRCTMS74P05G273N', 'Tommaso', 'Greco', 'M', '1974-09-05', '3 Via Garibaldi, 16121 Genoa');

INSERT INTO physiatrists (employee_code, first_name, last_name, phone, email) VALUES
('A1001', 'Sofia', 'Leone', '+39-320-555-0101', 'sofia.leone@rehabtrackclinic.com'),
('A1002', 'Riccardo', 'Morelli', '+39-320-555-0102', 'riccardo.morelli@rehabtrackclinic.com'),
('A1003', 'Valentina', 'Costa', '+39-320-555-0103', 'valentina.costa@rehabtrackclinic.com');

INSERT INTO physiotherapists (employee_code, first_name, last_name, phone, email) VALUES
('B2001', 'Davide', 'Serra', '+39-320-555-0201', 'davide.serra@rehabtrackclinic.com'),
('B2002', 'Chiara', 'Landi', '+39-320-555-0202', 'chiara.landi@rehabtrackclinic.com'),
('B2003', 'Nicolò', 'Biagi', '+39-320-555-0203', 'nicolo.biagi@rehabtrackclinic.com');

INSERT INTO prescriptions (prescription_id, prescription_date, sessions, physiatrist_code, patient_cf, rehab_type, anatomical_area, renewed_from_prescription_id) VALUES
(1, '2025-01-15', 12, 'A1001', 'FRRMRA85A41F205Z', 'Orthopedic', 'Right lower limb', NULL),
(2, '2025-02-03', 20, 'A1002', 'BLLLCU90C10H501K', 'Neurological - acute post-stroke', 'Left side', NULL),
(3, '2025-02-17', 10, 'A1003', 'RVAGLI78M52D612T', 'Respiratory', 'Cervical spine', NULL),
(4, '2025-03-02', 15, 'A1001', 'VNTRND67R18F839P', 'Orthopedic', 'Lumbar spine', NULL),
(5, '2025-03-10', 18, 'A1002', 'MRNLNE92T44L219B', 'Neurological - medium-term post-stroke', 'Right side', NULL),
(6, '2025-03-22', 14, 'A1003', 'GRCTMS74P05G273N', 'Orthopedic', 'Left upper limb', NULL),
(7, '2025-04-08', 8, 'A1001', 'FRRMRA85A41F205Z', 'Orthopedic', 'Right lower limb', 1),
(8, '2025-04-19', 16, 'A1002', 'BLLLCU90C10H501K', 'Neurological - medium-term post-stroke', 'Left side', 2),
(9, '2025-05-04', 12, 'A1003', 'RVAGLI78M52D612T', 'Respiratory', 'Upper limbs', NULL),
(10, '2025-05-12', 10, 'A1001', 'VNTRND67R18F839P', 'Orthopedic', 'Lumbar spine', 4),
(11, '2025-05-27', 12, 'A1002', 'MRNLNE92T44L219B', 'Neurological - long-term post-stroke', 'Right side', 5),
(12, '2025-06-03', 9, 'A1003', 'GRCTMS74P05G273N', 'Orthopedic', 'Left upper limb', 6),
(13, '2025-06-20', 6, 'A1001', 'FRRMRA85A41F205Z', 'Orthopedic', 'Right lower limb', 7),
(14, '2025-07-01', 14, 'A1002', 'BLLLCU90C10H501K', 'Neurological - long-term post-stroke', 'Left side', 8),
(15, '2025-07-16', 11, 'A1003', 'RVAGLI78M52D612T', 'Respiratory', 'Cervical spine', 3),
(16, '2025-08-05', 13, 'A1001', 'VNTRND67R18F839P', 'Orthopedic', 'Lumbar spine', 10),
(17, '2025-08-18', 10, 'A1002', 'MRNLNE92T44L219B', 'Neurological - long-term post-stroke', 'Right side', 11),
(18, '2025-09-01', 12, 'A1003', 'GRCTMS74P05G273N', 'Orthopedic', 'Left upper limb', 12);

INSERT INTO treatments (prescription_id, physiotherapist_code, start_date, end_date, assigned_sessions) VALUES
(1, 'B2001', '2025-01-20', '2025-02-18', 12),
(2, 'B2002', '2025-02-06', '2025-03-20', 12),
(2, 'B2003', '2025-02-06', '2025-03-20', 8),
(4, 'B2001', '2025-03-05', '2025-04-09', 15),
(5, 'B2002', '2025-03-14', '2025-04-25', 10),
(5, 'B2003', '2025-03-14', '2025-04-25', 8),
(7, 'B2001', '2025-04-10', '2025-05-02', 8),
(8, 'B2002', '2025-04-22', '2025-05-30', 10),
(8, 'B2003', '2025-04-22', '2025-05-30', 6),
(10, 'B2001', NULL, NULL, 10),
(11, 'B2002', NULL, NULL, 12),
(12, 'B2003', NULL, NULL, 9),
(13, 'B2001', NULL, NULL, 6),
(14, 'B2002', NULL, NULL, 9),
(14, 'B2003', NULL, NULL, 5),
(16, 'B2001', NULL, NULL, 13),
(17, 'B2002', NULL, NULL, 10),
(18, 'B2003', NULL, NULL, 12);
