USE beautysyncpro;

-- Insert into user table (10 users: 5 customers, 5 vendors)
INSERT INTO user (username, password_hash, email, is_admin, user_type) VALUES
('alice', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'alice@example.com', FALSE, 'customer'),
('bob', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'bob@example.com', FALSE, 'customer'),
('charlie', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'charlie@example.com', FALSE, 'customer'),
('diana', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'diana@example.com', FALSE, 'customer'),
('eve', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'eve@example.com', FALSE, 'customer'),
('vendor1', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'vendor1@example.com', FALSE, 'vendor'),
('vendor2', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'vendor2@example.com', FALSE, 'vendor'),
('vendor3', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'vendor3@example.com', FALSE, 'vendor'),
('vendor4', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'vendor4@example.com', FALSE, 'vendor'),
('vendor5', 'pbkdf2:sha256:600000$X8kL2q3z$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z', 'vendor5@example.com', FALSE, 'vendor');

-- Insert into salon table (10 salons, each owned by a vendor)
INSERT INTO salon (name, address, vendor_id) VALUES
('Glow Haven Spa', '123 Main St, Mumbai', 6),  -- Owned by vendor1
('Radiance Salon', '456 Oak Ave, Delhi', 7),  -- Owned by vendor2
('Bliss Beauty Lounge', '789 Pine Rd, Bangalore', 8),  -- Owned by vendor3
('Serene Spa', '101 Maple Dr, Chennai', 9),  -- Owned by vendor4
('Elegance Salon', '202 Cedar Ln, Hyderabad', 10),  -- Owned by vendor5
('Tranquil Touch', '303 Birch St, Pune', 6),  -- Owned by vendor1
('Luxe Beauty Studio', '404 Elm Ave, Kolkata', 7),  -- Owned by vendor2
('Harmony Spa', '505 Willow Rd, Ahmedabad', 8),  -- Owned by vendor3
('Chic Salon', '606 Ash Dr, Jaipur', 9),  -- Owned by vendor4
('Vogue Wellness', '707 Spruce Ln, Surat', 10);  -- Owned by vendor5

-- Insert into service table (10 services, distributed across salons)
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
(1, 1, 1, '2025-05-20 19:00:00', 'confirmed'),  -- Alice books Facial at Glow Haven Spa
(2, 1, 2, '2025-05-20 19:30:00', 'pending'),  -- Bob books Haircut at Glow Haven Spa
(3, 2, 3, '2025-05-21 09:00:00', 'confirmed'),  -- Charlie books Manicure at Radiance Salon
(4, 2, 4, '2025-05-21 10:00:00', 'pending'),  -- Diana books Pedicure at Radiance Salon
(5, 3, 5, '2025-05-21 11:00:00', 'confirmed'),  -- Eve books Massage at Bliss Beauty Lounge
(1, 4, 6, '2025-05-21 13:00:00', 'pending'),  -- Alice books Hair Coloring at Serene Spa
(2, 5, 7, '2025-05-22 09:00:00', 'confirmed'),  -- Bob books Waxing at Elegance Salon
(3, 6, 8, '2025-05-22 10:00:00', 'pending'),  -- Charlie books Eyebrow Threading at Tranquil Touch
(4, 7, 9, '2025-05-22 11:00:00', 'confirmed'),  -- Diana books Makeup at Luxe Beauty Studio
(5, 8, 10, '2025-05-22 12:00:00', 'pending');  -- Eve books Nail Art at Harmony Spa