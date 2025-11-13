# Boostly Data Model Documentation

## Overview
This document describes the complete data model for the Boostly application, including all entities, relationships, and business rules.

## Entity Relationship Diagram

```
┌─────────────┐
│  Students   │
└──────┬──────┘
       │
       ├───┐
       │   │
       ▼   ▼
┌──────────────────┐    ┌──────────────────────┐
│ Student Credits   │    │ Credit Transactions  │
└──────────────────┘    └──────────────────────┘
       │                          │
       │                          │
       ▼                          ▼
┌──────────────────┐    ┌──────────────────────┐
│  Notifications    │    │    Endorsements       │
└──────────────────┘    └──────────────────────┘
       │
       │
       ▼
┌──────────────────┐
│ Voucher Purchases │
└──────────────────┘
```

## Tables

### 1. Students
Stores all student information in the system.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier for each student |
| name | VARCHAR(255) | NOT NULL | Student's full name |
| roll_number | VARCHAR(50) | UNIQUE, NOT NULL | Student's roll number (e.g., "2K22/EC/63") |
| email | VARCHAR(255) | | Student's email address (optional) |
| avatar_url | TEXT | | URL to student's avatar image |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Record last update timestamp |

**Business Rules:**
- Roll number must be unique
- Each student must have a name and roll number

---

### 2. Student Credits
Tracks current credit balances and monthly limits for each student.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| student_id | UUID | FOREIGN KEY → students(id) | Reference to student |
| total_credits | INTEGER | DEFAULT 100, NOT NULL | Total available credits |
| credits_received | INTEGER | DEFAULT 0, NOT NULL | Credits received (redeemable) |
| credits_sent_this_month | INTEGER | DEFAULT 0, NOT NULL | Credits sent in current month |
| monthly_limit | INTEGER | DEFAULT 100, NOT NULL | Monthly sending limit |
| month_year | VARCHAR(7) | NOT NULL | Month tracking (format: 'YYYY-MM') |
| last_reset_date | DATE | | Date of last monthly reset |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Record last update timestamp |

**Unique Constraint:** (student_id, month_year)

**Business Rules:**
- Each student gets 100 credits every month (reset at start of month)
- Monthly sending limit is 100 credits
- Up to 50 unused credits can be carried forward
- Credits received can be redeemed, credits sent cannot

---

### 3. Credit Transactions
Records all credit transfers between students.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| sender_id | UUID | FOREIGN KEY → students(id) | Student sending credits |
| receiver_id | UUID | FOREIGN KEY → students(id) | Student receiving credits |
| amount | INTEGER | NOT NULL, CHECK > 0 | Number of credits transferred |
| message | TEXT | | Optional message from sender |
| transaction_type | VARCHAR(20) | DEFAULT 'transfer' | Type: 'transfer' or 'redemption' |
| created_at | TIMESTAMP | DEFAULT NOW() | Transaction timestamp |

**Constraints:**
- `sender_id != receiver_id` (no self-transfers)
- `amount > 0`

**Business Rules:**
- Students cannot send credits to themselves
- Each transaction creates notifications for both sender and receiver
- Credits sent are deducted from sender's balance
- Credits received are added to receiver's balance and credits_received

---

### 4. Notifications
Stores all notifications for students.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| student_id | UUID | FOREIGN KEY → students(id) | Student receiving notification |
| notification_type | VARCHAR(50) | NOT NULL | Type: 'credits_sent', 'credits_received', 'endorsement_received', 'endorsement_given' |
| title | VARCHAR(255) | NOT NULL | Notification title |
| message | TEXT | NOT NULL | Notification message |
| details | TEXT | | Additional details |
| related_student_id | UUID | FOREIGN KEY → students(id) | Related student (if applicable) |
| related_transaction_id | UUID | FOREIGN KEY → credit_transactions(id) | Related transaction (if applicable) |
| is_read | BOOLEAN | DEFAULT FALSE | Read status |
| created_at | TIMESTAMP | DEFAULT NOW() | Notification timestamp |

**Business Rules:**
- Notifications are created automatically for credit transactions
- Notifications are created for endorsements
- Students can mark notifications as read

---

### 5. Endorsements
Tracks endorsements given by students to other students.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| endorser_id | UUID | FOREIGN KEY → students(id) | Student giving endorsement |
| endorsee_id | UUID | FOREIGN KEY → students(id) | Student receiving endorsement |
| recognition_id | UUID | FOREIGN KEY → credit_transactions(id) | Related recognition/transaction |
| created_at | TIMESTAMP | DEFAULT NOW() | Endorsement timestamp |

**Unique Constraint:** (endorser_id, endorsee_id, recognition_id)

**Constraints:**
- `endorser_id != endorsee_id` (no self-endorsements)

**Business Rules:**
- Each endorser can endorse a recognition entry only once
- Endorsements are just a count - they don't affect credit balances
- Endorsements create notifications for both parties

---

### 6. Voucher Purchases
Records all voucher redemptions.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| student_id | UUID | FOREIGN KEY → students(id) | Student purchasing vouchers |
| num_vouchers | INTEGER | NOT NULL, CHECK > 0 | Number of vouchers purchased |
| credits_per_voucher | INTEGER | NOT NULL, CHECK > 0 | Credits used per voucher |
| total_credits | INTEGER | NOT NULL, CHECK > 0 | Total credits redeemed |
| total_value | DECIMAL(10,2) | NOT NULL, CHECK > 0 | Total voucher value in ₹ |
| voucher_rate | DECIMAL(5,2) | DEFAULT 5.00 | Conversion rate (₹5 per credit) |
| created_at | TIMESTAMP | DEFAULT NOW() | Purchase timestamp |

**Business Rules:**
- Credits are converted at ₹5 per credit
- Credits are permanently deducted when redeemed
- Students can only redeem credits they have received
- Multiple vouchers can be purchased in one transaction
- Total credits = num_vouchers × credits_per_voucher
- Total value = total_credits × voucher_rate

---

## Relationships

### One-to-Many Relationships

1. **Student → Student Credits**
   - One student can have multiple credit records (one per month)
   - Each credit record belongs to one student

2. **Student → Credit Transactions (as sender)**
   - One student can send multiple credit transactions
   - Each transaction has one sender

3. **Student → Credit Transactions (as receiver)**
   - One student can receive multiple credit transactions
   - Each transaction has one receiver

4. **Student → Notifications**
   - One student can have multiple notifications
   - Each notification belongs to one student

5. **Student → Endorsements (as endorser)**
   - One student can give multiple endorsements
   - Each endorsement has one endorser

6. **Student → Endorsements (as endorsee)**
   - One student can receive multiple endorsements
   - Each endorsement has one endorsee

7. **Student → Voucher Purchases**
   - One student can make multiple voucher purchases
   - Each purchase belongs to one student

8. **Credit Transaction → Endorsements**
   - One credit transaction can receive multiple endorsements
   - Each endorsement is linked to one recognition/transaction

---

## Business Logic Summary

### Credit Management
- **Monthly Reset:** Credits reset to 100 at the start of each calendar month
- **Carry Forward:** Up to 50 unused credits can be carried forward
- **Sending Limit:** 100 credits per month maximum
- **Self-Transfer:** Not allowed
- **Balance Check:** Cannot send more than available balance

### Endorsements
- **One-Time:** Each endorser can endorse a recognition only once
- **No Credit Impact:** Endorsements don't affect credit balances
- **Count Only:** Endorsements are just a count

### Redemptions
- **Rate:** ₹5 per credit
- **Permanent:** Credits are permanently deducted
- **Received Only:** Can only redeem received credits
- **Multiple:** Can purchase multiple vouchers at once

### Notifications
- **Auto-Generated:** Created automatically for transactions and endorsements
- **Types:** credits_sent, credits_received, endorsement_received, endorsement_given
- **Read Status:** Can be marked as read

---

## Indexes

The following indexes are created for performance optimization:

1. **student_credits:** student_id, month_year
2. **credit_transactions:** sender_id, receiver_id, created_at
3. **notifications:** student_id, notification_type, created_at, is_read
4. **endorsements:** endorser_id, endorsee_id, recognition_id
5. **voucher_purchases:** student_id, created_at

---

## Row Level Security (RLS)

All tables have RLS enabled with the following policies:

- **Students:** Viewable by everyone, updatable by owner
- **Student Credits:** Viewable by everyone, updatable by owner
- **Credit Transactions:** Viewable by everyone, insertable by sender
- **Notifications:** Viewable and updatable only by owner
- **Endorsements:** Viewable by everyone, insertable by endorser
- **Voucher Purchases:** Viewable and insertable only by owner

---

## Data Flow Examples

### Sending Credits
1. User selects recipient and enters amount
2. System validates: balance, monthly limit, no self-transfer
3. Create `credit_transaction` record
4. Update `student_credits` for both sender and receiver
5. Create `notifications` for both parties

### Endorsing
1. User selects student to endorse
2. System validates: not already endorsed, no self-endorsement
3. Create `endorsement` record
4. Create `notifications` for both parties
5. Update endorsement count

### Redeeming
1. User enters voucher details
2. System validates: sufficient received credits
3. Create `voucher_purchase` record
4. Update `student_credits` (deduct from total and received)
5. Create `credit_transaction` with type 'redemption'

---

## Notes

- All timestamps use `TIMESTAMP WITH TIME ZONE` for proper timezone handling
- UUIDs are used for all primary keys for better scalability
- Foreign keys use `ON DELETE CASCADE` or `ON DELETE SET NULL` as appropriate
- Check constraints ensure data integrity at the database level
- Unique constraints prevent duplicate endorsements and ensure data consistency

