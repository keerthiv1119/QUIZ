from flask import Flask, render_template, request,redirect,url_for,session, abort,flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import os
import pymysql
dbServerName    = "localhost"
dbUser          = "root"
dbPassword      = ""
dbName          = "quiz"
charSet         = "utf8mb4"
connectionObject   = pymysql.connect(host=dbServerName, user=dbUser,    				     password=dbPassword,db=dbName,charset=charSet,cursorclass=pymysql.cursors.DictCursor)
cursorObject = connectionObject.cursor()
globalquizname = ""
app = Flask(__name__)
@app.route('/index') 
def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)
app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string
@app.route('/') 
def index():
	app.secret_key = os.urandom(24)
   	return render_template('index.html')
@app.route('/login') 
def login():
	return render_template('login.html',login_var = 0)
@app.route('/login',methods = ['POST','GET'])  
def action_login():
	session['logged_in'] = False
	if request.form['button'] == 'forgot':
		return redirect(url_for('forgot'))
	elif request.form['button'] == 'register':
		return redirect(url_for('register'))
	elif request.form['button'] == 'login':
		x = 0
		uname = request.form['uname']
		print(uname)
	      	pswd = request.form['pswd']
		print(pswd)
		cursorObject = connectionObject.cursor()
		Username    = "select Username,Password from Register"
		cursorObject.execute(Username)
		usernames = cursorObject.fetchall()
		print(usernames)
		for row in usernames:
    			if row['Username'] == uname and row['Password'] == pswd:
        			session['logged_in'] = True
				global username
				username = row['Username']
				x = 1
				print("login succeded")
				return render_template("index.html")
				break
		if x==0:
			return render_template("login.html",login_var = 1)
	
@app.route('/logout')
def logout():
	session['logged_in'] = False
	return render_template("index.html")	
@app.route('/register')
def register():
	return render_template('register.html')
@app.route('/register',methods = ['GET','POST'])
def registration():
	if request.form['button'] == 'register':
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
			insertStatement = "INSERT INTO  Register(FirstName,LastName,Gender,Year,Branch,Email,Interests,Username,Password)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursorObject.execute(insertStatement,(fname,lname,gender,year,branch,email,interest,uname,pswd))
			sqlQuery    = "select * from Register"
			cursorObject.execute(sqlQuery)
			rows = cursorObject.fetchall()
			for row in rows:
		   		print(row)
	      	except Exception as e:
			print("Exeception occured:{}".format(e))
	      	finally:
			connectionObject.commit()
			result = request.form
			return redirect(url_for('login'))
@app.route('/quizname')
def quizname():
	return render_template("createquiz1.html")
@app.route('/quizname',methods = ['POST','GET'])
def actionquizname():
	if request.method == 'POST':
		 global globalquestionname
		 globalquestionname = request.form['quizname']
		 return redirect(url_for('createquiz'))
@app.route('/createquiz')
def createquiz():
	return render_template("create.html")
@app.route('/createquiz',methods = ['POST','GET'])
def createquestion():
	global count
	global maxcount
	maxcount = 1
	qcount = 1
	global op1,op2,op3,op4,quest
	op1=""
	op2=""
	op3=""
	op4=""
	quest=""
	if request.form['button'] == 'submit':
		question = request.form['question']
		option1=request.form['optiona']
		option2=request.form['optionb']
		option3=request.form['optionc']
		option4=request.form['optiond']
		try:
			cursorObject = connectionObject.cursor()
			insertquizid = "insert into Quizes(Username,Count) values (%s,%s)"
			cursorObject.execute(insertquizid,(username,qcount))
			connectionObject.commit()
			count = "select count(QuizId) from Quizes"
			cursorObject.execute(count)
			countdict = cursorObject.fetchone()
			quizid = countdict['count(QuizId)']
			insertStatement = "INSERT INTO  Questions(QuizName,QuizId,QuestionText,option1,option2,option3,option4,Answer)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
			cursorObject.execute(insertStatement,(globalquestionname,quizid,question,option1,option2,option3,option4,"A"))
			connectionObject.commit()
			questionscount = "select count(QuestionId) from Questions where QuizId = %s"
			cursorObject.execute(questionscount,quizid)
			questionscountdict = cursorObject.fetchone()
			questionsid = questionscountdict['count(QuestionId)']
			print(questionsid)
			updatequestions = "update Quizes set Count = %s where QuizId = %s"
			cursorObject.execute(updatequestions,(questionsid,quizid))
			connectionObject.commit()
			print("updated successfully")
		except Exception as e:
			print("Exeception occured:{}".format(e))
		finally:
			return redirect(url_for('index'))
	elif request.form['button'] == 'add':
		qcount = qcount + 1
		question = request.form['question']
		option1=request.form['optiona']
		option2=request.form['optionb']
		option3=request.form['optionc']
		option4=request.form['optiond']
		answer=request.form['answer']
		try:
			cursorObject = connectionObject.cursor()
			count = "select count(QuizId) from Quizes"
			cursorObject.execute(count)
			countdict = cursorObject.fetchone()
			quizid = countdict['count(QuizId)']
			quizidnext = int(quizid) + 1
			insertStatement = "INSERT INTO Questions(QuizName,QuizId,QuestionText,option1,option2,option3,option4,Answer)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursorObject.execute(insertStatement,(globalquestionname,quizidnext,question,option1,option2,option3,option4,answer))
			connectionObject.commit()
			print("insertion succeded")
		except Exception as e:
			print("Exeception occured:{}".format(e))
		finally:
			return redirect(url_for('createquiz'))
@app.route('/takequiz')
def takequiz():
	        try:
		        cursorObject = connectionObject.cursor()
			quizidStatement = "select QuizId from Quizes"
			cursorObject.execute(quizidStatement)
			rows = cursorObject.fetchall()
			global quiznames
			global quizids
			quiznames = []
			quizids = []
			print("hello")
			print(rows)
			for row in rows:
				quiznameStatement="select QuizName from Questions where QuizId=%s"
				
				cursorObject.execute(quiznameStatement,row['QuizId'])
				print(row['QuizId'])
				name = cursorObject.fetchone()
				print(name)
				quiznames.append(name['QuizName'])
				quizids.append(row['QuizId'])
			print(quiznames)
			print(quizids)
		except Exception as e:
			print("Exeception occured:{}".format(e))
		return render_template("takequiz.html",quiznames = quiznames)
@app.route('/takequiz',methods = ['POST','GET'])
def takequizquestion():
	if request.method == 'POST':
		global tempquizid
		if request.form['button'] == quiznames[0]:
			tempquizid = quizids[0]
		elif request.form['button'] == quiznames[1]:
			tempquizid = quizids[1]
		elif request.form['button'] == quiznames[2]:
			tempquizid = quizids[2]
		else:
			tempquizid = quizids[3]
		return redirect(url_for('question'))
@app.route('/question')
def question():
		try:
			cursorObject = connectionObject.cursor()
			getquestionStatement = "select QuestionId,QuestionText,option1,option2,option3,option4,Answer from Questions where QuizId=%s"
			
			cursorObject.execute(getquestionStatement,tempquizid)
			rows1 = cursorObject.fetchall()
			global displayquestions
			youranswers = []
			correctanswers = []
			displayquestions = rows1
			print(rows1)
			question = rows1[0]['QuestionText']
			option1 = rows1[0]['option1']
			option2 = rows1[0]['option2']
			option3 = rows1[0]['option3']
			option4 = rows1[0]['option4']
			print("entered question")
			global i
			i=0
			return render_template("question.html",i=i,question = question,option1 = option1,option2 = option2,option3 = option3,option4 = option4,ns = "Next")
		except Exception as e:
			print("Exeception occured:{}".format(e))
@app.route('/question',methods = ['POST','GET'])
def questionnext():
	if request.method == 'POST':
		try:
			#questionnext.c = 0
			#print(questionnext.c)
			global gcount
			cursorObject = connectionObject.cursor()
			print("connected")
			getcountstatement = "select Count from Quizes where QuizId = %s"
			cursorObject.execute(getcountstatement,tempquizid)
			getcount = cursorObject.fetchone()
			gcount = getcount['Count']
			print(gcount)
			i=int(request.form['no'])
			i = i+1
			print(i)
			#print("i="+str(i))
			global rows2
			global userid
			while i<gcount:
					getquestionStatement = "select QuestionId,QuestionText,option1,option2,option3,option4,Answer from Questions where QuizId=%s"
					cursorObject.execute(getquestionStatement,tempquizid)
					print("while loop")
					rows2 = cursorObject.fetchall()
					print(username)
					useridstatement = "select id from Register where Username = %s"
					cursorObject.execute(useridstatement,username)
					iduser = cursorObject.fetchone()
					
					userid = iduser['id']
					#questionnext.c = questionnext.c+1
					youranswer = request.form['answer']
					displayquestions[i-1]["YourAnswer"] = youranswer
					correctanswer = rows2[i-1]['Answer']
					questionid = rows2[i-1]['QuestionId']
					if youranswer == correctanswer:
						score = 1
					else:
						score = 0
					if gcount == i+1:
						ns = "Submit"
					else:
						ns = "Next"
					insertanswers = "insert into Participant(userid,quizid,questionid,CorrectAnswer,YourAnswer,score) values(%s,%s,%s,%s,%s,%s)"
					cursorObject.execute(insertanswers,(userid,tempquizid,questionid,correctanswer,youranswer,score))
					connectionObject.commit()
					question = rows2[i]['QuestionText']
					option1 = rows2[i]['option1']
					option2 = rows2[i]['option2']
					option3 = rows2[i]['option3']
					option4 = rows2[i]['option4']
					return render_template("question.html",i=i,question = question,option1 = option1,option2 = option2,option3 = option3,option4 = option4,ns = ns)
			youranswer = request.form['answer']
			displayquestions[i-1]["YourAnswer"] = youranswer
			correctanswer = rows2[i-1]['Answer']
			questionid = rows2[i-1]['QuestionId']
			if youranswer == correctanswer:
				score = 1
			else:
				score = 0
			insertanswers = "insert into Participant(userid,quizid,questionid,CorrectAnswer,YourAnswer,score) values(%s,%s,%s,%s,%s,%s)"
			cursorObject.execute(insertanswers,(userid,tempquizid,questionid,correctanswer,youranswer,score))
			connectionObject.commit()
			scorestatement = "select count(score) from Participant where QuizId = %s and score = %s and userid = %s"
			cursorObject.execute(scorestatement,(tempquizid,"1",userid))
			scorecount = cursorObject.fetchone()
			global yourscore
			yourscore = scorecount['count(score)']
			totalscorestatement = "select TotalScore from Register where id = %s"
			cursorObject.execute(totalscorestatement,userid)
			totalscore = cursorObject.fetchone()
			totalscore = totalscore['TotalScore']
			totalscore = int(totalscore)
			updatetscore = "update Register set TotalScore = %s where id = %s"
			cursorObject.execute(updatetscore,(totalscore+yourscore,userid))
			connectionObject.commit()
			insertleaderboard = "insert into leaderboard values(%s,%s,%s)"
			cursorObject.execute(insertleaderboard,(userid,tempquizid,yourscore))
			connectionObject.commit()
			return redirect(url_for('displayquestion'))
		except Exception as e:
			print("Exeception occured:{}".format(e))
@app.route('/displayquestion')
def displayquestion():
	return render_template("displayquestion.html",displayquestions = displayquestions,yourscore = yourscore)
@app.route('/leaderboard')
def leaderboard():
	leadersort = "select userid,score from leaderboard order by score desc"
	cursorObject.execute(leadersort)
	leadersortvalues = cursorObject.fetchall()
	allusernames = []
	allscores = []
	for leaders in leadersortvalues:
		userstatement = "select Username from Register where id = %s"
		cursorObject.execute(userstatement,leaders['userid'])
		leaderuser = cursorObject.fetchone()
		allusernames.append(leaderuser['Username'])
		allscores.append(leaders['score'])
	leadersortvalues[0]['rank'] = 1
	leadersortvalues[0]['username'] = allusernames[0]
	for t in range(1,len(allscores),1):
		if allscores[t] == allscores[t-1]:
			leadersortvalues[t]['username'] = allusernames[t]
			leadersortvalues[t]['rank'] = leadersortvalues[t-1]['rank']
		else:
			leadersortvalues[t]['username'] = allusernames[t]
			leadersortvalues[t]['rank'] = leadersortvalues[t-1]['rank'] + 1
	return render_template("leaderboard.html",leadersortvalues = leadersortvalues)
@app.route('/homeleaderboard')
def homeleaderboard():
	leadersorthome = "select id,TotalScore from Register order by TotalScore desc"
	cursorObject.execute(leadersorthome)
	leadersortvalues = cursorObject.fetchall()
	allusernames = []
	allscores = []
	for leaders in leadersortvalues:
		userstatement = "select Username from Register where id = %s"
		cursorObject.execute(userstatement,leaders['id'])
		leaderuser = cursorObject.fetchone()
		allusernames.append(leaderuser['Username'])
		allscores.append(leaders['TotalScore'])
		leaders['score'] = leaders['TotalScore']
	leadersortvalues[0]['rank'] = 1
	leadersortvalues[0]['username'] = allusernames[0]
	for t in range(1,len(allscores),1):
		if allscores[t] == allscores[t-1]:
			leadersortvalues[t]['username'] = allusernames[t]
			leadersortvalues[t]['rank'] = leadersortvalues[t-1]['rank']
		else:
			leadersortvalues[t]['username'] = allusernames[t]
			leadersortvalues[t]['rank'] = leadersortvalues[t-1]['rank'] + 1
	return render_template("leaderboard.html",leadersortvalues = leadersortvalues)
@app.route('/profile')
def profile():
	profilestatement="select * from Register where Username=%s"
	cursorObject.execute(profilestatement,username)
	profileinfo=cursorObject.fetchone()
	name=profileinfo["FirstName"]
	year=profileinfo["Year"]
	branch=profileinfo["Branch"]
	interests=profileinfo["Interests"]
	email=profileinfo["Email"]
	return render_template("profile.html",name=name,year=year,branch=branch,interests=interests,email=email,username=username)
@app.route('/forgot')
def forgot():
	return render_template("forgot.html")
@app.route('/forgot',methods = ['POST','GET'])
def forgotpass():
	if request.method=="POST":
		password=request.form['pswd']
		uname=request.form['uname']
		update="update Register set Password=%s where username=%s"
		cursorObject.execute(update,(password,uname))
		connectionObject.commit()
		return redirect(url_for('login'))
if __name__ == '__main__':
	app.jinja_env.cache = {}
   	app.run(debug = True)
