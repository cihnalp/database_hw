from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL
import MySQLdb.cursors 

app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['MYSQL_HOST'] = 'eu-cdbr-west-03.cleardb.net'
app.config['MYSQL_USER'] = 'b1f6b4ddcecdda'
app.config['MYSQL_PASSWORD'] = 'c90fb2a2'
app.config['MYSQL_DB'] = 'heroku_b149c46afedacc5'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute('SELECT COUNT(*) FROM donate') 
    d = cursor.fetchone()
    cursor.execute('SELECT COUNT(*) FROM user') 
    u = cursor.fetchone() 
    cursor.execute('SELECT COUNT(*) FROM hospital') 
    h = cursor.fetchone() 
    cursor.execute('SELECT COUNT(*) FROM stock') 
    s = cursor.fetchone()
    return render_template('index.html',s=s,h=h,u=u,d=d) 



@app.route('/login', methods=['GET', 'POST'])
def giris():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM user WHERE user_name = % s AND user_password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['ifhospital'] = False
            session['logged_in'] = True
            session['username'] = account['user_name']
            session['name'] = account['name_surname']
            session['blood_group'] = account['blood_group']
            session['region_id'] = account['region_id']
            session['telno'] = account['telephone_no']
            return redirect(url_for('profil')) 
        else: 
            msg = 'Kulanıcı Adı/Parola Yanlış!'
    return render_template('login.html', msg = msg) 

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['ifhospital'] = False
    session['logged_in'] = False
    return  redirect(url_for('homepage'))
   
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'parola' in request.form and 'sehir' in request.form and 'telno' in request.form and 'kangrubu' in request.form and 'isim' in request.form: 
        details = request.form
        user_name = (details['username'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM user WHERE user_name = % s', (user_name, ))  
        account = cursor.fetchone()
        if account:
            msg = "Bu kullanıcı adı alınmıştır. Lütfen farklı bir kullanıcı adı deneyiniz."
            return render_template('register.html',msg = msg)
        else:
            user_password = details['parola']
            name = (details['isim'])
            blood_group = (details['kangrubu'])
            telephone_no = (details['telno'])
            region_id = int(details['sehir'])

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO user(user_name, name_surname, user_password, blood_group, telephone_no, region_id) VALUES (%s, %s, %s, %s, %s, %s);", (user_name, name, user_password, blood_group, telephone_no, region_id,))
            mysql.connection.commit()
            cur.close()
            msg="Kaydınız Başarıyla Gerçekleştirildi, Lütfen Giriş Yapınız."
            return render_template('success.html',msg=msg)
    elif request.method == 'POST':
        msg="Lütfen tüm değerleri giriniz."
        return render_template('register.html',msg=msg)
        
    return render_template('register.html')

@app.route('/registerhospital', methods=['GET', 'POST'])
def hospitalregister():
    if request.method == 'POST' and 'username' in request.form and 'parola' in request.form and 'sehir' in request.form: 
        details = request.form
        user_name = (details['username'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM hospital WHERE hospital_username = % s', (user_name, )) 
        account = cursor.fetchone() 
        if account:
            msg = "Bu kullanıcı adı alınmıştır. Lütfen farklı bir kullanıcı adı deneyiniz."
            return render_template('registerhospital.html',msg=msg)
        else:
            user_password = details['parola']
            name = (details['isim'])
            region_id = int(details['sehir'])

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO hospital(hospital_username, hospital_name, hospital_password, region_id) VALUES (%s, %s, %s, %s);", (user_name, name, user_password, region_id))
            mysql.connection.commit()
            cur.close()
            msg="Hastane Kaydı Başarılı, Sistemi Kullanmak İçin Lütfen Giriş Yapınız."
            return render_template('success.html',msg=msg)
    elif request.method == 'POST':
        msg="Lütfen tüm değerleri giriniz."
        return render_template('registerhospital.html',msg=msg)
    return render_template('registerhospital.html')

@app.route('/loginhospital', methods=['GET', 'POST'])
def hospitallogin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM hospital WHERE hospital_username = % s AND hospital_password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['ifhospital'] = True
            session['logged_in'] = True
            session['username'] = account['hospital_username']
            session['name'] = account['hospital_name']
            session['region_id'] = account['region_id']
            return redirect(url_for('profilhospital'))
        else: 
            msg = 'Kullanıcı Adı/Parola Yanlış'
    return render_template('loginhospital.html', msg = msg) 

@app.route('/profil', methods=['GET', 'POST'])
def profil():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT COUNT(*) FROM donate WHERE donator_username = %s',(session['username'],)) 
        a = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM need WHERE needy_username = %s',(session['username'],)) 
        b = cursor.fetchone() 
        return render_template('profil.html',a=a,b=b)

@app.route('/profilhospital', methods=['GET', 'POST'])
def profilhospital():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT COUNT(*) FROM need WHERE needy_hospitalusername = %s',(session['username'],)) 
        bb = cursor.fetchone()
        b = bb['COUNT(*)']
        return render_template('profilhospital.html',b=b)

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == "POST":
        details = request.form

        user_name = session['username']
        amount = int(details['amount'])
        region_id = session["region_id"]
        blood_group = session['blood_group']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO donate(donator_username, amount, region_id) VALUES (%s, %s, %s);", (user_name, amount, region_id))
        mysql.connection.commit()
        cur.close()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM stock WHERE region_id = % s', (region_id,)) 
        stok = cursor.fetchone() 

        if blood_group == 'ARh+':
            amount += stok['Arhp']
            cursor.execute("UPDATE stock SET Arhp = %s WHERE region_id = %s", (amount,region_id))
        elif blood_group == 'ARh-':
            amount += stok['Arhn']
            cursor.execute("UPDATE stock SET Arhn = %s WHERE region_id = %s", (amount,region_id))
        elif blood_group == 'BRh+':
            amount += stok['Brhp']
            cursor.execute("UPDATE stock SET Brhp = %s WHERE region_id = %s", (amount,region_id))
        elif blood_group == 'BRh-':
            amount += stok['Brhn']
            cursor.execute("UPDATE stock SET Brhn = %s WHERE region_id = %s", (amount,region_id))
        elif blood_group == '0Rh+':
            amount += stok['zerorhp']
            cursor.execute("UPDATE stock SET zerorhp = %s WHERE region_id = %s", (amount,region_id))
        elif blood_group == '0Rh-':
            amount += stok['zerorhn']
            cursor.execute("UPDATE stock SET zerorhn = %s WHERE region_id = %s", (amount,region_id))
        elif blood_group == 'ABRh+':
            amount += stok['ABrhp']
            cursor.execute("UPDATE stock SET ABrhp = %s WHERE region_id = %s", (amount,region_id))
        elif blood_group == 'ABRh-':
            amount += stok['ABrhn']
            cursor.execute("UPDATE stock SET ABrhn = %s WHERE region_id = %s", (amount,region_id))
        mysql.connection.commit()
        cursor.close()
        msg="Bağışınız Başarıyla Kaydedildi, En yakın kan merkezimize bekliyoruz."
        return render_template('success.html',msg=msg)
    return render_template('donate.html')

@app.route('/changecity', methods=['GET', 'POST'])
def changecity():
    if request.method == "POST":
        details = request.form
        user_name = session['username']
        yeni_sehir = int(details['sehir'])
        session['region_id'] = yeni_sehir
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE user SET region_id = %s WHERE user_name = %s", (yeni_sehir,user_name))
        mysql.connection.commit()
        cur.close()
        msg="Şehir Değiştirme İşleminiz Başarıyla Gerçekleştirildi."
        return render_template('success.html',msg=msg)
    return render_template('changecity.html')

@app.route('/deleteuser', methods=['GET', 'POST'])
def delete():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM user WHERE user_name = % s AND user_password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            user_name = account['user_name']
            cursor = mysql.connection.cursor()

            sorgu = "DELETE FROM user WHERE user_name = %s"
            cursor.execute(sorgu,(user_name,))
            sorgu = "DELETE FROM need WHERE needy_username = %s"
            cursor.execute(sorgu,(user_name,))
            mysql.connection.commit()
            session['logged_in'] = False
            msg="Tüm Talepleriniz Silindi, Hesabınız Sistemden Başarıyla Kaldırıldı."
            return render_template('success.html',msg=msg) 
        else: 
            msg = 'Kullanıcı Adı/Parola Hatalı.'
    return render_template('deleteuser.html', msg = msg) 


@app.route('/deletehospital', methods=['GET', 'POST'])
def deletehospital():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM hospital WHERE hospital_username = % s AND hospital_password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            user_name = account['hospital_username']
            cursor = mysql.connection.cursor()

            sorgu = "DELETE FROM hospital WHERE hospital_username = %s"
            cursor.execute(sorgu,(user_name,))

            sorgu = "DELETE FROM need WHERE needy_hospitalusername = %s"
            cursor.execute(sorgu,(user_name,))
            mysql.connection.commit()
            session['logged_in'] = False
            msg="Tüm Talepleriniz Silindi. Hastane Kaydınız Sistemden Başarıyla Kaldırıldı."
            return render_template('success.html',msg=msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('deletehospital.html', msg = msg) 

@app.route('/stok', methods=['GET', 'POST'])
def stock():
        region_id = session['region_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM stock WHERE region_id = % s', (region_id,)) 
        stok = cursor.fetchone() 
        
        return render_template('stok.html',stok = stok) 

@app.route('/mydonates', methods=['GET', 'POST'])
def mydonates():
        username = session['username']
        name = session['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM donate WHERE donator_username = % s', (username,)) 
        donate = cursor.fetchall() 
        
        return render_template('mydonates.html',donate = donate,name =name) 

@app.route('/alldonates', methods=['GET', 'POST'])
def alldonates():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute('SELECT donate.amount,donate.region_id,user.name_surname,user.blood_group FROM donate INNER JOIN user ON donate.donator_username=user.user_name') 
    donate = cursor.fetchall()

    return render_template('alldonates.html',donate = donate) 

@app.route('/need', methods=['GET', 'POST'])
def need():
    if request.method == "POST":
        details = request.form

        user_name = session['username']
        amount = int(details['amount'])
        region_id = session["region_id"]
        blood_group = details['kangrubu']
        comment = details['comment']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO need(needy_username, amount, region_id, blood_group, need_comment) VALUES (%s, %s, %s, %s, %s);", (user_name, amount, region_id, blood_group, comment))
        mysql.connection.commit()
        cur.close()
        msg="Talebiniz başarıyla oluşturuldu."
        return render_template('success.html',msg=msg)
    return render_template('need.html')

@app.route('/needhospital', methods=['GET', 'POST'])
def needhospital():
    if request.method == "POST":
        if request.form['amount']:
            details = request.form

            user_name = session['username']
            amount = int(details['amount'])
            region_id = session["region_id"]
            blood_group = details['kangrubu']
            comment = details['comment']

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO need(needy_hospitalusername, amount, region_id, blood_group, need_comment) VALUES (%s, %s, %s, %s, %s);", (user_name, amount, region_id, blood_group, comment))
            mysql.connection.commit()
            cur.close()
            msg="Talebiniz Başarıyla Oluşturuldu."
            return render_template('success.html',msg=msg)
        else:
            msg="Lütfen gerekli kan miktarını giriniz."
            return render_template('needhospital.html',msg=msg)
    return render_template('needhospital.html')

@app.route('/allneeds', methods=['GET', 'POST'])
def allneeds():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute('SELECT need.amount,need.region_id,need.blood_group,need.need_comment,user.name_surname FROM need INNER JOIN user ON need.needy_username=user.user_name') 
    needuser = cursor.fetchall()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cur.execute('SELECT need.amount,need.region_id,need.blood_group,need.need_comment,hospital.hospital_name FROM need INNER JOIN hospital ON need.needy_hospitalusername=hospital.hospital_username')
    needhospital = cur.fetchall()
    return render_template('allneeds.html',needuser = needuser,needhospital = needhospital) 

@app.route('/stoktaniste', methods=['GET', 'POST'])
def stoktaniste():
    if request.method == "POST" and 'amount' in request.form:
        if request.form['amount']:
            details = request.form
            amount = int(details['amount'])
            region_id = session["region_id"]
            blood_group = details['kangrubu']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM stock WHERE region_id = % s', (region_id,)) 
            stok = cursor.fetchone() 
            msg = "Stokta istenilen miktarda kan yok, Lütfen stok durumunu kontrol ediniz."
            if blood_group == 'ARh+':
                if amount > stok['Arhp']:
                    return render_template('stoktaniste.html', msg = msg)
                else:    
                    amount = stok['Arhp'] - amount
                    cursor.execute("UPDATE stock SET Arhp = %s WHERE region_id = %s", (amount,region_id))
            elif blood_group == 'ARh-':
                if amount > stok['Arhn']:
                    return render_template('stoktaniste.html', msg = msg)
                else:    
                    amount = stok['Arhn'] - amount
                    cursor.execute("UPDATE stock SET Arhn = %s WHERE region_id = %s", (amount,region_id))
            elif blood_group == 'BRh+':
                if amount > stok['Brhp']:
                    return render_template('stoktaniste.html', msg = msg)
                else:    
                    amount = stok['Brhp'] - amount
                    cursor.execute("UPDATE stock SET Brhp = %s WHERE region_id = %s", (amount,region_id))
            elif blood_group == 'BRh-':
                if amount > stok['Brhn']:
                    return render_template('stoktaniste.html', msg = msg)
                else:    
                    amount = stok['Brhn'] - amount
                    cursor.execute("UPDATE stock SET Brhn = %s WHERE region_id = %s", (amount,region_id))
            elif blood_group == '0Rh+':
                if amount > stok['zerorhp']:
                    return render_template('stoktaniste.html', msg = msg)
                else:       
                    amount = stok['zerorhp'] - amount
                    cursor.execute("UPDATE stock SET zerorhp = %s WHERE region_id = %s", (amount,region_id))
            elif blood_group == '0Rh-':
                if amount > stok['zerorhn']:
                    return render_template('stoktaniste.html', msg = msg)
                else:    
                    amount = stok['zerorhn'] - amount
                    cursor.execute("UPDATE stock SET zerorhn = %s WHERE region_id = %s", (amount,region_id))
            elif blood_group == 'ABRh+':
                if amount > stok['ABrhp']:
                    return render_template('stoktaniste.html', msg = msg)
                else:    
                    amount = stok['ABrhp'] - amount
                    cursor.execute("UPDATE stock SET ABrhp = %s WHERE region_id = %s", (amount,region_id))
            elif blood_group == 'ABRh-':
                if amount > stok['ABrhn']:
                    return render_template('stoktaniste.html', msg = msg)
                else:    
                    amount = stok['ABrhn'] - amount
                    cursor.execute("UPDATE stock SET ABrhn = %s WHERE region_id = %s", (amount,region_id))
            mysql.connection.commit()
            cursor.close()
            msg="Stokta Yeterli Kan Var, En Yakın Zamanda Hastanenize Ulaştırılacaktır."
            return render_template('success.html',msg=msg)

        elif request.method == "POST":
            msg="Lütfen Geçerli Bir Değer Girin."
            return render_template('stoktaniste.html',msg=msg)
    
    return render_template('stoktaniste.html')

@app.route('/changeneedhospital', methods=['GET', 'POST'])
def changeneedhospital():
    username = session['username']
    name = session['name']
    if request.method == "POST":
        details = request.form
        
        
        if details['amount']:
            amount = int(details['amount'])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM need WHERE needy_hospitalusername = % s AND need_id = %s', (username,amount))
            cont = cursor.fetchone()
        
            if cont:
                cursor = mysql.connection.cursor()
                sorgu = "DELETE FROM need WHERE need_id = %s"
                cursor.execute(sorgu,(amount,))
                mysql.connection.commit()
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM need WHERE needy_hospitalusername = % s', (username,)) 
                need = cursor.fetchall()
                msg = 'Talep başarıyla silindi.'   
                return render_template('changeneedhospital.html',need = need,name =name,msg = msg)
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                cursor.execute('SELECT * FROM need WHERE needy_hospitalusername = % s', (username,)) 
                need = cursor.fetchall()
                msg="Bu talebi silmeye yetkiniz yok"         
                return render_template('changeneedhospital.html',need = need,name =name,msg=msg) 
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM need WHERE needy_hospitalusername = % s', (username,)) 
            need = cursor.fetchall()
            msg="Lütfen bir değer giriniz."         
            return render_template('changeneedhospital.html',need = need,name =name,msg=msg) 
    else:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM need WHERE needy_hospitalusername = % s', (username,)) 
        need = cursor.fetchall()         
        return render_template('changeneedhospital.html',need = need,name =name) 

@app.route('/changeneed', methods=['GET', 'POST'])
def changeneed():
    if request.method == "POST":
        details = request.form
        
        username = session['username']
        name = session['name']
        if details['amount']:
            amount = int(details['amount'])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM need WHERE needy_username = % s AND need_id = %s', (username,amount)) 
            cont = cursor.fetchone()
            if cont:
                cursor = mysql.connection.cursor()
                sorgu = "DELETE FROM need WHERE need_id = %s"
                cursor.execute(sorgu,(amount,))
                mysql.connection.commit()
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                cursor.execute('SELECT * FROM need WHERE needy_username = % s', (username,)) 
                need = cursor.fetchall()
                msg = 'Talep başarıyla silindi.'  
                return render_template('changeneed.html',need = need,name =name,msg=msg)
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                cursor.execute('SELECT * FROM need WHERE needy_username = % s', (username,)) 
                need = cursor.fetchall()
                msg="Bu talebi silmeye yetkiniz yok"        
                return render_template('changeneed.html',need = need,name =name,msg=msg)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM need WHERE needy_username = % s', (username,)) 
            need = cursor.fetchall()
            msg="Lütfen bir değer giriniz."        
            return render_template('changeneed.html',need = need,name =name,msg=msg) 
    else:    
        username = session['username']
        name = session['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM need WHERE needy_username = % s', (username,)) 
        need = cursor.fetchall()         
        return render_template('changeneed.html',need = need,name =name) 


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


