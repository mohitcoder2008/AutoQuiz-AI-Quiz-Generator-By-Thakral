
import pdfplumber    #pdf keliye library
from docx import Document      #docs file keliye library
import os    #text file keliye 



def read_txt_file(file_path):                          #text file ko accept krke data nikalne vala function
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        return text

    except FileNotFoundError:
        print("Error: File not found!")
        return ""

    except UnicodeDecodeError:
        print("Error: File encoding is not supported!")
        return ""

    
def read_pdf_file(file_path):                         # pdf file ko accept krke data nikalne vala function
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def read_docx_file(file_path):                           #docx file ko accept krke data nikalne vala function
    document = Document(file_path)
    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def read_file(file_path):                                  #ye function check krta hai ki input krri gyi file ka format kya haiii
    if file_path.endswith(".txt"):
        return read_txt_file(file_path)

    elif file_path.endswith(".pdf"):
        return read_pdf_file(file_path)

    elif file_path.endswith(".docx"):
        return read_docx_file(file_path)

    else:
        print("Unsupported file format!")
        return ""


if __name__ == "__main__":
    content = read_txt_file("sample.txt")
    print("===== FILE CONTENT =====")
    print(content)
