from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.', static_folder='static')

# Your existing Flask-Mail configuration and email verification code here...

# Sample user data (replace this with your user authentication logic)
users = {
    'user@example.com': {
        'password': '12345',
        'full_name': 'Animesh'
    }
}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the user exists and the password is correct
    if email in users and users[email]['password'] == password:
        return jsonify({'status': 'success', 'message': 'Login successful', 'full_name': users[email]['full_name']})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid email or password'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
