from file_reader import read_file
from text_processor import clean_text
from text_chunker import split_text
from validator import validate_questions
from question_generator import generate_questions

print("===== AUTOQUIZ =====")

file_path = input("Enter your text file name: ")

content = read_file(file_path)
content = clean_text(content)
if not content:
    print("File is empty! Please upload a file with text.")
else:
    chunks = split_text(content,100)
    print("Total chunks:",len(chunks))
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}:")
        print(chunk)
        questions = generate_questions(chunk)

        if validate_questions(questions):
            print("Questions generated successfully!")
            print(questions)
        else:
            print("Invalid questions generated!")
if content:
    print("\nFile read successfully!")
    print("\n===== STUDY MATERIAL =====")
    print(content)
else:
    print("Could not read the file.")

