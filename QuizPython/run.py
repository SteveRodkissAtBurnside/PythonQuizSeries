"""
Really sinple quiz program using two arrays for questions and answers
By Steve Rodkiss
"""

#data
questions = ["What is 1+1?", "What is the fastest animal on the planet?", "what is the capital of NZ?"]
answers = ["2","cheetah","wellington"]

def add_question(question, answer):
    '''add a question and an answer to the question/answer lists'''
    questions.append(question)
    answers.append(answer)

def delete_question(i):
    '''delete the question at a particular index i'''
    if i in range(len(questions)):
        questions.pop(i)
        answers.pop(i)

def display_questions_and_answers():
    print("Question                                          Answer")
    for i in range(len(questions)):
        print(f"{questions[i]:<50}{answers[i]:<50}")

def ask_question(i):
    '''Ask a particular question and return true if correct answer is given, false if wrong'''
    if i in range(len(questions)):
        #we are not out of range
        answer = input(questions[i] + "\n")
        if answer.lower() == answers[i]:
            return True
        else:
            return False


print("Hello and welcome to my quiz")
score = 0
for i in range(len(questions)):
    if ask_question(i) == True:
        print("Correct")
        score += 1
    else:
        print("Sorry- Wrong Answer")

print(f"Your final score was {score}\n")
