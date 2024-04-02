from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import hashlib

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MariaDB 연결 정보
db = pymysql.connect(host='tatamama.iptime.org',
                     port=3306,
                     user='sw',
                     password='SWen2402@#',
                     database='sw',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256()
        hashed_password.update(password.encode('utf-8'))
        password = hashed_password.hexdigest()

        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            db.commit()
            session['username'] = username
            return redirect(url_for('home'))
        except Exception as e:
            db.rollback()
            return str(e)
        finally:
            cursor.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(password)

        hashed_password = hashlib.sha256()
        hashed_password.update(password.encode('utf-8'))
        password = hashed_password.hexdigest()

        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5005, debug=True)
