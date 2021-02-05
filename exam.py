import json
import time
import random

# exam simulator using created JSON

question_nums = list(range(1, 101))
score = 0
with open("DECA_BUSINESS_ADMINISTRATION_CORE_EXAM_1181.json") as f:
    exam = json.load(f)

while question_nums:
    question_num = random.choice(question_nums)
    question_nums.remove(question_num)

    full_question = exam[str(question_num)]
    print(f"{question_num}: {full_question['question']}")
    print("A:", full_question["choice_a"])
    print("B:", full_question["choice_b"])
    print("C:", full_question["choice_c"])
    print("D:", full_question["choice_d"])

    user_answer = input("Enter your answer (the letter, ex. 'A'): ").lower()
    correct_answer = [full_question["letter_answer"], full_question["word_answer"]]

    if user_answer == correct_answer[0].lower():
        score += 1
        print(f"\nCorrect! Your score is now {score}.")
    else:
        print("\nIncorrect! The correct answer was", correct_answer[0] + ": " + correct_answer[1])

    view_solution = input("Enter 'Y' to view the solution. Otherwise, enter 'N': ")
    if view_solution.lower() == "y":
        print("\n", full_question["solution"])
        time.sleep(5)

    print("\n")