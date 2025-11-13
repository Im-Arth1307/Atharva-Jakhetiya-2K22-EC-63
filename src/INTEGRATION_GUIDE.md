# Database Integration Guide

## Quick Start: Connect Streamlit to Supabase

### Step 1: Set Up Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Supabase credentials:
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGc...
   ```

### Step 2: Update app.py

Add at the top of `app.py`:

```python
import os
from dotenv import load_dotenv
from db_helper import *

# Load environment variables
load_dotenv()

# Check connection
if is_connected():
    st.sidebar.success("✅ Connected to database")
else:
    st.sidebar.warning("⚠️ Using session state (no database)")
```

### Step 3: Replace Session State with Database Calls

#### Example: Load Students from Database

**Before (session state):**
```python
STUDENTS = [
    {"name": "Sarah Johnson", "roll": "2K22/EC/45"},
    # ...
]
```

**After (database):**
```python
# In main() function
if is_connected():
    students_data = get_all_students()
    STUDENTS = [
        {"name": s['name'], "roll": s['roll_number']} 
        for s in students_data
    ]
else:
    # Fallback to hardcoded data
    STUDENTS = [...]
```

#### Example: Load Notifications

**Before:**
```python
NOTIFICATIONS = [
    {"type": "credits_sent", ...},
    # ...
]
```

**After:**
```python
# Get current student ID (you'll need to implement login)
current_student_id = get_current_student_id()

if is_connected() and current_student_id:
    notifications_data = get_notifications(current_student_id)
    NOTIFICATIONS = [
        {
            "type": n['notification_type'],
            "title": n['title'],
            "message": n['message'],
            "timestamp": n['created_at'],
            "details": n.get('details', '')
        }
        for n in notifications_data
    ]
```

#### Example: Send Credits

**Before:**
```python
st.session_state.total_credits -= credits_to_send
st.session_state.credits_sent += credits_to_send
```

**After:**
```python
if is_connected():
    sender_id = get_current_student_id()
    receiver_id = STUDENTS[selected_idx]['id']  # Store IDs in STUDENTS
    
    result = send_credits(sender_id, receiver_id, credits_to_send, message)
    if result:
        st.success("Credits sent successfully!")
        st.rerun()  # Refresh to show updated data
    else:
        st.error("Failed to send credits")
```

### Step 4: Implement Real-Time Updates

Add this to your main function:

```python
import time
from threading import Thread

def setup_realtime_updates():
    """Set up real-time subscriptions"""
    if not is_connected():
        return
    
    current_student_id = get_current_student_id()
    if not current_student_id:
        return
    
    def on_new_notification(notification):
        st.rerun()  # Refresh page when new notification arrives
    
    def on_credit_update(credits):
        st.rerun()  # Refresh when credits change
    
    # Subscribe to changes
    subscribe_to_notifications(current_student_id, on_new_notification)
    subscribe_to_credits(current_student_id, on_credit_update)

# Call in main()
if is_connected():
    setup_realtime_updates()
```

### Step 5: Add Authentication (Optional but Recommended)

Create `auth_helper.py`:

```python
import streamlit as st
from db_helper import get_student_by_roll

def get_current_student():
    """Get current logged-in student"""
    if 'current_student' not in st.session_state:
        # For now, use hardcoded or session
        # In production, implement proper login
        roll_number = st.session_state.get('user_roll', '2K22/EC/63')
        student = get_student_by_roll(roll_number)
        if student:
            st.session_state['current_student'] = student
        else:
            st.session_state['current_student'] = None
    return st.session_state.get('current_student')

def get_current_student_id():
    """Get current student's ID"""
    student = get_current_student()
    return student['id'] if student else None
```

Then use in `app.py`:

```python
from auth_helper import get_current_student_id

# In functions that need student ID
current_student_id = get_current_student_id()
```

## Complete Integration Example

Here's a minimal example showing how to integrate:

```python
import streamlit as st
from dotenv import load_dotenv
from db_helper import *

load_dotenv()

st.title("Boostly")

# Check connection
if is_connected():
    st.success("✅ Connected to database")
    
    # Get students
    students = get_all_students()
    st.write(f"Found {len(students)} students")
    
    # Get current student (you'll implement login)
    current_student_id = "your-student-id-here"
    
    # Get notifications
    notifications = get_notifications(current_student_id)
    for notif in notifications:
        st.write(f"**{notif['title']}**: {notif['message']}")
    
    # Get stats
    stats = get_student_stats(current_student_id)
    st.metric("Total Credits", stats['total_credits'])
    
else:
    st.warning("⚠️ Database not connected - using session state")
    # Fallback to hardcoded data
```

## Migration Strategy

### Phase 1: Hybrid Approach (Recommended)

1. Keep session state as fallback
2. Use database when connected
3. Gradually migrate features

```python
def get_students():
    if is_connected():
        return get_all_students()
    else:
        return HARDCODED_STUDENTS
```

### Phase 2: Full Database

1. Remove all session state
2. Use database for everything
3. Add proper error handling

### Phase 3: Real-Time

1. Add subscriptions
2. Implement auto-refresh
3. Add loading states

## Testing Your Integration

### Test 1: Connection
```python
from db_helper import is_connected
print(f"Connected: {is_connected()}")
```

### Test 2: Read Data
```python
from db_helper import get_all_students
students = get_all_students()
print(f"Students: {len(students)}")
```

### Test 3: Write Data
```python
from db_helper import send_credits
# Test with sample IDs
result = send_credits("sender-id", "receiver-id", 10, "Test")
print(f"Success: {result is not None}")
```

## Troubleshooting

### "Module not found: supabase"
```bash
pip install supabase python-dotenv
```

### "Connection failed"
- Check `.env` file exists
- Verify SUPABASE_URL and SUPABASE_KEY are correct
- Check Supabase project is active

### "Permission denied"
- Verify RLS policies are set up
- Check you're using anon key (not service_role)
- Ensure policies allow your operations

### "Real-time not working"
- Check Realtime is enabled in Supabase dashboard
- Verify table has RLS policies
- Check network connection

## Performance Tips

1. **Cache Data**: Use Streamlit's caching for frequently accessed data
   ```python
   @st.cache_data(ttl=60)
   def get_cached_students():
       return get_all_students()
   ```

2. **Batch Operations**: Group multiple operations
3. **Indexes**: Already set up in schema
4. **Pagination**: Use limit/offset for large datasets

## Next Steps

1. ✅ Set up Supabase project
2. ✅ Run database schema
3. ✅ Install dependencies
4. ✅ Configure environment variables
5. ⬜ Integrate with app.py
6. ⬜ Test all features
7. ⬜ Add real-time updates
8. ⬜ Deploy!

See `QUICK_SETUP.md` for initial setup steps.

