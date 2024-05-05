import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import re
from tkinter import ttk
from student import Student

# class Student:
#     def __init__(self, name, age, gender, score):
#         self.name = name
#         self.age = age
#         self.gender = gender
#         self.score = score

class StudentManager:
    def __init__(self):
        self.students = []
        
    def add_student(self, student):
        self.students.append(student)
        
    def save_to_file_txt(self, filename):
        try:
            with open(filename, 'w') as file:
                for student in self.students:
                    file.write(f"{student.name},{student.age},{student.gender},{float(student.score)}\n")
            print("File saved successfully.")
        except IOError:
            print("Error: Unable to save file.")
    
    def load_from_file_txt(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    match = re.match(r'([^,]+),(\d+),([^,]+),(\d+\.\d+)', line.strip())
                    if match:
                        name, age, gender, score = match.groups()
                        age = int(age)
                        self.students.append(Student(name, age, gender, score))
            print("File loaded successfully.")
        except IOError:
            print("Error: Unable to load file.")

# create ui

class AddStudentForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Add Student')
        
        self.name_label = tk.Label(self, text='Name:')
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.age_label = tk.Label(self, text='Age:')
        self.age_label.grid(row=1, column=0, padx=5, pady=5)
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.gender_label = tk.Label(self, text='Gender:')
        self.gender_label.grid(row=2, column=0, padx=5, pady=5)
        self.gender_entry = tk.Entry(self)
        self.gender_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.score_label = tk.Label(self, text='Score:')
        self.score_label.grid(row=3, column=0, padx=5, pady=5)
        self.score_entry = tk.Entry(self)
        self.score_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.add_button = tk.Button(self, text='Add Student', command=self.add_student)
        self.add_button.grid(row=4, columnspan=2, padx=5, pady=5)
        
    def add_student(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        score = self.score_entry.get()
        
        if self.master.validate_input(name, age, gender, score):
            student = Student(name, age, gender, score)
            self.master.student_manager.add_student(student)
            messagebox.showinfo('Success', 'Student added successfully.')
            self.master.update_table()
            self.destroy()
        else:
            messagebox.showerror('Error', 'Invalid input.')

class StudentManagerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Student Manager')
        self.geometry('600x400')
        
        self.student_manager = StudentManager()
        
        self.tree = ttk.Treeview(self)
        self.tree["columns"]=("Name","Age","Gender","Score")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Name", width=150)
        self.tree.column("Age", width=50)
        self.tree.column("Gender", width=100)
        self.tree.column("Score", width=50)
        
        self.tree.heading("#0",text="")
        self.tree.heading("Name",text="Name")
        self.tree.heading("Age",text="Age")
        self.tree.heading("Gender",text="Gender")
        self.tree.heading("Score",text="Score")
        
        self.tree.pack(fill="both", expand=True)
        
        self.load_students()

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Add Student", command=self.open_add_student_form)
        self.file_menu.add_command(label="Save Students", command=self.save_students)
        self.file_menu.add_command(label="Load Students", command=self.load_students)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)



    def open_add_student_form(self):
        AddStudentForm(self)
        
    def update_table(self):
        for student in self.tree.get_children():
            self.tree.delete(student)
        for student in self.student_manager.students:
            self.tree.insert("", "end", values=(student.name, student.age, student.gender, student.score))
        
    def load_students(self):
        # remove all students from the list
        self.student_manager.students = []
        try:
            self.student_manager.load_from_file_txt('students.txt')
            self.update_table()
        except IOError:
            print("Error: Unable to load file.")

    def save_students(self):
        try:
            self.student_manager.save_to_file_txt('students.txt')
        except IOError:
            print("Error: Unable to save file.")

    def validate_input(self, name, age, gender, score):
        if not name or not age or not gender or not score:
            return False
        
        if not re.match(r'^[a-zA-Z\s]+$', name):
            return False
        
        if not re.match(r'^\d+$', str(age)):
            return False
        
        if not re.match(r'^(?:male|female)$', gender, re.IGNORECASE):
            return False
        
        if not re.match(r'^\d+(\.\d+)?$', str(score)):
            return False
        
        return True

if __name__ == '__main__':
    app = StudentManagerUI()
    app.mainloop()
