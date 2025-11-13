# Quick Supabase Setup Guide

## Fastest Way to Set Up Database

### Option 1: One-Click SQL Script (Recommended - 2 minutes)

1. **Create Supabase Project:**
   - Go to [supabase.com](https://supabase.com)
   - Sign up/Login
   - Click "New Project"
   - Fill in:
     - Name: `boostly`
     - Database Password: (choose strong password)
     - Region: (closest to you)
   - Click "Create new project"
   - Wait 2-3 minutes for setup

2. **Run SQL Schema:**
   - In Supabase dashboard, click **SQL Editor** (left sidebar)
   - Click **New Query**
   - Open `database_schema.sql` from this folder
   - **Copy the ENTIRE file** (Ctrl+A, Ctrl+C)
   - **Paste into SQL Editor** (Ctrl+V)
   - Click **Run** (or press Ctrl+Enter)
   - Wait for "Success" message

3. **Get API Keys:**
   - Go to **Settings** → **API**
   - Copy:
     - **Project URL**: `https://xxxxx.supabase.co`
     - **anon public key**: `eyJhbGc...` (long string)

4. **Done!** Your database is ready.

### Option 2: Supabase Dashboard (Alternative - 5 minutes)

If you prefer using the UI:

1. Create tables manually in **Table Editor**
2. Add columns one by one
3. Set up relationships
4. Configure RLS policies

**Not recommended** - SQL script is much faster!

---

## Connect Your Streamlit App

### Step 1: Install Supabase Client

```bash
pip install supabase
```

Or add to `requirements.txt`:
```
supabase>=2.0.0
```

### Step 2: Create Config File

Create `config.py`:

```python
import os
from supabase import create_client, Client

# Get from Supabase Dashboard → Settings → API
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key-here")

# Create client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
```

### Step 3: Use in Your App

See `db_helper.py` for complete examples.

---

## Real-Time Updates Setup

Supabase supports real-time subscriptions out of the box!

### Enable Realtime (Already done in schema)

The schema already includes:
- Row Level Security (RLS)
- Proper table structure
- Indexes for performance

### Subscribe to Changes

```python
from supabase import create_client

# Subscribe to credit transactions
subscription = supabase.table('credit_transactions')\
    .on('INSERT', handle_new_transaction)\
    .subscribe()

# Subscribe to notifications
subscription = supabase.table('notifications')\
    .on('INSERT', handle_new_notification)\
    .subscribe()
```

See `db_helper.py` for complete real-time implementation.

---

## Testing Your Connection

Run this in Python:

```python
from supabase import create_client

url = "https://your-project.supabase.co"
key = "your-anon-key"

supabase = create_client(url, key)

# Test query
result = supabase.table('students').select('*').limit(1).execute()
print(result.data)
```

If you see data (or empty list), connection works!

---

## Common Issues

### "relation does not exist"
- Make sure you ran the SQL schema
- Check you're in the correct database

### "permission denied"
- Check RLS policies are set up
- Verify you're using the anon key (not service_role)

### "connection timeout"
- Check your internet connection
- Verify Supabase project is active
- Check firewall settings

---

## Next Steps

1. ✅ Database setup complete
2. ✅ Get API keys
3. ⬜ Install supabase client
4. ⬜ Update app.py to use database
5. ⬜ Test real-time updates

See `db_helper.py` for ready-to-use code!

