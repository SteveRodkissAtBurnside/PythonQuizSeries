from flask import Flask, g
import sqlite3

from flask.templating import render_template

#set up the app and db at the top so accessable to all code
app = Flask(__name__)
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
    return "Hello World"

@app.route("/all_questions")
def all_questions():
    cursor = get_db().cursor()
    sql = "SELECT * FROM questions"
    cursor.execute(sql)
    questions = cursor.fetchall()
    return render_template("all_questions.html", questions=questions)


@app.route("/admin")
def admin():
    '''the admin route to add and remove questions- get all the current questions and send them to admin page'''
    cursor = get_db().cursor()
    sql = "SELECT * FROM questions"
    cursor.execute(sql)
    questions = cursor.fetchall()
    return render_template("admin.html", questions=questions)


##############################################################################################################################
#Run the main program and start the app
if __name__ == "__main__":
    app.run(debug=True)