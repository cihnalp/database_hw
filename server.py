from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'blood_donation_system'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form

        user_name = (details['isim'])
        user_password = details['parola']
        blood_group = (details['kangrubu'])
        telephone_no = (details['telno'])
        region_id = int(details['sehir'])

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO user(user_name, user_password, blood_group, telephone_no, region_id) VALUES (%s, %s, %s, %s, %s);", (user_name, user_password, blood_group, telephone_no, region_id))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)