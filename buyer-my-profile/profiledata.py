from flask import Flask, render_template, session, request
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import mysql.connector
from flask_cors import  CORS
from flask import jsonify
from flask_cors import cross_origin
import base64

app = Flask(__name__, template_folder='.', static_folder='static')
CORS(app, supports_credentials=True, methods=['GET', 'POST'], allow_headers=['Content-Type', 'Access-Control-Allow-Origin'])
app.secret_key = 'animesh12'  # Replace with a secret key for session management

# Flask-Login configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Replace 'login' with the route for your login page
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'user_registration_dbb'
}
# Assuming you have a function to get data from the database
def get_buyer_data(user_id):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='user_registration_dbb'
    )
    cursor = connection.cursor()
    query = f"SELECT buyer_name, email, phone, age, state, city, gender, address FROM buyers WHERE user_id = {user_id}"
    print(query)  # Print the query to check if it's constructing correctly
    cursor.execute(query)
    data = cursor.fetchone()
    print(data)
    connection.close()
    return data
@app.route('/get-buyer-data', methods=['GET'])
@cross_origin()
def get_buyer_data_route():
    try:
        user_id = request.values.get('userid')
        if user_id:
            buyer_data = get_buyer_data(user_id)
            if buyer_data:
                return jsonify({'status': 'success', 'buyer_data': buyer_data})
            else:
                return jsonify({'status': 'failure', 'message': 'Failed to fetch buyer data'})
        else:
            return jsonify({'status': 'failure', 'message': 'User ID not provided'})
    except Exception as e:
        print(str(e))
        return jsonify({'status': 'failure', 'message': 'An error occurred'})


def update_buyer_data(user_id, new_name, new_email, new_phone, new_age, new_state, new_city, new_gender, new_address):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='user_registration_dbb'
        )
        cursor = connection.cursor()
        update_query = "UPDATE buyers SET buyer_name = %s, email = %s, phone = %s, age = %s, state = %s, city = %s, gender = %s, address = %s WHERE user_id = %s"
        cursor.execute(update_query, (new_name, new_email, new_phone, new_age, new_state, new_city, new_gender, new_address, user_id))

        connection.commit()
        cursor.close()
        connection.close()

        return True  # Successful update
    except Exception as e:
        print(str(e))
        return False  # Update failed

@app.route('/save-buyer-data', methods=['POST'])
@cross_origin()
def save_buyer_data_route():
    try:
        user_id = request.form.get('userid')
        new_name = request.form.get('newname')
        new_email = request.form.get('newemail')
        new_phone = request.form.get('newphone')
        new_age = request.form.get('newage')
        new_state = request.form.get('newstate')
        new_city = request.form.get('newcity')
        new_gender = request.form.get('newgender')
        new_address = request.form.get('newaddress')


        # Assuming you have a function to update data in the database
        update_buyer_data(user_id, new_name, new_email, new_phone, new_age, new_state, new_city, new_gender,new_address)

        return jsonify({'status': 'success', 'message': 'Data saved successfully'})

    except Exception as e:
        print(str(e))
        return jsonify({'status': 'failure', 'message': 'An error occurred during data save'})


# inventory

@app.route('/add-item', methods=['POST'])
def add_item():
    try:
        # Get form data from the request
        buyerid = request.form.get('buyerid')
        item_name =    request.form.get('itemName')
        quantity  =    request.form.get('itemQuantity')
        total_price =  request.form.get('itemPrice')
        quantityUnit = request.form.get('quantityUnit')

        print(buyerid)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Assuming user_id is available in the session

        cursor.execute('INSERT INTO buyer_inventory (buyer_id, item_name, quantity, total_price, quantityunit) VALUES (%s, %s, %s, %s, %s)',
                       (buyerid, item_name, quantity, total_price, quantityUnit))

        conn.commit()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Item added successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to add item: {str(e)}'}), 500


@app.route('/delete-item', methods=['POST'])
def delete_item():
    try:
        # Get buyer id from form data
        buyer_id = request.form.get('buyerid')
        itemname=request.form.get('itemname')
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Direct SQL query to delete the item
        delete_query = f"DELETE FROM buyer_inventory WHERE buyer_id={buyer_id} AND item_name='{itemname}'"
        cursor.execute(delete_query)
        conn.commit()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to delete item: {str(e)}'}), 500


@app.route('/edit-item', methods=['POST'])
def edit_item():
    try:
        # Get form data from the request
        buyerid = request.form.get('buyerid')
        itemname = request.form.get('itemname')
        itemQuantity = request.form.get('itemQuantity')
        itemtPrice = request.form.get('itemtPrice')
        quantityUnit = request.form.get('quantityUnit')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Update the item in the database
        cursor.execute('UPDATE buyer_inventory SET quantity = %s, total_price = %s, quantityunit = %s '
                       'WHERE buyer_id = %s AND item_name = %s',
                       (itemQuantity, itemtPrice, quantityUnit, buyerid, itemname))

        conn.commit()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Item updated successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to update item: {str(e)}'}), 500

@app.route('/get-items', methods=['GET'])
@cross_origin()
def fetch_items():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        buyerid = request.values.get('buyerid')

        # Query the database to fetch items for the current buyer
        cursor.execute('SELECT item_name, quantity, total_price, quantityunit FROM buyer_inventory WHERE buyer_id = %s', (buyerid,))
        print(buyerid)
        items = cursor.fetchall()
        print(items)

        conn.close()
        return jsonify({'status': 'success', 'items': items})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to fetch items: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(port=5005, debug=True)