# MovieBooking Application

The **MovieBooking** application is a web-based system for booking tickets for movies, plays, events, activities, and sports. It features user registration, login, seat selection, Razorpay integration for payments, and an admin dashboard.

---

## Features

1. **User Authentication**:
   - User registration and login with password hashing.
   - Admin registration and login with a secure dashboard.

2. **Search and Navigation**:
   - Dynamic search to navigate between movies, plays, events, activities, and sports.

3. **Ticket Booking**:
   - Real-time seat availability.
   - Secure seat booking and Razorpay payment gateway integration.

4. **Contact Us**:
   - Collect and store user inquiries for further assistance.

5. **Admin Dashboard**:
   - View all users and seats.
   - Manage seat bookings.

---

## Prerequisites

### 1. Install Required Packages
- Python 3.7+
- Flask
- MySQL Connector
- Werkzeug
- Razorpay Python SDK

Install dependencies using:
```bash
pip install flask mysql-connector-python werkzeug razorpay
2. Database Configuration
MySQL server running locally or on a remote host.
Database moviebooking created with the following tables:
users (for user accounts)
admins (for admin accounts)
seats (for seat availability)
enquiry (for storing inquiries)
Setup
1. Clone Repository
Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/your-repo/moviebooking.git
cd moviebooking
2. Configure Database
Update the database configuration in db_config:

python
Copy code
db_config = {
    'host': 'localhost',
    'database': 'moviebooking',
    'user': 'root',
    'password': 'root'
}
3. Set Razorpay Credentials
Set your Razorpay RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in the app:

python
Copy code
RAZORPAY_KEY_ID = 'your_key_id'
RAZORPAY_KEY_SECRET = 'your_key_secret'
4. Run the Application
Run the application locally:

bash
Copy code
python app.py
Access the application at: http://127.0.0.1:5000

Usage
User Features:
Sign up or log in.
Browse movies, plays, or events.
Select seats and make payments.
View booking confirmation and download tickets.
Admin Features:
Log in to the admin dashboard.
View registered users and manage bookings.
File Structure
app.py - Main application code.
templates/ - HTML templates for the frontend.
static/ - Static files (CSS, JS, images).
requirements.txt - List of Python dependencies.
Screenshots
Add screenshots of the application here to showcase its UI/UX.

