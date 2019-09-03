from flask import Flask, render_template, request,flash, redirect,request,abort,url_for
import pymysql
dbServerName    = "localhost"
dbUser          = "root"
dbPassword      = ""
dbName          = "quiz"
charSet         = "utf8mb4"
connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset=charSet,cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

@app.route("/")
def student():
   return render_template('register.html')
def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)
app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

@app.route("/register",methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      fname = str(request.form['fname'])
      lname = request.form['lname']
      gender = request.form['gender']
      branch = request.form['branch']
      year = request.form['year']
      email = request.form['email']
      interest = request.form['interest']
      uname = request.form['uname']
      pswd = request.form['pswd']

      try:
	cursorObject = connectionObject.cursor()
	insertStatement = "INSERT INTO  Regester(FirstName,LastName,Gender,Year,Branch,Email,Interests,Username,Password)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	cursorObject.execute(insertStatement,(fname,lname,gender,year,branch,email,interest,uname,pswd))
	sqlQuery    = "select * from Regester"
	cursorObject.execute(sqlQuery)
	rows = cursorObject.fetchall()
	for row in rows:
	   print(row)
      except Exception as e:
	print("Exeception occured:{}".format(e))
      finally:
	connectionObject.commit()
	connectionObject.close()
      result = request.form
      #return render_template("profile.html",result = result)
      return render_template('register.html') 
if __name__ == '__main__':
   app.run(debug = True,use_reloader=True)

