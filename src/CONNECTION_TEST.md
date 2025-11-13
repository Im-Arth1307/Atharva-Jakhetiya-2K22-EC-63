# Database Connection Test

## Quick Test

Run this to test your database connection:

```bash
cd src
python -c "from db_helper import is_connected; print('Connected!' if is_connected() else 'Not connected')"
```

## Expected Output

If connected: `Connected!`
If not: `Not connected`

## Troubleshooting

### "Module not found: supabase"
```bash
pip install supabase python-dotenv
```

### "Not connected"
1. Check `config.py` has correct URL and KEY
2. Verify Supabase project is active
3. Check internet connection

### "Permission denied"
- RLS policies might be blocking
- Check Supabase dashboard → Authentication → Policies

## Next Steps

Once connected:
1. Run `streamlit run app.py`
2. Check sidebar for "✅ Connected to database"
3. Test sending credits, endorsements, etc.

