from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import random
import string

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send-email-verification', methods=['POST'])
def send_email_verification():
    email = request.form.get('email')
    verification_code = generate_verification_code()
    name = request.form.get('name')

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
        del verification_codes[email]
        return 'Verification successful!'
    else:
        return 'Invalid verification code.', 400


def generate_verification_code():
    return ''.join(random.choices( string.digits, k=6))


if __name__ == '__main__':
    app.run(debug=True)
