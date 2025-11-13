-- =====================================================
-- Fix RLS Policies for Credit Transactions
-- =====================================================
-- Run this if you're getting permission errors when sending credits
-- This makes the policies more permissive for testing

-- Drop existing policies
DROP POLICY IF EXISTS "Credit transactions are viewable by everyone" ON credit_transactions;
DROP POLICY IF EXISTS "Students can create credit transactions" ON credit_transactions;

-- Create more permissive policies (for testing/development)
CREATE POLICY "Credit transactions are viewable by everyone"
    ON credit_transactions FOR SELECT
    USING (true);

CREATE POLICY "Anyone can create credit transactions"
    ON credit_transactions FOR INSERT
    WITH CHECK (true);

-- Also fix student_credits policies
DROP POLICY IF EXISTS "Student credits are viewable by everyone" ON student_credits;
DROP POLICY IF EXISTS "Students can update their own credits" ON student_credits;

CREATE POLICY "Student credits are viewable by everyone"
    ON student_credits FOR SELECT
    USING (true);

CREATE POLICY "Anyone can update student credits"
    ON student_credits FOR UPDATE
    USING (true);

-- Fix notifications policies
DROP POLICY IF EXISTS "Users can view their own notifications" ON notifications;
DROP POLICY IF EXISTS "Users can update their own notifications" ON notifications;

CREATE POLICY "Notifications are viewable by everyone"
    ON notifications FOR SELECT
    USING (true);

CREATE POLICY "Anyone can create notifications"
    ON notifications FOR INSERT
    WITH CHECK (true);

-- Fix endorsements
DROP POLICY IF EXISTS "Endorsements are viewable by everyone" ON endorsements;
DROP POLICY IF EXISTS "Students can create endorsements" ON endorsements;

CREATE POLICY "Endorsements are viewable by everyone"
    ON endorsements FOR SELECT
    USING (true);

CREATE POLICY "Anyone can create endorsements"
    ON endorsements FOR INSERT
    WITH CHECK (true);

-- Verify policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename IN ('credit_transactions', 'student_credits', 'notifications', 'endorsements')
ORDER BY tablename, policyname;

