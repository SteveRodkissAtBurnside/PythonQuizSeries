"""Really simple quiz like the quiz python but now with an sqlite database"""
import sqlite3

#get connection- local path to the folder thats open
db = sqlite3.connect("./QuizSQLite/quiz.db")

cursor = db.cursor()
sql = "SELECT * FROM questions"
cursor.execute(sql)
results = cursor.fetchall()
print(results)

db.close()
