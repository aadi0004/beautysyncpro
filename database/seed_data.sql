USE beautysyncpro;

-- Clear existing appointments to avoid conflicts
DELETE FROM appointment;

-- Re-insert users, salons, and services (unchanged)
INSERT INTO user (username, password_hash, email, is_admin) VALUES
('alice', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'alice@example.com', FALSE),
('bob', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'bob@example.com', FALSE),
('charlie', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'charlie@example.com', FALSE),
('diana', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'diana@example.com', FALSE),
('eve', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'eve@example.com', FALSE),
('frank', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'frank@example.com', FALSE),
('grace', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'grace@example.com', FALSE),
('henry', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'henry@example.com', FALSE),
('isabel', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'isabel@example.com', FALSE),
('admin', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'admin@example.com', TRUE);

INSERT INTO salon (name, address) VALUES
('Glow Haven Spa', '123 Main St, Mumbai'),
('Radiance Salon', '456 Oak Ave, Delhi'),
('Bliss Beauty Lounge', '789 Pine Rd, Bangalore'),
('Serene Spa', '101 Maple Dr, Chennai'),
('Elegance Salon', '202 Cedar Ln, Hyderabad'),
('Tranquil Touch', '303 Birch St, Pune'),
('Luxe Beauty Studio', '404 Elm Ave, Kolkata'),
('Harmony Spa', '505 Willow Rd, Ahmedabad'),
('Chic Salon', '606 Ash Dr, Jaipur'),
('Vogue Wellness', '707 Spruce Ln, Surat');

INSERT INTO service (name, duration, salon_id) VALUES
('Facial', 60, 1),
('Haircut', 45, 1),
('Manicure', 30, 2),
('Pedicure', 40, 2),
('Massage', 90, 3),
('Hair Coloring', 120, 4),
('Waxing', 30, 5),
('Eyebrow Threading', 15, 6),
('Makeup', 60, 7),
('Nail Art', 45, 8);

-- Insert appointments (spread across May 20-22, 2025)
INSERT INTO appointment (user_id, salon_id, service_id, start_time, status) VALUES
(1, 1, 1, '2025-05-20 19:00:00', 'confirmed'),  -- Alice books Facial at Glow Haven Spa (today, after 06:36 PM)
(2, 1, 2, '2025-05-20 19:30:00', 'pending'),  -- Bob books Haircut at Glow Haven Spa (today)
(3, 2, 3, '2025-05-21 09:00:00', 'confirmed'),  -- Charlie books Manicure at Radiance Salon
(4, 2, 4, '2025-05-21 10:00:00', 'pending'),  -- Diana books Pedicure at Radiance Salon
(5, 3, 5, '2025-05-21 11:00:00', 'confirmed'),  -- Eve books Massage at Bliss Beauty Lounge
(6, 4, 6, '2025-05-21 13:00:00', 'pending'),  -- Frank books Hair Coloring at Serene Spa
(7, 5, 7, '2025-05-22 09:00:00', 'confirmed'),  -- Grace books Waxing at Elegance Salon
(8, 6, 8, '2025-05-22 10:00:00', 'pending'),  -- Henry books Eyebrow Threading at Tranquil Touch
(9, 7, 9, '2025-05-22 11:00:00', 'confirmed'),  -- Isabel books Makeup at Luxe Beauty Studio
(1, 8, 10, '2025-05-22 12:00:00', 'pending');  -- Alice books Nail Art at Harmony Spa