"""
alexa_jokes.py
---------------
Exercise 2 — "Alexa tell me a Joke"
Human-written, polished Tkinter GUI that:
 - Loads jokes from randomJokes.txt (setup?punchline per line)
 - Shows a setup when "Alexa tell me a Joke" is clicked
 - Reveals punchline on "Show Punchline"
 - "Next Joke" gives a new random joke (no repeats until exhausted)
 - "Quit" closes the program

Drop this file into the same folder as randomJokes.txt.
Optional extras:
 - If you have sounds.py with welcome/correct/wrong, the script will use it for small UI sounds.
"""

import tkinter as tk
from tkinter import messagebox, font
import random
import os
import sys


try:
    import sounds
    HAVE_SOUNDS = True
except Exception:
    HAVE_SOUNDS = False


try:
    import winsound
    HAVE_WINSOUND = True
except Exception:
    HAVE_WINSOUND = False


try:
    from background import THEME
    HAVE_BACKGROUND = True
except Exception:
    HAVE_BACKGROUND = False
    THEME = {
        "dark": "#2c3e50",
        "light": "#ecf0f1",
        "primary": "#3498db",
        "secondary": "#2ecc71",
        "danger": "#e74c3c",
        "muted": "#7f8c8d",
        "button": "#66d9ff",
        "accent": "#ff7ab6"
    }


class AlexaJokesApp:
    """Main GUI class for the Alexa-style joke teller."""

    def __init__(self, root, jokes_file="Assessment 1 - Skills Portfolio/A1 - Resources/Excersize 2/randomJokes.txt"):
        """Create the UI and load jokes."""
        self.root = root
        self.root.title("Alexa — Tell Me a Joke")
        self.root.geometry("760x420")
        self.root.resizable(False, False)

        # Fonts (human-chosen and readable)
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.setup_font = font.Font(family="Helvetica", size=16)
        self.punch_font = font.Font(family="Helvetica", size=16, slant="italic")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        # State
        self.jokes_file = jokes_file
        self.all_jokes = []        # list of (setup, punchline)
        self.remaining = []        # jokes not yet told in this cycle
        self.current_joke = None   # currently shown (setup, punchline)
        self.audio_enabled = HAVE_SOUNDS or (HAVE_WINSOUND and sys.platform == "win32")

        # Build UI
        self._build_ui()

        # Load jokes (safe)
        try:
            self.load_jokes(self.jokes_file)
        except FileNotFoundError:
            messagebox.showerror("Missing file", f"Could not find {self.jokes_file} in the folder.")
            # keep app running but disable joke buttons
            self.tell_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            self.punch_btn.config(state="disabled")

    # -------------------- UI construction -------------------- #
    def _build_ui(self):
        """Create and place widgets."""
        self.container = tk.Frame(self.root, bg=THEME.get("dark"))
        self.container.pack(fill="both", expand=True)

        # Title area
        title_frame = tk.Frame(self.container, bg=THEME.get("dark"))
        title_frame.place(relx=0.5, rely=0.12, anchor="center")

        title_label = tk.Label(title_frame, text="Alexa — Tell Me a Joke", font=self.title_font,
                               bg=THEME.get("dark"), fg=THEME.get("light"))
        title_label.pack()

        subtitle = tk.Label(title_frame, text="Press the button and Alexa will tell you a joke!",
                            font=self.setup_font, bg=THEME.get("dark"), fg=THEME.get("muted"))
        subtitle.pack(pady=(6, 0))

        # Card area for the joke setup + punchline
        card = tk.Frame(self.container, bg=THEME.get("light"), bd=2, relief="ridge")
        card.place(relx=0.5, rely=0.45, anchor="center", width=700, height=220)

        # Setup label (large, left-aligned)
        self.setup_lbl = tk.Label(card, text="(Alexa is ready to tell you a joke)", wraplength=660,
                                  justify="center", font=self.setup_font, bg=THEME.get("light"),
                                  fg=THEME.get("dark"))
        self.setup_lbl.pack(pady=(20, 6))

        # Punchline label (hidden until requested)
        self.punch_lbl = tk.Label(card, text="", wraplength=660, justify="center",
                                  font=self.punch_font, bg=THEME.get("light"), fg=THEME.get("primary"))
        self.punch_lbl.pack(pady=(6, 14))

        # Button row
        btn_frame = tk.Frame(self.container, bg=THEME.get("dark"))
        btn_frame.place(relx=0.5, rely=0.82, anchor="center")

        self.tell_btn = tk.Button(btn_frame, text="Alexa tell me a Joke", font=self.button_font,
                                  bg=THEME.get("primary"), fg="white", padx=18, pady=8,
                                  command=self.tell_joke)
        self.tell_btn.grid(row=0, column=0, padx=8)

        self.punch_btn = tk.Button(btn_frame, text="Show Punchline", font=self.button_font,
                                   bg=THEME.get("accent"), fg="white", padx=18, pady=8,
                                   command=self.show_punchline, state="disabled")
        self.punch_btn.grid(row=0, column=1, padx=8)

        self.next_btn = tk.Button(btn_frame, text="Next Joke", font=self.button_font,
                                  bg=THEME.get("secondary"), fg="white", padx=18, pady=8,
                                  command=self.next_joke, state="disabled")
        self.next_btn.grid(row=0, column=2, padx=8)

        quit_btn = tk.Button(btn_frame, text="Quit", font=self.button_font,
                             bg=THEME.get("danger"), fg="white", padx=18, pady=8,
                             command=self.root.destroy)
        quit_btn.grid(row=0, column=3, padx=8)

        # Small status/credit
        credit = tk.Label(self.container, text="Jokes from randomJokes.txt — Developed for Exercise 2",
                          font=("Helvetica", 9), bg=THEME.get("dark"), fg=THEME.get("muted"))
        credit.place(relx=0.5, rely=0.95, anchor="center")

    # -------------------- Joke file handling -------------------- #
    def load_jokes(self, filepath):
        """
        Load jokes from a text file.
        Each line: setup?punchline
        Returns list of tuples.
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError(filepath)

        jokes = []
        with open(filepath, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                # split at the first question mark
                if "?" in line:
                    setup, punch = line.split("?", 1)
                    setup = setup.strip()
                    punch = punch.strip()
                    if setup and punch:
                        jokes.append((setup + "?", punch))
                else:
                    # If no question mark, skip it (keeps dataset clean)
                    continue

        if not jokes:
            raise ValueError("No valid jokes found in file.")

        self.all_jokes = jokes
        # Start with a shuffled copy for non-repeating picks
        self.remaining = list(self.all_jokes)
        random.shuffle(self.remaining)

    # -------------------- Joke selection & UI updates -------------------- #
    def _select_random(self):
        """Return a (setup, punchline) tuple without repeats until exhausted."""
        if not self.remaining:
            # refill (allow repeats after full cycle)
            self.remaining = list(self.all_jokes)
            random.shuffle(self.remaining)
        return self.remaining.pop()

    def tell_joke(self):
        """Handler for 'Alexa tell me a Joke' button. Shows setup only."""
        try:
            joke = self._select_random()
        except Exception as e:
            messagebox.showerror("Error", f"Could not select a joke: {e}")
            return

        self.current_joke = joke
        setup, _ = joke
        self.setup_lbl.config(text=setup)
        self.punch_lbl.config(text="")       # hide punchline until requested

        # Enable punchline and next buttons
        self.punch_btn.config(state="normal")
        self.next_btn.config(state="normal")

        # play a gentle UI sound if available
        self._play_ui_sound("welcome")

    def show_punchline(self):
        """Show the punchline for the current joke."""
        if not self.current_joke:
            messagebox.showinfo("No joke yet", "Ask Alexa to tell you a joke first.")
            return

        _, punch = self.current_joke
        self.punch_lbl.config(text=punch)

        # small UI sound for reveal
        self._play_ui_sound("correct")

    def next_joke(self):
        """Quickly show a new setup (equivalent to pressing 'Alexa tell me a Joke')."""
        # simply call tell_joke again
        self.tell_joke()

    def _play_ui_sound(self, key):
        """Play optional UI sounds safely. Key names arbitrary (welcome/correct/wrong)."""
        if not self.audio_enabled:
            return

        # If sounds module is available, use keys; otherwise fallback to simple beep
        if HAVE_SOUNDS:
            try:
                sounds.play_sound(key)
                return
            except Exception:
                pass

        if HAVE_WINSOUND and sys.platform == "win32":
            try:
                # a short beep to signal action
                winsound.Beep(700 if key == "welcome" else 900, 150)
            except Exception:
                pass

# -------------------- Entry point -------------------- #
def main():
    root = tk.Tk()
    app = AlexaJokesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()