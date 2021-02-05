from tika import parser
import urllib.request
from re import sub
from json import dump
from os import rename

# get exam PDF from website, convert to text, parse, store in JSON file for exam simulator

def renameFiles(text_file):
    with open(text_file) as file:
        txt = file.read()
    test_position = txt.index("Test ")
    test_number = txt[test_position + 5: test_position + 9]
    cluster = ""

    for i, char in enumerate(txt, test_position + 9):
        if char == "1":
            char_position = txt.index(char, test_position + 9)
            cluster += txt[test_position + 9: char_position]
            break

    cluster = cluster.strip().replace(" ", "_")
    exam_name = f"DECA_{cluster}_{test_number}"
    return exam_name


def makeJSON(q_and_a, main_name):
    with open(main_name + ".json", "w") as file:
        dump(q_and_a, file, indent=5)


def createDictionary(newest_text):

    nums = [f" {num}. " for num in range(0, 101)]
    q_and_a = {}

    for i in range(1, len(nums)+1):
        num = nums[i]
        q_num_position = newest_text.index(num) + len(num)
        a_num_position = newest_text.rindex(num) + len(num)

        if i < 100:
            next_num = nums[i+1]
            q_next_num_position = newest_text.index(next_num)
            q_and_choices = newest_text[q_num_position: q_next_num_position]

            a_next_num_position = newest_text.rindex(next_num)
            a_and_solutions = newest_text[a_num_position: a_next_num_position]

        else:
            q_and_choices = newest_text[q_num_position:].strip("  ")
            a_and_solutions = newest_text[a_num_position:].strip("  ")

        q_and_choices2 = q_and_choices.split(" A. ")
        question = q_and_choices2[0]
        q_and_choices3 = q_and_choices2[1].split(" B. ")
        choice_a = q_and_choices3[0]
        q_and_choices4 = q_and_choices3[1].split(" C. ")
        choice_b = q_and_choices4[0]
        q_and_choices5 = q_and_choices4[1].split(" D. ")
        choice_c = q_and_choices5[0]
        choice_d = q_and_choices5[1][:q_and_choices5[1].find("  ")]

        a_and_solutions = a_and_solutions.split("  ", 1)
        letter_answer = a_and_solutions[0]
        a_and_solutions = a_and_solutions[1].split(".", 1)
        word_answer = a_and_solutions[0] + "."
        solution = a_and_solutions[1][:a_and_solutions[1].find("  ")]

        q_and_a[i] = {}
        q_and_a[i]["question"] = question
        q_and_a[i]["choice_a"] = choice_a
        q_and_a[i]["choice_b"] = choice_b
        q_and_a[i]["choice_c"] = choice_c
        q_and_a[i]["choice_d"] = choice_d
        q_and_a[i]["letter_answer"] = letter_answer
        q_and_a[i]["word_answer"] = word_answer
        q_and_a[i]["solution"] = solution

        if i >= 100:
            break

    return q_and_a


def reformatText(text_file):
    with open(text_file) as file:
        text = file.read()

    new_text = sub("\n\n\s\s", " ", text)
    newer_text = sub("\s\s", " ", new_text)
    newest_text = sub("\n", " ", newer_text)

    return newest_text


def pdfReader(pdf_file):
    raw = parser.from_file(pdf_file)
    with open(pdf_file.rstrip(".pdf") + ".txt", "a") as text_file:
        text = raw["content"]
        text_file.write(text)


def getPDF(url, pdf_file):
    urllib.request.urlretrieve(url, pdf_file)


if __name__ == "__main__":
    url = "https://www.deca.org/wp-content/uploads/2014/08/HS_Business_Administration_Core_Sample_Exam.pdf"
    main_name = "file1"
    pdf_name = main_name + ".pdf"
    text_file = main_name + ".txt"

    exam_name = renameFiles(text_file)
    for file_type in (".pdf", ".txt"):
        rename(rf'{main_name}{file_type}', rf'{exam_name}{file_type}')
