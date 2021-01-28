"""Really simple quiz like the quiz python but now with an sqlite database"""
import sqlite3
from sqlite3.dbapi2 import Connection

#get connection- local path to the folder thats open
db = sqlite3.connect("./QuizSQLite/quiz.db")

def show_all_questions(db: Connection):
    '''print out all the questions nicly- using a type hint to help code completions!!'''
    cursor = db.cursor()
    #get all results
    sql = "SELECT * FROM questions"
    cursor.execute(sql)
    results = cursor.fetchall()
    print("id        Question                                          Answer")
    for result in results:
        print(f"{result[0]:<10}{result[1]:<50}{result[2]:<50}")


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
    answer = input(question[1]+"\n")
    if answer.lower() == question[2].lower():
        print("Correct!")
        score += 1
    else:
        print("Wrong!")


db.close()
