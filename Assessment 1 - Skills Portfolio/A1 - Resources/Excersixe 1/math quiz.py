"""
maths_quiz.py
--------------

Features:
- GUI with welcome screen, difficulty menu and 10-question quiz
- Two attempts per question: 10 points first attempt, 5 points second attempt
- Sound support via sounds.py (preferred) or winsound fallback on Windows
- Functions required by the brief implemented:
    displayMenu, randomInt, decideOperation, displayProblem, isCorrect, displayResults
- Input validation & friendly messages
- Keeps the original UI layout but with clearer structure and comments

Author: Abdul Wahab
Date: 2025
"""

import tkinter as tk
from tkinter import messagebox, font
import random
import sys


try:
    import sounds # type: ignore
    HAVE_SOUNDS = True
except:
    HAVE_SOUNDS = False

try:
    import winsound
    HAVE_WINSOUND = True
except:
    HAVE_WINSOUND = False


class MathsQuiz:
    """Main Maths Quiz Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz Challenge")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Colours
        self.colors = {
            "primary": "#3498db",
            "secondary": "#2ecc71",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "dark": "#2c3e50",
            "light": "#ecf0f1",
            "muted": "#7f8c8d",
            "success": "#27ae60",
        }

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.heading_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.problem_font = font.Font(family="Courier", size=36, weight="bold")

        # Game state variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.first_attempt = True
        self.num1 = 0
        self.num2 = 0
        self.correct_answer = 0
        self.operation = "+"
        self.audio_enabled = True

        # Container
        self.container = tk.Frame(self.root, bg=self.colors["dark"])
        self.container.pack(fill="both", expand=True)

        # Show initial menu
        self.displayMenu()

    # --------------------------- SOUND SYSTEM --------------------------- #

    def play_sound(self, key=None, freq=600, duration=180):
        """Play sound via sounds.py or fallback to winsound."""
        if not self.audio_enabled:
            return

        
        if HAVE_SOUNDS and key:
            try:
                sounds.play_sound(key)
                return
            except:
                pass

        # Fallback simple beep (Windows)
        if HAVE_WINSOUND and sys.platform == "win32":
            try:
                winsound.Beep(freq, duration)
            except:
                pass

    def toggle_audio(self):
        """Enable or disable sound."""
        self.audio_enabled = not self.audio_enabled

        # Update button text
        try:
            self.audio_btn.config(
                text="🔊 Sound: ON" if self.audio_enabled else "🔇 Sound: OFF"
            )
        except:
            pass

        # Confirmation beep
        if self.audio_enabled:
            self.play_sound(freq=600, duration=120)

    # --------------------------- MENU SCREEN --------------------------- #

    def displayMenu(self):
        """Display the welcome + difficulty menu."""
        self.clear_frame()

        frame = tk.Frame(self.container, bg=self.colors["dark"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            frame,
            text="🎯 MATHS QUIZ CHALLENGE",
            font=self.title_font,
            bg=self.colors["dark"],
            fg=self.colors["light"],
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            frame,
            text="Choose a difficulty level to begin",
            font=self.normal_font,
            bg=self.colors["dark"],
            fg=self.colors["muted"],
        )
        subtitle.pack(pady=5)

        # Audio toggle
        self.audio_btn = tk.Button(
            frame,
            text="🔊 Sound: ON",
            bg=self.colors["primary"],
            fg="white",
            font=self.button_font,
            command=self.toggle_audio,
        )
        self.audio_btn.pack(pady=10)

        # Difficulty buttons
        btn_frame = tk.Frame(frame, bg=self.colors["dark"])
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Easy (1 digit)",
            width=20,
            bg=self.colors["secondary"],
            fg="white",
            font=self.button_font,
            command=lambda: self.start_quiz(1),
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Moderate (2 digits)",
            width=20,
            bg=self.colors["warning"],
            fg="white",
            font=self.button_font,
            command=lambda: self.start_quiz(2),
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Advanced (4 digits)",
            width=20,
            bg=self.colors["danger"],
            fg="white",
            font=self.button_font,
            command=lambda: self.start_quiz(3),
        ).grid(row=1, column=0, columnspan=2, pady=5)

        footer = tk.Label(
            frame,
            text="Programming Skills Portfolio – Exercise 1",
            font=("Helvetica", 10),
            bg=self.colors["dark"],
            fg=self.colors["muted"],
        )
        footer.pack(pady=10)

        self.play_sound("welcome", freq=550, duration=600)

    # --------------------------- QUIZ LOGIC --------------------------- #

    def start_quiz(self, difficulty):
        """Initialise quiz variables."""
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.first_attempt = True
        self.generate_problem()
        self.displayProblem()

    def randomInt(self, level):
        """Generate number based on difficulty (required function)."""
        if level == 1:
            return random.randint(0, 9)
        elif level == 2:
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def decideOperation(self):
        """Randomly return '+' or '-' (required function)."""
        return "+" if random.choice([True, False]) else "-"

    def generate_problem(self):
        """Generate a new arithmetic problem."""
        self.num1 = self.randomInt(self.difficulty)
        self.num2 = self.randomInt(self.difficulty)
        self.operation = self.decideOperation()

        if self.operation == "+":
            self.correct_answer = self.num1 + self.num2
        else:
            # avoid negative answers
            if self.num1 < self.num2:
                self.num1, self.num2 = self.num2, self.num1
            self.correct_answer = self.num1 - self.num2

        self.first_attempt = True

    # --------------------------- PROBLEM SCREEN --------------------------- #

    def displayProblem(self):
        """Required function: display the problem."""
        self.clear_frame()

        frame = tk.Frame(self.container, bg=self.colors["dark"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Score header
        header = tk.Frame(frame, bg=self.colors["dark"])
        header.pack(pady=10)

        tk.Label(
            header,
            text=f"Score: {self.score}",
            font=self.button_font,
            bg=self.colors["primary"],
            fg="white",
            padx=15,
            pady=5,
        ).pack(side="left", padx=10)

        tk.Label(
            header,
            text=f"Question {self.current_question+1}/{self.total_questions}",
            font=self.button_font,
            bg=self.colors["warning"],
            fg="white",
            padx=15,
            pady=5,
        ).pack(side="right", padx=10)

        # Problem
        problem_text = f"{self.num1} {self.operation} {self.num2} ="
        tk.Label(
            frame,
            text=problem_text,
            font=self.problem_font,
            bg=self.colors["dark"],
            fg=self.colors["light"],
        ).pack(pady=20)

        # Answer entry
        self.answer_var = tk.StringVar()
        entry = tk.Entry(
            frame,
            textvariable=self.answer_var,
            font=self.problem_font,
            width=10,
            justify="center",
        )
        entry.pack(pady=10)
        entry.focus()
        entry.bind("<Return>", lambda e: self.isCorrect())

        # Submit button
        tk.Button(
            frame,
            text="SUBMIT ANSWER",
            font=self.button_font,
            bg=self.colors["secondary"],
            fg="white",
            command=self.isCorrect,
        ).pack(pady=20)

        # Attempt info
        attempt_text = (
            "First Attempt (10 points)" if self.first_attempt else "Second Attempt (5 points)"
        )
        tk.Label(
            frame,
            text=attempt_text,
            font=self.normal_font,
            bg=self.colors["dark"],
            fg=self.colors["muted"],
        ).pack(pady=5)

    # --------------------------- ANSWER CHECK --------------------------- #

    def isCorrect(self):
        """Required function: check correctness + scoring."""
        raw = self.answer_var.get().strip()

        if raw == "":
            messagebox.showwarning("No Answer", "Please enter an answer.")
            self.play_sound(freq=300, duration=200)
            return

        try:
            user_answer = int(raw)
        except:
            messagebox.showerror("Invalid", "Please enter a valid number.")
            self.play_sound(freq=300, duration=200)
            return

        if user_answer == self.correct_answer:
            # Correct
            points = 10 if self.first_attempt else 5
            self.score += points

            messagebox.showinfo(
                "Correct!",
                f"Well done! +{points} points.\n{self.num1} {self.operation} {self.num2} = {self.correct_answer}",
            )
            self.play_sound("correct", freq=800, duration=180)

            self.current_question += 1

            # Quiz finished?
            if self.current_question >= self.total_questions:
                self.displayResults()
            else:
                self.generate_problem()
                self.displayProblem()

        else:
            # Incorrect
            self.play_sound("wrong", freq=300, duration=300)

            if self.first_attempt:
                self.first_attempt = False
                messagebox.showwarning("Incorrect", "Wrong! Try again.")
                self.displayProblem()
            else:
                messagebox.showerror(
                    "Incorrect",
                    f"Wrong again! The answer was {self.correct_answer}.",
                )

                self.current_question += 1

                if self.current_question >= self.total_questions:
                    self.displayResults()
                else:
                    self.generate_problem()
                    self.displayProblem()

    # --------------------------- RESULTS SCREEN --------------------------- #

    def displayResults(self):
        """Required function: display score + grade."""
        self.clear_frame()

        frame = tk.Frame(self.container, bg=self.colors["dark"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame,
            text="QUIZ COMPLETE!",
            font=self.title_font,
            bg=self.colors["dark"],
            fg=self.colors["light"],
        ).pack(pady=10)

        pct = (self.score / (self.total_questions * 10)) * 100

        tk.Label(
            frame,
            text=f"Final Score: {self.score} / 100 ({pct:.1f}%)",
            font=self.heading_font,
            bg=self.colors["dark"],
            fg=self.colors["muted"],
        ).pack(pady=5)

        # Grade
        if pct >= 90:
            grade = "A+"
            remark = "Outstanding! 🎉"
        elif pct >= 80:
            grade = "A"
            remark = "Excellent!"
        elif pct >= 70:
            grade = "B"
            remark = "Good work!"
        elif pct >= 60:
            grade = "C"
            remark = "Fair effort!"
        else:
            grade = "F"
            remark = "Keep practicing!"

        tk.Label(
            frame,
            text=f"Grade: {grade}",
            font=("Helvetica", 34, "bold"),
            bg=self.colors["dark"],
            fg=self.colors["primary"],
        ).pack(pady=10)

        tk.Label(
            frame,
            text=remark,
            font=self.normal_font,
            bg=self.colors["dark"],
            fg=self.colors["light"],
        ).pack(pady=5)

        # Action buttons
        tk.Button(
            frame,
            text="PLAY AGAIN",
            bg=self.colors["secondary"],
            fg="white",
            font=self.button_font,
            command=lambda: self.start_quiz(self.difficulty),
        ).pack(pady=10)

        tk.Button(
            frame,
            text="BACK TO MENU",
            bg=self.colors["primary"],
            fg="white",
            font=self.button_font,
            command=self.displayMenu,
        ).pack(pady=5)

        tk.Button(
            frame,
            text="QUIT GAME",
            bg=self.colors["danger"],
            fg="white",
            font=self.button_font,
            command=self.root.destroy,
        ).pack(pady=8)

    # --------------------------- UTILITY --------------------------- #

    def clear_frame(self):
        """Remove all widgets from the main container."""
        for widget in self.container.winfo_children():
            widget.destroy()


# --------------------------- RUN APP --------------------------- #

def main():
    root = tk.Tk()
    app = MathsQuiz(root)
    root.mainloop()


if __name__ == "__main__":
    main()