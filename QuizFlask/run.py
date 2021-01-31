from flask import Flask, g, request, redirect, url_for, render_template, flash
import sqlite3

#set up the app and db at the top so accessable to all code
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#create the connection and the closing of connection- from https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
#database file as a constant
DATABASE = "quiz.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

############################################################################################################################
'''Region for all the routes'''
@app.route("/")
def home():
    cursor = get_db().cursor()
    sql = "SELECT * FROM questions"
    cursor.execute(sql)
    questions = cursor.fetchall()
    return render_template("home.html", questions=questions)

#dynamic routing- get the id from the anchir tag clicked in the home page- send the correct question to the ask_question template
@app.route("/ask_question/<int:id>", methods=["GET","POST"])
def ask_question(id):
    '''get the specific question and put it on the page'''
    cursor = get_db().cursor()
    sql = "SELECT id,question,answer FROM questions WHERE id=?"
    cursor.execute(sql,(id,))
    entry = cursor.fetchone()
    if request.method == "POST":
        '''we posted- check answer and flash message'''
        actual_answer = entry['answer']
        user_answer = request.form.get("answer")
        if user_answer.lower() == actual_answer.lower():
            flash("Correct")
        else:
            flash("Incorrect")

    return render_template("ask_question.html",entry=entry)

@app.route("/admin")
def admin():
    '''the admin route to add and remove questions- get all the current questions and send them to admin page'''
    cursor = get_db().cursor()
    sql = "SELECT * FROM questions"
    cursor.execute(sql)
    questions = cursor.fetchall()
    return render_template("admin.html", questions=questions)

@app.route("/add_question", methods=['GET','POST'])
def add_question():
    '''this will add a posted question to the database and redirect to the admin route again'''
    if request.form:
        #we got a form back now process by getting the items by their name
        question = request.form.get("question")
        answer = request.form.get("answer")
        sql = "INSERT INTO questions(question,answer) VALUES(?,?)"
        cursor = get_db().cursor()
        cursor.execute(sql,(question,answer))
        get_db().commit()
    return redirect(url_for("admin"))

@app.route("/delete_question", methods=["GET","POST"])
def delete_question():
    #get the value og the hidden input named "question_id" in the html template
    if request.form:
        question_id = request.form.get("question_id")
        #and do sql stuff to remove it!
        cursor = get_db().cursor()
        sql = "DELETE FROM questions WHERE id=?"
        cursor.execute(sql,(question_id,))
        get_db().commit()
    return redirect(url_for("admin"))





##############################################################################################################################
#Run the main program and start the app
if __name__ == "__main__":
    app.run(debug=True)