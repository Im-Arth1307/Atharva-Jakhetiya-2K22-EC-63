"""
Example: Real-Time Updates in Streamlit with Supabase

This shows how to implement real-time database updates in your Streamlit app.
"""

import streamlit as st
from dotenv import load_dotenv
from db_helper import *
import time

load_dotenv()

st.set_page_config(page_title="Real-Time Example", layout="wide")

st.title("🔥 Real-Time Database Updates")

# Check connection
if not is_connected():
    st.error("⚠️ Database not connected. Set up SUPABASE_URL and SUPABASE_KEY in .env file")
    st.stop()

# Get current student (in real app, this would come from login)
CURRENT_STUDENT_ID = "your-student-id-here"  # Replace with actual ID

# =====================================================
# Method 1: Auto-Refresh (Simplest)
# =====================================================

st.header("Method 1: Auto-Refresh")

if st.checkbox("Enable auto-refresh", value=False):
    auto_refresh = st.number_input("Refresh interval (seconds)", min_value=1, value=5)
    
    # Get latest data
    notifications = get_notifications(CURRENT_STUDENT_ID, limit=5)
    stats = get_student_stats(CURRENT_STUDENT_ID)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Credits", stats.get('total_credits', 0))
        st.metric("Notifications", len(notifications))
    
    with col2:
        st.metric("Credits Received", stats.get('credits_received', 0))
        st.metric("Endorsements", stats.get('endorsements_received', 0))
    
    # Auto-refresh
    time.sleep(auto_refresh)
    st.rerun()

# =====================================================
# Method 2: Manual Refresh Button
# =====================================================

st.header("Method 2: Manual Refresh")

col1, col2 = st.columns([3, 1])
with col1:
    st.write("Click refresh to get latest data")
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

# Display data
notifications = get_notifications(CURRENT_STUDENT_ID, limit=10)
stats = get_student_stats(CURRENT_STUDENT_ID)

st.subheader("Recent Notifications")
for notif in notifications:
    with st.expander(f"{notif['title']} - {notif['created_at']}"):
        st.write(notif['message'])
        if notif.get('details'):
            st.caption(notif['details'])

# =====================================================
# Method 3: Real-Time Subscriptions (Advanced)
# =====================================================

st.header("Method 3: Real-Time Subscriptions")

st.info("""
Real-time subscriptions automatically update when data changes in the database.
This is the most efficient method for live updates.
""")

if st.button("Start Real-Time Subscription"):
    st.session_state['realtime_enabled'] = True

if st.session_state.get('realtime_enabled'):
    st.success("✅ Real-time subscription active")
    
    # Set up subscription
    def on_new_notification(notification):
        st.session_state['new_notification'] = notification
        st.rerun()
    
    def on_credit_update(credits):
        st.session_state['credit_updated'] = True
        st.rerun()
    
    # Subscribe (in real app, do this once at startup)
    if 'subscribed' not in st.session_state:
        subscribe_to_notifications(CURRENT_STUDENT_ID, on_new_notification)
        subscribe_to_credits(CURRENT_STUDENT_ID, on_credit_update)
        st.session_state['subscribed'] = True
    
    # Show notification if new one arrived
    if 'new_notification' in st.session_state:
        notif = st.session_state['new_notification']
        st.success(f"🔔 New: {notif['title']} - {notif['message']}")
        del st.session_state['new_notification']
    
    if 'credit_updated' in st.session_state:
        st.info("💰 Credit balance updated!")
        del st.session_state['credit_updated']

# =====================================================
# Method 4: Polling with Streamlit (Recommended)
# =====================================================

st.header("Method 4: Polling (Recommended for Streamlit)")

st.info("""
Streamlit works best with polling - check for updates periodically.
This is simpler than real-time subscriptions and works reliably.
""")

# Store last check time
if 'last_check' not in st.session_state:
    st.session_state['last_check'] = time.time()

# Check for updates every 5 seconds
if time.time() - st.session_state['last_check'] > 5:
    # Get latest notification count
    latest_notifications = get_notifications(CURRENT_STUDENT_ID, limit=1)
    latest_count = len(latest_notifications)
    
    if 'notification_count' not in st.session_state:
        st.session_state['notification_count'] = latest_count
    
    # If count changed, refresh
    if latest_count > st.session_state['notification_count']:
        st.session_state['notification_count'] = latest_count
        st.session_state['last_check'] = time.time()
        st.rerun()
    
    st.session_state['last_check'] = time.time()

# Display current state
st.write("**Current Status:**")
st.json({
    "Notifications": len(get_notifications(CURRENT_STUDENT_ID)),
    "Last Check": time.strftime("%H:%M:%S", time.localtime(st.session_state['last_check']))
})

# =====================================================
# Example: Live Credit Balance
# =====================================================

st.header("Live Credit Balance")

# Get current balance
stats = get_student_stats(CURRENT_STUDENT_ID)

# Display with auto-refresh
placeholder = st.empty()

with placeholder.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Credits", stats.get('total_credits', 0))
    with col2:
        st.metric("Received", stats.get('credits_received', 0))
    with col3:
        st.metric("Sent This Month", stats.get('credits_sent_this_month', 0))
    with col4:
        st.metric("Endorsements", stats.get('endorsements_received', 0))

# Auto-refresh every 3 seconds
time.sleep(3)
st.rerun()

# =====================================================
# Usage in Your App
# =====================================================

st.header("How to Use in Your App")

st.code("""
# In your app.py, add this pattern:

import streamlit as st
from db_helper import *

# At the top of your page function
@st.cache_data(ttl=5)  # Cache for 5 seconds
def get_live_data(student_id):
    return {
        'notifications': get_notifications(student_id),
        'stats': get_student_stats(student_id),
        'students': get_all_students()
    }

# In your main function
if st.button("🔄 Refresh"):
    st.cache_data.clear()  # Clear cache
    st.rerun()

# Use the data
data = get_live_data(current_student_id)
notifications = data['notifications']
stats = data['stats']
""", language="python")

st.info("""
**Best Practice for Streamlit:**
- Use `@st.cache_data` with short TTL (5-10 seconds)
- Add manual refresh button
- Use `st.rerun()` to refresh
- Real-time subscriptions work but polling is simpler
""")

