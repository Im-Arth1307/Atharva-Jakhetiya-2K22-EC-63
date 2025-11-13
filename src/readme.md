# Boostly - Student Recognition Platform

A Streamlit-based web application that enables college students to recognize their peers, allocate monthly credits, and redeem earned rewards. The platform encourages appreciation and engagement across student communities with a simple, transparent system for celebrating contributions and converting recognition into tangible value.

## Table of Contents

- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Application Structure](#application-structure)
- [Pages and Functionality](#pages-and-functionality)
- [Database Schema](#database-schema)
- [Business Rules](#business-rules)
- [UI/UX Design](#uiux-design)
- [File Structure](#file-structure)
- [Future Enhancements](#future-enhancements)

## Features

### Core Functionality

1. **Recognition System**
   - Send credits to other students
   - Receive credits from peers
   - Track credit transactions with messages
   - Monthly credit allocation (100 credits per month)
   - Monthly sending limit (100 credits)

2. **Endorsement System**
   - Endorse other students' recognitions
   - One-time endorsement per student
   - Track endorsements given and received
   - Endorsements are count-only (don't affect credits)

3. **Redemption System**
   - Convert received credits into vouchers
   - Fixed conversion rate: ₹5 per credit
   - Purchase multiple vouchers at once
   - Permanent credit deduction on redemption
   - Only redeemable credits can be used

4. **Notifications**
   - Real-time notification feed
   - Four notification types:
     - Credits Sent
     - Credits Received
     - Endorsement Received
     - Endorsement Given
   - Color-coded notification cards
   - Relative timestamp display

5. **User Dashboard**
   - Profile display with name and roll number
   - Real-time statistics:
     - Total Credits
     - Credits Sent
     - Credits Received
     - Endorsements Received
     - Days Until Monthly Reset

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- (Optional) Supabase account for database integration

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd src
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install Streamlit directly:
   ```bash
   pip install streamlit
   ```

3. **Verify installation:**
   ```bash
   streamlit --version
   ```

### Database Setup (Optional)

If you want to integrate with Supabase:

1. **Create a Supabase project:**
   - Sign up at [supabase.com](https://supabase.com)
   - Create a new project
   - Note your project URL and API keys

2. **Run the database schema:**
   - Open `database_schema.sql` in Supabase SQL Editor
   - Execute the entire script
   - Verify tables are created

3. **Configure connection (if integrating):**
   - Update `app.py` to use Supabase client
   - Add connection credentials securely

For detailed database setup, see `database_setup_guide.md`.

### Environment Variables (Optional)

Currently, the application uses hardcoded data. For production use with database:

```bash
# Create a .env file (optional)
SUPABASE_URL=your-project-url
SUPABASE_KEY=your-api-key
```

## Running the Application

1. **Navigate to the src directory:**
   ```bash
   cd src
   ```

2. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

3. **Access the application:**
   - The application will automatically open in your default web browser
   - If it doesn't, navigate to: `http://localhost:8501`
   - The default port is 8501

4. **Stop the application:**
   - Press `Ctrl+C` in the terminal

## Application Structure

### Main Components

- **`app.py`**: Main application file containing all pages and logic
- **Session State Management**: Tracks user data, credits, endorsements, and page navigation
- **Page Routing**: Multi-page application with sidebar navigation

### Data Storage

Currently uses **session state** for data persistence (in-memory):
- Student information
- Credit balances
- Transaction history
- Endorsement records
- Notification feed
- Voucher purchases

**Note:** Data is reset when the application restarts. For persistent storage, integrate with the Supabase database using the provided schema.

## Pages and Functionality

### 1. Notifications Page (Home)

**Route:** Default page (`/`)

**Features:**
- Displays all recent notifications in chronological order
- Color-coded notification cards:
  - **Pink/Red**: Credits Sent
  - **Blue**: Credits Received
  - **Purple**: Endorsement Received
  - **Orange/Peach**: Endorsement Given
- Relative timestamp formatting (e.g., "2 hours ago", "Yesterday")
- Scrollable notification feed

**Notification Types:**
- `credits_sent`: When you send credits to another student
- `credits_received`: When you receive credits from another student
- `endorsement_received`: When your recognitions receive endorsements
- `endorsement_given`: When you endorse someone else's recognition

### 2. Send Credits Page

**Route:** Accessed via "📤 Send Credits" button

**Features:**
- **Student Selection:**
  - Grid layout showing all students
  - Student cards with name and roll number
  - Click to select a student
  - Visual feedback for selected student

- **Credit Input Form:**
  - Number input for credits to send (1-100)
  - Optional message field
  - Real-time validation
  - Purchase summary display

- **Validation Rules:**
  - Credits must be > 0
  - Cannot exceed monthly sending limit (100 - credits_sent)
  - Cannot exceed available balance
  - Cannot send to yourself

- **Success/Error Handling:**
  - Error messages for invalid inputs
  - Form persists on error (allows retry)
  - Success notification on completion
  - Automatic balance update

**Business Logic:**
- Deducts credits from sender's total balance
- Adds credits to receiver's balance and received credits
- Updates monthly sent counter
- Creates notifications for both parties

### 3. Endorse Page

**Route:** Accessed via "👍 Endorse" button

**Features:**
- **Student Grid:**
  - Display all students in blocks
  - Visual indication of already endorsed students
  - Endorse button for each student

- **Endorsement Rules:**
  - One endorsement per student
  - Cannot endorse yourself
  - Endorsements are count-only (no credit impact)
  - Visual feedback for endorsed students

- **Statistics:**
  - Students Endorsed count
  - Endorsements Received count

**Business Logic:**
- Tracks endorsed students in session state
- Prevents duplicate endorsements
- Updates endorsement statistics
- Creates notifications for endorsements

### 4. Redeem Page

**Route:** Accessed via "💰 Redeem" button

**Features:**
- **Voucher Purchase Form:**
  - Number of vouchers (1-100)
  - Credits per voucher
  - Real-time calculation of total value
  - Purchase summary display

- **Conversion Rate:**
  - Fixed rate: ₹5 per credit
  - Total value = credits × 5

- **Validation:**
  - Can only redeem received credits
  - Cannot exceed available received credits
  - Cannot exceed total balance
  - Credits must be > 0

- **Purchase History:**
  - Display recent voucher purchases
  - Expandable details for each purchase
  - Timestamp and value information

**Business Logic:**
- Permanently deducts credits from balance
- Deducts from both total and received credits
- Records voucher purchase details
- Creates transaction record

## Database Schema

The application includes a complete database schema for Supabase integration:

### Tables

1. **students**: Student profiles (name, roll number, email)
2. **student_credits**: Monthly credit balances and limits
3. **credit_transactions**: All credit transfers
4. **notifications**: System notifications
5. **endorsements**: Endorsement records
6. **voucher_purchases**: Redemption history

### Documentation

- **`database_schema.sql`**: Complete SQL schema with tables, indexes, and RLS policies
- **`data_model.md`**: Detailed data model documentation
- **`database_setup_guide.md`**: Step-by-step Supabase setup guide
- **`common_queries.sql`**: Useful SQL queries for common operations

## Business Rules

### Credit Management

1. **Monthly Allocation:**
   - Each student receives 100 credits every month
   - Credits reset at the start of each calendar month
   - Up to 50 unused credits can be carried forward

2. **Sending Limits:**
   - Monthly sending limit: 100 credits
   - Cannot send more than available balance
   - Cannot send to yourself
   - Monthly limit resets with credit allocation

3. **Credit Types:**
   - **Total Credits**: All available credits
   - **Credits Received**: Credits that can be redeemed
   - **Credits Sent**: Monthly tracking of sent credits

### Endorsements

1. **One-Time Rule:**
   - Each student can be endorsed only once
   - Endorsements are per student, not per recognition

2. **No Credit Impact:**
   - Endorsements don't affect credit balances
   - Endorsements are count-only

### Redemptions

1. **Conversion Rate:**
   - Fixed rate: ₹5 per credit
   - Cannot be changed

2. **Redemption Rules:**
   - Only received credits can be redeemed
   - Credits are permanently deducted
   - Multiple vouchers can be purchased at once

3. **Permanent Deduction:**
   - Redeemed credits are removed from balance
   - Cannot be recovered

## UI/UX Design

### Design Philosophy

- **Soft Pastel Colors**: Pleasing, modern aesthetic
- **Card-Based Layout**: Clean, organized information display
- **Responsive Design**: Works on different screen sizes
- **Visual Feedback**: Clear indication of actions and states

### Color Scheme

- **Credits Sent**: Pink/Red pastel (#ffb3ba)
- **Credits Received**: Blue pastel (#bae1ff)
- **Endorsements Received**: Purple pastel (#c7ceea)
- **Endorsements Given**: Orange/Peach pastel (#ffdfba)
- **Student Cards**: Blue gradient with hover effects
- **Selected States**: Pink/Red highlight

### User Experience Features

1. **Sidebar Navigation:**
   - Persistent sidebar with user profile
   - Action buttons (Send Credits, Redeem, Endorse)
   - Real-time statistics display
   - Days until reset counter

2. **Form Validation:**
   - Real-time error messages
   - Form persistence on error
   - Clear success/error feedback
   - Input constraints and limits

3. **Visual Indicators:**
   - Selected student highlighting
   - Endorsed student opacity
   - Hover effects on interactive elements
   - Color-coded notification types

## File Structure

```
src/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── readme.md                   # This file
├── database_schema.sql         # Supabase database schema
├── data_model.md              # Data model documentation
├── database_setup_guide.md    # Database setup instructions
└── common_queries.sql          # Useful SQL queries
```

## Key Functions

### Main Functions

- `main()`: Main application entry point, handles routing
- `notifications_page()`: Displays notification feed
- `send_credits_page()`: Handles credit sending functionality
- `endorse_page()`: Manages endorsement system
- `redeem_page()`: Handles voucher redemption

### Helper Functions

- `display_notification()`: Renders notification cards
- `display_student_card()`: Renders student cards
- `format_timestamp()`: Formats timestamps to relative time
- `get_days_until_reset()`: Calculates days until monthly reset
- `get_notification_class()`: Returns CSS class for notification type

## Session State Variables

- `page`: Current page route
- `total_credits`: Total available credits
- `credits_sent`: Credits sent this month
- `credits_received`: Credits received (redeemable)
- `endorsements_received`: Count of endorsements received
- `endorsed_students`: List of endorsed student IDs
- `vouchers_purchased`: List of voucher purchase records
- `selected_student`: Currently selected student index

## Sample Data

The application includes hardcoded sample data:

- **8 Students**: Various names and roll numbers
- **10 Notifications**: Mix of all notification types
- **Initial Credits**: 150 total, 85 received, 55 sent
- **Initial Endorsements**: 12 received

## Testing the Application

### Test Scenarios

1. **Send Credits:**
   - Select a student
   - Enter valid credit amount
   - Add optional message
   - Verify balance updates

2. **Endorse:**
   - Click endorse on a student
   - Verify endorsement is recorded
   - Try to endorse again (should be disabled)

3. **Redeem:**
   - Enter voucher details
   - Verify validation works
   - Complete purchase
   - Check balance deduction

4. **Validation:**
   - Try sending more than limit
   - Try sending to yourself
   - Try redeeming more than received credits

## Troubleshooting

### Common Issues

1. **Application won't start:**
   - Verify Streamlit is installed: `pip install streamlit`
   - Check Python version: `python --version` (should be 3.7+)

2. **Port already in use:**
   - Change port: `streamlit run app.py --server.port 8502`
   - Or stop other Streamlit instances

3. **Data resets on refresh:**
   - This is expected with session state
   - Integrate with database for persistence

4. **Import errors:**
   - Install all dependencies: `pip install -r requirements.txt`
   - Verify file structure matches expected layout

## Future Enhancements

### Planned Features

1. **Database Integration:**
   - Connect to Supabase
   - Persistent data storage
   - Real-time updates

2. **Authentication:**
   - User login system
   - Session management
   - Secure access control

3. **Monthly Reset Automation:**
   - Automatic credit reset
   - Carry-forward logic
   - Notification system

4. **Leaderboard:**
   - Top recipients ranking
   - Recognition counts
   - Endorsement totals

5. **Advanced Features:**
   - Search functionality
   - Filter notifications
   - Export transaction history
   - Email notifications

### Code Improvements

- Refactor into modular components
- Add unit tests
- Implement error logging
- Add data validation layer
- Optimize performance

## Dependencies

```
streamlit>=1.28.0
```

## License

This project is part of a coding assessment/assignment.

## Support

For issues or questions:
- Review the documentation files in the `src/` directory
- Check `database_setup_guide.md` for database setup help
- Refer to `data_model.md` for data structure details
- See `common_queries.sql` for database query examples

---

**Note:** This application currently uses in-memory session state for data storage. For production use, integrate with the provided Supabase database schema for persistent data storage and multi-user support.
