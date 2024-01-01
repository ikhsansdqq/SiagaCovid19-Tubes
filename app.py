from datetime import datetime

import markdown2
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

user = "root"
pin = "Hoodwink77!"
host = "localhost"
db_name = "covid19"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_POOL_PRE_PING"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 5
app.config["SQLALCHEMY_POOL_USE_LIFO"] = True
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30

CORS(app, resources={r"/server": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db = SQLAlchemy(app)


class LaporCovid(db.Model):
    __tablename__ = "laporcovid"
    id = db.Column(db.String(10), primary_key=True, autoincrement=True)
    nik_pelapor = db.Column(db.String(16))
    nama_pelapor = db.Column(db.String(100))
    nama_terlapor = db.Column(db.String(100))
    alamat_terlapor = db.Column(db.String(100))
    gejala = db.Column(db.String(100))
    waktu_dilaporkan = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    try:
        nik_pelapor = request.form.get('nik_pelapor')
        nama_pelapor = request.form.get('nama_pelapor')
        nama_terlapor = request.form.get('nama_terlapor')
        alamat_terlapor = request.form.get('alamat_terlapor')
        gejala = request.form.get('gejala')

        if (any(char.isalpha() for char in nama_pelapor) and any(char.isdigit() for char in nama_pelapor)) and (
                any(char.isalpha() for char in nama_terlapor) and any(char.isdigit() for char in nama_terlapor)):
            return 'Your name has a number inside. Please try again.'
        elif nama_pelapor.replace('.', '', 1).isdigit() and nama_terlapor.replace('.', '', 1).isdigit():
            return 'Your name is a number? Please try again.'
        else:
            # server_url = "http://127.0.0.1:3000/server/add-data"
            server_url = "http://192.168.0.8:3000/server/server/add-data"

            data = {
                'nik_pelapor': nik_pelapor,
                'nama_pelapor': nama_pelapor,
                'nama_terlapor': nama_terlapor,
                'alamat_terlapor': alamat_terlapor,
                'gejala': gejala,
                'waktu_dilaporkan': datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            }

            requests.post(server_url, json=data)

            print('Form submitted sucessfully!', 'success')

            return redirect(url_for('pengaduan'))

    except Exception as e:
        print(f'Error submitting form: {str(e)}', 'danger')
        return f'An error occurred while processing your request. Please try again. {e}'


@app.route('/pengaduan')
def pengaduan():
    try:
        # response = requests.get(
        #     'http://127.0.0.1:3000/server')
        response = requests.get(
            'http://192.168.0.8:3000/server')
        if response.status_code == 200:
            reports = response.json()
            return render_template('pengaduan.html', reports=reports)
        else:
            return render_template('pengaduan.html', error="Failed to fetch data")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return render_template('pengaduan.html', error="An error occurred while fetching data")


@app.route('/delete/<int:id>', methods=['POST'])
def delete_report(id):
    try:
        query = text('DELETE FROM LAPORCOVID WHERE id = :id')
        db.session.execute(query, {'id': id})
        db.session.commit()

        print(f'Report with ID {id} deleted successfully!')
    except Exception as e:
        print(f'Error deleting report: {str(e)}')

    return redirect(url_for('pengaduan'))


@app.route('/pengaduan/<int:nik_pelapor>', methods=['GET', 'POST'])  # Updated route to include ID
def pengaduan_specific(nik_pelapor):
    try:
        # response = requests.get(f'http://127.0.0.1:3000/{nik_pelapor}')
        response = requests.get(f'http://192.168.0.8:3000/server/{nik_pelapor}')
        if response.status_code == 200:
            report = response.json()
            return render_template('pengaduan.html', report=report)
        else:
            return render_template('pengaduan.html', error="Failed to fetch data")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return render_template('pengaduan.html', error="An error occurred while fetching data")


@app.route('/how-it-works')
def guide():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    html_content = markdown2.markdown(content)
    return render_template('guideline.html', html_content=html_content)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
