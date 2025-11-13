# Student Setup Guide - Connect Supabase to App

## Quick Setup (Choose One Method)

### Method 1: Python Script (Recommended - Easiest)

1. **Run the setup script:**
   ```bash
   cd src
   python setup_students.py
   ```

2. **That's it!** The script will:
   - Create all students in Supabase
   - Assign unique IDs automatically
   - Initialize credits for each student
   - Set up current student (2K22/EC/63) with sample data

### Method 2: SQL Script (Alternative)

1. **Open Supabase SQL Editor**
2. **Copy and paste** the contents of `populate_students.sql`
3. **Click Run**
4. **Done!**

---

## What Gets Created

### Students Table
- 9 students with unique UUIDs
- Names and roll numbers
- Email addresses (optional)

### Student Credits Table
- Credit balances for current month
- Current user (2K22/EC/63) gets:
  - 150 total credits
  - 85 received credits
  - 55 sent this month
- Other students get:
  - 100 total credits
  - 0 received credits
  - 0 sent this month

---

## Verify Setup

### Check in Supabase Dashboard

1. Go to **Table Editor** → `students`
2. You should see 9 students
3. Each has a unique `id` (UUID)
4. Check `student_credits` table for credit balances

### Check in Python

```python
from db_helper import get_all_students

students = get_all_students()
print(f"Found {len(students)} students")
for s in students:
    print(f"{s['name']} ({s['roll_number']}) - ID: {s['id']}")
```

### Check in App

1. Run `streamlit run app.py`
2. Go to "Send Credits" page
3. Students should appear with database IDs
4. Sidebar should show "✅ Connected to database"

---

## How Student IDs Work

### Database Structure
- Each student gets a **unique UUID** when created
- UUID format: `550e8400-e29b-41d4-a716-446655440000`
- IDs are permanent and never change

### In Your App
- Students loaded from database have `id` field
- Students from hardcoded fallback have `id: None`
- App uses IDs for:
  - Sending credits (needs receiver ID)
  - Creating endorsements (needs endorsee ID)
  - Tracking relationships

---

## Troubleshooting

### "No students found"
**Solution:** Run `setup_students.py` or `populate_students.sql`

### "Students have no IDs"
**Solution:** 
1. Check students exist in Supabase
2. Clear cache: `st.cache_data.clear()` in app
3. Restart Streamlit app

### "Can't send credits - no receiver ID"
**Solution:**
1. Make sure students are loaded from database
2. Check `get_students()` returns students with `id` field
3. Verify connection: sidebar should show "✅ Connected"

### "Duplicate students"
**Solution:**
- Script uses `ON CONFLICT` to handle duplicates
- Existing students are updated, not duplicated
- Roll numbers are unique (enforced by database)

---

## Adding New Students

### Using Python Script
Edit `setup_students.py` and add to `STUDENTS_DATA`:
```python
{"name": "New Student", "roll_number": "2K22/EC/99", "email": "new@example.com"}
```
Then run: `python setup_students.py`

### Using SQL
```sql
INSERT INTO students (name, roll_number, email)
VALUES ('New Student', '2K22/EC/99', 'new@example.com')
ON CONFLICT (roll_number) DO NOTHING;
```

### Using Supabase Dashboard
1. Go to Table Editor → `students`
2. Click "Insert row"
3. Fill in name and roll_number
4. Click "Save"

---

## Current Student Setup

The app uses **roll number `2K22/EC/63`** as the current logged-in user.

**To change current user:**
1. Edit `app.py` line 191:
   ```python
   st.session_state.current_student_roll = "YOUR_ROLL_NUMBER"
   ```

2. Or set it in the app (future feature)

**Important:** Make sure the current student exists in the database!

---

## Connection Flow

```
App Starts
    ↓
Load config.py (Supabase credentials)
    ↓
Connect to Supabase
    ↓
get_all_students() → Returns students with IDs
    ↓
get_current_student_id() → Gets/creates current user
    ↓
App uses IDs for all operations
```

---

## Testing the Connection

### Test 1: Check Students Load
```python
from db_helper import get_all_students
students = get_all_students()
print([s['id'] for s in students])  # Should show UUIDs
```

### Test 2: Check Current Student
```python
from db_helper import get_student_by_roll
student = get_student_by_roll('2K22/EC/63')
print(student['id'])  # Should show UUID
```

### Test 3: Send Credits
1. Go to Send Credits page
2. Select a student (must have ID)
3. Send credits
4. Check Supabase → `credit_transactions` table

---

## Next Steps

1. ✅ Run `setup_students.py`
2. ✅ Verify students in Supabase
3. ✅ Run Streamlit app
4. ✅ Test sending credits
5. ✅ Test endorsements
6. ✅ Check database for new records

---

## Files Reference

- **`setup_students.py`** - Python script to populate students
- **`populate_students.sql`** - SQL script (alternative)
- **`config.py`** - Your Supabase credentials
- **`db_helper.py`** - Database functions
- **`app.py`** - Main application

---

**🎉 Once students are set up, your app will automatically use database IDs for all operations!**

