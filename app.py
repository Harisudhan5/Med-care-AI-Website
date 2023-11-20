from flask import Flask, render_template,url_for,request,session,redirect,make_response
import warnings
import requests
import json
import mysql.connector
import pdfkit

app = Flask(__name__)


# Configure the MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2580'
app.config['MYSQL_DB'] = 'health'

# Configure the secret key for sessions
app.secret_key = '7645ewsrdguset45!^@$&#%tgrd65(&%0)^%$RFGdtexe142rs!t'

def get_db():
    db_config = {
        "host": app.config['MYSQL_HOST'],
        "user": app.config['MYSQL_USER'],
        "password": app.config['MYSQL_PASSWORD'],
        "database": app.config['MYSQL_DB']
    }

    # Create a database connection
    db = mysql.connector.connect(**db_config)
    return db

@app.route('/')
def new():
    if "user" in session:
        print(session)
        return render_template('video_call.html')
    else:
        return render_template('index.html')
    

@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/login')
def login():
    return render_template("signin.html")


'''@app.route('/')
def index():
    return  render_template("index.html")'''

@app.route('/signups', methods=['GET', 'POST'])
def signups():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('phone')
        state = request.form.get('state')
        email = request.form.get('email')
        password = request.form.get('password')

        curs = get_db()
        cursor = curs.cursor()

        cursor.execute("INSERT INTO user (name,number,email,state,password) VALUES (%s, %s, %s, %s, %s)",(name,number,email,state,password))
        curs.commit()
        cursor.close()

        return render_template('index.html')
    else:
        return render_template('signup.html')

@app.route('/logins',methods=['POST','GET'])
def logins():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        curs = get_db()
        cursor = curs.cursor()

        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s",(email,password))

        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template("user.html")
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")
    
@app.route('/pdf',methods=["POST","GET"])
def pdf():
    return ""
    
@app.route('/video_call')
def video_call():
    return render_template("video_call.html")

@app.route('/details')
def details():
    return render_template("details.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
@app.route('/doctor')
def doctor():
    return render_template("doctor.html")

if __name__ == "__main__":
    app.run(debug=True,port = 8081)