import requests
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        response = requests.get(f"https://parking.pythonanywhere.com/api/parking_history?phone_number={phone_number}")
        if response.status_code == 200:
            data = response.json()
            return render_template('index.html', data=data)
        else:
            return render_template('auth.html', error="Invalid phone number or API error")
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(debug=True)
    