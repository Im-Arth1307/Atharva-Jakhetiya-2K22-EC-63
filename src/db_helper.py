"""
Database Helper Module for Boostly
Provides functions to interact with Supabase database
"""

from supabase import create_client, Client
from typing import List, Dict, Optional
from datetime import datetime
import os

# Initialize Supabase client
# Try to get from environment variables first, then from config
try:
    from config import SUPABASE_URL, SUPABASE_KEY
except ImportError:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Create client (will be None if keys not set)
supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Warning: Could not connect to Supabase: {e}")
        supabase = None


# =====================================================
# STUDENT OPERATIONS
# =====================================================

def get_all_students() -> List[Dict]:
    """Get all students from database"""
    if not supabase:
        return []
    
    try:
        response = supabase.table('students').select('*').order('name').execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching students: {e}")
        return []


def get_student_by_roll(roll_number: str) -> Optional[Dict]:
    """Get student by roll number"""
    if not supabase:
        return None
    
    try:
        response = supabase.table('students').select('*').eq('roll_number', roll_number).single().execute()
        return response.data if response.data else None
    except Exception as e:
        print(f"Error fetching student: {e}")
        return None


def get_student_credits(student_id: str, month_year: Optional[str] = None) -> Optional[Dict]:
    """Get student's current credit balance"""
    if not supabase:
        return None
    
    if not month_year:
        month_year = datetime.now().strftime('%Y-%m')
    
    try:
        response = supabase.table('student_credits')\
            .select('*')\
            .eq('student_id', student_id)\
            .eq('month_year', month_year)\
            .single().execute()
        return response.data if response.data else None
    except Exception as e:
        print(f"Error fetching student credits: {e}")
        return None


# =====================================================
# CREDIT TRANSACTIONS
# =====================================================

def send_credits(sender_id: str, receiver_id: str, amount: int, message: Optional[str] = None) -> Optional[Dict]:
    """Send credits from one student to another"""
    if not supabase:
        return None
    
    try:
        # Create transaction
        transaction_data = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'amount': amount,
            'message': message,
            'transaction_type': 'transfer'
        }
        
        response = supabase.table('credit_transactions').insert(transaction_data).execute()
        transaction = response.data[0] if response.data else None
        
        if transaction:
            # Update sender credits
            month_year = datetime.now().strftime('%Y-%m')
            sender_credits = get_student_credits(sender_id, month_year)
            
            if sender_credits:
                supabase.table('student_credits').update({
                    'total_credits': sender_credits['total_credits'] - amount,
                    'credits_sent_this_month': sender_credits['credits_sent_this_month'] + amount
                }).eq('id', sender_credits['id']).execute()
            
            # Update receiver credits
            receiver_credits = get_student_credits(receiver_id, month_year)
            if receiver_credits:
                supabase.table('student_credits').update({
                    'total_credits': receiver_credits['total_credits'] + amount,
                    'credits_received': receiver_credits['credits_received'] + amount
                }).eq('id', receiver_credits['id']).execute()
            else:
                # Create new credit record for receiver
                supabase.table('student_credits').insert({
                    'student_id': receiver_id,
                    'total_credits': 100 + amount,
                    'credits_received': amount,
                    'credits_sent_this_month': 0,
                    'monthly_limit': 100,
                    'month_year': month_year
                }).execute()
            
            # Create notifications
            create_notification(sender_id, 'credits_sent', 
                              f'You sent {amount} credits', 
                              f'You sent {amount} credits to {receiver_id}',
                              message, receiver_id, transaction['id'])
            
            create_notification(receiver_id, 'credits_received',
                              f'You received {amount} credits',
                              f'You received {amount} credits from {sender_id}',
                              message, sender_id, transaction['id'])
        
        return transaction
    except Exception as e:
        print(f"Error sending credits: {e}")
        return None


def get_credit_transactions(student_id: str, as_sender: bool = True) -> List[Dict]:
    """Get credit transactions for a student"""
    if not supabase:
        return []
    
    try:
        table = supabase.table('credit_transactions')
        if as_sender:
            response = table.select('*').eq('sender_id', student_id).order('created_at', desc=True).execute()
        else:
            response = table.select('*').eq('receiver_id', student_id).order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []


# =====================================================
# NOTIFICATIONS
# =====================================================

def create_notification(student_id: str, notification_type: str, title: str, 
                       message: str, details: Optional[str] = None,
                       related_student_id: Optional[str] = None,
                       related_transaction_id: Optional[str] = None) -> Optional[Dict]:
    """Create a notification for a student"""
    if not supabase:
        return None
    
    try:
        notification_data = {
            'student_id': student_id,
            'notification_type': notification_type,
            'title': title,
            'message': message,
            'details': details,
            'related_student_id': related_student_id,
            'related_transaction_id': related_transaction_id,
            'is_read': False
        }
        
        response = supabase.table('notifications').insert(notification_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating notification: {e}")
        return None


def get_notifications(student_id: str, limit: int = 50) -> List[Dict]:
    """Get notifications for a student"""
    if not supabase:
        return []
    
    try:
        response = supabase.table('notifications')\
            .select('*')\
            .eq('student_id', student_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching notifications: {e}")
        return []


def mark_notification_read(notification_id: str) -> bool:
    """Mark a notification as read"""
    if not supabase:
        return False
    
    try:
        supabase.table('notifications').update({'is_read': True}).eq('id', notification_id).execute()
        return True
    except Exception as e:
        print(f"Error marking notification as read: {e}")
        return False


# =====================================================
# ENDORSEMENTS
# =====================================================

def create_endorsement(endorser_id: str, endorsee_id: str, recognition_id: Optional[str] = None) -> Optional[Dict]:
    """Create an endorsement"""
    if not supabase:
        return None
    
    try:
        endorsement_data = {
            'endorser_id': endorser_id,
            'endorsee_id': endorsee_id,
            'recognition_id': recognition_id
        }
        
        response = supabase.table('endorsements').insert(endorsement_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating endorsement: {e}")
        return None


def check_endorsement_exists(endorser_id: str, endorsee_id: str) -> bool:
    """Check if an endorsement already exists"""
    if not supabase:
        return False
    
    try:
        response = supabase.table('endorsements')\
            .select('id')\
            .eq('endorser_id', endorser_id)\
            .eq('endorsee_id', endorsee_id)\
            .execute()
        return len(response.data) > 0 if response.data else False
    except Exception as e:
        print(f"Error checking endorsement: {e}")
        return False


def get_endorsements_received(student_id: str) -> int:
    """Get count of endorsements received by a student"""
    if not supabase:
        return 0
    
    try:
        response = supabase.table('endorsements')\
            .select('id', count='exact')\
            .eq('endorsee_id', student_id)\
            .execute()
        return response.count if hasattr(response, 'count') else 0
    except Exception as e:
        print(f"Error counting endorsements: {e}")
        return 0


# =====================================================
# VOUCHER PURCHASES
# =====================================================

def purchase_vouchers(student_id: str, num_vouchers: int, credits_per_voucher: int) -> Optional[Dict]:
    """Purchase vouchers by redeeming credits"""
    if not supabase:
        return None
    
    try:
        VOUCHER_RATE = 5.00
        total_credits = num_vouchers * credits_per_voucher
        total_value = total_credits * VOUCHER_RATE
        
        # Get student credits
        month_year = datetime.now().strftime('%Y-%m')
        student_credits = get_student_credits(student_id, month_year)
        
        if not student_credits:
            return None
        
        # Validate
        if total_credits > student_credits['credits_received']:
            return None  # Insufficient received credits
        
        # Create voucher purchase
        voucher_data = {
            'student_id': student_id,
            'num_vouchers': num_vouchers,
            'credits_per_voucher': credits_per_voucher,
            'total_credits': total_credits,
            'total_value': float(total_value),
            'voucher_rate': VOUCHER_RATE
        }
        
        response = supabase.table('voucher_purchases').insert(voucher_data).execute()
        voucher = response.data[0] if response.data else None
        
        if voucher:
            # Deduct credits
            supabase.table('student_credits').update({
                'total_credits': student_credits['total_credits'] - total_credits,
                'credits_received': student_credits['credits_received'] - total_credits
            }).eq('id', student_credits['id']).execute()
        
        return voucher
    except Exception as e:
        print(f"Error purchasing vouchers: {e}")
        return None


def get_voucher_purchases(student_id: str, limit: int = 10) -> List[Dict]:
    """Get voucher purchase history for a student"""
    if not supabase:
        return []
    
    try:
        response = supabase.table('voucher_purchases')\
            .select('*')\
            .eq('student_id', student_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching voucher purchases: {e}")
        return []


# =====================================================
# REAL-TIME SUBSCRIPTIONS
# =====================================================

def subscribe_to_notifications(student_id: str, callback):
    """Subscribe to real-time notifications for a student"""
    if not supabase:
        return None
    
    try:
        def handle_change(payload):
            if payload.get('new') and payload['new'].get('student_id') == student_id:
                callback(payload['new'])
        
        subscription = supabase.table('notifications')\
            .on('INSERT', handle_change)\
            .subscribe()
        
        return subscription
    except Exception as e:
        print(f"Error subscribing to notifications: {e}")
        return None


def subscribe_to_credits(student_id: str, callback):
    """Subscribe to real-time credit balance changes"""
    if not supabase:
        return None
    
    try:
        def handle_change(payload):
            if payload.get('new') and payload['new'].get('student_id') == student_id:
                callback(payload['new'])
        
        subscription = supabase.table('student_credits')\
            .on('UPDATE', handle_change)\
            .subscribe()
        
        return subscription
    except Exception as e:
        print(f"Error subscribing to credits: {e}")
        return None


# =====================================================
# UTILITY FUNCTIONS
# =====================================================

def get_student_stats(student_id: str) -> Dict:
    """Get comprehensive stats for a student"""
    if not supabase:
        return {}
    
    try:
        month_year = datetime.now().strftime('%Y-%m')
        credits = get_student_credits(student_id, month_year)
        
        # Get transaction counts
        sent_count = len(get_credit_transactions(student_id, as_sender=True))
        received_count = len(get_credit_transactions(student_id, as_sender=False))
        
        # Get endorsements
        endorsements_received = get_endorsements_received(student_id)
        
        return {
            'total_credits': credits['total_credits'] if credits else 100,
            'credits_received': credits['credits_received'] if credits else 0,
            'credits_sent_this_month': credits['credits_sent_this_month'] if credits else 0,
            'monthly_limit': credits['monthly_limit'] if credits else 100,
            'endorsements_received': endorsements_received,
            'transactions_sent': sent_count,
            'transactions_received': received_count
        }
    except Exception as e:
        print(f"Error getting student stats: {e}")
        return {}


def is_connected() -> bool:
    """Check if database connection is available"""
    return supabase is not None

