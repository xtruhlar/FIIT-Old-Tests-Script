import random
import os
import subprocess
import sys
import inquirer

# Ensure inquirer is installed
subprocess.check_call([sys.executable, "-m", "pip", "install", "inquirer"])

def load_file(file):
    encodings = ['utf-8', 'cp1250', 'latin-1', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    raise UnicodeDecodeError(f"Unable to decode file with any of these encodings: {encodings}")

def split_questions(text):
    questions = []
    current_question = None
    question_body = []  # Temporary storage for multiline questions

    for line in text.split('\n'):
        if line.strip() == '':
            continue
        elif line[0].isdigit() and '.' in line:  # Start of a new question
            if current_question:
                current_question['question'] = ' '.join(question_body).strip()
                questions.append(current_question)
            current_question = {'question': '', 'answers': [], 'type': 'checkbox'}
            question_body = [line.strip()]  # Start capturing question text
        elif 'a)' in line and current_question:  # Start of options
            parts = line.split('a)', 1)
            question_body.append(parts[0].strip())
            current_question['question'] = ' '.join(question_body).strip()
            current_question['answers'].append('a) ' + parts[1].strip())
        elif current_question and current_question['answers']:  # Part of an answer
            if line.strip()[0] in ('a', 'b', 'c', 'd', 'e','f','g','h','i','j','k','l','m','n') and ')' in line.strip()[:3]:
                current_question['answers'].append(line.strip())
            else:
                current_question['answers'][-1] += ' ' + line.strip()
        else:  # Part of a multiline question
            question_body.append(line.strip())

    # Add the last question if any
    if current_question:
        current_question['question'] = ' '.join(question_body).strip()
        questions.append(current_question)

    return questions

def get_answers(text):
    answers = {}
    for line in text.split('\n'):
        if line.strip() and line[0].isdigit():
            question_number, answer = line.split('.', 1)
            # Extract just the letters from the answers (e.g., "a) b)" -> ["a", "b"])
            answer_letters = [a.split(')')[0].strip() for a in answer.split()]
            answers[question_number.strip()] = answer_letters
    return answers

def load_wrong_answers(file='wrong_answers.md'):
    wrong_answers = {}
    try:
        with open(file, 'r') as f:
            for line in f:
                question_number, count = line.strip().split(':')
                wrong_answers[question_number] = int(count)
    except FileNotFoundError:
        pass
    return wrong_answers

def save_wrong_answers(wrong_answers, file='wrong_answers.md'):
    with open(file, 'w') as f:
        for question_number, count in wrong_answers.items():
            f.write(f"{question_number}:{count}\n")

def test_user(questions, correct_answers, wrong_answers):
    points = 0
    for q in questions:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Points: {round(points, 2)} / {questions.index(q)}\n")
        question_number = q['question'].split('.')[0]

        # Shuffle the options before displaying the question
        original_answers = q['answers'][:]
        random.shuffle(q['answers'])

        # Create a dictionary to map the original answers to their text
        answer_dict = {a.split(')')[0].strip(): a for a in original_answers}

        # Create a dictionary to map the shuffled answers back to their original letters
        shuffled_answer_dict = {a.split(') ', 1)[1] if ') ' in a else a: a.split(')')[0].strip() for a in q['answers']}

        # Strip the letters from the options
        display_answers = [a.split(') ', 1)[1] if ') ' in a else a for a in q['answers']]

        # Escape curly braces in the question message
        q['question'] = q['question'].replace('{', '{{').replace('}', '}}')

        # Display question and get user answers
        answer = inquirer.prompt([
            inquirer.Checkbox(
                name='answer',
                message=q['question'],
                choices=display_answers
            )
        ])

        # Extract only the letters (e.g., "a)", "b)") from the user-selected answers
        user_answers = set([shuffled_answer_dict[a] for a in answer['answer']])
        correct_set = set(correct_answers.get(question_number, []))

        # Compare user's answers with the correct answers
        if user_answers == correct_set:
            print("Correct!\n")
            points += 1
        else:
            correct_text = ', '.join([answer_dict[c] for c in correct_answers.get(question_number, [])])
            print(f"Wrong, the correct answers are {correct_text}\n")
            wrong_answers[question_number] = wrong_answers.get(question_number, 0) + 1

        input("Press Enter ⏎ to continue")

    save_wrong_answers(wrong_answers)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    # Course Selection
    course_questions = [
        inquirer.List(
            'course',
            message="Select course",
            choices=['PIB', 'IAU'],
        )
    ]
    course_answer = inquirer.prompt(course_questions)
    course = course_answer['course']

    if course == 'PIB':
        file = 'PIB_Qs.md'
        file2 = 'PIB_answers.md'
    elif course == 'IAU':
        file = 'terminal_friendly.md'
        file2 = 'IAU Odpovede.md'

    text = load_file(file)
    answers_text = load_file(file2)

    questions = split_questions(text)
    correct_answers = get_answers(answers_text)
    wrong_answers = load_wrong_answers()

    # Mode Selection
    mode_questions = [
        inquirer.List(
            'mode',
            message="Select mode",
            choices=['Sequential', 'Random', '30 Questions Test', 'Starting with...', 'Train 30 Questions with Most Wrong Answers'],
        )
    ]
    mode_answer = inquirer.prompt(mode_questions)
    mode = mode_answer['mode']

    if mode == 'Random':
        random.shuffle(questions)
    elif mode == '30 Questions Test':
        questions = random.sample(questions, 30)
    elif mode == 'Starting with...':
        start_question = inquirer.prompt([
            inquirer.Text('start', message="Start from question number")
        ])
        start = int(start_question['start'])
        questions = questions[start - 1:start + 35]
    elif mode == 'Train 30 Questions with Most Wrong Answers':
        sorted_questions = sorted(questions, key=lambda q: wrong_answers.get(q['question'].split('.')[0], 0), reverse=True)
        questions = sorted_questions[:30]

    test_user(questions, correct_answers, wrong_answers)

if __name__ == "__main__":
    main()