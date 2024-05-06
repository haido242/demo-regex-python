
import re


class Student:
    def __init__(self, name, age, gender, score):
        self.name = name
        self.age = age
        self.gender = gender
        self.score = score

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