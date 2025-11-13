"""
Script to populate Supabase with students and ensure proper setup
Run this once to set up your students in the database
"""

import os
from datetime import datetime
from supabase import create_client

# Import config
try:
    from config import SUPABASE_URL, SUPABASE_KEY
except ImportError:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_KEY must be set in config.py or .env")
    exit(1)

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Sample students data
STUDENTS_DATA = [
    {"name": "Student Name", "roll_number": "2K22/EC/63", "email": "student@example.com"},
    {"name": "Sarah Johnson", "roll_number": "2K22/EC/45", "email": "sarah@example.com"},
    {"name": "Michael Chen", "roll_number": "2K22/EC/52", "email": "michael@example.com"},
    {"name": "Emma Wilson", "roll_number": "2K22/EC/38", "email": "emma@example.com"},
    {"name": "David Martinez", "roll_number": "2K22/EC/67", "email": "david@example.com"},
    {"name": "Lisa Anderson", "roll_number": "2K22/EC/29", "email": "lisa@example.com"},
    {"name": "Alex Thompson", "roll_number": "2K22/EC/71", "email": "alex@example.com"},
    {"name": "James Brown", "roll_number": "2K22/EC/56", "email": "james@example.com"},
    {"name": "Olivia Davis", "roll_number": "2K22/EC/42", "email": "olivia@example.com"},
]

def setup_students():
    """Insert or update students in the database"""
    print("🔄 Setting up students in Supabase...")
    print(f"📊 Found {len(STUDENTS_DATA)} students to process\n")
    
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    for student_data in STUDENTS_DATA:
        roll_number = student_data['roll_number']
        
        try:
            # Check if student exists
            existing = supabase.table('students')\
                .select('id, name, roll_number')\
                .eq('roll_number', roll_number)\
                .execute()
            
            if existing.data:
                # Student exists, update if needed
                student_id = existing.data[0]['id']
                supabase.table('students')\
                    .update({
                        'name': student_data['name'],
                        'email': student_data.get('email')
                    })\
                    .eq('id', student_id)\
                    .execute()
                print(f"✅ Updated: {student_data['name']} ({roll_number})")
                updated_count += 1
            else:
                # Create new student
                result = supabase.table('students')\
                    .insert(student_data)\
                    .execute()
                
                if result.data:
                    student_id = result.data[0]['id']
                    print(f"➕ Created: {student_data['name']} ({roll_number}) - ID: {student_id}")
                    created_count += 1
                    
                    # Initialize credits for new student
                    month_year = datetime.now().strftime('%Y-%m')
                    credits_data = {
                        'student_id': student_id,
                        'total_credits': 100,
                        'credits_received': 0,
                        'credits_sent_this_month': 0,
                        'monthly_limit': 100,
                        'month_year': month_year
                    }
                    
                    # Check if credits already exist
                    existing_credits = supabase.table('student_credits')\
                        .select('id')\
                        .eq('student_id', student_id)\
                        .eq('month_year', month_year)\
                        .execute()
                    
                    if not existing_credits.data:
                        supabase.table('student_credits')\
                            .insert(credits_data)\
                            .execute()
                        print(f"   💰 Initialized credits for {student_data['name']}")
                else:
                    print(f"❌ Failed to create: {student_data['name']}")
                    skipped_count += 1
                    
        except Exception as e:
            print(f"❌ Error processing {student_data['name']}: {e}")
            skipped_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   ➕ Created: {created_count}")
    print(f"   ✅ Updated: {updated_count}")
    print(f"   ⚠️  Skipped: {skipped_count}")
    print(f"   📝 Total: {len(STUDENTS_DATA)}")

def initialize_current_student_credits():
    """Initialize credits for current student (2K22/EC/63) with sample data"""
    print("\n🔄 Initializing credits for current student...")
    
    try:
        # Get current student
        result = supabase.table('students')\
            .select('id')\
            .eq('roll_number', '2K22/EC/63')\
            .single()\
            .execute()
        
        if result.data:
            student_id = result.data[0]['id']
            month_year = datetime.now().strftime('%Y-%m')
            
            # Update or create credits with initial values
            credits_data = {
                'total_credits': 150,
                'credits_received': 85,
                'credits_sent_this_month': 55,
                'monthly_limit': 100,
                'month_year': month_year
            }
            
            # Check if exists
            existing = supabase.table('student_credits')\
                .select('id')\
                .eq('student_id', student_id)\
                .eq('month_year', month_year)\
                .execute()
            
            if existing.data:
                supabase.table('student_credits')\
                    .update(credits_data)\
                    .eq('id', existing.data[0]['id'])\
                    .execute()
                print("✅ Updated credits for current student")
            else:
                credits_data['student_id'] = student_id
                supabase.table('student_credits')\
                    .insert(credits_data)\
                    .execute()
                print("✅ Created credits for current student")
        else:
            print("⚠️  Current student not found")
    except Exception as e:
        print(f"❌ Error: {e}")

def verify_setup():
    """Verify the setup by listing all students"""
    print("\n🔍 Verifying setup...\n")
    
    try:
        result = supabase.table('students')\
            .select('id, name, roll_number')\
            .order('name')\
            .execute()
        
        if result.data:
            print(f"✅ Found {len(result.data)} students in database:\n")
            for student in result.data:
                print(f"   • {student['name']} ({student['roll_number']}) - ID: {student['id']}")
        else:
            print("⚠️  No students found in database")
    except Exception as e:
        print(f"❌ Error verifying: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Boostly Student Setup Script")
    print("=" * 60)
    print()
    
    # Test connection
    try:
        result = supabase.table('students').select('id').limit(1).execute()
        print("✅ Connected to Supabase\n")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        print("\nPlease check:")
        print("   1. config.py has correct SUPABASE_URL and SUPABASE_KEY")
        print("   2. Supabase project is active")
        print("   3. Database schema has been run")
        exit(1)
    
    # Setup students
    setup_students()
    
    # Initialize current student credits
    initialize_current_student_credits()
    
    # Verify
    verify_setup()
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print("\nYou can now run your Streamlit app:")
    print("   streamlit run app.py")

