#Importing important modules from Flask for web app development
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import json
import markdown2

#Creating a Flask web application instance
app = Flask(__name__)

#constructing the path to SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'site.db')

#configuring the Flask app with the database URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# data = {}

class Report(db.Model): #Defining a class so it represents a database table
    #defining database column
    id = db.Column(db.Integer, primary_key=True)
    nik_pelapor = db.Column(db.String(16), nullable=False)
    nama_pelapor = db.Column(db.String(100), nullable=False)
    nama_terlapor = db.Column(db.String(100), nullable=False)
    alamat_terlapor = db.Column(db.String(255), nullable=False)
    gejala = db.Column(db.String(255), nullable=False)


def fetch_reports_parallel(): #defining a function to fetch reports from database
    with app.app_context():
        reports = Report.query.all()
    return reports

def normal_fetch():  #defining another function for normal report fetching
    with app.app_context():
        reports = Report.query.all()
    return reports

@app.route('/', methods=['GET', 'POST']) #defining a route for the root URL with support for GET and POST methods
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST']) #degining a route for form submission with POST method
def submit():
    try:
        #retrieving data from the request
        nik_pelapor = request.form.get('nik_pelapor')
        nama_pelapor = request.form.get('nama_pelapor')
        nama_terlapor = request.form.get('nama_terlapor')
        alamat_terlapor = request.form.get('alamat_terlapor')
        gejala = request.form.get('gejala')

        server_url = "http://127.0.0.1:3000/server"

        #create a dictionary 'data' with form data
        data = {
            'nik_pelapor': nik_pelapor, 
            'nama_pelapor': nama_pelapor, 
            'nama_terlapor': nama_terlapor, 
            'alamat_terlapor': alamat_terlapor, 
            'gejala': gejala
        }

        json_string = json.dumps(data)  #converting thee dictionary to a JSON string

        requests.post(server_url, json=data) #sending a POST request to the server URL with JSON data

        # new_report = Report (
        #     nik_pelapor=nik_pelapor,
        #     nama_pelapor=nama_pelapor,
        #     nama_terlapor=nama_terlapor,
        #     alamat_terlapor=alamat_terlapor,
        #     gejala=gejala
        # )

        #printing data and its types (for debugging)
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



@app.route('/pengaduan') # Example route handling the redirection to the server
def pengaduan():
    try:
        response = requests.get('http://localhost:3000/server_get_data')  # Replace with the correct URL of the /getdata endpoint
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
    
@app.route('/delete/<int:report_id>', methods=['POST']) #defining a route for deleting a report with a specified ID ('/delete/<int:report_id>')
def delete_report(report_id):
    try:
        report = Report.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        print('Report deleted successfully!')
    except Exception as e:
        print(f'Error deleting report: {str(e)}')
    return redirect(url_for('pengaduan'))


@app.route('/how-it-works') #defining a route for displaying a guide on how it works ('/how-it-works')
def guide():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read() 
    html_content = markdown2.markdown(content) #converting the Markdown content to HTML
    return render_template('guideline.html', html_content=html_content)

#defining a route for a test page ('/test')
@app.route('/test')
def test():
    return render_template('test.html')

#run the Flask app if this script is the main entry point
if __name__ == '__main__':
    app.run()