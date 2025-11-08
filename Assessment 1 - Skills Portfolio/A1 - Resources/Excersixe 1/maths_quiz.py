"""
Maths Quiz Game - Advanced Version
Author: Sheikh Abdul Wahab
Date: 5 November 2025

This Tkinter-based quiz is part of the Programming Skills Portfolio (Exercise 1).
It demonstrates structured, event-driven programming, GUI development, and
Python functions. The app includes difficulty levels, score tracking, time limits,
and grading, with a clean user interface and smooth flow.

Features:
- Difficulty menu (Easy, Moderate, Advanced)
- 10 random arithmetic questions (+ / -)
- Timer-based gameplay
- Score tracking with two attempts per question
- Replay and session history display
- Error handling and feedback system
"""

import tkinter as tk
from tkinter import messagebox
import random
import time

# Global Variables
score = 0
current_question = 0
difficulty = ""
first_attempt = True
num1 = num2 = 0
operation = ""
timer_label = None
time_left = 10
session_scores = []  # stores last few session results

# Core Functions

def clear_window():
    """Clear all widgets from the main window."""
    for widget in root.winfo_children():
        widget.destroy()


def randomInt(level):
    """Generate random integer based on difficulty level."""
    if level == "Easy":
        return random.randint(1, 9)
    elif level == "Moderate":
        return random.randint(10, 99)
    return random.randint(1000, 9999)


def decideOperation():
    """Randomly return '+' or '-'."""
    return random.choice(["+", "-"])


def displayMenu():
    """Display difficulty selection screen."""
    clear_window()
    root.config(bg="#f3f7fa")

    title = tk.Label(root, text="🎯 Maths Quiz Game", font=("Arial Rounded MT Bold", 20), bg="#f3f7fa")
    title.pack(pady=15)

    desc = tk.Label(root, text="Choose a difficulty level to begin:", font=("Arial", 12), bg="#f3f7fa")
    desc.pack(pady=5)

    tk.Button(root, text="Easy (1-digit)", width=20, bg="#a2d2ff", command=lambda: start_quiz("Easy")).pack(pady=5)
    tk.Button(root, text="Moderate (2-digit)", width=20, bg="#ffc8dd", command=lambda: start_quiz("Moderate")).pack(pady=5)
    tk.Button(root, text="Advanced (4-digit)", width=20, bg="#bde0fe", command=lambda: start_quiz("Advanced")).pack(pady=5)

    if session_scores:
        history = "Recent Scores: " + ", ".join([str(s) for s in session_scores[-3:]])
        tk.Label(root, text=history, font=("Arial", 10, "italic"), bg="#f3f7fa", fg="gray").pack(pady=10)


def start_quiz(level):
    """Initialize variables and start the quiz."""
    global difficulty, score, current_question
    difficulty = level
    score = 0
    current_question = 0
    displayProblem()


def displayProblem():
    """Display a new math problem."""
    global num1, num2, operation, first_attempt, time_left
    clear_window()
    first_attempt = True
    time_left = 10  # seconds per question

    if current_question == 10:
        displayResults()
        return

    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    tk.Label(root, text=f"Question {current_question + 1} of 10", font=("Arial", 13, "bold"), bg="#f3f7fa").pack(pady=10)
    tk.Label(root, text=f"{num1} {operation} {num2} = ?", font=("Arial", 16), bg="#f3f7fa").pack(pady=5)

    entry = tk.Entry(root, width=8, font=("Arial", 14), justify="center")
    entry.pack(pady=5)
    entry.focus()

    feedback_label = tk.Label(root, text="", font=("Arial", 12), bg="#f3f7fa")
    feedback_label.pack(pady=5)

    def update_timer():
        """Countdown timer for each question."""
        global time_left
        if time_left > 0:
            timer_label.config(text=f"⏱ Time Left: {time_left}s")
            time_left -= 1
            root.after(1000, update_timer)
        else:
            feedback_label.config(text="⏰ Time’s up!", fg="red")
            root.after(1000, next_question)

    def check_answer():
        """Validate and check user's answer."""
        user_input = entry.get().strip()
        if not user_input or not (user_input.lstrip('-').isdigit()):
            feedback_label.config(text="Please enter a valid number.", fg="red")
            return

        correct_answer = num1 + num2 if operation == "+" else num1 - num2
        user_answer = int(user_input)
        handle_result(user_answer, correct_answer, feedback_label)

    timer_label = tk.Label(root, text="", font=("Arial", 10), bg="#f3f7fa", fg="gray")
    timer_label.pack(pady=3)
    update_timer()

    tk.Button(root, text="Submit Answer", bg="#a2d2ff", command=check_answer).pack(pady=8)


def handle_result(user_answer, correct_answer, feedback_label):
    """Handle correctness logic and score updates."""
    global score, first_attempt, current_question
    if user_answer == correct_answer:
        points = 10 if first_attempt else 5
        score += points
        feedback_label.config(text=f"✅ Correct! +{points} points", fg="green")
        root.after(800, next_question)
    else:
        if first_attempt:
            first_attempt = False
            feedback_label.config(text="❌ Incorrect! Try once more.", fg="red")
        else:
            feedback_label.config(text=f"✖ Wrong again! Answer: {correct_answer}", fg="red")
            root.after(1000, next_question)


def next_question():
    """Move to the next question."""
    global current_question
    current_question += 1
    displayProblem()


def grade_user(score):
    """Assign grade based on total score."""
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "Fail"


def displayResults():
    """Display the final score and grading."""
    clear_window()
    session_scores.append(score)
    grade = grade_user(score)

    tk.Label(root, text="🎉 Quiz Complete!", font=("Arial Rounded MT Bold", 18), bg="#f3f7fa").pack(pady=15)
    tk.Label(root, text=f"Your Score: {score}/100", font=("Arial", 14), bg="#f3f7fa").pack(pady=5)
    tk.Label(root, text=f"Grade: {grade}", font=("Arial", 14, "bold"), bg="#f3f7fa").pack(pady=5)

    remarks = {
        "A+": "Outstanding! You mastered this quiz!",
        "A": "Excellent work!",
        "B": "Great effort!",
        "C": "Good try — keep practicing!",
        "Fail": "Don’t worry, try again to improve!"
    }
    tk.Label(root, text=remarks[grade], font=("Arial", 12, "italic"), bg="#f3f7fa").pack(pady=10)

    tk.Button(root, text="Play Again", width=15, bg="#bde0fe", command=displayMenu).pack(pady=5)
    tk.Button(root, text="Exit", width=15, bg="#ffc8dd", command=root.destroy).pack(pady=5)


# Main Program

root = tk.Tk()
root.title("Maths Quiz Game")
root.geometry("400x400")
root.resizable(False, False)
root.config(bg="#f3f7fa")

displayMenu()
root.mainloop()
