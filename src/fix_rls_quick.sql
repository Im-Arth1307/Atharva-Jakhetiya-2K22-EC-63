-- =====================================================
-- Quick Fix: Update RLS Policies for Anon Access
-- =====================================================
-- Run this in Supabase SQL Editor to allow operations without authentication
-- This is needed because we're using anon key, not authenticated users

-- Credit Transactions: Allow everyone to insert (for testing)
DROP POLICY IF EXISTS "Students can create credit transactions" ON credit_transactions;
CREATE POLICY "Anyone can create credit transactions"
    ON credit_transactions FOR INSERT
    WITH CHECK (true);

-- Student Credits: Allow updates
DROP POLICY IF EXISTS "Students can update their own credits" ON student_credits;
CREATE POLICY "Anyone can update student credits"
    ON student_credits FOR UPDATE
    USING (true);

-- Notifications: Allow inserts
DROP POLICY IF EXISTS "Users can update their own notifications" ON notifications;
CREATE POLICY "Anyone can create notifications"
    ON notifications FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Anyone can view notifications"
    ON notifications FOR SELECT
    USING (true);

-- Endorsements: Already should work, but make sure
DROP POLICY IF EXISTS "Students can create endorsements" ON endorsements;
CREATE POLICY "Anyone can create endorsements"
    ON endorsements FOR INSERT
    WITH CHECK (true);

-- Voucher Purchases: Allow inserts
DROP POLICY IF EXISTS "Students can create voucher purchases" ON voucher_purchases;
CREATE POLICY "Anyone can create voucher purchases"
    ON voucher_purchases FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Anyone can view voucher purchases"
    ON voucher_purchases FOR SELECT
    USING (true);

-- Verify
SELECT 'RLS policies updated successfully!' as status;

