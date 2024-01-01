from datetime import datetime

import mysql.connector
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from mysql.connector import Error

app = Flask(__name__)
CORS(app, resources={r"/server": {"origins": "*"}})  # enabling CORS for the '/server' route

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Hoodwink77!",
    "database": "COVID19",
}

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:Hoodwink77!@localhost/covid19"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_POOL_PRE_PING"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 5
app.config["SQLALCHEMY_POOL_USE_LIFO"] = True
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30

db = SQLAlchemy()
db.init_app(app)


class LaporCovid(db.Model):
    __tablename__ = "laporcovid"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nik_pelapor = db.Column(db.String(16))
    nama_pelapor = db.Column(db.String(100))
    nama_terlapor = db.Column(db.String(100))
    alamat_terlapor = db.Column(db.String(100))
    gejala = db.Column(db.String(100))

    waktu_dilaporkan = db.Column(db.DateTime, default=datetime.utcnow)


def create_db():
    with app.app_context():
        db.create_all()


# Use MySQL
@app.route('/server')
def server():
    try:
        details = LaporCovid.query.order_by(LaporCovid.id).all()

        details_list = [
            {
                'id': entry.id,
                'nik_pelapor': entry.nik_pelapor,
                'nama_pelapor': entry.nama_pelapor,
                'nama_terlapor': entry.nama_terlapor,
                'alamat_terlapor': entry.alamat_terlapor,
                'gejala': entry.gejala,
                'waktu_dilaporkan': datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            }
            for entry in details
        ]

        return details_list

    except Exception as e:
        print('ERROR:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/server/add-data', methods=['GET', 'POST'])
def handle_form_data():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()

                connection = mysql.connector.connect(
                    user="root",
                    password="Hoodwink77!",
                    host="localhost",
                    database="COVID19"
                )

                cursor = connection.cursor()

                query = ("INSERT INTO LAPORCOVID (nik_pelapor, nama_pelapor, nama_terlapor, alamat_terlapor, "
                         "gejala) VALUES (%s, %s, %s, %s, %s);")

                # Prepare the data values for the query
                values = (data['nik_pelapor'], data['nama_pelapor'], data['nama_terlapor'], data['alamat_terlapor'],
                          data['gejala'], data['waktu_dilaporkan'])

                cursor.execute(query, values)

                connection.commit()

                cursor.close()
                connection.close()

                return redirect(url_for('server'))
            else:
                return jsonify({'error': 'Invalid content type. Expected application/json'}), 415
        elif request.method == 'GET':
            return redirect(url_for('server'))

    except Error as e:
        print(f"Error: {e}")
        return 'Error storing data', 500


@app.route('/<int:nik_pelapor>')
def get_specific_data():
    try:
        details = LaporCovid.query.all()

        if not details:
            return jsonify({'error': 'Data not found for the specified nik_pelapor'}), 404

        details_list = [
            {
                'id': entry.id,
                'nik_pelapor': entry.nik_pelapor,
                'nama_pelapor': entry.nama_pelapor,
                'nama_terlapor': entry.nama_terlapor,
                'alamat_terlapor': entry.alamat_terlapor,
                'gejala': entry.gejala,
                'waktu_dilaporkan': entry.waktu_dilaporkan
            }
            for entry in details
        ]

        return jsonify(details_list)

    except Exception as e:
        print('ERROR:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=3000)
