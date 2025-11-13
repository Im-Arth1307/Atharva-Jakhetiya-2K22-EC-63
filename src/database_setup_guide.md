# Supabase Database Setup Guide

## Prerequisites
- A Supabase account (sign up at https://supabase.com)
- A new or existing Supabase project

## Setup Steps

### 1. Create a New Supabase Project
1. Log in to your Supabase dashboard
2. Click "New Project"
3. Fill in project details:
   - Name: `boostly` (or your preferred name)
   - Database Password: (choose a strong password)
   - Region: (select closest to your users)
4. Click "Create new project"
5. Wait for the project to be provisioned (2-3 minutes)

### 2. Access SQL Editor
1. In your Supabase dashboard, navigate to the **SQL Editor** from the left sidebar
2. Click "New Query" to create a new SQL query

### 3. Run the Schema Script
1. Open the `database_schema.sql` file from the `src` folder
2. Copy the entire contents of the file
3. Paste it into the Supabase SQL Editor
4. Click "Run" or press `Ctrl+Enter` (Windows/Linux) or `Cmd+Enter` (Mac)
5. Wait for all commands to execute successfully

### 4. Verify Tables Created
1. Navigate to **Table Editor** in the Supabase dashboard
2. You should see the following tables:
   - `students`
   - `student_credits`
   - `credit_transactions`
   - `notifications`
   - `endorsements`
   - `voucher_purchases`

### 5. Verify Row Level Security
1. Go to **Authentication** → **Policies** in the Supabase dashboard
2. Verify that RLS is enabled on all tables
3. Check that policies are created for each table

### 6. Get Connection Details
1. Go to **Settings** → **API** in your Supabase dashboard
2. Note down:
   - **Project URL**: `https://your-project.supabase.co`
   - **anon/public key**: (for client-side access)
   - **service_role key**: (for server-side access - keep secret!)

## Connecting to the Database

### Using Python (Supabase Client)
```python
from supabase import create_client, Client

url: str = "https://your-project.supabase.co"
key: str = "your-anon-key"
supabase: Client = create_client(url, key)
```

### Using PostgreSQL Connection String
1. Go to **Settings** → **Database**
2. Find the **Connection string** section
3. Copy the connection string (URI format)
4. Use it with any PostgreSQL client or library

## Testing the Setup

### Insert a Test Student
```sql
INSERT INTO students (name, roll_number) 
VALUES ('Test Student', '2K22/EC/99')
RETURNING *;
```

### Check Student Credits
```sql
SELECT s.name, s.roll_number, sc.total_credits, sc.credits_received
FROM students s
LEFT JOIN student_credits sc ON s.id = sc.student_id
WHERE sc.month_year = TO_CHAR(NOW(), 'YYYY-MM');
```

## Important Notes

### Authentication Setup
The schema includes Row Level Security (RLS) policies that reference `auth.uid()`. To use these:

1. **Enable Supabase Auth:**
   - Go to **Authentication** → **Providers**
   - Enable email/password or other providers as needed

2. **Update RLS Policies:**
   - If you're not using Supabase Auth, you'll need to modify the RLS policies
   - Remove or adjust policies that reference `auth.uid()`

### Monthly Credit Reset
To implement automatic monthly credit resets:

1. Create a scheduled function or cron job
2. Run at the start of each month:
   ```sql
   -- Reset credits for new month
   INSERT INTO student_credits (student_id, total_credits, credits_received, credits_sent_this_month, month_year)
   SELECT 
       id,
       LEAST(100 + COALESCE((
           SELECT LEAST(total_credits, 50) 
           FROM student_credits 
           WHERE student_id = s.id 
           AND month_year = TO_CHAR(NOW() - INTERVAL '1 month', 'YYYY-MM')
       ), 0), 150),
       0,
       0,
       TO_CHAR(NOW(), 'YYYY-MM')
   FROM students s
   WHERE NOT EXISTS (
       SELECT 1 FROM student_credits 
       WHERE student_id = s.id 
       AND month_year = TO_CHAR(NOW(), 'YYYY-MM')
   );
   ```

## Troubleshooting

### Error: "relation does not exist"
- Make sure you ran the entire SQL script
- Check that you're connected to the correct database

### Error: "permission denied"
- Check RLS policies
- Verify you're using the correct API keys
- Ensure authentication is properly set up

### Error: "duplicate key value"
- The sample data might already exist
- Remove the sample data section or use `ON CONFLICT DO NOTHING`

## Next Steps

1. **Update Application Code:**
   - Replace hardcoded data with database queries
   - Use Supabase client library to interact with the database
   - Implement proper error handling

2. **Add More Sample Data:**
   - Insert more students
   - Create test transactions
   - Generate test notifications

3. **Set Up Backups:**
   - Configure automatic backups in Supabase dashboard
   - Set up point-in-time recovery if needed

4. **Monitor Performance:**
   - Use Supabase dashboard to monitor query performance
   - Add additional indexes if needed
   - Optimize slow queries

## Support

For issues with:
- **Supabase:** Check [Supabase Documentation](https://supabase.com/docs)
- **SQL Schema:** Review `data_model.md` for detailed table structures
- **Application:** Check the main application code in `app.py`

