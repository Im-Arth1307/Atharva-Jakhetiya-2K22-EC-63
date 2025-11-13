-- =====================================================
-- Populate Students in Supabase
-- =====================================================
-- Run this in Supabase SQL Editor to populate students
-- Or use setup_students.py Python script

-- Insert students (will skip if roll_number already exists)
INSERT INTO students (name, roll_number, email) VALUES
    ('Student Name', '2K22/EC/63', 'student@example.com'),
    ('Sarah Johnson', '2K22/EC/45', 'sarah@example.com'),
    ('Michael Chen', '2K22/EC/52', 'michael@example.com'),
    ('Emma Wilson', '2K22/EC/38', 'emma@example.com'),
    ('David Martinez', '2K22/EC/67', 'david@example.com'),
    ('Lisa Anderson', '2K22/EC/29', 'lisa@example.com'),
    ('Alex Thompson', '2K22/EC/71', 'alex@example.com'),
    ('James Brown', '2K22/EC/56', 'james@example.com'),
    ('Olivia Davis', '2K22/EC/42', 'olivia@example.com')
ON CONFLICT (roll_number) DO UPDATE
SET name = EXCLUDED.name, email = EXCLUDED.email;

-- Initialize credits for all students for current month
INSERT INTO student_credits (student_id, total_credits, credits_received, credits_sent_this_month, monthly_limit, month_year)
SELECT 
    s.id,
    CASE 
        WHEN s.roll_number = '2K22/EC/63' THEN 150  -- Current user gets more credits
        ELSE 100
    END as total_credits,
    CASE 
        WHEN s.roll_number = '2K22/EC/63' THEN 85  -- Current user has received credits
        ELSE 0
    END as credits_received,
    CASE 
        WHEN s.roll_number = '2K22/EC/63' THEN 55  -- Current user has sent credits
        ELSE 0
    END as credits_sent_this_month,
    100 as monthly_limit,
    TO_CHAR(NOW(), 'YYYY-MM') as month_year
FROM students s
WHERE NOT EXISTS (
    SELECT 1 FROM student_credits 
    WHERE student_id = s.id 
    AND month_year = TO_CHAR(NOW(), 'YYYY-MM')
);

-- Verify students were created
SELECT 
    s.id,
    s.name,
    s.roll_number,
    COALESCE(sc.total_credits, 100) as total_credits,
    COALESCE(sc.credits_received, 0) as credits_received
FROM students s
LEFT JOIN student_credits sc ON s.id = sc.student_id 
    AND sc.month_year = TO_CHAR(NOW(), 'YYYY-MM')
ORDER BY s.name;

