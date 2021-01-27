"""
Really sinple quiz program using two arrays for questions and answers
By Steve Rodkiss
"""

#data
questions = ["What is 1+1?", "What is the fastest animal on the planet?", "what is the capital of NZ?"]
answers = ["2","cheetah","wellington"]

print("Hello and welcome to my quiz")
score = 0
for i in range(len(questions)):
    answer = input(questions[i]+"\n").lower()
    if answer == answers[i]:
        print("Correct!\n")
        score += 1
    else:
        print("Sorry that is incorrect\n")
print(f"Your final score was {score}\n")