import json

with open('quiz.json', 'r') as file:
    quiz_data = json.load(file)
    questions = quiz_data["questions"]


while(True):
    # Path: create_questions.py
    question = input("Enter a question: ")
    
    if(question == "done"):
        break

    possible_answers = []
    while (True):
        ans = input("Enter an answer: ")
        if(ans == "done"):
            break
        possible_answers.append(ans)

    answer = input("Enter the correct answer: ")
    quiz_data["questions"].append({"question": question, "options": possible_answers, "answer": answer})
    
    quiz_file = open("quiz.json", 'w')
    quiz_file.write(json.dumps(quiz_data))
    quiz_file.close()
        

