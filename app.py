import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        response = requests.get(f"https://parking.pythonanywhere.com/api/parking_history?phone_number={phone_number}")
        if response.status_code == 200:
            data = response.json()
            html = """


if __name__ == '__main__':
    app.run(debug=True)