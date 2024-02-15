from flask import Flask, render_template, request, jsonify
import mysql.connector
from werkzeug.security import  check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import  CORS
import random
from flask_mail import Mail, Message
import string
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

app = Flask(__name__, template_folder='.', static_folder='static')
CORS(app, supports_credentials=True, methods=['POST'], allow_headers=['Content-Type'])

app.secret_key = 'animesh123'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# Your existing Flask-Mail configuration and email verification code here...
class User(UserMixin):
    pass
# Database configuration

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'agritechbazaar@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'cnbd oncd lsvt nsis'  # Replace with your email password

mail = Mail(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'user_registration_db'
}
@app.route('/')
def index():
    return render_template('my-profile.html')

@login_manager.user_loader
def load_user(user_id):
    # Load user from the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user = User()
        user.id = user_data[0]
        user.email = user_data[2]
        user.full_name = user_data[1]
        user.profile = user_data[4]
        return user
    return None


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email)
    # Check user authentication in the database using parameterized query
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user_data = cursor.fetchone()

        if user_data and check_password_hash(user_data[3], password):
            full_name = user_data[1]
            session['user_id'] = user_data[0]
            print(session)

            # Store user information in the session
            user = User()
            user.id = user_data[0]
            user.email = user_data[2]
            user.full_name = user_data[1]
            user.profile = user_data[4]

            login_user(user)

            conn.close()
            return jsonify({'status': 'success', 'message': 'Login successful', 'full_name': full_name})
        else:
            conn.close()
            print(f"Login failed for user {email}")
            return jsonify({'status': 'error', 'message': 'Invalid email or password'})
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Database error during login: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'}), 500


# Store generated verification codes (in-memory for simplicity, consider using a database)
fverification_codes = {}


@app.route('/send-forgotpass-email-verification', methods=['POST'])
def send_email_verification():
    femail = request.form.get('email')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE email = %s', (femail,))
        user_data = cursor.fetchone()

        if user_data is None:
            return jsonify({'status': 'error', 'message': 'Invalid email address'})

        fverification_code = generate_verification_code()

        fverification_codes[femail] = fverification_code

        fname = user_data[1]

        msg = Message('Email Verification Code', sender='your-email@gmail.com', recipients=[femail])
        # Use HTML and include styling
        # Render HTML from template
        msg.html = render_template(
            'static/forgotpass_template.html',
            name=fname,
            email=femail,
            verification_code=fverification_code
        )
        mail.send(msg)

        return 'Email sent successfully'
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to send verification email: {str(e)}'}), 500
    finally:
        conn.close()


@app.route('/fverify-email-otp', methods=['POST'])
def fverify_email_otp():
    femail = request.form.get('femail')
    fentered_code = request.form.get('fcode')

    # Check if the entered code matches the stored code
    if fverification_codes.get(femail) == fentered_code:

        # Remove the verified email from the dictionary to ensure the code is used only once
        del fverification_codes[femail]
        return 'Verification successful!'
    else:
        return 'Invalid verification code.', 400

def generate_verification_code():
    return ''.join(random.choices( string.digits, k=6))


@app.route('/freset-password', methods=['POST'])
def reset_password():
    femail = request.form.get('femail')
    new_password = request.form.get('fpassword')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE email = %s', (femail,))
        user_data = cursor.fetchone()

        if user_data is None:
            return jsonify({'status': 'error', 'message': 'Invalid email address'}), 400

        # Hash and salt the new password before updating the database
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

        # Update the password in the database
        cursor.execute('UPDATE users SET password = %s WHERE email = %s', (hashed_password, femail))
        conn.commit()

        return jsonify({'status': 'success', 'message': 'Password reset successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': f'Failed to reset password: {str(e)}'}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
