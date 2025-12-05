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
"""
Main Maths Quiz Program
Uses:
 - background.py (for gradient & theme)
 - sounds.py     (for welcome/correct/wrong sounds)
"""

import tkinter as tk
from tkinter import messagebox
import os
import random

# import background theme + drawing
from background import THEME, draw_colorful_background # type: ignore

# import sound system
from sounds import init_sound, play_sound # type: ignore


# -------------------------------- GLOBALS -------------------------------- #
QUIZ_LENGTH = 10
SECONDS_PER_QUESTION = 12

score = 0
current_q = 0
first_attempt = True
difficulty = None
num1 = num2 = 0
operation = "+"
time_left = SECONDS_PER_QUESTION
timer_job = None
session_scores = []


# ----------------------------- UTILITY FUNCTIONS ----------------------------- #
def clear_window():
    """Remove all widgets from root."""
    for w in root.winfo_children():
        w.destroy()


def safe_int(value):
    """Convert to int safely; return None if invalid."""
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    if value.lstrip("-").isdigit():
        return int(value)
    return None


# ----------------------------- REQUIRED FUNCTIONS ----------------------------- #
def randomInt(level):
    """Return random numbers based on difficulty."""
    if level == "Easy":
        return random.randint(1, 9)
    elif level == "Moderate":
        return random.randint(10, 99)
    return random.randint(1000, 9999)


def decideOperation():
    """Return random + or -."""
    return random.choice(["+", "-"])


def displayMenu():
    """Show the main difficulty menu."""
    clear_window()

    # initialize sound & play welcome sound
    init_sound()
    play_sound("welcome")

    # background canvas
    canvas = tk.Canvas(root, width=520, height=520, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    draw_colorful_background(canvas)

    # Welcome Card
    card = tk.Frame(root, bg=THEME["card"])
    card.place(relx=0.5, rely=0.18, anchor="center", width=420, height=130)

    tk.Label(card, text="🎉 Welcome to the Maths Quiz 🎉",
             font=("Segoe UI", 16, "bold"), bg=THEME["card"]).pack(pady=10)

    tk.Label(card, text="Choose a difficulty to begin!",
             font=("Segoe UI", 11), bg=THEME["card"]).pack()

    # Difficulty Options
    btn_frame = tk.Frame(root, bg=THEME["bg_top"])
    btn_frame.place(relx=0.5, rely=0.45, anchor="center")

    tk.Button(btn_frame, text="Easy (1-digit)", width=20,
              bg=THEME["button"], command=lambda: start_quiz("Easy")).grid(row=0, column=0, padx=8, pady=8)

    tk.Button(btn_frame, text="Moderate (2-digit)", width=20,
              bg=THEME["button"], command=lambda: start_quiz("Moderate")).grid(row=1, column=0, padx=8, pady=8)

    tk.Button(btn_frame, text="Advanced (4-digit)", width=20,
              bg=THEME["button"], command=lambda: start_quiz("Advanced")).grid(row=2, column=0, padx=8, pady=8)


# ----------------------------- QUIZ LOGIC ----------------------------- #
def start_quiz(level):
    """Initialize quiz."""
    global difficulty, score, current_q
    difficulty = level
    score = 0
    current_q = 0
    displayProblem()


def displayProblem():
    """Display a math problem."""
    global num1, num2, operation, first_attempt, time_left, timer_job

    clear_window()
    first_attempt = True
    time_left = SECONDS_PER_QUESTION

    if current_q >= QUIZ_LENGTH:
        displayResults()
        return

    # background canvas
    canvas = tk.Canvas(root, width=520, height=520, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    draw_colorful_background(canvas)

    # Card Layout
    card = tk.Frame(root, bg=THEME["card"])
    card.place(relx=0.5, rely=0.45, anchor="center", width=420, height=300)

    tk.Label(card, text=f"Question {current_q+1}/{QUIZ_LENGTH}",
             font=("Segoe UI", 11), bg=THEME["card"]).pack(pady=10)

    # generate numbers
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    tk.Label(card, text=f"{num1} {operation} {num2} =", font=("Segoe UI", 22, "bold"),
             bg=THEME["card"]).pack()

    # answer entry
    entry = tk.Entry(card, font=("Segoe UI", 14), justify="center", width=8)
    entry.pack(pady=8)
    entry.focus()

    feedback = tk.Label(card, text="", bg=THEME["card"], font=("Segoe UI", 10))
    feedback.pack()

    # Timer Label
    timer_label = tk.Label(card, text=f"⏱ {time_left}s", bg=THEME["card"])
    timer_label.pack()

    # Count Down Timer
    def countdown():
        global time_left, timer_job
        if time_left <= 0:
            play_sound("wrong")
            feedback.config(text="⏰ Time's up!", fg="red")
            root.after(800, next_question)
            return
        timer_label.config(text=f"⏱ {time_left}s")
        time_left -= 1
        timer_job = root.after(1000, countdown)

    countdown()

    def submit():
        user_val = safe_int(entry.get())

        if user_val is None:
            feedback.config(text="Enter a number.", fg="red")
            return

        correct_answer = num1 + num2 if operation == "+" else num1 - num2
        isCorrect(user_val, correct_answer, feedback)

    tk.Button(card, text="Submit Answer", bg=THEME["accent"], fg="white",
              command=submit).pack(pady=8)


def isCorrect(user_answer, correct_answer, feedback):
    """Check if answer is right/wrong."""
    global score, first_attempt

    if user_answer == correct_answer:
        play_sound("correct")
        if first_attempt:
            score += 10
            feedback.config(text="Correct! +10", fg="green")
        else:
            score += 5
            feedback.config(text="Correct! +5", fg="green")

        root.after(800, next_question)
    else:
        play_sound("wrong")
        if first_attempt:
            first_attempt = False
            feedback.config(text="Incorrect, try again.", fg="orange")
        else:
            feedback.config(text=f"Wrong! Answer: {correct_answer}", fg="red")
            root.after(900, next_question)


def next_question():
    """Move to next question."""
    global current_q
    current_q += 1
    displayProblem()


def grade_user(s):
    if s >= 90:
        return "A+"
    if s >= 80:
        return "A"
    if s >= 70:
        return "B"
    if s >= 60:
        return "C"
    return "Fail"


def displayResults():
    """Show final score & grade."""
    clear_window()

    session_scores.append(score)

    card = tk.Frame(root, bg=THEME["card"])
    card.place(relx=0.5, rely=0.45, anchor="center", width=420, height=300)

    tk.Label(card, text="Quiz Complete!", font=("Segoe UI", 18, "bold"),
             bg=THEME["card"]).pack(pady=15)

    tk.Label(card, text=f"Score: {score}/100", font=("Segoe UI", 14),
             bg=THEME["card"]).pack()

    g = grade_user(score)
    tk.Label(card, text=f"Grade: {g}", font=("Segoe UI", 14, "bold"),
             bg=THEME["card"]).pack(pady=10)

    tk.Button(card, text="Play Again", bg=THEME["button"],
              command=displayMenu).pack(pady=10)

    tk.Button(card, text="Exit", bg="#f0c27b",
              command=root.destroy).pack()


# ----------------------------- Sounds ----------------------------- #
import numpy as np
import wave
import struct


def create_tone(filename, frequency, duration=0.4, volume=0.5, framerate=44100):
    """
    Create a simple sine-wave based .wav file.
    """
    print(f"Creating: {filename} ...")

    # generate time values
    t = np.linspace(0, duration, int(framerate * duration))

    # build sine wave
    waveform = volume * np.sin(2 * np.pi * frequency * t)

    # open wav file for writing
    with wave.open(filename, "w") as wav_file:
        wav_file.setparams(
            (1, 2, framerate, 0, "NONE", "not compressed")
        )

        # write samples
        for sample in waveform:
            value = int(sample * 32767)
            wav_file.writeframes(struct.pack("<h", value))

    print(f"✔ {filename} created successfully.\n")



# ----------------- Create the 3 WAV sound files -----------------

print("\nGenerating Maths Quiz sound files...\n")

create_tone("welcome.wav", frequency=550, duration=0.7)
create_tone("correct.wav", frequency=900, duration=0.3)
create_tone("wrong.wav", frequency=200, duration=0.35)

print("All sound files generated!\n")

# ----------------------------- RUN MAIN PROGRAM ----------------------------- #
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("520x520")
root.resizable(False, False)
displayMenu()
root.mainloop()
