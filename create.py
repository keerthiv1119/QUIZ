from flask import Flask, render_template, request,flash, redirect,request,abort,url_for
import questionname
import pymysql
dbServerName    = "localhost"
dbUser          = "root"
dbPassword      = ""
dbName          = "quiz"
charSet         = "utf8mb4"
app = Flask(__name__)

@app.route("/")
def student():
   return render_template('create.html')
@app.route("/")
def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)
app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

@app.route("/",methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      question = request.form['question']
      option1=request.form['optiona']
      option2=request.form['optionb']
      option3=request.form['optionc']
      option4=request.form['optiond']
      try:
	connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset=charSet,cursorclass=pymysql.cursors.DictCursor)
	cursorObject = connectionObject.cursor()
	insertStatement = "INSERT INTO  User(QuizName,QuestionText,option1,option2,option3,option4)  VALUES (%s,%s,%s,%s,%s,%s)"
	cursorObject.execute(insertStatement,(globalquizname,question,option1,option2,option3,option4))
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
      return render_template('create.html') 
if __name__ == '__main__':
   app.run(debug = True,use_reloader=True)

