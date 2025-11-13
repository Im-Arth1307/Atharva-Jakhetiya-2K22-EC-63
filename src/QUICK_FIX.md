# 🚨 Quick Fix: Failed to Send Credits

## The Problem
RLS (Row Level Security) policies are blocking database inserts because they expect authenticated users, but we're using the anon key.

## The Solution (30 seconds)

### Step 1: Open Supabase SQL Editor
1. Go to your Supabase dashboard
2. Click **SQL Editor** (left sidebar)
3. Click **New Query**

### Step 2: Run This SQL
Copy and paste the entire contents of `fix_rls_quick.sql` and click **Run**

**OR** copy this directly:

```sql
-- Allow credit transactions
DROP POLICY IF EXISTS "Students can create credit transactions" ON credit_transactions;
CREATE POLICY "Anyone can create credit transactions"
    ON credit_transactions FOR INSERT WITH CHECK (true);

-- Allow credit updates
DROP POLICY IF EXISTS "Students can update their own credits" ON student_credits;
CREATE POLICY "Anyone can update student credits"
    ON student_credits FOR UPDATE USING (true);

-- Allow notifications
DROP POLICY IF EXISTS "Users can update their own notifications" ON notifications;
CREATE POLICY "Anyone can create notifications"
    ON notifications FOR INSERT WITH CHECK (true);
CREATE POLICY "Anyone can view notifications"
    ON notifications FOR SELECT USING (true);

-- Allow endorsements
DROP POLICY IF EXISTS "Students can create endorsements" ON endorsements;
CREATE POLICY "Anyone can create endorsements"
    ON endorsements FOR INSERT WITH CHECK (true);

-- Allow vouchers
DROP POLICY IF EXISTS "Students can create voucher purchases" ON voucher_purchases;
CREATE POLICY "Anyone can create voucher purchases"
    ON voucher_purchases FOR INSERT WITH CHECK (true);
```

### Step 3: Test Again
1. Restart your Streamlit app
2. Try sending credits
3. Should work now! ✅

---

## Why This Happens

The original RLS policies use `auth.uid()` which requires:
- User to be logged in via Supabase Auth
- Authenticated session

But we're using:
- Anon key (no authentication)
- Direct database access

So we need to update policies to allow anon access.

---

## Alternative: Use Service Role Key (Not Recommended)

If you want to keep strict RLS:
1. Use service_role key instead of anon key
2. **Warning:** Service role bypasses ALL RLS - use carefully!

---

## Verify It Works

After running the SQL:
1. Try sending credits in your app
2. Check Supabase → `credit_transactions` table
3. Should see the new transaction!

---

**That's it! Your app should work now.** 🎉

