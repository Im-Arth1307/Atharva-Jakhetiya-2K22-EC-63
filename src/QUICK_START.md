# 🚀 Quick Start - Connect Supabase to Your App

## Step 1: Populate Students (2 minutes)

### Option A: Python Script (Easiest)
```bash
cd src
python setup_students.py
```

### Option B: SQL Script
1. Open Supabase → SQL Editor
2. Copy contents of `populate_students.sql`
3. Paste and Run

**✅ Done!** Students now have unique IDs in database.

---

## Step 2: Verify Connection

```bash
# Test connection
python -c "from db_helper import is_connected, get_all_students; print('✅ Connected!' if is_connected() else '❌ Not connected'); students = get_all_students(); print(f'Found {len(students)} students')"
```

**Expected output:**
```
✅ Connected!
Found 9 students
```

---

## Step 3: Run Your App

```bash
streamlit run app.py
```

**Check sidebar:**
- Should show: "✅ Connected to database"
- Stats should load from database
- Students should have IDs

---

## Step 4: Test It!

1. **Send Credits:**
   - Go to "Send Credits" page
   - Select a student
   - Send credits
   - Check Supabase → `credit_transactions` table

2. **Endorse:**
   - Go to "Endorse" page
   - Endorse a student
   - Check Supabase → `endorsements` table

3. **View Data:**
   - Open Supabase → Table Editor
   - See your data in real-time!

---

## Troubleshooting

### "No students found"
→ Run `setup_students.py`

### "Not connected"
→ Check `config.py` has correct credentials

### "Students have no IDs"
→ Clear cache and restart app

---

## What You Get

✅ 9 students with unique UUIDs  
✅ Credit balances initialized  
✅ Current student (2K22/EC/63) with sample data  
✅ All database operations working  
✅ Real-time data sync  

---

**🎉 Your app is now fully connected to Supabase!**

