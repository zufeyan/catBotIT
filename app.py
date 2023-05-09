from flask import Flask, render_template, request, url_for, flash,session
from werkzeug.utils import redirect
from flask_mysqldb import MySQL,MySQLdb
import bcrypt


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'




mysql = MySQL(app)
@app.route('/')
def log():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')
    



#REGISTER

@app.route('/register', methods= ["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (name,email,password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = name
        session['email'] = email
        session['password']= password   
        return redirect(url_for("user"))
    
    
#LOGIN ด้วย email----------

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password'].encode('utf-8')

#         cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cur.execute('SELECT * FROM user WHERE email = %s', (email,))
#         user = cur.fetchone()
#         cur.close()

#         if bcrypt.hashpw(password,user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
#             session['name'] = user['name']
#             session['email'] = user['email']
#             flash('You have successfully logged in.')
#             return render_template('index.html')
#         else:
#             return "erorr"
#     else:
#         return render_template('login.html')
    

# LOGIN ด้วย user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM user WHERE name = %s', (name,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            session['name'] = user['name']
            flash('You have successfully logged in.')
            return render_template('index.html')
        else:
            flash('รหัสผิด')
            return render_template('login.html' )
    else:
        return render_template('login.html')

    

# LOGOUT--------------

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")








# INSERT---------
    
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        question = request.form['question']
        answer = request.form['answer']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO message (question, answer) VALUES (%s, %s)", (question, answer))
        mysql.connection.commit()
        return redirect(url_for('message'))


# DELETE
@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM message WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('message'))


#UPDATE -------

@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        question = request.form['question']
        answer = request.form['answer']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE message SET question=%s, answer=%s WHERE id=%s", (question, answer, id_data))
        mysql.connection.commit()
        flash("บันทึกแล้ว")
        cur.close()
        return redirect(url_for('message'))
    


# MESSAGE---

@app.route('/message')
def message():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM message")
    row = cur.fetchall()
    cur.close()
    mysql.connection.commit()
    return render_template("message.html" , data=row)



@app.route('/user')
def user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    user = cur.fetchall()
    cur.close()
    mysql.connection.commit()
    return render_template("user.html", user=user)


# delete user

@app.route('/delete_user/<string:id_data>', methods = ['GET'])
def delete_user(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('user'))


#update user
@app.route('/update_user', methods= ['POST', 'GET'])
def update_user():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user SET name=%s, password=%s WHERE id=%s", (name, password, id_data))
        mysql.connection.commit()
        flash("บันทึกแล้ว")
        cur.close()
        return redirect(url_for('user'))
    



#RUN-------

if __name__ == "__main__":
    app.run(debug=True)
