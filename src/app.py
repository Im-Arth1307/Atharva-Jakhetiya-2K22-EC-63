import streamlit as st

# Configure page - MUST be first Streamlit command
st.set_page_config(
    page_title="Boostly - Notifications",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import other modules
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import database helper (after page config)
try:
    from db_helper import *
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    st.warning("⚠️ Database helper not available. Using session state only.")

# Custom CSS for pastel colors
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .notification-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid;
    }
    .notification-credits-sent {
        border-left-color: #ffb3ba;
        background: linear-gradient(90deg, #fff5f5 0%, #ffffff 100%);
    }
    .notification-credits-received {
        border-left-color: #bae1ff;
        background: linear-gradient(90deg, #f0f8ff 0%, #ffffff 100%);
    }
    .notification-endorsement-received {
        border-left-color: #c7ceea;
        background: linear-gradient(90deg, #f5f6fa 0%, #ffffff 100%);
    }
    .notification-endorsement-given {
        border-left-color: #ffdfba;
        background: linear-gradient(90deg, #fff8f0 0%, #ffffff 100%);
    }
    .notification-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .notification-message {
        color: #5a6c7d;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .notification-time {
        color: #95a5a6;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #e8f4f8;
        color: #2c3e50;
        border: 2px solid #b8d4e3;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #d4e8f0;
        border-color: #9bc4d4;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #fafbfc;
    }
    h1 {
        color: #2c3e50;
    }
    .user-profile {
        display: flex;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e8f4f8;
    }
    .user-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #bae1ff 0%, #ffb3ba 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-right: 1rem;
        flex-shrink: 0;
    }
    .user-info {
        flex: 1;
    }
    .user-name {
        font-size: 1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.25rem;
    }
    .user-roll {
        font-size: 0.85rem;
        color: #5a6c7d;
    }
    .student-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #bae1ff;
        background: linear-gradient(90deg, #f0f8ff 0%, #ffffff 100%);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .student-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .student-card.selected {
        border-left-color: #ffb3ba;
        background: linear-gradient(90deg, #fff5f5 0%, #ffffff 100%);
    }
    .student-card.endorsed {
        border-left-color: #c7ceea;
        background: linear-gradient(90deg, #f5f6fa 0%, #ffffff 100%);
        opacity: 0.7;
    }
    .student-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .student-roll {
        color: #5a6c7d;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'notifications'
if 'selected_student' not in st.session_state:
    st.session_state.selected_student = None
if 'form_error' not in st.session_state:
    st.session_state.form_error = None
if 'last_credits_input' not in st.session_state:
    st.session_state.last_credits_input = 1
if 'last_message_input' not in st.session_state:
    st.session_state.last_message_input = ""
if 'endorsed_students' not in st.session_state:
    st.session_state.endorsed_students = []  # Track which students have been endorsed (list of student IDs)
if 'endorsements_received' not in st.session_state:
    st.session_state.endorsements_received = 0  # Initial endorsements received
if 'credits_received' not in st.session_state:
    st.session_state.credits_received = 85  # Credits received (can be redeemed)
if 'total_credits' not in st.session_state:
    st.session_state.total_credits = 150  # Total credits
if 'credits_sent' not in st.session_state:
    st.session_state.credits_sent = 0  # Credits sent this month
if 'current_student_id' not in st.session_state:
    st.session_state.current_student_id = None  # Current logged-in student ID
if 'current_student_roll' not in st.session_state:
    st.session_state.current_student_roll = "2K22/EC/63"  # Default current user

# Load students from database or use hardcoded fallback
@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_students() -> List[Dict]:
    """Get students from database or fallback to hardcoded"""
    if DB_AVAILABLE and is_connected():
        try:
            students_data = get_all_students()
            if students_data and len(students_data) > 0:
                # Filter out current user
                current_roll = st.session_state.current_student_roll
                students = [
                    {"id": str(s['id']), "name": s['name'], "roll": s['roll_number']}
                    for s in students_data if s['roll_number'] != current_roll
                ]
                if students:
                    return students
        except Exception as e:
            st.error(f"Error loading students: {e}")
    
    # Fallback to hardcoded (without IDs - will use session state only)
    return [
        {"id": None, "name": "Sarah Johnson", "roll": "2K22/EC/45"},
        {"id": None, "name": "Michael Chen", "roll": "2K22/EC/52"},
        {"id": None, "name": "Emma Wilson", "roll": "2K22/EC/38"},
        {"id": None, "name": "David Martinez", "roll": "2K22/EC/67"},
        {"id": None, "name": "Lisa Anderson", "roll": "2K22/EC/29"},
        {"id": None, "name": "Alex Thompson", "roll": "2K22/EC/71"},
        {"id": None, "name": "James Brown", "roll": "2K22/EC/56"},
        {"id": None, "name": "Olivia Davis", "roll": "2K22/EC/42"},
    ]

# Load students (will be cached)
STUDENTS = get_students()

# Get or create current student in database
def get_current_student_id() -> Optional[str]:
    """Get current student ID from database"""
    if not (DB_AVAILABLE and is_connected()):
        return None
    
    if st.session_state.current_student_id:
        return st.session_state.current_student_id
    
    try:
        current_roll = st.session_state.current_student_roll
        student = get_student_by_roll(current_roll)
        if student:
            student_id = str(student['id'])  # Ensure string format
            st.session_state.current_student_id = student_id
            return student_id
        else:
            # Create student if doesn't exist
            try:
                from supabase import create_client
                # Try to get from config first, then env
                try:
                    from config import SUPABASE_URL, SUPABASE_KEY
                except ImportError:
                    SUPABASE_URL = os.getenv("SUPABASE_URL")
                    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
                
                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                result = supabase.table('students').insert({
                    'name': 'Student Name',
                    'roll_number': current_roll
                }).execute()
                if result.data:
                    student_id = str(result.data[0]['id'])  # Ensure string format
                    st.session_state.current_student_id = student_id
                    # Initialize credits
                    month_year = datetime.now().strftime('%Y-%m')
                    supabase.table('student_credits').insert({
                        'student_id': student_id,
                        'total_credits': 150,
                        'credits_received': 85,
                        'credits_sent_this_month': 55,
                        'monthly_limit': 100,
                        'month_year': month_year
                    }).execute()
                    return student_id
            except Exception as e:
                st.error(f"Error creating student: {e}")
    except Exception as e:
        st.error(f"Error getting student: {e}")
    
    return None

# Load notifications from database or use hardcoded fallback
def get_notifications_data() -> List[Dict]:
    """Get notifications from database or fallback to hardcoded"""
    current_student_id = get_current_student_id()
    
    if DB_AVAILABLE and is_connected() and current_student_id:
        try:
            notifications_data = get_notifications(current_student_id, limit=50)
            if notifications_data:
                return [
                    {
                        "type": n['notification_type'],
                        "title": n['title'],
                        "message": n['message'],
                        "timestamp": n['created_at'],
                        "details": n.get('details', '')
                    }
                    for n in notifications_data
                ]
        except Exception as e:
            st.error(f"Error loading notifications: {e}")
    
    # Fallback to hardcoded
    return [
    {
        "type": "credits_sent",
        "title": "Credits Sent",
        "message": "You sent 25 credits to Sarah Johnson",
        "timestamp": "2024-01-15 14:30:00",
        "details": "Recognition for helping with the group project"
    },
    {
        "type": "credits_received",
        "title": "Credits Received",
        "message": "You received 30 credits from Michael Chen",
        "timestamp": "2024-01-15 13:15:00",
        "details": "For your excellent presentation skills"
    },
    {
        "type": "endorsement_received",
        "title": "Endorsement Received",
        "message": "Your recognition received 5 endorsements",
        "timestamp": "2024-01-15 12:00:00",
        "details": "Emma, David, Lisa, James, and Alex endorsed your recognition of Sarah"
    },
    {
        "type": "endorsement_given",
        "title": "Endorsement Given",
        "message": "You endorsed Michael's recognition of Lisa",
        "timestamp": "2024-01-15 11:45:00",
        "details": "Supporting recognition for teamwork"
    },
    {
        "type": "credits_received",
        "title": "Credits Received",
        "message": "You received 15 credits from Emma Wilson",
        "timestamp": "2024-01-15 10:20:00",
        "details": "For organizing the study group"
    },
    {
        "type": "credits_sent",
        "title": "Credits Sent",
        "message": "You sent 20 credits to David Martinez",
        "timestamp": "2024-01-14 16:45:00",
        "details": "Recognition for coding assistance"
    },
    {
        "type": "endorsement_received",
        "title": "Endorsement Received",
        "message": "Your recognition received 3 endorsements",
        "timestamp": "2024-01-14 15:30:00",
        "details": "Sarah, Michael, and Emma endorsed your recognition of David"
    },
    {
        "type": "endorsement_given",
        "title": "Endorsement Given",
        "message": "You endorsed Sarah's recognition of James",
        "timestamp": "2024-01-14 14:10:00",
        "details": "Supporting recognition for leadership"
    },
    {
        "type": "credits_sent",
        "title": "Credits Sent",
        "message": "You sent 10 credits to Lisa Anderson",
        "timestamp": "2024-01-14 13:00:00",
        "details": "Recognition for peer review feedback"
    },
    {
        "type": "credits_received",
        "title": "Credits Received",
        "message": "You received 40 credits from Alex Thompson",
        "timestamp": "2024-01-14 11:30:00",
        "details": "For mentoring in data structures"
    }
]

def get_notification_class(notification_type: str) -> str:
    """Get CSS class based on notification type"""
    class_mapping = {
        "credits_sent": "notification-credits-sent",
        "credits_received": "notification-credits-received",
        "endorsement_received": "notification-endorsement-received",
        "endorsement_given": "notification-endorsement-given"
    }
    return class_mapping.get(notification_type, "notification-card")

def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - dt
        
        if diff.days == 0:
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} minutes ago" if minutes > 0 else "Just now"
            else:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        else:
            return dt.strftime("%B %d, %Y")
    except:
        return timestamp_str

def get_days_until_reset() -> int:
    """Calculate days until the next month's credit reset (first day of next month)"""
    now = datetime.now()
    # Get first day of next month
    if now.month == 12:
        next_month = datetime(now.year + 1, 1, 1)
    else:
        next_month = datetime(now.year, now.month + 1, 1)
    
    # Calculate difference
    days_until = (next_month - now).days
    return days_until

def display_notification(notification: Dict):
    """Display a single notification card"""
    css_class = get_notification_class(notification["type"])
    
    st.markdown(f"""
        <div class="notification-card {css_class}">
            <div class="notification-title">{notification["title"]}</div>
            <div class="notification-message">{notification["message"]}</div>
            <div class="notification-message" style="font-style: italic; margin-top: 0.5rem;">
                {notification["details"]}
            </div>
            <div class="notification-time">{format_timestamp(notification["timestamp"])}</div>
        </div>
    """, unsafe_allow_html=True)

def display_student_card(student: Dict, is_selected: bool = False, is_endorsed: bool = False):
    """Display a student card"""
    classes = []
    if is_selected:
        classes.append("selected")
    if is_endorsed:
        classes.append("endorsed")
    class_str = " ".join(classes) if classes else ""
    st.markdown(f"""
        <div class="student-card {class_str}">
            <div class="student-name">{student["name"]}</div>
            <div class="student-roll">{student["roll"]}</div>
        </div>
    """, unsafe_allow_html=True)

def send_credits_page():
    """Page for sending credits to students"""
    st.title("📤 Send Credits")
    st.markdown("---")
    
    # Get stats from database
    stats = get_student_stats_from_db()
    monthly_limit = 100
    credits_sent = stats['credits_sent']
    remaining_limit = monthly_limit - credits_sent
    available_credits = stats['total_credits']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Credits", f"{available_credits}")
    with col2:
        st.metric("Credits Sent This Month", f"{credits_sent}")
    with col3:
        st.metric("Remaining Limit", f"{remaining_limit}")
    
    st.markdown("---")
    
    # Display students in a grid
    st.markdown("### Select a Student")
    
    # Create columns for student cards
    cols = st.columns(2)
    
    for idx, student in enumerate(STUDENTS):
        col_idx = idx % 2
        with cols[col_idx]:
            is_selected = (st.session_state.selected_student == idx)
            display_student_card(student, is_selected)
            
            # Button to select student
            if st.button(f"Select {student['name']}", key=f"select_{idx}", use_container_width=True):
                st.session_state.selected_student = idx
                st.rerun()
    
    st.markdown("---")
    
    # Credit input form
    if st.session_state.selected_student is not None:
        selected_student_data = STUDENTS[st.session_state.selected_student]
        st.markdown(f"### Send Credits to {selected_student_data['name']}")
        
        # Display error message if there was a validation error
        if st.session_state.form_error:
            st.error(st.session_state.form_error)
            st.session_state.form_error = None  # Clear error after displaying
        
        with st.form("send_credits_form", clear_on_submit=False):
            # Calculate max credits that can be sent
            max_credits = min(available_credits, remaining_limit) if remaining_limit > 0 else 0
            if max_credits <= 0:
                max_credits = 100  # Default max for input field
            
            # Use session state to preserve value on error
            default_credits = st.session_state.last_credits_input if 'last_credits_input' in st.session_state else 1
            credits_to_send = st.number_input(
                "Enter number of credits to send:",
                min_value=0,
                max_value=max_credits,
                value=default_credits,
                step=1,
                key="credits_input"
            )
            
            # Use session state to preserve message on error
            default_message = st.session_state.last_message_input if 'last_message_input' in st.session_state else ""
            message = st.text_area(
                "Message (optional):",
                placeholder="Add a message to send along with the credits...",
                value=default_message,
                key="message_input",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Send Credits", use_container_width=True)
            with col2:
                cancel_button = st.form_submit_button("Cancel", use_container_width=True)
            
            if cancel_button:
                st.session_state.selected_student = None
                st.session_state.form_error = None
                st.session_state.last_credits_input = 1
                st.session_state.last_message_input = ""
                st.rerun()
            
            if submit_button:
                # Save input values to session state
                st.session_state.last_credits_input = credits_to_send
                st.session_state.last_message_input = message
                
                # Validation: Check if credits are valid
                if credits_to_send <= 0:
                    st.session_state.form_error = f"❌ Error: Number of credits must be greater than 0."
                    st.rerun()
                elif credits_to_send > remaining_limit:
                    st.session_state.form_error = f"❌ Error: Monthly sending limit reached! You can only send {remaining_limit} more credits this month (100 - {credits_sent} = {remaining_limit})."
                    st.rerun()
                elif credits_to_send > available_credits:
                    st.session_state.form_error = f"❌ Error: Insufficient credits! You only have {available_credits} credits available."
                    st.rerun()
                else:
                    # Send credits using database or session state
                    current_student_id = get_current_student_id()
                    receiver_id = selected_student_data.get('id')
                    
                    if DB_AVAILABLE and is_connected() and current_student_id and receiver_id:
                        # Use database
                        result = send_credits(current_student_id, receiver_id, credits_to_send, message)
                        if result:
                            st.success(f"✅ Successfully sent {credits_to_send} credits to {selected_student_data['name']}!")
                            if message and message.strip():
                                st.info(f"Message: {message.strip()}")
                            # Refresh stats after sending
                            st.rerun()
                        else:
                            st.error("❌ Failed to send credits. Please try again.")
                    else:
                        # Fallback to session state
                        st.session_state.total_credits -= credits_to_send
                        st.session_state.credits_sent += credits_to_send
                        st.success(f"✅ Successfully sent {credits_to_send} credits to {selected_student_data['name']}!")
                        if message and message.strip():
                            st.info(f"Message: {message.strip()}")
                    
                    # Reset selection and form state after successful send
                    st.session_state.selected_student = None
                    st.session_state.form_error = None
                    st.session_state.last_credits_input = 1
                    st.session_state.last_message_input = ""
                    st.rerun()
    
    # Back button
    if st.button("← Back to Notifications", use_container_width=True):
        st.session_state.page = 'notifications'
        st.session_state.selected_student = None
        st.rerun()

def endorse_page():
    """Page for endorsing students"""
    st.title("👍 Endorse Students")
    st.markdown("---")
    
    st.info("💡 Endorse students to recognize their contributions. You can endorse each student only once.")
    
    st.markdown("---")
    
    # Display students in a grid
    st.markdown("### Select a Student to Endorse")
    
    # Create columns for student cards
    cols = st.columns(2)
    
    for idx, student in enumerate(STUDENTS):
        col_idx = idx % 2
        with cols[col_idx]:
            student_id = f"{student['name']}_{student['roll']}"
            # Check if endorsed (database or session state)
            current_student_id = get_current_student_id()
            endorsee_id = student.get('id')
            
            if DB_AVAILABLE and is_connected() and current_student_id and endorsee_id:
                is_endorsed = check_endorsement_exists(current_student_id, endorsee_id)
            else:
                is_endorsed = student_id in st.session_state.endorsed_students
            
            display_student_card(student, is_selected=False, is_endorsed=is_endorsed)
            
            # Button to endorse student
            if is_endorsed:
                st.button(
                    f"✓ Already Endorsed",
                    key=f"endorse_{idx}",
                    use_container_width=True,
                    disabled=True
                )
            else:
                if st.button(f"👍 Endorse {student['name']}", key=f"endorse_{idx}", use_container_width=True):
                    # Endorse using database or session state
                    current_student_id = get_current_student_id()
                    endorsee_id = student.get('id')
                    
                    if DB_AVAILABLE and is_connected() and current_student_id and endorsee_id:
                        # Check if already endorsed in database
                        if not check_endorsement_exists(current_student_id, endorsee_id):
                            result = create_endorsement(current_student_id, endorsee_id)
                            if result:
                                st.success(f"✅ Successfully endorsed {student['name']}!")
                                # Also add to session state for UI
                                if student_id not in st.session_state.endorsed_students:
                                    st.session_state.endorsed_students.append(student_id)
                                st.rerun()
                            else:
                                st.error("❌ Failed to create endorsement. Please try again.")
                        else:
                            st.warning("Already endorsed!")
                            if student_id not in st.session_state.endorsed_students:
                                st.session_state.endorsed_students.append(student_id)
                            st.rerun()
                    else:
                        # Fallback to session state
                        if student_id not in st.session_state.endorsed_students:
                            st.session_state.endorsed_students.append(student_id)
                        st.success(f"✅ Successfully endorsed {student['name']}!")
                        st.rerun()
    
    st.markdown("---")
    
    # Show endorsement stats
    st.markdown("### Your Endorsements")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Students Endorsed", f"{len(st.session_state.endorsed_students)}")
    with col2:
        # Get endorsements from database or session state
        current_student_id = get_current_student_id()
        if DB_AVAILABLE and is_connected() and current_student_id:
            try:
                endorsements_count = get_endorsements_received(current_student_id)
                st.metric("Endorsements Received", f"{endorsements_count}")
            except:
                st.metric("Endorsements Received", f"{st.session_state.endorsements_received}")
        else:
            st.metric("Endorsements Received", f"{st.session_state.endorsements_received}")
    
    # Back button
    if st.button("← Back to Notifications", use_container_width=True):
        st.session_state.page = 'notifications'
        st.rerun()

def redeem_page():
    """Page for redeeming credits into vouchers"""
    st.title("💰 Redeem Credits")
    st.markdown("---")
    
    # Voucher conversion rate
    VOUCHER_RATE = 5  # ₹5 per credit
    
    # Get stats from database or session state
    stats = get_student_stats_from_db()
    available_for_redemption = stats.get('credits_received', st.session_state.credits_received)
    total_credits = stats.get('total_credits', st.session_state.total_credits)
    
    # Info section
    st.info(f"💡 **Redeem your received credits into vouchers!** Each credit is worth ₹{VOUCHER_RATE}. You can only redeem credits you have received.")
    
    st.markdown("---")
    
    # Display current balance
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Credits", f"{total_credits}")
    with col2:
        st.metric("Credits Received", f"{available_for_redemption}")
    with col3:
        max_voucher_value = available_for_redemption * VOUCHER_RATE
        st.metric("Max Voucher Value", f"₹{max_voucher_value}")
    
    st.markdown("---")
    
    # Redemption form
    st.markdown("### Purchase Vouchers")
    
    with st.form("redeem_form", clear_on_submit=False):
        # Number of vouchers to purchase
        num_vouchers = st.number_input(
            "Number of vouchers to purchase:",
            min_value=1,
            max_value=100,
            value=1,
            step=1,
            key="num_vouchers_input",
            help="You can purchase multiple vouchers at once"
        )
        
        # Credits per voucher
        credits_per_voucher = st.number_input(
            "Credits per voucher:",
            min_value=1,
            max_value=available_for_redemption,
            value=1,
            step=1,
            key="credits_per_voucher_input",
            help=f"Maximum: {available_for_redemption} credits (your received credits)"
        )
        
        # Calculate total credits needed and voucher value
        total_credits_needed = num_vouchers * credits_per_voucher
        total_voucher_value = total_credits_needed * VOUCHER_RATE
        
        # Display calculation
        st.markdown("---")
        st.markdown("### Purchase Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Credits Needed", f"{total_credits_needed}")
        with col2:
            st.metric("Total Voucher Value", f"₹{total_voucher_value}")
        with col3:
            st.metric("Vouchers", f"{num_vouchers}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Purchase Vouchers", use_container_width=True)
        with col2:
            cancel_button = st.form_submit_button("Cancel", use_container_width=True)
        
        if cancel_button:
            st.rerun()
        
        if submit_button:
            # Validation
            if credits_per_voucher <= 0:
                st.error("❌ Error: Credits per voucher must be greater than 0.")
            elif num_vouchers <= 0:
                st.error("❌ Error: Number of vouchers must be greater than 0.")
            elif total_credits_needed > available_for_redemption:
                st.error(f"❌ Error: Insufficient received credits! You can only redeem {available_for_redemption} credits (credits you have received). You tried to redeem {total_credits_needed} credits.")
            elif total_credits_needed > total_credits:
                st.error(f"❌ Error: Insufficient total credits! You only have {total_credits} credits available.")
            else:
                # Process redemption
                # Deduct from both total credits and received credits
                st.session_state.total_credits -= total_credits_needed
                st.session_state.credits_received -= total_credits_needed
                
                # Record voucher purchase
                voucher_info = {
                    "num_vouchers": num_vouchers,
                    "credits_per_voucher": credits_per_voucher,
                    "total_credits": total_credits_needed,
                    "total_value": total_voucher_value,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.vouchers_purchased.append(voucher_info)
                
                # Success message
                if num_vouchers == 1:
                    st.success(f"✅ Successfully purchased {num_vouchers} voucher worth ₹{total_voucher_value}!")
                else:
                    st.success(f"✅ Successfully purchased {num_vouchers} vouchers worth ₹{total_voucher_value} total!")
                
                st.info(f"Your remaining balance: {st.session_state.total_credits} credits ({st.session_state.credits_received} received credits available for redemption)")
                st.rerun()
    
    st.markdown("---")
    
    # Display purchase history
    if st.session_state.vouchers_purchased:
        st.markdown("### Recent Voucher Purchases")
        for idx, voucher in enumerate(reversed(st.session_state.vouchers_purchased[-5:])):  # Show last 5
            with st.expander(f"Voucher Purchase #{len(st.session_state.vouchers_purchased) - idx} - {voucher['timestamp']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Vouchers", f"{voucher['num_vouchers']}")
                with col2:
                    st.metric("Credits Used", f"{voucher['total_credits']}")
                with col3:
                    st.metric("Total Value", f"₹{voucher['total_value']}")
    
    # Back button
    if st.button("← Back to Notifications", use_container_width=True):
        st.session_state.page = 'notifications'
        st.rerun()

def notifications_page():
    """Main notifications page"""
    st.title("🎉 Recent Notifications")
    st.markdown("---")
    
    # Load notifications (from database or fallback)
    notifications = get_notifications_data()
    
    # Display all notifications
    if notifications:
        for notification in notifications:
            display_notification(notification)
    else:
        st.info("No notifications to display.")

def get_student_stats_from_db():
    """Get student stats from database or return defaults"""
    current_student_id = get_current_student_id()
    
    if DB_AVAILABLE and is_connected() and current_student_id:
        try:
            stats = get_student_stats(current_student_id)
            if stats:
                return {
                    'total_credits': stats.get('total_credits', 150),
                    'credits_sent': stats.get('credits_sent_this_month', 0),
                    'credits_received': stats.get('credits_received', 85),
                    'endorsements_received': stats.get('endorsements_received', 0)
                }
        except Exception as e:
            st.error(f"Error loading stats: {e}")
    
    # Fallback to session state or defaults
    return {
        'total_credits': getattr(st.session_state, 'total_credits', 150),
        'credits_sent': getattr(st.session_state, 'credits_sent', 55),
        'credits_received': getattr(st.session_state, 'credits_received', 85),
        'endorsements_received': getattr(st.session_state, 'endorsements_received', 12)
    }

def main():
    # Check database connection status
    if DB_AVAILABLE and is_connected():
        st.sidebar.success("✅ Connected to database")
    elif DB_AVAILABLE:
        st.sidebar.warning("⚠️ Database not connected - check config.py")
    
    # Sidebar
    with st.sidebar:
        # User Profile Section
        st.markdown("""
            <div class="user-profile">
                <div class="user-avatar">👤</div>
                <div class="user-info">
                    <div class="user-name">Student Name</div>
                    <div class="user-roll">2K22/EC/63</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("## 🎯 Actions")
        st.markdown("---")
        
        if st.button("📤 Send Credits", use_container_width=True):
            st.session_state.page = 'send_credits'
            st.rerun()
        
        if st.button("💰 Redeem", use_container_width=True):
            st.session_state.page = 'redeem'
            st.rerun()
        
        if st.button("👍 Endorse", use_container_width=True):
            st.session_state.page = 'endorse'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        
        # Load stats from database
        stats = get_student_stats_from_db()
        st.metric("Total Credits", f"{stats['total_credits']}")
        st.metric("Credits Sent", f"{stats['credits_sent']}")
        st.metric("Credits Received", f"{stats['credits_received']}")
        st.metric("Endorsements Received", f"{stats['endorsements_received']}")
        
        # Days until reset
        days_until_reset = get_days_until_reset()
        st.metric("Days Until Reset", f"{days_until_reset}", 
                  delta=f"{days_until_reset} days remaining" if days_until_reset > 0 else "Reset today!")
        
        # Refresh button for database updates
        if DB_AVAILABLE and is_connected():
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
    
    # Main content area - route to appropriate page
    if st.session_state.page == 'send_credits':
        send_credits_page()
    elif st.session_state.page == 'endorse':
        endorse_page()
    elif st.session_state.page == 'redeem':
        redeem_page()
    else:
        notifications_page()

if __name__ == "__main__":
    main()

