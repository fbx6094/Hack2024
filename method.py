from flask import Flask, request, jsonify, render_template
import json
import requests

app = Flask(__name__)

data_file = 'parking_spots.txt'

def load_parking_spots():
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_parking_spots(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

parking_spots = load_parking_spots()

@app.route('/api/parking_spots/add', methods=['POST'])
def add_parking_spot():
    new_spot = request.json

    required_fields = ["polygonCoordinates", "price", "centerCoordinate"]
    if not all(field in new_spot for field in required_fields):
        return jsonify({"status": "error", "message": "Недостаточно данных"}), 400

    for coord in new_spot["polygonCoordinates"]:
        if not all(key in coord for key in ["latitude", "longitude"]):
            return jsonify({"status": "error", "message": "Некорректные координаты"}), 400

    if not all(key in new_spot["centerCoordinate"] for key in ["latitude", "longitude"]):
        return jsonify({"status": "error", "message": "Некорректные координаты центра"}), 400

    parking_spots.append(new_spot)

    save_parking_spots(parking_spots)

    return jsonify({"status": "success", "message": "Парковочное место добавлено"}), 201

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        response = requests.get(f"https://parking.pythonanywhere.com/api/parking_spots?phone_number={phone_number}")
        if response.status_code == 200:
            data = response.json()
            return render_template('index.html', data=data)
        else:
            return render_template('auth.html', error="Invalid phone number or API error")
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(debug=True)