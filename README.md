# AutoQuiz – AI Quiz Generator

AutoQuiz is an AI-powered quiz generation application built using Python, Ollama and Tkinter.

It allows users to upload study materials and automatically generate multiple-choice questions (MCQs) for practice and learning.

## Features

- Upload study materials in TXT, PDF and DOCX formats.
- Extract and process text from uploaded documents.
- Generate AI-powered multiple-choice questions.
- Four options for each question.
- Interactive quiz interface using Tkinter.
- One question displayed at a time.
- 10-minute quiz timer.
- Automatic score and percentage calculation.
- Review answers with explanations.
- Start a new quiz.

## Technologies Used

- Python
- Ollama
- Llama 3.2 (1B)
- Tkinter
- JSON
- PDFPlumber
- Python-docx

## Project Structure

```text
AutoQuiz/
│
├── gui.py
├── main.py
├── file_reader.py
├── question_generator.py
├── text_chunker.py
├── text_processor.py
├── validator.py
└── requirements.txt
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/mohitcoder2008/AutoQuiz-AI-Quiz-Generator-By-Thakral.git
```

2. Open the project folder:

```bash
cd AutoQuiz-AI-Quiz-Generator-By-Thakral
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install Ollama and download the required model:

```bash
ollama pull llama3.2:1b
```

5. Run the application:

```bash
python gui.py
```

## How It Works

1. Upload a study document.
2. AutoQuiz extracts and cleans the text.
3. The text is divided into smaller chunks.
4. Ollama generates MCQs from the study material.
5. Generated questions are validated.
6. Users attempt the quiz and receive their results.

## Developer

**Mohit Thakral**

B.Tech – Computer Science and Engineering

## Project Purpose

The purpose of AutoQuiz is to make learning and self-assessment easier by automatically converting study materials into interactive quizzes using Artificial Intelligence.
