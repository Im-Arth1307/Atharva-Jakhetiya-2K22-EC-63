# Debug: Failed to Send Credits

## Quick Fixes

### 1. Check RLS Policies (Most Common Issue)

Run this in Supabase SQL Editor:
```sql
-- Copy contents of fix_rls_policies.sql and run it
```

Or manually:
1. Go to Supabase → Authentication → Policies
2. Check `credit_transactions` table
3. Make sure INSERT policy allows inserts

### 2. Verify Students Have IDs

```bash
python -c "from db_helper import get_all_students; students = get_all_students(); print('Students with IDs:'); [print(f\"{s['name']}: {s.get('id', 'NO ID')}\") for s in students[:5]]"
```

**Expected:** All students should have UUIDs, not "NO ID"

### 3. Check Current Student ID

```bash
python -c "from db_helper import get_student_by_roll; student = get_student_by_roll('2K22/EC/63'); print(f\"Current student ID: {student['id'] if student else 'NOT FOUND'}\")"
```

**Expected:** Should show a UUID

### 4. Test Database Connection

```bash
python -c "from db_helper import is_connected, supabase; print(f'Connected: {is_connected()}'); result = supabase.table('students').select('id').limit(1).execute(); print(f'Can read: {result.data is not None}')"
```

### 5. Check Console Output

When you try to send credits, check:
- Streamlit terminal/console
- Look for error messages
- Check Supabase → Logs → API Logs

## Common Errors

### "permission denied"
→ Run `fix_rls_policies.sql`

### "relation does not exist"
→ Run `database_schema.sql` again

### "null value in column"
→ Make sure students have IDs (run `setup_students.py`)

### "foreign key constraint"
→ Make sure both sender and receiver exist in `students` table

## Step-by-Step Debug

1. **Verify Setup:**
   ```bash
   python setup_students.py
   ```

2. **Check Students:**
   - Supabase → Table Editor → `students`
   - Should see 9 students with UUIDs

3. **Check Credits:**
   - Supabase → Table Editor → `student_credits`
   - Current student (2K22/EC/63) should have credits

4. **Test Connection:**
   ```bash
   python -c "from db_helper import is_connected; print(is_connected())"
   ```

5. **Try Sending:**
   - Run app
   - Go to Send Credits
   - Select student (must have ID)
   - Send credits
   - Check console for errors

## If Still Failing

1. **Check Supabase Logs:**
   - Dashboard → Logs → API Logs
   - Look for error messages

2. **Test Direct Insert:**
   ```python
   from db_helper import supabase
   result = supabase.table('credit_transactions').insert({
       'sender_id': 'your-sender-id',
       'receiver_id': 'your-receiver-id',
       'amount': 10,
       'transaction_type': 'transfer'
   }).execute()
   print(result.data)
   ```

3. **Verify RLS:**
   - Supabase → Authentication → Policies
   - Check all tables have proper policies

## Quick Test Script

Create `test_send.py`:
```python
from db_helper import *
from config import SUPABASE_URL, SUPABASE_KEY

# Get student IDs
students = get_all_students()
if len(students) < 2:
    print("Need at least 2 students")
    exit(1)

sender_id = students[0]['id']
receiver_id = students[1]['id']

print(f"Sending from {students[0]['name']} to {students[1]['name']}")
result = send_credits(sender_id, receiver_id, 10, "Test")
print(f"Result: {result}")
```

Run: `python test_send.py`

