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
            <html>
            <head>
                <title>Parking History</title>
            </head>
            <body>
                <table border="1">
                    <tr>
                        <th>Дата</th>
                        <th>Время нахождения</th>
                        <th>Местоположение</th>
                    </tr>
            """
            for history in data["parking_history"]:
                html += f"""
                    <tr>
                        <td>{history['date']}</td>
                        <td>{history['duration']}</td>
                        <td>{history['location']}</td>
                    </tr>
                """
            html += """
                </table>
            </body>
            </html>
            """
            return html
        else:
            return "Ошибка авторизации!"
    return """
    <html>
    <head>
        <title>Parking History</title>
    </head>
    <body>
        <h1>Вход</h1>
        <form action="" method="post">
            <input type="text" name="phone_number" placeholder="Номер телефона">
            <input type="submit" value="Вход">
        </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)