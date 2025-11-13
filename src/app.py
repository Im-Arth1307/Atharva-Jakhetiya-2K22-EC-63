import streamlit as st
from datetime import datetime
from typing import List, Dict

# Configure page
st.set_page_config(
    page_title="Boostly - Notifications",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
if 'credits_sent' not in st.session_state:
    st.session_state.credits_sent = 55  # Initial credits sent
if 'total_credits' not in st.session_state:
    st.session_state.total_credits = 150  # Initial total credits
if 'selected_student' not in st.session_state:
    st.session_state.selected_student = None

# Hardcoded student list (excluding current user)
STUDENTS: List[Dict] = [
    {"name": "Sarah Johnson", "roll": "2K22/EC/45"},
    {"name": "Michael Chen", "roll": "2K22/EC/52"},
    {"name": "Emma Wilson", "roll": "2K22/EC/38"},
    {"name": "David Martinez", "roll": "2K22/EC/67"},
    {"name": "Lisa Anderson", "roll": "2K22/EC/29"},
    {"name": "Alex Thompson", "roll": "2K22/EC/71"},
    {"name": "James Brown", "roll": "2K22/EC/56"},
    {"name": "Olivia Davis", "roll": "2K22/EC/42"},
]

# Hardcoded notification data
NOTIFICATIONS: List[Dict] = [
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

def display_student_card(student: Dict, is_selected: bool = False):
    """Display a student card"""
    selected_class = "selected" if is_selected else ""
    st.markdown(f"""
        <div class="student-card {selected_class}">
            <div class="student-name">{student["name"]}</div>
            <div class="student-roll">{student["roll"]}</div>
        </div>
    """, unsafe_allow_html=True)

def send_credits_page():
    """Page for sending credits to students"""
    st.title("📤 Send Credits")
    st.markdown("---")
    
    # Show current balance and limit
    monthly_limit = 100
    remaining_limit = monthly_limit - st.session_state.credits_sent
    available_credits = st.session_state.total_credits
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Credits", f"{available_credits}")
    with col2:
        st.metric("Credits Sent This Month", f"{st.session_state.credits_sent}")
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
        
        with st.form("send_credits_form"):
            credits_to_send = st.number_input(
                "Enter number of credits to send:",
                min_value=1,
                max_value=min(available_credits, remaining_limit),
                value=1,
                step=1,
                key="credits_input"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Send Credits", use_container_width=True)
            with col2:
                cancel_button = st.form_submit_button("Cancel", use_container_width=True)
            
            if cancel_button:
                st.session_state.selected_student = None
                st.rerun()
            
            if submit_button:
                # Validation: Check if credits exceed (100 - credits_sent)
                if credits_to_send > remaining_limit:
                    st.error(f"❌ Error: Monthly sending limit reached! You can only send {remaining_limit} more credits this month (100 - {st.session_state.credits_sent} = {remaining_limit}).")
                elif credits_to_send > available_credits:
                    st.error(f"❌ Error: Insufficient credits! You only have {available_credits} credits available.")
                else:
                    # Deduct credits
                    st.session_state.total_credits -= credits_to_send
                    st.session_state.credits_sent += credits_to_send
                    
                    st.success(f"✅ Successfully sent {credits_to_send} credits to {selected_student_data['name']}!")
                    st.info(f"Your remaining balance: {st.session_state.total_credits} credits")
                    
                    # Reset selection after a short delay
                    st.session_state.selected_student = None
                    st.rerun()
    
    # Back button
    if st.button("← Back to Notifications", use_container_width=True):
        st.session_state.page = 'notifications'
        st.session_state.selected_student = None
        st.rerun()

def notifications_page():
    """Main notifications page"""
    st.title("🎉 Recent Notifications")
    st.markdown("---")
    
    # Display all notifications
    if NOTIFICATIONS:
        for notification in NOTIFICATIONS:
            display_notification(notification)
    else:
        st.info("No notifications to display.")

def main():
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
            st.info("Redeem feature - Clicked!")
            # In a real app, this would open a redemption form
        
        if st.button("👍 Endorse", use_container_width=True):
            st.info("Endorse feature - Clicked!")
            # In a real app, this would show a list of recognitions to endorse
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        st.metric("Total Credits", f"{st.session_state.total_credits}")
        st.metric("Credits Sent", f"{st.session_state.credits_sent}")
        st.metric("Credits Received", "85")
        
        # Days until reset
        days_until_reset = get_days_until_reset()
        st.metric("Days Until Reset", f"{days_until_reset}", 
                  delta=f"{days_until_reset} days remaining" if days_until_reset > 0 else "Reset today!")
    
    # Main content area - route to appropriate page
    if st.session_state.page == 'send_credits':
        send_credits_page()
    else:
        notifications_page()

if __name__ == "__main__":
    main()

