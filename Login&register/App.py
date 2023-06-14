from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users_login WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        
        if user:
            # User logged in successfully
            return 'Login Successful'
        else:
            # Invalid credentials
            return 'Invalid Username or Password'
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users_login (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        
        return 'Account created successfully' 
    
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)