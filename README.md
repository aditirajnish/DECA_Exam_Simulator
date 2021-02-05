Simulates DECA exam with randomized questions. All DECA exam content belongs to DECA.

JSONCreator.py fetches exam PDF with a link, creating a text file with Apache Tika Text Extraction/OCR. 
This is parsed using regex and string functions, dividing questions, multiple choice options, and solutions. 
Finally, they are stored in a JSON file.

exam.py uses the JSON to practice the exam: randomly selecting questions, responding to user input, and keeping score.
