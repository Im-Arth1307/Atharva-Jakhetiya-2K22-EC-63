-- =====================================================
-- Boostly Database Schema for Supabase
-- =====================================================
-- This file contains the complete database schema for the Boostly application
-- Run these commands in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. STUDENTS TABLE
-- =====================================================
-- Stores all student information
CREATE TABLE IF NOT EXISTS students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 2. STUDENT_CREDITS TABLE
-- =====================================================
-- Tracks current credit balances and monthly limits per student
CREATE TABLE IF NOT EXISTS student_credits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    total_credits INTEGER DEFAULT 100 NOT NULL,
    credits_received INTEGER DEFAULT 0 NOT NULL,
    credits_sent_this_month INTEGER DEFAULT 0 NOT NULL,
    monthly_limit INTEGER DEFAULT 100 NOT NULL,
    month_year VARCHAR(7) NOT NULL, -- Format: 'YYYY-MM' for tracking monthly limits
    last_reset_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(student_id, month_year)
);

-- =====================================================
-- 3. CREDIT_TRANSACTIONS TABLE
-- =====================================================
-- Records all credit transfers between students
CREATE TABLE IF NOT EXISTS credit_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    receiver_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL CHECK (amount > 0),
    message TEXT,
    transaction_type VARCHAR(20) DEFAULT 'transfer' CHECK (transaction_type IN ('transfer', 'redemption')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT no_self_transfer CHECK (sender_id != receiver_id)
);

-- =====================================================
-- 4. NOTIFICATIONS TABLE
-- =====================================================
-- Stores all notifications for students
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL CHECK (
        notification_type IN (
            'credits_sent', 
            'credits_received', 
            'endorsement_received', 
            'endorsement_given'
        )
    ),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    details TEXT,
    related_student_id UUID REFERENCES students(id) ON DELETE SET NULL,
    related_transaction_id UUID REFERENCES credit_transactions(id) ON DELETE SET NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 5. ENDORSEMENTS TABLE
-- =====================================================
-- Tracks endorsements given by students to other students
CREATE TABLE IF NOT EXISTS endorsements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    endorser_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    endorsee_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    recognition_id UUID REFERENCES credit_transactions(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT no_self_endorsement CHECK (endorser_id != endorsee_id),
    -- Ensure one endorsement per endorser-endorsee-recognition combination
    UNIQUE(endorser_id, endorsee_id, recognition_id)
);

-- =====================================================
-- 6. VOUCHER_PURCHASES TABLE
-- =====================================================
-- Records all voucher redemptions
CREATE TABLE IF NOT EXISTS voucher_purchases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    num_vouchers INTEGER NOT NULL CHECK (num_vouchers > 0),
    credits_per_voucher INTEGER NOT NULL CHECK (credits_per_voucher > 0),
    total_credits INTEGER NOT NULL CHECK (total_credits > 0),
    total_value DECIMAL(10, 2) NOT NULL CHECK (total_value > 0),
    voucher_rate DECIMAL(5, 2) DEFAULT 5.00, -- ₹5 per credit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Student credits indexes
CREATE INDEX IF NOT EXISTS idx_student_credits_student_id ON student_credits(student_id);
CREATE INDEX IF NOT EXISTS idx_student_credits_month_year ON student_credits(month_year);

-- Credit transactions indexes
CREATE INDEX IF NOT EXISTS idx_credit_transactions_sender ON credit_transactions(sender_id);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_receiver ON credit_transactions(receiver_id);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_created_at ON credit_transactions(created_at DESC);

-- Notifications indexes
CREATE INDEX IF NOT EXISTS idx_notifications_student_id ON notifications(student_id);
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(notification_type);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);

-- Endorsements indexes
CREATE INDEX IF NOT EXISTS idx_endorsements_endorser ON endorsements(endorser_id);
CREATE INDEX IF NOT EXISTS idx_endorsements_endorsee ON endorsements(endorsee_id);
CREATE INDEX IF NOT EXISTS idx_endorsements_recognition ON endorsements(recognition_id);

-- Voucher purchases indexes
CREATE INDEX IF NOT EXISTS idx_voucher_purchases_student ON voucher_purchases(student_id);
CREATE INDEX IF NOT EXISTS idx_voucher_purchases_created_at ON voucher_purchases(created_at DESC);

-- =====================================================
-- FUNCTIONS AND TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for student_credits updated_at
CREATE TRIGGER update_student_credits_updated_at
    BEFORE UPDATE ON student_credits
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for students updated_at
CREATE TRIGGER update_students_updated_at
    BEFORE UPDATE ON students
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_credits ENABLE ROW LEVEL SECURITY;
ALTER TABLE credit_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE endorsements ENABLE ROW LEVEL SECURITY;
ALTER TABLE voucher_purchases ENABLE ROW LEVEL SECURITY;

-- Students: Users can read all students, but only update their own
CREATE POLICY "Students are viewable by everyone"
    ON students FOR SELECT
    USING (true);

CREATE POLICY "Students can update their own profile"
    ON students FOR UPDATE
    USING (auth.uid()::text = id::text);

-- Student Credits: Users can view all, but only update their own
CREATE POLICY "Student credits are viewable by everyone"
    ON student_credits FOR SELECT
    USING (true);

CREATE POLICY "Students can update their own credits"
    ON student_credits FOR UPDATE
    USING (auth.uid()::text = student_id::text);

-- Credit Transactions: Users can view all transactions
CREATE POLICY "Credit transactions are viewable by everyone"
    ON credit_transactions FOR SELECT
    USING (true);

CREATE POLICY "Students can create credit transactions"
    ON credit_transactions FOR INSERT
    WITH CHECK (auth.uid()::text = sender_id::text);

-- Notifications: Users can only view their own notifications
CREATE POLICY "Users can view their own notifications"
    ON notifications FOR SELECT
    USING (auth.uid()::text = student_id::text);

CREATE POLICY "Users can update their own notifications"
    ON notifications FOR UPDATE
    USING (auth.uid()::text = student_id::text);

-- Endorsements: Users can view all endorsements
CREATE POLICY "Endorsements are viewable by everyone"
    ON endorsements FOR SELECT
    USING (true);

CREATE POLICY "Students can create endorsements"
    ON endorsements FOR INSERT
    WITH CHECK (auth.uid()::text = endorser_id::text);

-- Voucher Purchases: Users can only view their own purchases
CREATE POLICY "Users can view their own voucher purchases"
    ON voucher_purchases FOR SELECT
    USING (auth.uid()::text = student_id::text);

CREATE POLICY "Students can create voucher purchases"
    ON voucher_purchases FOR INSERT
    WITH CHECK (auth.uid()::text = student_id::text);

-- =====================================================
-- SAMPLE DATA (Optional - for testing)
-- =====================================================

-- Insert sample students
INSERT INTO students (id, name, roll_number) VALUES
    ('00000000-0000-0000-0000-000000000001', 'Student Name', '2K22/EC/63'),
    ('00000000-0000-0000-0000-000000000002', 'Sarah Johnson', '2K22/EC/45'),
    ('00000000-0000-0000-0000-000000000003', 'Michael Chen', '2K22/EC/52'),
    ('00000000-0000-0000-0000-000000000004', 'Emma Wilson', '2K22/EC/38'),
    ('00000000-0000-0000-0000-000000000005', 'David Martinez', '2K22/EC/67'),
    ('00000000-0000-0000-0000-000000000006', 'Lisa Anderson', '2K22/EC/29'),
    ('00000000-0000-0000-0000-000000000007', 'Alex Thompson', '2K22/EC/71'),
    ('00000000-0000-0000-0000-000000000008', 'James Brown', '2K22/EC/56'),
    ('00000000-0000-0000-0000-000000000009', 'Olivia Davis', '2K22/EC/42')
ON CONFLICT (roll_number) DO NOTHING;

-- Initialize student credits for current month
INSERT INTO student_credits (student_id, total_credits, credits_received, credits_sent_this_month, month_year)
SELECT 
    id,
    150, -- total_credits
    85,  -- credits_received
    55,  -- credits_sent_this_month
    TO_CHAR(NOW(), 'YYYY-MM') -- current month
FROM students
ON CONFLICT (student_id, month_year) DO NOTHING;

