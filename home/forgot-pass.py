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
app.config['MAIL_USERNAME'] = 'agritechbazaar@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'cnbd oncd lsvt nsis'  # Replace with your email password

mail = Mail(app)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'user_registration_db'
}
# Store generated verification codes (in-memory for simplicity, consider using a database)
fverification_codes = {}


@app.route('/')
def index():
    return render_template('index.html')


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
    app.run(host='0.0.0.0',port=5001,debug=True)
