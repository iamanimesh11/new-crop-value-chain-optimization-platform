from flask import Flask, render_template, request, jsonify
import mysql.connector
from werkzeug.security import  check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import  CORS
app = Flask(__name__, template_folder='.', static_folder='static')
CORS(app)

app.secret_key = 'animesh123'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# Your existing Flask-Mail configuration and email verification code here...
class User(UserMixin):
    pass
# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'user_registration_dbb'
}
@app.route('/')
def index():
    return render_template('index.html')

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
        print(user_data)


        if user_data and check_password_hash(user_data[3], password):

            userid= user_data[0]
            full_name = user_data[1]
            # Store user information in the session

            user = User()

            user.id = user_data[0]
            user.email = user_data[2]
            user.full_name = user_data[1]
            user.profile = user_data[4]
            login_user(user)
            print('pa1ss')

            if user.profile == "farmer":
                query = "SELECT farmer_id FROM farmers WHERE user_id = %s"
                print(userid)
                cursor.execute(query, (userid,))
                result = cursor.fetchone()
                farmer_id = result[0]
                conn.close()
                return jsonify({'status': 'success', 'message': 'Login successful', 'userid': userid,'farmer_id': farmer_id,'full_name': full_name})
            else:
                query = "SELECT buyer_id FROM buyers WHERE user_id = %s"
                cursor.execute(query, (userid,))
                result = cursor.fetchone()
                buyer_id = result[0]
                conn.close()
                return jsonify(
                    {'status': 'success', 'message': 'Login successful', 'userid': userid, 'buyer_id': buyer_id,
                     'full_name': full_name})
        else:
            conn.close()
            print(f"Login failed for user {email}")
            return jsonify({'status': 'error', 'message': 'Invalid email or password'})
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Database error during login: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
