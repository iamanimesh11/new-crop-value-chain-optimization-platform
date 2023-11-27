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
app.config['MAIL_USERNAME'] = 'agritechbazaar@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'cnbd oncd lsvt nsis'  # Replace with your email password

mail = Mail(app)
fusers = {
    'animeshm27singh@gmail.com': {
        'password': '12345',
        'full_name': 'Animesh'
        'otp'
    }
}
# Store generated verification codes (in-memory for simplicity, consider using a database)
fverification_codes = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send-forgotpass-email-verification', methods=['POST'])
def send_email_verification():
    femail = request.form.get('email')
    fverification_code = generate_verification_code()
    # Check if the email exists in your user data
    if femail not in fusers:
        return jsonify({'status': 'error', 'message': 'Invalid email '})
    # Store the verification code for later verification
    fverification_codes[femail] = fverification_code

    user_data = fusers[femail]
    fname = user_data['full_name']

    # Email content
    msg = Message('Email Verification Code', sender='your-email@gmail.com', recipients=[femail])
    # Use HTML and include styling
    # Render HTML from template
    msg.html = render_template(
        'static/forgotpass_template.html',
        name=fname,
        email=femail,
        verification_code=fverification_code
    )


    # Send the email
    mail.send(msg)


    return 'Email sent successfully'


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

    # Check if the email exists in your user data
    if femail not in fusers:
        return jsonify({'status': 'error', 'message': 'Invalid email address'}), 400

    # Update the password in your user data
    fusers[femail]['password'] = new_password

    return jsonify({'status': 'success', 'message': 'Password reset successfully'})



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
