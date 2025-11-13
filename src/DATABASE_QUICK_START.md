# Database Quick Start - 5 Minute Setup

## Fastest Way to Set Up Everything

### ⚡ Option 1: Copy-Paste SQL (2 minutes)

1. **Create Supabase Project:**
   - Go to https://supabase.com → Sign up/Login
   - Click "New Project"
   - Name: `boostly`, choose region, set password
   - Wait 2-3 minutes

2. **Run SQL:**
   - In Supabase: Click **SQL Editor** (left sidebar)
   - Click **New Query**
   - Open `database_schema.sql` from this folder
   - **Copy ALL** (Ctrl+A, Ctrl+C)
   - **Paste** into SQL Editor (Ctrl+V)
   - Click **Run** (or Ctrl+Enter)
   - ✅ Done! All tables created

3. **Get Keys:**
   - Go to **Settings** → **API**
   - Copy **Project URL** and **anon public key**

4. **Connect App:**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file
   echo "SUPABASE_URL=https://your-project.supabase.co" > .env
   echo "SUPABASE_KEY=your-anon-key" >> .env
   ```

5. **Use in Code:**
   ```python
   from db_helper import *
   
   # Check connection
   if is_connected():
       students = get_all_students()
       print(f"Found {len(students)} students")
   ```

### 📋 What Gets Created

✅ 6 Tables:
- `students` - Student profiles
- `student_credits` - Credit balances
- `credit_transactions` - All transfers
- `notifications` - Notification feed
- `endorsements` - Endorsement records
- `voucher_purchases` - Redemption history

✅ Indexes for fast queries
✅ Row Level Security (RLS) policies
✅ Triggers for auto-updates

### 🔗 Real-Time Updates

Supabase supports real-time out of the box! Just use:

```python
from db_helper import subscribe_to_notifications

def on_new_notification(notification):
    st.rerun()  # Refresh Streamlit

# Subscribe
subscribe_to_notifications(student_id, on_new_notification)
```

That's it! Changes in database automatically trigger callbacks.

### 📁 Files You Need

1. **`database_schema.sql`** - Run this in Supabase SQL Editor
2. **`db_helper.py`** - Ready-to-use database functions
3. **`.env`** - Your Supabase credentials (create this)
4. **`requirements.txt`** - Already updated with supabase

### 🚀 Next Steps

1. ✅ Run SQL schema (2 min)
2. ✅ Get API keys (1 min)
3. ✅ Create .env file (1 min)
4. ✅ Test connection (1 min)
5. ⬜ Integrate with app.py (see INTEGRATION_GUIDE.md)

### 💡 Pro Tips

- **Test First**: Use `db_helper.py` functions to test before integrating
- **Hybrid Approach**: Keep session state as fallback if DB fails
- **Real-Time**: Supabase real-time works automatically - just subscribe!

### ❓ Need Help?

- **Setup Issues**: See `QUICK_SETUP.md`
- **Integration**: See `INTEGRATION_GUIDE.md`
- **Database Details**: See `data_model.md`
- **SQL Queries**: See `common_queries.sql`

---

**Total Time: ~5 minutes to get database running!**

