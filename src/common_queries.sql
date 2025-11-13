-- =====================================================
-- Common SQL Queries for Boostly Application
-- =====================================================
-- This file contains useful queries for common operations

-- =====================================================
-- STUDENT QUERIES
-- =====================================================

-- Get all students
SELECT id, name, roll_number, email, created_at
FROM students
ORDER BY name;

-- Get student by roll number
SELECT * FROM students WHERE roll_number = '2K22/EC/63';

-- Get student with current credit balance
SELECT 
    s.id,
    s.name,
    s.roll_number,
    COALESCE(sc.total_credits, 100) as total_credits,
    COALESCE(sc.credits_received, 0) as credits_received,
    COALESCE(sc.credits_sent_this_month, 0) as credits_sent_this_month,
    COALESCE(sc.monthly_limit, 100) as monthly_limit
FROM students s
LEFT JOIN student_credits sc ON s.id = sc.student_id 
    AND sc.month_year = TO_CHAR(NOW(), 'YYYY-MM')
WHERE s.roll_number = '2K22/EC/63';

-- =====================================================
-- CREDIT TRANSACTION QUERIES
-- =====================================================

-- Get all credit transactions for a student (as sender)
SELECT 
    ct.id,
    ct.amount,
    ct.message,
    ct.created_at,
    receiver.name as receiver_name,
    receiver.roll_number as receiver_roll
FROM credit_transactions ct
JOIN students receiver ON ct.receiver_id = receiver.id
WHERE ct.sender_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
ORDER BY ct.created_at DESC;

-- Get all credit transactions for a student (as receiver)
SELECT 
    ct.id,
    ct.amount,
    ct.message,
    ct.created_at,
    sender.name as sender_name,
    sender.roll_number as sender_roll
FROM credit_transactions ct
JOIN students sender ON ct.sender_id = sender.id
WHERE ct.receiver_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
ORDER BY ct.created_at DESC;

-- Get total credits sent this month
SELECT COALESCE(SUM(amount), 0) as total_sent
FROM credit_transactions
WHERE sender_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
AND DATE_TRUNC('month', created_at) = DATE_TRUNC('month', NOW())
AND transaction_type = 'transfer';

-- Get total credits received (all time)
SELECT COALESCE(SUM(amount), 0) as total_received
FROM credit_transactions
WHERE receiver_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
AND transaction_type = 'transfer';

-- =====================================================
-- NOTIFICATION QUERIES
-- =====================================================

-- Get all notifications for a student
SELECT 
    id,
    notification_type,
    title,
    message,
    details,
    is_read,
    created_at
FROM notifications
WHERE student_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
ORDER BY created_at DESC
LIMIT 50;

-- Get unread notifications count
SELECT COUNT(*) as unread_count
FROM notifications
WHERE student_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
AND is_read = FALSE;

-- Mark notification as read
UPDATE notifications
SET is_read = TRUE
WHERE id = 'notification-uuid-here';

-- Mark all notifications as read
UPDATE notifications
SET is_read = TRUE
WHERE student_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
AND is_read = FALSE;

-- =====================================================
-- ENDORSEMENT QUERIES
-- =====================================================

-- Get all endorsements given by a student
SELECT 
    e.id,
    e.created_at,
    endorsee.name as endorsee_name,
    endorsee.roll_number as endorsee_roll
FROM endorsements e
JOIN students endorsee ON e.endorsee_id = endorsee.id
WHERE e.endorser_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
ORDER BY e.created_at DESC;

-- Get all endorsements received by a student
SELECT 
    e.id,
    e.created_at,
    endorser.name as endorser_name,
    endorser.roll_number as endorser_roll
FROM endorsements e
JOIN students endorser ON e.endorser_id = endorser.id
WHERE e.endorsee_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
ORDER BY e.created_at DESC;

-- Get total endorsements received
SELECT COUNT(*) as total_endorsements
FROM endorsements
WHERE endorsee_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63');

-- Check if student has already endorsed another student
SELECT EXISTS(
    SELECT 1 FROM endorsements
    WHERE endorser_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
    AND endorsee_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/45')
) as already_endorsed;

-- =====================================================
-- VOUCHER QUERIES
-- =====================================================

-- Get all voucher purchases for a student
SELECT 
    id,
    num_vouchers,
    credits_per_voucher,
    total_credits,
    total_value,
    created_at
FROM voucher_purchases
WHERE student_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63')
ORDER BY created_at DESC;

-- Get total vouchers purchased
SELECT 
    COUNT(*) as total_purchases,
    SUM(num_vouchers) as total_vouchers,
    SUM(total_credits) as total_credits_redeemed,
    SUM(total_value) as total_value_redeemed
FROM voucher_purchases
WHERE student_id = (SELECT id FROM students WHERE roll_number = '2K22/EC/63');

-- =====================================================
-- STATISTICS QUERIES
-- =====================================================

-- Get student dashboard stats
SELECT 
    s.name,
    s.roll_number,
    COALESCE(sc.total_credits, 100) as total_credits,
    COALESCE(sc.credits_received, 0) as credits_received,
    COALESCE(sc.credits_sent_this_month, 0) as credits_sent_this_month,
    COALESCE(sc.monthly_limit, 100) as monthly_limit,
    (SELECT COUNT(*) FROM endorsements WHERE endorsee_id = s.id) as endorsements_received,
    (SELECT COUNT(*) FROM credit_transactions WHERE receiver_id = s.id AND transaction_type = 'transfer') as total_received_count,
    (SELECT COUNT(*) FROM credit_transactions WHERE sender_id = s.id AND transaction_type = 'transfer') as total_sent_count
FROM students s
LEFT JOIN student_credits sc ON s.id = sc.student_id 
    AND sc.month_year = TO_CHAR(NOW(), 'YYYY-MM')
WHERE s.roll_number = '2K22/EC/63';

-- Get leaderboard (top recipients by credits received)
SELECT 
    s.name,
    s.roll_number,
    COALESCE(SUM(ct.amount), 0) as total_credits_received,
    COUNT(ct.id) as recognition_count,
    (SELECT COUNT(*) FROM endorsements e 
     JOIN credit_transactions ct2 ON e.recognition_id = ct2.id 
     WHERE ct2.receiver_id = s.id) as total_endorsements
FROM students s
LEFT JOIN credit_transactions ct ON s.id = ct.receiver_id 
    AND ct.transaction_type = 'transfer'
GROUP BY s.id, s.name, s.roll_number
ORDER BY total_credits_received DESC, s.roll_number ASC
LIMIT 10;

-- =====================================================
-- TRANSACTION QUERIES (For Application Logic)
-- =====================================================

-- Send credits transaction (with validation)
-- This should be wrapped in a transaction
BEGIN;

-- 1. Check sender balance and monthly limit
SELECT 
    total_credits,
    credits_sent_this_month,
    monthly_limit
FROM student_credits
WHERE student_id = 'sender-uuid-here'
AND month_year = TO_CHAR(NOW(), 'YYYY-MM')
FOR UPDATE;

-- 2. Create credit transaction
INSERT INTO credit_transactions (sender_id, receiver_id, amount, message)
VALUES ('sender-uuid', 'receiver-uuid', 25, 'Recognition message')
RETURNING id;

-- 3. Update sender credits
UPDATE student_credits
SET 
    total_credits = total_credits - 25,
    credits_sent_this_month = credits_sent_this_month + 25
WHERE student_id = 'sender-uuid'
AND month_year = TO_CHAR(NOW(), 'YYYY-MM');

-- 4. Update receiver credits
INSERT INTO student_credits (student_id, total_credits, credits_received, month_year)
VALUES ('receiver-uuid', 100 + 25, 25, TO_CHAR(NOW(), 'YYYY-MM'))
ON CONFLICT (student_id, month_year) DO UPDATE
SET 
    total_credits = student_credits.total_credits + 25,
    credits_received = student_credits.credits_received + 25;

-- 5. Create notifications
INSERT INTO notifications (student_id, notification_type, title, message, details, related_student_id, related_transaction_id)
VALUES 
    ('sender-uuid', 'credits_sent', 'Credits Sent', 'You sent 25 credits to Receiver Name', 'Recognition message', 'receiver-uuid', 'transaction-uuid'),
    ('receiver-uuid', 'credits_received', 'Credits Received', 'You received 25 credits from Sender Name', 'Recognition message', 'sender-uuid', 'transaction-uuid');

COMMIT;

-- =====================================================
-- MONTHLY RESET QUERY
-- =====================================================

-- Reset credits for new month (run at start of each month)
INSERT INTO student_credits (student_id, total_credits, credits_received, credits_sent_this_month, monthly_limit, month_year, last_reset_date)
SELECT 
    s.id,
    -- New total: 100 base + carry forward (max 50)
    LEAST(100 + COALESCE((
        SELECT LEAST(total_credits, 50) 
        FROM student_credits 
        WHERE student_id = s.id 
        AND month_year = TO_CHAR(NOW() - INTERVAL '1 month', 'YYYY-MM')
    ), 0), 150) as total_credits,
    0 as credits_received,  -- Reset received credits
    0 as credits_sent_this_month,  -- Reset monthly sent
    100 as monthly_limit,
    TO_CHAR(NOW(), 'YYYY-MM') as month_year,
    CURRENT_DATE as last_reset_date
FROM students s
WHERE NOT EXISTS (
    SELECT 1 FROM student_credits 
    WHERE student_id = s.id 
    AND month_year = TO_CHAR(NOW(), 'YYYY-MM')
);

-- =====================================================
-- UTILITY QUERIES
-- =====================================================

-- Get days until next month reset
SELECT 
    DATE_PART('day', 
        DATE_TRUNC('month', NOW() + INTERVAL '1 month') - NOW()
    )::INTEGER as days_until_reset;

-- Get current month/year
SELECT TO_CHAR(NOW(), 'YYYY-MM') as current_month;

-- Get students who can be endorsed (not already endorsed by current user)
SELECT 
    s.id,
    s.name,
    s.roll_number
FROM students s
WHERE s.id != 'current-user-uuid'
AND NOT EXISTS (
    SELECT 1 FROM endorsements
    WHERE endorser_id = 'current-user-uuid'
    AND endorsee_id = s.id
)
ORDER BY s.name;

