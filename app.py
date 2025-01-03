from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import razorpay

app = Flask(__name__)
app.secret_key = 'qwertyu'  

# Razorpay credentials
RAZORPAY_KEY_ID = 'your id detals'
RAZORPAY_KEY_SECRET = 'your key details'
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'moviebooking',
    'user': 'root',
    'password': 'root'
}
    
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None



@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    flash(f'Search query: {query}', 'info')
    flash(f'User session: {session.get("user", "Not logged in")}', 'info')
    if 'movie' in query:
        flash("Redirecting to Movies")
        return redirect(url_for('booking'))
    elif 'play' in query:
        flash("Redirecting to Plays")
        return redirect(url_for('plays'))
    elif 'event' in query:
        flash("Redirecting to Events")
        return redirect(url_for('events'))
    elif 'activity' in query:
        flash("Redirecting to Activities")
        return redirect(url_for('activities'))
    elif 'sports' in query:
        flash("Redirecting to Sports")
        return redirect(url_for('sports'))
    elif 'aboutus' in query:
        flash("Redirecting to Aboutus")
        return redirect(url_for('aboutus'))
    elif 'contactus' in query:
        flash("Redirecting to Contactus")
        return redirect(url_for('contactus'))    
    else:
        flash("Redirecting to Home")
        return redirect(url_for('home'))
    
@app.route('/')
def base():
    return render_template('login.html')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/collectcontactus", methods=["POST", "GET"])
def collectcontactus():
    if request.method == "POST":
        fullname = request.form["name"]
        mobile = request.form["mobile"]
        mail = request.form["email"]
        print(f"Full Name: {fullname}, Mobile: {mobile}, Email: {mail}")
        
        try:
            conn = get_db_connection()
            print("Database connection successful")
            
            cursor = conn.cursor()
            q = "SELECT * FROM ENQUIRY"
            cursor.execute(q)
            rows = cursor.fetchall()
            print(f"Rows from ENQUIRY: {rows}")
            
            existed_emails = [i[2] for i in rows]
            if mail in existed_emails:
                x = f"Dear {fullname}, you are already in our database. Our team will get back to you"
                cursor.close()
                conn.close()
                return render_template("contactresult.html", message=x)
            q1 = "INSERT INTO ENQUIRY (name, mobile, email) VALUES (%s, %s, %s)"
            cursor.execute(q1, (fullname, mobile, mail))
            conn.commit()
            print("Commit successful")
            
            cursor.close()
            conn.close()
            
            x = f"Dear {fullname}, our team will get back to you"
            return render_template("contactresult.html", message=x)

        except Exception as e:
            print(f"Error occurred: {e}")
            return render_template("contactresult.html", message="Data not properly sent to the server")
    
    else:
        return "Data sent by unauthorized person"

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/contactresult")
def contactresult():
    return render_template("contactresult.html")

@app.route("/enquirydata")
def enquirydata():
    return redirect(url_for('gatherenquirydata'))

@app.route("/gatherenquirydata")
def gatherenquirydata():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        q = "SELECT * FROM ENQUIRY"
        cursor.execute(q)
        rows = cursor.fetchall()
        print(rows)
        return render_template("enquirydata.html", data=rows)
    except Exception as e:
        print(f"Error: {e}")
        x = "Some error occurred while fetching enquiry data from the database."
        return render_template("contactresult.html", message=x)

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/plays')
def plays():
    return render_template('plays.html')

@app.route('/sports')
def sports():
    return render_template('sports.html')

@app.route('/activities')
def activities():
    return render_template('activities.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    print("Request method:", request.method)
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print("Username:", username)
        print("Password:", password)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
            print("User found:", user)
            conn.close()

            if user and check_password_hash(user['password'], password):
                session['username'] = username
                flash('Login successful', 'success')
                print("Redirecting to home")
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')
                print("Login failed")
                return render_template('login.html')
    return render_template('login.html')


   
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form['username']
        address=request.form['address']
        student_id=request.form['mobile_number']
        password=request.form['password']
        email=request.form['email']
        print(password)
        print(email)
        hash_password=generate_password_hash(password)
        print(hash_password)
        conn=get_db_connection()
        if conn:
            cursor=conn.cursor()
            cursor.execute("SELECT* FROM users WHERE username=%s",(username,))
            existing_user=cursor.fetchone()
            if existing_user:
                print("Username already exists.please choose another one.")
                conn.close()
                return redirect(url_for('register'))
            cursor.execute("insert into users(username,address,mobile_number,password,email) values(%s,%s,%s,%s,%s)",(username,address,student_id,hash_password,email))
            conn.commit()
            cursor.close()
            conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')




@app.route('/admin/signup')
def admin_signup():
    return render_template('admin_signup.html')

@app.route('/admin/register', methods=['POST'])
def admin_register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
            existing_admin = cursor.fetchone()
            if existing_admin:
                flash("Admin username already exists. Please choose another one.", 'danger')
                conn.close()
                return redirect(url_for('admin_signup'))

            cursor.execute(
                "INSERT INTO admins (username, password, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash("Admin registration successful! Please login.", 'success')
            return redirect(url_for('admin_login'))
    return redirect(url_for('admin_signup'))

@app.route('/admin/login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
            admin = cursor.fetchone()
            conn.close()

            if admin and check_password_hash(admin['password'], password):
                session['admin_username'] = username
                flash("Admin login successful", 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash("Invalid admin username or password", 'danger')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_username' not in session:
        flash("You must log in to access the admin dashboard.", 'danger')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM seats")
        seats = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('admin_dashboard.html', users=users, seats=seats)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_username', None)
    flash("Admin logged out successfully.", 'info')
    return redirect(url_for('admin_login'))


@app.route("/storecart1", methods=["POST", "GET"])
def storecart1():
    if request.method == "POST":
        # Get data from the form
        data = request.form.get("cart")
        movie_name = session.get("movie_name")
        price = session.get("price")
        
        if not data or not movie_name or not price:
            return "Invalid data.", 400
        
        selected_seats = data.split(",") 

        if len(selected_seats) == 0:
            return "No seats selected.", 400
        
        ticket_price = int(price)  # Price in rupees
        quantity = len(selected_seats)
        rowss = [(movie_name, ticket_price, quantity)]
        total_price = ticket_price * quantity

        # Create a new order with Razorpay
        order = client.order.create({
            "amount": total_price * 100,
            "currency": "INR",
            "payment_capture": "1"
        })

        # Database update and other logic
        conn = get_db_connection()
        cursor = conn.cursor()

        for seat in selected_seats:
            row = seat[0]  # Row letter
            column = seat[1:]  # Column number
            
            cursor.execute("""
                UPDATE seats
                SET booked = 1
                WHERE `row` = %s AND `column` = %s
            """, (row, column))

        conn.commit()
        cursor.close()
        conn.close()

        return render_template(
            "shoppingcart.html",
            data=rowss,
            total=total_price,
            order=order,
            email="sairajumantipally1328@gmail.com"  # Replace with dynamic email if required
        )
    return render_template("booking.html")





@app.route("/seats", methods=["GET", "POST"])
def seats():
    if request.method == "POST":
        movie_name = request.form.get("movie_name")
        price = request.form.get("price")
        session["movie_name"] = movie_name
        session["price"] = price
        return redirect(url_for("seats"))
    movie_name = session.get("movie_name")
    price = session.get("price")
    if not movie_name or not price:
        return redirect(url_for("booking"))
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, `row`, `column`, booked FROM seats")
        seats = cursor.fetchall()
        seat_status = [["available"] * 10 for _ in range(10)]
        for seat in seats:
            row_index = ord(seat[1]) - 65  
            col_index = int(seat[2]) - 1 
            seat_status[row_index][col_index] = "booked" if seat[3] else "available"

        row_labels = [chr(65 + i) for i in range(10)] 
        return render_template("seats.html", seat_status=seat_status, row_labels=row_labels, movie_name=movie_name, price=price)
    
    finally:
        cursor.close()
        conn.close()



@app.route("/book_seats", methods=["POST"])
def book_seats():
    selected_seats = request.json.get("seats")

    if not selected_seats:
        return jsonify({"message": "No seats selected!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(selected_seats))
    cursor.execute(f"SELECT id FROM seats WHERE id IN ({placeholders}) AND booked = FALSE", tuple(selected_seats))
    available_seats = cursor.fetchall()

    if len(available_seats) != len(selected_seats):
        return jsonify({"message": "Some selected seats are already booked!"}), 400

    cursor.executemany(
        "UPDATE seats SET booked = TRUE WHERE id = %s", [(seat,) for seat in selected_seats]
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Seats booked successfully!", "redirect_url": url_for("storecart1")})

@app.route("/success", methods=["POST", "GET"])
def success():
    payment_id = request.form.get('razorpay_payment_id')
    order_id = request.form.get('razorpay_order_id')
    total_price = request.form.get('total_price')
    user_email = request.form.get('email')
    movie_name = request.form.get('movie_name')

    return render_template("ticket_payslip.html", ticket={
        "movie_name": movie_name,
        "total_price": total_price,
        "payment_id": payment_id,
        "order_id": order_id
    })


        
@app.route('/logout')
def logout():
    session.pop('username',None)
    flash("You've been logedout")
    return redirect(url_for('login'))   

if __name__ == '__main__':

    app.run(debug=True)
    
    
    
    
    
    
