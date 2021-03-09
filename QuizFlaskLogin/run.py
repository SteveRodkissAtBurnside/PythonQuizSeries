from flask import Flask, g, render_template, redirect, request, url_for, flash
from flask_login.mixins import UserMixin
from flask_login.utils import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user

#################################################################################
#initialization

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

##################################################################################
#create a class to hold the data model
class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(200))
    answer = db.Column(db.String(200))
    #use the magic method __repr__ to display it when people use it.
    def __repr__(self):
        return f"{self.question} : {self.answer}"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(50))
    def __repr__(self):
        return f"Username: {self.username}"
    def check_password(self,password):
        return self.password == password

'''don't forget to create the databse using this model from the console!!!!!!!! Use Python repl
    >>>from run import db
    >>>db.create_all()
'''

#required for the user longin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) # Fetch the user from the database


#################################################################################
#   routes
#################################################################################

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        #we posted the form- try to login
        #get the user from the forms username field
        user = User.query.filter_by(username=request.form.get("username")).first()
        #chek if we got one and that the password's match- MUST USE HASHED PASSWORDS!!! THIS IS JUST A DEMO!!
        if user and user.check_password(request.form.get("password")):
            login_user(user)
            #now current_user is set to this user- redirect back to home
            return redirect(url_for("home"))
        #else flash a message?
        else:
            flash("Username and password not recognised")
    return render_template("login.html")

@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    '''log out the user- pretty self-explanatory'''
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    ''' Display all the questions- users click on  question to display it on a new page '''
    questions = Question.query.all()
    return render_template('home.html', questions=questions)

@app.route('/admin')
@login_required
def admin():
    '''the admin route to add and delete questions'''
    questions = Question.query.all()
    return render_template("admin.html", questions=questions)

@app.route('/delete_question', methods=['GET','POST'])
@login_required
def delete_question():
    #get the value og the hidden input named "question_id" in the html template if the form exists from the post
    if request.form:
        question_id = request.form.get("question_id")
        #and do sql stuff to remove it! find the question we want to dlete from it's id
        question_to_delete = Question.query.filter_by(id=question_id).first()
        db.session.delete(question_to_delete)#delete it
        db.session.commit()#commit change to db
    return redirect(url_for("admin"))

@app.route('/add_question', methods=['GET','POST'])
@login_required
def add_question():
    '''this will add a posted question to the database and redirect to the admin route again'''
    if request.form:
        #we got a form back now process by getting the items by their name
        new_question = request.form.get("question")#get questions from form
        new_answer = request.form.get("answer")     #get answer from form
        new_question = Question(question=new_question,answer=new_answer)  #create a new question instance
        db.session.add(new_question)    #add it and commit change to db
        db.session.commit()
    return redirect(url_for("admin"))

@app.route('/ask_question/<int:id>', methods=['GET','POST'])
def ask_question(id):
    '''ask the specific question passed by the parameter'''
    question_to_ask = Question.query.filter_by(id=id).first()
    '''check if we posted an answer and display the correct question and a flash to show correct/wrong'''
    if request.method == 'POST':
        #we posted, check answer
        user_answer = request.form.get("answer")
        #get the answer from the question entry in the database
        actual_answer = question_to_ask.answer
        if user_answer.lower() == actual_answer.lower():
            flash("You are correct!")
        else:
            flash("Sorry, you got it wrong :(")
    return render_template("ask_question.html",entry=question_to_ask)

if __name__ == "__main__":
    app.run(debug=True)

