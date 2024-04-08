from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import random
import string
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder='.', static_folder='static')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'rpaanimesh@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'vwja copm znpy akhw'  # Replace with your email password

mail = Mail(app)

# Store generated verification codes (in-memory for simplicity, consider using a database)
verification_codes = {}

# MySQL database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'user_registration_db'
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        profile VARCHAR(50)
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS buyers (
        buyer_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        buyer_name VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS farmers (
        farmer_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        farmer_name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(20),
        age INT,
        state VARCHAR(100),
        city VARCHAR(100),
        gender VARCHAR(10),
        address VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')
conn.commit()
conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send-email-verification', methods=['POST'])
def send_email_verification():
    email = request.form.get('email')
    verification_code = generate_verification_code()
    name = request.form.get('name')
    password= request.form.get('password')
    # Store the verification code for later verification

    verification_codes[email] = verification_code
    # Email content
    msg = Message('Email Verification Code', sender='your-email@gmail.com', recipients=[email])
    # Use HTML and include styling
    # Render HTML from template
    msg.html = render_template(
        'static/mail-template.html',
        name=name,
        email=email,
        verification_code=verification_code
    )


    # Send the email
    mail.send(msg)


    return 'Email sent successfully'


@app.route('/verify-email-otp', methods=['POST'])
def verify_email_otp():
    email = request.form.get('email')
    entered_code = request.form.get('code')

    # Check if the entered code matches the stored code
    if verification_codes.get(email) == entered_code:
        # Remove the verified email from the dictionary to ensure the code is used only once
        return 'Verification successful!'
    else:
        return 'Invalid verification code.', 400

@app.route('/register', methods=['POST'])
def register():
    print("Received registration request")

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    chooseProfile = request.form.get('chooseProfile')

    # Check if the email already exists in the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        # Email already registered
        return jsonify({'success': False, 'message': 'Email already registered. Please log in.'}), 400

    # Check if the entered code matches the stored code
    if verification_codes.get(email):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Store user details in the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (full_name, email, password, profile) VALUES (%s, %s, %s, %s)',
                       (name, email, hashed_password, chooseProfile))
        conn.commit()

        # Retrieve the user_id of the newly inserted user
        cursor.execute('SELECT user_id FROM users WHERE email = %s', (email,))
        user_id = cursor.fetchone()[0]

        # Store profile-specific details in the corresponding table (farmers/buyers)
        if chooseProfile == 'farmer':
            cursor.execute('INSERT INTO farmers (user_id, farmer_name) VALUES (%s, %s)',
                           (user_id, name))
        elif chooseProfile == 'buyer':
            cursor.execute('INSERT INTO buyers (user_id, buyer_name) VALUES (%s, %s)',
                           (user_id, name))

        else :
            print("error in famera")
        conn.commit()
        conn.close()

        del verification_codes[email]

        return jsonify({'success': True, 'message': 'Registration successful!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid verification code or email not verified.'}), 400

def generate_verification_code():
    return ''.join(random.choices( string.digits, k=6))


if __name__ == '__main__':
    app.run(debug=True)
