from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import json
import markdown2

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'site.db')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# data = {}

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nik_pelapor = db.Column(db.String(16), nullable=False)
    nama_pelapor = db.Column(db.String(100), nullable=False)
    nama_terlapor = db.Column(db.String(100), nullable=False)
    alamat_terlapor = db.Column(db.String(255), nullable=False)
    gejala = db.Column(db.String(255), nullable=False)


def fetch_reports_parallel():
    with app.app_context():
        reports = Report.query.all()
    return reports

def normal_fetch():
    with app.app_context():
        reports = Report.query.all()
    return reports

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

        server_url = "http://127.0.0.1:3000/server"

        data = {
            'nik_pelapor': nik_pelapor, 
            'nama_pelapor': nama_pelapor, 
            'nama_terlapor': nama_pelapor, 
            'alamat_terlapor': alamat_terlapor, 
            'gejala': gejala
        }

        json_string = json.dumps(data)

        requests.post(server_url, json=data)

        # new_report = Report (
        #     nik_pelapor=nik_pelapor,
        #     nama_pelapor=nama_pelapor,
        #     nama_terlapor=nama_terlapor,
        #     alamat_terlapor=alamat_terlapor,
        #     gejala=gejala
        # )

        # db.session.add(new_report)
        # db.session.commit()
        print(data)
        print(type(data))
        print(json_string)
        print(type(json_string))
        print('Form submitted sucessfully!', 'success')
    except Exception as e:
        print(f'Error submitting form: {str(e)}', 'danger')

    # return redirect(url_for('pengaduan'))
    return redirect(url_for('redirect_to_server'))

# Example route handling the redirection to the server
@app.route('/redirect-to-server')
def redirect_to_server():
    # Use the absolute URL
    return redirect('http://127.0.0.1:3000/server')


@app.route('/pengaduan')
def pengaduan():
    reports = Report.query.all()

    if not reports:
        return render_template('pengaduan.html', no_data=True)
    else:
        return render_template('pengaduan.html', reports=reports)
    

@app.route('/delete/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    try:
        report = Report.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        print('Report deleted successfully!')
    except Exception as e:
        print(f'Error deleting report: {str(e)}')
    return redirect(url_for('pengaduan'))


@app.route('/how-it-works')
def guide():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    html_content = markdown2.markdown(content)
    return render_template('guideline.html', html_content=html_content)


@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run()