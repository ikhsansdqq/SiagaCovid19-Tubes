from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS
import requests
import json
import markdown2

app = Flask(__name__)

CORS(app, resources={r"/server": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db = SQLAlchemy()

user = "root"
pin = "Hoodwink77!"
host = "localhost"
db_name = "covid19"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


class LaporCovid(db.Model):
    id = db.Column(db.String(10), primary_key=True, autoincrement=True)
    nik_pelapor = db.Column(db.String(16))
    nama_pelapor = db.Column(db.String(100))
    nama_terlapor = db.Column(db.String(100))
    alamat_terlapor = db.Column(db.String(100))
    gejala = db.Column(db.String(100))


def fetch_reports_parallel():
    with app.app_context():
        reports = LaporCovid.query.all()
    return reports


def normal_fetch():
    with app.app_context():
        reports = LaporCovid.query.all()
    return reports


@app.route('/', methods=['GET', 'POST'])  # defining a route for the root URL with support for GET and POST methods
def index():
    return render_template('index.html')


# STILL NEED TO FIX
@app.route('/submit', methods=['POST'])  # degining a route for form submission with POST method
def submit():
    try:
        # retrieving data from the request
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
            server_url = "http://127.0.0.1:3000/server/add-data"

            data = {
                'nik_pelapor': nik_pelapor,
                'nama_pelapor': nama_pelapor,
                'nama_terlapor': nama_terlapor,
                'alamat_terlapor': alamat_terlapor,
                'gejala': gejala
            }

            json_string = json.dumps(data)
            requests.post(server_url, json=data)

            print('Form submitted sucessfully!', 'success')

            # return redirect(url_for('pengaduan'))
            return redirect(url_for('pengaduan'))

    except Exception as e:
        print(f'Error submitting form: {str(e)}', 'danger')


@app.route('/pengaduan')  # Example route handling the redirection to the server
def pengaduan():
    try:
        response = requests.get(
            'http://127.0.0.1:3000/server')  # Replace with the correct URL of the /getdata endpoint
        if response.status_code == 200:
            reports = response.json()
            return render_template('pengaduan.html', reports=reports)
        else:
            # Handle cases where the request was not successful
            return render_template('pengaduan.html', error="Failed to fetch data")
    except requests.exceptions.RequestException as e:
        # Handle any exceptions during the request
        print(f"An error occurred: {e}")
        return render_template('pengaduan.html', error="An error occurred while fetching data")


@app.route('/delete/<int:id>', methods=['POST'])
def delete_report(id):
    try:
        # Execute a raw SQL query to delete the report with the specified ID
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
        # The URL now includes the ID to fetch specific data
        response = requests.get(f'http://127.0.0.1:3000/server/get-specific-data/{nik_pelapor}')
        if response.status_code == 200:
            report = response.json()
            return render_template('pengaduan.html', report=report)
        else:
            # Handle cases where the request was not successful
            return render_template('pengaduan.html', error="Failed to fetch data")
    except requests.exceptions.RequestException as e:
        # Handle any exceptions during the request
        print(f"An error occurred: {e}")
        return render_template('pengaduan.html', error="An error occurred while fetching data")


@app.route('/how-it-works')  # defining a route for displaying a guide on how it works ('/how-it-works')
def guide():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    html_content = markdown2.markdown(content)  # converting the Markdown content to HTML
    return render_template('guideline.html', html_content=html_content)


@app.route('/<int:nik>', methods=['GET', 'POST'])
def show_page_by_nik():
    # Bikin Placeholder buat search by NIK, page khusus
    # Antara nampilin JSON sesuai search/ nampilin lewat HTML

    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
