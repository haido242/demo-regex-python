import re
import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
from student import Student, StudentManager


class AddStudentForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Add Student')
        
        self.name_label = tk.Label(self, text='Name:')
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_error_label = tk.Label(self, text='', fg='red')
        self.name_error_label.grid(row=1, column=1, padx=5, pady=0, sticky='w')
        
        self.age_label = tk.Label(self, text='Age:')
        self.age_label.grid(row=2, column=0, padx=5, pady=5)
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)
        self.age_error_label = tk.Label(self, text='', fg='red')
        self.age_error_label.grid(row=3, column=1, padx=5, pady=0, sticky='w')
        
        self.gender_label = tk.Label(self, text='Gender:')
        self.gender_label.grid(row=4, column=0, padx=5, pady=5)
        self.gender_var = tk.StringVar(self)
        self.gender_var.set("male")  # Default value
        self.gender_menu = tk.OptionMenu(self, self.gender_var, "male", "female")
        self.gender_menu.grid(row=4, column=1, padx=5, pady=5)
        
        self.score_label = tk.Label(self, text='Score:')
        self.score_label.grid(row=6, column=0, padx=5, pady=5)
        self.score_entry = tk.Entry(self)
        self.score_entry.grid(row=6, column=1, padx=5, pady=5)
        self.score_error_label = tk.Label(self, text='', fg='red')
        self.score_error_label.grid(row=7, column=1, padx=5, pady=0, sticky='w')
        
        self.add_button = tk.Button(self, text='Add Student', command=self.add_student)
        self.add_button.grid(row=8, columnspan=2, padx=5, pady=5)
        
        # Validation functions
        validate_name = self.register(self.validate_name)
        validate_age = self.register(self.validate_age)
        validate_score = self.register(self.validate_score)
        
        # Apply validation to entry widgets
        self.name_entry.config(validate="key", validatecommand=(validate_name, "%P"))
        self.age_entry.config(validate="key", validatecommand=(validate_age, "%P"))
        self.score_entry.config(validate="key", validatecommand=(validate_score, "%P"))
        
    def validate_name(self, name):
        print (name)
        if re.match(r'^[a-zA-Z\s]*$', name) or name == "":
            self.name_error_label.config(text='')
            return True
        else:
            self.name_error_label.config(text='Name can only contain letters and spaces')
            return False
        
    def validate_age(self, age):
        if re.match(r'^\d*$', age) or age == "":
            self.age_error_label.config(text='')
            return True
        else:
            self.age_error_label.config(text='Age can only contain numbers')
            return False
        
    def validate_score(self, score):
        if re.match(r'^\d*(\.\d{0,2})?$', score) or score == "":
            self.score_error_label.config(text='')
            return True
        else:
            self.score_error_label.config(text='Score can only contain numbers and a decimal point')
            return False
        
    def add_student(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_var.get()
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
            #alert
            messagebox.showerror('Error', 'Unable to load file.')

    def save_students(self):
        try:
            self.student_manager.save_to_file_txt('students.txt')
        except IOError:
            #alert
            messagebox.showerror('Error', 'Unable to save file.')

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