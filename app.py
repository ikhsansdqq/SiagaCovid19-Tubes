from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/pengaduan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def pengaduan():
    return render_template('pengaduan.html')

@app.route('/creator')
def creator():
    return 'Creator Page'

if __name__ == '__main__':
    app.run(debug=True, host="192.168.0.13")