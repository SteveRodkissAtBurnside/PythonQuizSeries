"""Really simple quiz like the quiz python but now with an sqlite database"""
import sqlite3
from sqlite3.dbapi2 import Connection

#get connection- local path to the folder thats open- so for this app, its in the PythonQuizSeries Folder (not the QuizSQLite folder!!!)
db = sqlite3.connect("quiz.db")
#create a row factory with it so we get useful stuff back from quesry rather that tuples
db.row_factory = sqlite3.Row


def show_all_questions(db: Connection):
    '''print out all the questions nicly- using a type hint to help code completions!!'''
    cursor = db.cursor()
    #get all results
    sql = "SELECT * FROM questions"
    cursor.execute(sql)
    results = cursor.fetchall()
    print("id        Question                                          Answer")
    for result in results:
        print(f"{result['id']:<10}{result['question']:<50}{result['answer']:<50}")


def delete_question_with_id(db:Connection, id):
    '''delete the question with the given id from the database'''
    cursor = db.cursor()
    sql = "DELETE FROM questions WHERE id=?"
    cursor.execute(sql,(id,))    #exectue the sql passing a tuple to replace the question mark(s)
    db.commit()


def add_question(db, question, answer):
    cursor = db.cursor()
    entry = (question,answer)
    sql = "INSERT INTO questions(question,answer) VALUES (?,?);"
    cursor.execute(sql,entry)
    db.commit()

def get_all_questions(db:Connection):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM questions")
    results = cursor.fetchall()
    return results

#main game loop
score = 0
questions = get_all_questions(db)
for question in questions:
    answer = input(question['question']+"\n")
    if answer.lower() == question['answer'].lower():
        print("Correct!")
        score += 1
    else:
        print("Wrong!")
print(f"Your score was {score}/{len(questions)}")

db.close()
