#importing important modules and libraries
import pymysql
import pymysql
from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

#creating a Flask web application instance
app = Flask(__name__)
CORS(app, resources={r"/server": {"origins": "*"}}) #enabling CORS for the '/server' route
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  #configuring Flask to pretty-print JSON responses

db = SQLAlchemy()

#defining MySQL database connection parameters
user = "root"
pin = "12345" # ISI PASSWORD MYSQL
host = "localhost"
db_name = "COVID19" # NAMA DATABASE COVID19
 
# Configuring database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
 
# Disable modification tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Creating Models
class Books(db.Model):
    __tablename__ = "LAPORCOVID" # NAMA TABLE LAPORCOVID STRUKTURNYA DI BAWAH
    #defining table columns
    nik_pelapor = db.Column(db.String(16), nullable=False, primary_key=True)
    nama_pelapor = db.Column(db.String(100), nullable=False)
    nama_terlapor = db.Column(db.String(100), nullable=False)
    alamat_terlapor = db.Column(db.String(100), nullable=False)
    gejala = db.Column(db.String(100), nullable=False)

def create_db():
    with app.app_context():
        db.create_all()

# Use MySQL
@app.route('/server1')
def server1():
    try:
        # Query all data from the LAPORCOVID table
        details = Books.query.all()

        # Convert the data to a list of dictionaries
        details_list = [
            {
                'nik_pelapor': entry.nik_pelapor,
                'nama_pelapor': entry.nama_pelapor,
                'nama_terlapor': entry.nama_terlapor,
                'alamat_terlapor': entry.alamat_terlapor,
                'gejala': entry.gejala
            }
            for entry in details
        ]

        # Return the data as JSON
        return jsonify(details_list)
    
    except Exception as e:
        print('ERROR:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/server1/add', methods=['GET', 'POST']) #defining a route for adding new data to the 'LAPORCOVID' table
def add_laporan():
    if request.method == "POST":
        nik_pelapor = request.form.get('nik_pelapor')
        nama_pelapor = request.form.get('nama_pelapor')
        alamat_terlapor = request.form.get('alamat_terlapor')
        gejala = request.form.get('gejala')

        add_details = Books ( #creating a new 'Books' instance and add it to the database
            nik_pelapor=nik_pelapor,
            nama_pelapor=nama_pelapor,
            alamat_terlapor=alamat_terlapor,
            gejala=gejala
        )

        db.session.add(add_details)
        db.session.commit()
        return redirect('/')
    return jsonify(add_details)

# TEST
@app.route('/server', methods=['GET', 'POST']) # defining a route for handling form data, both POST and GET requests

# Define a function to handle form data
def handle_form_data():
    try:
        # Check if the HTTP request method is POST
        if request.method == 'POST':
            # Check if the request content type is JSON
            if request.is_json:
                # Parse JSON data from the request
                data = request.get_json()
                
                # Establish a connection to the MySQL database
                connection = mysql.connector.connect (
                    user="root",
                    password="12345",  # Use the correct parameter for the password
                    host="localhost",
                    database="COVID19"  # Use the correct parameter for the database name
                )
                
                # Create a cursor object to interact with the database
                cursor = connection.cursor()

                # Define an SQL query to insert data into the database
                query = "INSERT INTO LAPORCOVID (nik_pelapor, nama_pelapor, nama_terlapor, alamat_terlapor, gejala) VALUES (%s, %s, %s, %s, %s);"
                
                # Prepare the data values for the query
                values = (data['nik_pelapor'], data['nama_pelapor'], data['nama_terlapor'], data['alamat_terlapor'], data['gejala'])
                
                # Execute the SQL query with the provided values
                cursor.execute(query, values)

                # Commit the changes to the database
                connection.commit()
                
                # Close the cursor and database connection
                cursor.close()
                connection.close()
                
                # Redirect to the 'server1' route
                return redirect(url_for('server1'))
            else:
                # Return an error response if the content type is not JSON
                return jsonify({'error': 'Invalid content type. Expected application/json'}), 415
        elif request.method == 'GET':
            # Redirect to the 'server1' route for GET requests
            return redirect(url_for('server1'))
    
    except Error as e:
        # Handle and print any exceptions that occur
        print(f"Error: {e}")
        return 'Error storing data', 500

# Define a route for '/server_get_data'
@app.route('/server_get_data')
def get_data():
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect (
        user="root",
        password="12345",  # Use the correct parameter for the password
        host="localhost",
        database="COVID19"  # Use the correct parameter for the database name
    )
    
    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    
    # Define an SQL query to select data from the database
    query = "SELECT id, nik_pelapor, nama_terlapor, alamat_terlapor, gejala FROM LAPORCOVID"
    
    # Execute the SQL query
    cursor.execute(query)

    # Fetch all the data rows from the query result
    data = cursor.fetchall()
    
    # Close the cursor and database connection
    cursor.close()
    connection.close()

    # Convert the fetched data into a list of dictionaries
    data_list = [
        {
            'id': row[0],
            'nik_pelapor': row[1],
            'nama_terlapor': row[2],
            'alamat_terlapor': row[3],
            'gejala': row[4]
        }
        for row in data
    ]

    # Return the data as a JSON response
    return jsonify(data_list)

# Entry point of the application
if __name__ == "__main__":
    # Call a function 'create_db()' (not shown in the provided code) to create the database
    create_db()
    
    # Run the Flask app in debug mode on localhost and port 3000
    app.run(debug=True, port=3000, host='localhost')
