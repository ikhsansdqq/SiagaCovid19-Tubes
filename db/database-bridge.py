import pymysql
from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
CORS(app, resources={r"/server": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db = SQLAlchemy()

user = "root"
pin = "Hoodwink77!" # ISI PASSWORD MYSQL
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

@app.route('/server1/add', methods=['GET', 'POST'])
def add_laporan():
    if request.method == "POST":
        nik_pelapor = request.form.get('nik_pelapor')
        nama_pelapor = request.form.get('nama_pelapor')
        alamat_terlapor = request.form.get('alamat_terlapor')
        gejala = request.form.get('gejala')

        add_details = Books (
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
@app.route('/server', methods=['GET', 'POST'])
def handle_form_data():
    try:
        if request.is_json:
            data = request.get_json()
            connection = mysql.connector.connect (
                user="root",
                password="Hoodwink77!",  # Use the correct parameter for the password
                host="localhost",
                database="COVID19"  # Use the correct parameter for the database name
            )

            cursor = connection.cursor()

            query = "INSERT INTO LAPORCOVID (nik_pelapor, nama_pelapor, nama_terlapor, alamat_terlapor, gejala) VALUES (%s, %s, %s, %s, %s);"
            values = (data['nik_pelapor'], data['nama_pelapor'], data['nama_terlapor'], data['alamat_terlapor'], data['gejala'])
            cursor.execute(query, values)

            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('server1'))
        else:
            return jsonify({'error': 'Invalid content type. Expected application/json'}), 415
        
    except Error as e:
        print(f"Error: {e}")
        return 'Error storing data', 500


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=3000, host='localhost')