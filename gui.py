import tkinter as tk
from tkinter import filedialog     #computer se file select krne vali window
import os
import threading
import queue
import time

from file_reader import read_file
from text_processor import clean_text
from text_chunker import split_text
from question_generator import generate_questions
from validator import validate_questions


selected_file_path = ""
all_questions = []
current_question_index = 0
selected_answers = {}
quiz_queue = queue.Queue()
quiz_time_left = 600
timer_job = None


# Create main window
root = tk.Tk()
root.title("AutoQuiz - AI Quiz Generator By Thakral")
root.geometry("800x600")
root.minsize(600, 400)
root.configure(bg="#F1F5F9")

# Main container
container = tk.Frame(root, bg="#F1F5F9")
container.pack(fill="both", expand=True)

# Canvas
canvas = tk.Canvas(container, highlightthickness=0, bg="#F1F5F9")

# Scrollbar
scrollbar = tk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = tk.Frame(canvas, bg="#F1F5F9")

# Update scroll region
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

# Create canvas window
canvas_window = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

# Make frame width equal to canvas width
canvas.bind(
    "<Configure>",
    lambda e: canvas.itemconfig(
        canvas_window,
        width=e.width
    )
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Mouse scrolling
canvas.bind_all(
    "<MouseWheel>",
    lambda e: canvas.yview_scroll(
        int(-1 * (e.delta / 120)), "units"
    )
)

heading = tk.Label(
    scrollable_frame,
    text="Welcome to AutoQuiz By Thakral",
    font=("Arial", 24, "bold"),
    bg="#F1F5F9",
    fg="#1E3A8A"
)

heading.pack(pady=30)

description = tk.Label(
    scrollable_frame,
    text="Upload your study material and generate AI-powered quizzes!",
    font=("Arial", 12),
    bg="#F1F5F9",
    fg="#1E3A8A"
)

description.pack(pady=10)

def upload_file():
    global selected_file_path    #global function ko btata hai ki bhar vala variable use krna hai
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_file_path  = file_path

        file_name = os.path.basename(file_path)
        file_label.config(text="Selected File: " + file_name)

def select_answer(option):
    selected_answers[current_question_index] = option

    for button in options_frame.winfo_children():
        if button["text"].startswith(option + "."):
            button.config(bg="#DCFCE7", fg="#166534")
        else:
            button.config(bg="#FFFFFF", fg="#334155")
def show_question():
    global current_question_index

    quiz_display.delete("1.0", tk.END)

    for widget in options_frame.winfo_children():
        widget.destroy()

    if current_question_index < len(all_questions):

        question = all_questions[current_question_index]
        progress_label.config(
            text=f"Question {current_question_index + 1} / {len(all_questions)}"
        )

        progress_label.pack(pady=5)
        
        if current_question_index == len(all_questions) - 1:
            next_button.config(text="Finish Quiz")
        else:
            next_button.config(text="Next Question")

        quiz_display.insert(
            tk.END,
            f"Question {current_question_index + 1} / {len(all_questions)}\n\n"
        )

        quiz_display.insert(
            tk.END,
            question["question"] + "\n\n"
        )

        for option, value in question["options"].items():

            button = tk.Button(
                options_frame,
                text=f"{option}. {value}",
                width=50,
                font=("Arial", 11),
                bg="#FFFFFF",
                fg="#334155",
                activebackground="#DBEAFE",
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=10,
                pady=8,
                command=lambda opt=option: select_answer(opt)
            )

            button.pack(pady=5)

def next_question():
    global current_question_index

    if current_question_index not in selected_answers:
        quiz_display.insert(tk.END, "\n\nPlease select an answer first!")
        return

    if current_question_index < len(all_questions) - 1:
        current_question_index += 1
        show_question()
    else:
        finish_quiz()

def finish_quiz():
    global timer_job

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None
    score = 0

    for index, question in enumerate(all_questions):
        if selected_answers.get(index) == question["correct_answer"]:
            score += 1

    quiz_display.delete("1.0", tk.END)

    quiz_display.insert(
        tk.END,
        "QUIZ COMPLETED!\n\n"
    )

    quiz_display.insert(
        tk.END,
        f"Your Score: {score} / {len(all_questions)}\n\n"
    )

    quiz_display.insert(
        tk.END,
        f"Percentage: {(score / len(all_questions)) * 100:.1f}%"
    )

    for widget in options_frame.winfo_children():
        widget.destroy()

    next_button.pack_forget()
    progress_label.pack_forget()
    review_button.pack(pady=10)
    new_quiz_button.pack(pady=10)
    exit_button.pack(pady=10)

def reset_quiz():
    global all_questions, current_question_index
    global selected_answers, selected_file_path
    global quiz_time_left, timer_job

    all_questions = []
    current_question_index = 0
    selected_answers = {}
    selected_file_path = ""

    # Stop old timer
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    # Reset timer
    quiz_time_left = 600
    timer_label.config(text="Time Left: 10:00")
    timer_label.pack_forget()

    quiz_display.delete("1.0", tk.END)
    file_label.config(text="No file selected")

    for widget in options_frame.winfo_children():
        widget.destroy()

    next_button.pack_forget()
    new_quiz_button.pack_forget()
    exit_button.pack_forget()
    review_button.pack_forget()

    generate_button.config(state="normal")

def review_answers():
    quiz_display.delete("1.0", tk.END)

    for index, question in enumerate(all_questions):

        quiz_display.insert(
            tk.END,
            f"Question {index + 1}: {question['question']}\n"
        )

        quiz_display.insert(
            tk.END,
            f"Your Answer: {selected_answers.get(index, 'Not Attempted')}\n"
        )

        quiz_display.insert(
            tk.END,
            f"Correct Answer: {question['correct_answer']}\n"
        )

        quiz_display.insert(
            tk.END,
            f"Explanation: {question.get('explanation', 'Not available')}\n\n"
        )

def process_quiz():
    global all_questions

    content = read_file(selected_file_path)
    content = clean_text(content)

    if not content:
        return []

    chunks = split_text(content, 100)

    generated_questions = []

    for chunk in chunks:
        questions_data = generate_questions(chunk)

        if validate_questions(questions_data):
            generated_questions.extend(
                questions_data["questions"]
            )

        if len(generated_questions) >= 10:
            break

    return generated_questions[:10]

def worker():
    try:
        questions = process_quiz()
        quiz_queue.put(("success", questions))

    except Exception as error:
        quiz_queue.put(("error", str(error)))


def check_queue():
    global all_questions, current_question_index

    try:
        status, result = quiz_queue.get_nowait()

        if status == "success":
            all_questions = result
            current_question_index = 0

            generate_button.config(state="normal")

            if all_questions:
                show_question()

                global quiz_time_left
                quiz_time_left = 600

                timer_label.pack(pady=10)
                update_timer()
            else:
                quiz_display.delete("1.0", tk.END)
                quiz_display.insert(tk.END, "No valid questions generated.")

        elif status == "error":
            quiz_display.delete("1.0", tk.END)
            quiz_display.insert(tk.END, "Error: " + result)

            generate_button.config(state="normal")

    except queue.Empty:
        root.after(100, check_queue)

def update_timer():
    global quiz_time_left, timer_job

    minutes = quiz_time_left // 60
    seconds = quiz_time_left % 60

    timer_label.config(
        text=f"Time Left: {minutes:02d}:{seconds:02d}"
    )

    if quiz_time_left == 0:
        timer_job = None
        finish_quiz()
    else:
        quiz_time_left -= 1
        timer_job = root.after(1000, update_timer)


def generate_quiz():
    if selected_file_path == "":
        print("Please upload a file first!")

    else:
        quiz_display.delete("1.0", tk.END)
        quiz_display.insert(tk.END, "Generating quiz... Please wait.")
        generate_button.config(state="disabled")
        threading.Thread(target=worker, daemon=True).start()
        root.after(100, check_queue)

file_label = tk.Label(
    scrollable_frame,
    text="No file selected",
    font=("Arial", 10),
    bg="#F1F5F9",
    fg="#64748B"
)

file_label.pack(pady=10)

upload_button = tk.Button(
    scrollable_frame,
    text="Upload Study Material",
    font=("Arial", 12, "bold"),
    command=upload_file,
    bg="#DBEAFE",
    fg="#1D4ED8",
    activebackground="#BFDBFE",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=8
)

upload_button.pack(pady=10)

generate_button = tk.Button(
    scrollable_frame,
    text="Generate Quiz",
    font=("Arial", 12, "bold"),
    command=generate_quiz,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=10
)

generate_button.pack(pady=10)

next_button = tk.Button(
    scrollable_frame,
    text="Next Question",
    font=("Arial", 12, "bold"),
    command=next_question,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=8
)
    
next_button.pack(pady=10)

timer_label = tk.Label(
    scrollable_frame,
    text="Time Left: 10:00",
    font=("Arial", 14, "bold"),
    bg="#F1F5F9",
    fg="#166534"
)

timer_label.pack(pady=10)
timer_label.pack_forget()

quiz_display = tk.Text(
    scrollable_frame,
    height=15,
    width=75,
    font=("Arial", 11),
    bg="#FFFFFF",
    fg="#1E293B",
    insertbackground="#1E293B",
    relief="flat",
    bd=0,
    padx=15,
    pady=15,
    wrap="word"
)

progress_label = tk.Label(
    scrollable_frame,
    text="Question 0 / 10",
    font=("Arial", 11, "bold"),
    bg="#F1F5F9",
    fg="#1D4ED8"
)

progress_label.pack(pady=5)
progress_label.pack_forget()

quiz_display.pack(pady=20)
options_frame = tk.Frame(scrollable_frame, bg="#F1F5F9")
options_frame.pack(pady=10)
result_frame = tk.Frame(scrollable_frame, bg="#F1F5F9")
result_frame.pack(pady=20)

exit_button = tk.Button(
    result_frame,
    text="Exit",
    font=("Arial", 12, "bold"),
    command=root.destroy,
    bg="#FEE2E2",
    fg="#B91C1C",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=8
)

exit_button.pack(pady=10)
exit_button.pack_forget()

new_quiz_button = tk.Button(
    result_frame,
    text="New Quiz",
    font=("Arial", 12, "bold"),
    command=reset_quiz,
    bg="#2563EB",
    fg="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=8
)

new_quiz_button.pack(pady=10)
new_quiz_button.pack_forget()

review_button = tk.Button(
    result_frame,
    text="Review Answers",
    font=("Arial", 12, "bold"),
    command=review_answers,
    bg="#DBEAFE",
    fg="#1D4ED8",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=8
)

review_button.pack(pady=10)
review_button.pack_forget()

# Run the application
root.mainloop()
