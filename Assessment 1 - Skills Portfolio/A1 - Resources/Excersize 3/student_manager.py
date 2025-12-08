"""
student_manager.py
-------------------
Human-written Student Manager application for Exercise 3.

Features:
- Sidebar menu (professional theme consistent with Exercises 1 & 2)
- Read and write studentMarks.txt safely (first line is student count)
- View all records (table), view individual, highest, lowest
- Sort (ascending/descending by overall percentage)
- Add, Delete, Update student records (file changes persist)
- Grades and percentage calculation (out of 160 total)
- Clear, modular code with explanatory comments

Usage:
 - Ensure studentMarks.txt sits in the same folder as this script.
 - Run: python student_manager.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import random
import copy

# --------------------------- Theme / Colours --------------------------- #
THEME = {
    "bg": "#2c3e50",       # dark background (sidebar)
    "panel": "#ecf0f1",    # light panel background
    "primary": "#3498db",  # blue
    "secondary": "#2ecc71",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "muted": "#7f8c8d",
    "text_dark": "#2c3e50",
}

DATA_FILE = "Assessment 1 - Skills Portfolio/A1 - Resources/Excersize 3/studentMarks.txt"  # expects same folder

# --------------------------- Helper Functions --------------------------- #
def read_students_from_file(path):
    """
    Read student data from file. Returns list of student dicts and declared_count.
    File format:
      first line: integer count
      subsequent lines: code,name,mark1,mark2,mark3,exam
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} not found.")

    students = []
    with open(path, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    if not lines:
        raise ValueError("File is empty.")

    # First line should be integer count
    try:
        declared_count = int(lines[0].strip())
    except Exception:
        raise ValueError("First line must be the integer number of students.")

    for ln in lines[1:]:
        if not ln.strip():
            continue
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) < 6:
            # skip invalid lines but report
            continue
        code = parts[0]
        name = parts[1]
        try:
            c1 = int(parts[2])
            c2 = int(parts[3])
            c3 = int(parts[4])
            exam = int(parts[5])
        except Exception:
            # skip invalid numeric lines
            continue
        students.append({
            "code": code,
            "name": name,
            "c1": c1,
            "c2": c2,
            "c3": c3,
            "exam": exam
        })

    return students, declared_count

def write_students_to_file(path, students):
    """
    Overwrite the file with updated students.
    First line is integer count, then each student line.
    """
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"{len(students)}\n")
        for s in students:
            line = f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n"
            fh.write(line)

def compute_coursework_total(student):
    """Total of three coursework marks (each out of 20)."""
    return student["c1"] + student["c2"] + student["c3"]

def compute_overall_percentage(student):
    """
    Overall percentage scaled from total available marks (60 Coursework + 100 Exam = 160).
    Return value between 0 and 100 (float).
    """
    total_course = compute_coursework_total(student)
    exam = student["exam"]
    overall = (total_course + exam) / 160.0 * 100.0
    return overall

def compute_grade(percent):
    """Return grade letter based on percentage."""
    if percent >= 70:
        return "A"
    if percent >= 60:
        return "B"
    if percent >= 50:
        return "C"
    if percent >= 40:
        return "D"
    return "F"

# --------------------------- Main Application --------------------------- #
class StudentManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Manager")
        self.master.geometry("1000x620")
        self.master.config(bg=THEME["bg"])

        # Data store
        try:
            self.students, declared = read_students_from_file(DATA_FILE)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not load {DATA_FILE}:\n{e}")
            self.students = []
        # keep a working copy for sorting/display
        self.display_students = copy.deepcopy(self.students)

        # Build UI (sidebar + content)
        self._build_sidebar()
        self._build_main_area()

        # show default view all
        self.view_all_records()

    # --------------------------- UI Construction --------------------------- #
    def _build_sidebar(self):
        sidebar = tk.Frame(self.master, bg=THEME["bg"], width=220)
        sidebar.pack(side="left", fill="y")

        # title
        title = tk.Label(sidebar, text="Student Manager", bg=THEME["bg"], fg=THEME["panel"], 
                         font=("Helvetica", 16, "bold"))
        title.pack(pady=(18,8))

        # Buttons list
        btn_config = {"font": ("Helvetica", 11), "width": 20, "padx": 6, "pady": 6}

        tk.Button(sidebar, text="1. View All Records", command=self.view_all_records, **btn_config).pack(pady=4)
        tk.Button(sidebar, text="2. View Individual", command=self.view_individual_prompt, **btn_config).pack(pady=4)
        tk.Button(sidebar, text="3. Highest Overall", command=self.show_highest, **btn_config).pack(pady=4)
        tk.Button(sidebar, text="4. Lowest Overall", command=self.show_lowest, **btn_config).pack(pady=4)

        # Separator
        sep = tk.Frame(sidebar, height=2, bg=THEME["panel"])
        sep.pack(fill="x", pady=10, padx=6)

        tk.Button(sidebar, text="5. Sort Records", command=self.sort_menu, **btn_config).pack(pady=4)
        tk.Button(sidebar, text="6. Add Student", command=self.add_student_prompt, **btn_config).pack(pady=4)
        tk.Button(sidebar, text="7. Delete Student", command=self.delete_student_prompt, **btn_config).pack(pady=4)
        tk.Button(sidebar, text="8. Update Student", command=self.update_student_prompt, **btn_config).pack(pady=4)

        # Spacer and Quit
        tk.Label(sidebar, text="", bg=THEME["bg"]).pack(expand=True, fill="y")
        tk.Button(sidebar, text="Quit", bg=THEME["danger"], fg="white", command=self.master.destroy,
                  font=("Helvetica", 11), width=20, padx=6, pady=6).pack(pady=10)

    def _build_main_area(self):
        # Main right panel
        self.main_panel = tk.Frame(self.master, bg=THEME["panel"])
        self.main_panel.pack(side="right", fill="both", expand=True)

        # Title of content area
        self.heading = tk.Label(self.main_panel, text="", bg=THEME["panel"], fg=THEME["text_dark"],
                                font=("Helvetica", 14, "bold"))
        self.heading.pack(pady=12)

        # Create a Treeview to show table data
        columns = ("code","name","coursework","exam","percentage","grade")
        self.tree = ttk.Treeview(self.main_panel, columns=columns, show="headings", height=18)
        self.tree.heading("code", text="Student No.")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("coursework", text="Coursework (out of 60)")
        self.tree.heading("exam", text="Exam (out of 100)")
        self.tree.heading("percentage", text="Overall %")
        self.tree.heading("grade", text="Grade")

        # column widths
        self.tree.column("code", width=100, anchor="center")
        self.tree.column("name", width=260, anchor="w")
        self.tree.column("coursework", width=140, anchor="center")
        self.tree.column("exam", width=100, anchor="center")
        self.tree.column("percentage", width=100, anchor="center")
        self.tree.column("grade", width=60, anchor="center")

        # add scrollbar
        vsb = ttk.Scrollbar(self.main_panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=12, pady=6)

        # Summary area (label)
        self.summary_lbl = tk.Label(self.main_panel, text="", bg=THEME["panel"], fg=THEME["text_dark"],
                                    font=("Helvetica", 11), anchor="w", justify="left")
        self.summary_lbl.pack(fill="x", padx=12, pady=(6,12))

    # --------------------------- Display Utilities --------------------------- #
    def _clear_tree(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

    def _populate_tree(self, students):
        """
        Given a list of students (dicts), populate the Treeview.
        """
        self._clear_tree()
        for s in students:
            coursework_total = compute_coursework_total(s)
            pct = compute_overall_percentage(s)
            grade = compute_grade(pct)
            self.tree.insert("", "end", values=(
                s["code"], s["name"], f"{coursework_total}/60", f"{s['exam']}/100", f"{pct:.1f}%", grade
            ))

    def _update_summary(self, students):
        if not students:
            self.summary_lbl.config(text="No student data available.")
            return
        count = len(students)
        avg = sum(compute_overall_percentage(s) for s in students) / count
        self.summary_lbl.config(text=f"Students: {count}   Average overall %: {avg:.2f}%")

    # --------------------------- Menu Actions --------------------------- #
    def view_all_records(self):
        """Menu item 1: View all student records and show summary."""
        self.heading.config(text="All Student Records")
        # Use display_students = full students
        self.display_students = copy.deepcopy(self.students)
        self._populate_tree(self.display_students)
        self._update_summary(self.display_students)

    def view_individual_prompt(self):
        """Ask user for student code or name, then show record."""
        self.heading.config(text="View Individual Student")
        # Prompt a small dialog offering both options
        answer = simpledialog.askstring("Select Student", "Enter student code or name (partial allowed):")
        if not answer:
            return
        query = answer.strip().lower()
        matches = [s for s in self.students if query in s["code"].lower() or query in s["name"].lower()]
        if not matches:
            messagebox.showinfo("No match", "No student matched your search.")
            return
        # If multiple matches, show a selection dialog
        if len(matches) > 1:
            sel = self._choose_from_list([f"{m['code']} - {m['name']}" for m in matches], title="Select Student")
            if sel is None:
                return
            index = sel
            selected = matches[index]
        else:
            selected = matches[0]
        # Display single record
        self.display_students = [selected]
        self._populate_tree(self.display_students)
        self._update_summary(self.display_students)

    def show_highest(self):
        """Menu item 3: Show student with highest overall mark."""
        if not self.students:
            messagebox.showinfo("No data", "No student records available.")
            return
        best = max(self.students, key=lambda s: compute_overall_percentage(s))
        self.heading.config(text="Student with Highest Overall Mark")
        self.display_students = [best]
        self._populate_tree(self.display_students)
        self._update_summary(self.display_students)

    def show_lowest(self):
        """Menu item 4: Show student with lowest overall mark."""
        if not self.students:
            messagebox.showinfo("No data", "No student records available.")
            return
        worst = min(self.students, key=lambda s: compute_overall_percentage(s))
        self.heading.config(text="Student with Lowest Overall Mark")
        self.display_students = [worst]
        self._populate_tree(self.display_students)
        self._update_summary(self.display_students)

    # --------------------------- Extension: Sort --------------------------- #
    def sort_menu(self):
        """Menu item 5: Ask ascending/descending and sort by overall percentage."""
        if not self.students:
            messagebox.showinfo("No data", "No student records available.")
            return
        choice = messagebox.askquestion("Sort Order", "Sort by overall percentage in ascending order? (No = descending)")
        ascending = True if choice == "yes" else False
        self.display_students = sorted(self.students, key=lambda s: compute_overall_percentage(s), reverse=not ascending)
        self._populate_tree(self.display_students)
        self.heading.config(text=f"Sorted Records ({'Ascending' if ascending else 'Descending'})")
        self._update_summary(self.display_students)

    # --------------------------- Extension: Add --------------------------- #
    def add_student_prompt(self):
        """Menu item 6: Prompt the user to add a new student record."""
        # Gather fields using simpledialogs for clarity
        self.heading.config(text="Add New Student")
        code = simpledialog.askstring("Student Code", "Enter student code (1000-9999):")
        if not code:
            return
        code = code.strip()
        if any(s["code"] == code for s in self.students):
            messagebox.showerror("Duplicate", "A student with this code already exists.")
            return

        name = simpledialog.askstring("Student Name", "Enter student name:")
        if not name:
            return
        try:
            c1 = int(simpledialog.askstring("Coursework 1", "Enter coursework 1 (0-20):"))
            c2 = int(simpledialog.askstring("Coursework 2", "Enter coursework 2 (0-20):"))
            c3 = int(simpledialog.askstring("Coursework 3", "Enter coursework 3 (0-20):"))
            exam = int(simpledialog.askstring("Exam", "Enter exam mark (0-100):"))
        except Exception:
            messagebox.showerror("Invalid", "One or more marks were not valid integers.")
            return

        # Validate ranges
        if any(not (0 <= m <= 20) for m in (c1, c2, c3)) or not (0 <= exam <= 100):
            messagebox.showerror("Invalid range", "Coursework must be 0-20 and exam 0-100.")
            return

        new_student = {"code": code, "name": name.strip(), "c1": c1, "c2": c2, "c3": c3, "exam": exam}
        self.students.append(new_student)
        # persist immediately
        write_students_to_file(DATA_FILE, self.students)
        messagebox.showinfo("Added", f"Student {name} added successfully.")
        self.view_all_records()

    # --------------------------- Extension: Delete --------------------------- #
    def delete_student_prompt(self):
        """Menu item 7: Delete a student by code or name."""
        if not self.students:
            messagebox.showinfo("No data", "No student records available.")
            return
        query = simpledialog.askstring("Delete Student", "Enter student code or name to delete:")
        if not query:
            return
        query = query.strip().lower()
        matches = [s for s in self.students if query in s["code"].lower() or query in s["name"].lower()]
        if not matches:
            messagebox.showinfo("No match", "No matching student found.")
            return
        if len(matches) > 1:
            sel = self._choose_from_list([f"{m['code']} - {m['name']}" for m in matches], title="Pick to Delete")
            if sel is None:
                return
            to_delete = matches[sel]
        else:
            to_delete = matches[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete {to_delete['code']} - {to_delete['name']}?")
        if not confirm:
            return
        self.students = [s for s in self.students if s["code"] != to_delete["code"]]
        write_students_to_file(DATA_FILE, self.students)
        messagebox.showinfo("Deleted", f"Student {to_delete['name']} deleted.")
        self.view_all_records()

    # --------------------------- Extension: Update --------------------------- #
    def update_student_prompt(self):
        """Menu item 8: Update a chosen student's record."""
        if not self.students:
            messagebox.showinfo("No data", "No records to update.")
            return
        query = simpledialog.askstring("Update Student", "Enter student code or name to update:")
        if not query:
            return
        query = query.strip().lower()
        matches = [s for s in self.students if query in s["code"].lower() or query in s["name"].lower()]
        if not matches:
            messagebox.showinfo("No match", "No student matched your search.")
            return
        if len(matches) > 1:
            sel = self._choose_from_list([f"{m['code']} - {m['name']}" for m in matches], title="Pick to Update")
            if sel is None:
                return
            student = matches[sel]
        else:
            student = matches[0]

        # present a sub-menu of fields
        fields = ["Student Code", "Student Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam"]
        sel = self._choose_from_list(fields, title="Choose field to update")
        if sel is None:
            return

        if fields[sel] == "Student Code":
            new_code = simpledialog.askstring("New Code", "Enter new student code:")
            if not new_code:
                return
            if any(s["code"] == new_code and s is not student for s in self.students):
                messagebox.showerror("Duplicate", "Another student has that code.")
                return
            student["code"] = new_code.strip()
        elif fields[sel] == "Student Name":
            new_name = simpledialog.askstring("New Name", "Enter new student name:")
            if not new_name:
                return
            student["name"] = new_name.strip()
        elif fields[sel] in ("Coursework 1", "Coursework 2", "Coursework 3"):
            field_map = {"Coursework 1":"c1","Coursework 2":"c2","Coursework 3":"c3"}
            key = field_map[fields[sel]]
            try:
                val = int(simpledialog.askstring("New Mark", f"Enter new mark for {fields[sel]} (0-20):"))
            except Exception:
                messagebox.showerror("Invalid", "Please enter an integer.")
                return
            if not (0 <= val <= 20):
                messagebox.showerror("Invalid range", "Coursework mark must be 0-20.")
                return
            student[key] = val
        elif fields[sel] == "Exam":
            try:
                val = int(simpledialog.askstring("New Mark", "Enter new exam mark (0-100):"))
            except Exception:
                messagebox.showerror("Invalid", "Please enter an integer.")
                return
            if not (0 <= val <= 100):
                messagebox.showerror("Invalid range", "Exam mark must be 0-100.")
                return
            student["exam"] = val

        # Persist changes
        write_students_to_file(DATA_FILE, self.students)
        messagebox.showinfo("Updated", "Student record updated successfully.")
        self.view_all_records()

    # --------------------------- Small Helpers --------------------------- #
    def _choose_from_list(self, items, title="Choose"):
        """
        Present a simple chooser dialog returning the selected index or None.
        Uses a modal Toplevel with a Listbox.
        """
        dlg = tk.Toplevel(self.master)
        dlg.transient(self.master)
        dlg.grab_set()
        dlg.title(title)
        dlg.geometry("420x300")
        dlg.configure(bg=THEME["panel"])

        lbl = tk.Label(dlg, text=title, bg=THEME["panel"], font=("Helvetica", 12, "bold"))
        lbl.pack(pady=(8,4))

        lb = tk.Listbox(dlg, width=60, height=10)
        lb.pack(padx=12, pady=8, expand=True, fill="both")

        for it in items:
            lb.insert("end", it)

        sel_index = {"value": None}

        def on_ok():
            try:
                sel = lb.curselection()
                if not sel:
                    sel_index["value"] = None
                else:
                    sel_index["value"] = sel[0]
                dlg.destroy()
            except Exception:
                dlg.destroy()

        def on_cancel():
            sel_index["value"] = None
            dlg.destroy()

        btn_frame = tk.Frame(dlg, bg=THEME["panel"])
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="OK", width=12, command=on_ok).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancel", width=12, command=on_cancel).pack(side="left", padx=8)

        self.master.wait_window(dlg)
        return sel_index["value"]

# --------------------------- Run the application --------------------------- #
def main():
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
