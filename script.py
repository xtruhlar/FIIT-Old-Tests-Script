import random
import os

def load_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

def split_questions(text):
    questions = []
    current_question = None
    for line in text.split('\n'):
        if line.strip() == '':
            if current_question:
                questions.append(current_question)
                current_question = None
        elif line[0].isdigit():
            if current_question:
                questions.append(current_question)
            current_question = {'question': line, 'answers': []}
        elif line.startswith('\t'):
            if current_question:
                current_question['answers'].append(line.strip())
    if current_question:
        questions.append(current_question)
    return questions

def get_answers(text):
    answers = {}
    for line in text.split('\n'):
        if line.strip() and line[0].isdigit():
            question_number, answer = line.split('.', 1)
            answers[question_number.strip()] = answer.strip()
    return answers

def normalize_answer(answer):
    normalized = set(answer.replace(',', '').lower().split())
    single_letter_answers = {a[0] for a in normalized if len(a) > 1 and a[1] == ')'}
    normalized.update(single_letter_answers)
    return normalized

def check_answer(question_number, user_answer, correct_answers):
    correct_answer = correct_answers.get(question_number)
    if correct_answer:
        user_set = normalize_answer(user_answer)
        correct_set = normalize_answer(correct_answer)
        correct_count = len(user_set & correct_set)
        incorrect_count = len(user_set - correct_set)
        total_correct = len(correct_set)
        score = (correct_count - incorrect_count) / total_correct
        return max(score, 0)  # Ensure the score is not negative
    return 0

def test_user(questions, correct_answers):
    points = 0
    for q in questions:
        os.system('clear')
        # points / current question / total questions
        print(f"Points: {round(points, 2)} / {questions.index(q)}\n")
        question_number = q['question'].split('.')[0]
        print(q['question'])
        for a in q['answers']:
            print(a)
        user_answer = input("\nYour answer: ")
        score = check_answer(question_number, user_answer, correct_answers)
        if score == 1:
            print("Correct!\n")
            points += 1
        elif score > 0:
            print(f"Partially correct! You got {round(score * 100, 2)}% of the answer correct.\nThe correct answer is: {correct_answers.get(question_number, 'Unknown')}\n")
            points += score
        else:
            print(f"Incorrect! The correct answer is: {correct_answers.get(question_number, 'Unknown')}\n")
        input("Press Enter ⏎ to continue")

def main():
    os.system('clear')
    file = 'terminal_friendly.md'
    file2 = 'IAU Odpovede.md'
    text = load_file(file)
    answers_text = load_file(file2)

    questions = split_questions(text)
    correct_answers = get_answers(answers_text)

    mode = input("Select mode\n1: Sequential, \n2: Random, \n3: 30 Questions Test \nMode:")
    if mode == '2':
        random.shuffle(questions)
    elif mode == '3':
        questions = random.sample(questions, 30)

    test_user(questions, correct_answers)

if __name__ == "__main__":
    main()