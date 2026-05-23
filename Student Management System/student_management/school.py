import json
from student_management import timer,logger
from student_management import Student,StudentNotFoundError
class School:
    def __init__(self,school_name):
        self.school_name = school_name
        self.__students = []
    @logger
    def add_student(self,student):
        self.__students.append(student)
    def find_student(self,roll_no):
        for student in self.__students:
            if student.roll_no == roll_no:
                return student
            raise StudentNotFoundError(roll_no)
    def top_student(self):
        return max(self.__students, key=lambda s: s.average())
    def all_students(self):
        if not self.__students:
            print(f"There are no students yet.")
        for student in self.__students:
            print(f"{student.info()}")
    @timer
    def school_report(self):
        print(f"\n{'='*35}")
        print(f"        {self.school_name}")
        print(f"        SCHOOL REPORT")
        print(f"{'='*35}")
        print(f"Total Students:{len(self.__students)}")
        print(f"Top Student:{self.top_student().name} - {self.top_student().average():.1f}%")
        print(f"\n{'*'*35}")
        print(f"      ALL ENROLLED STUDENTS")
        for student in self.__students:
            print(f"{student.name} - {student.average():.1f}%")
    def save_to_file(self,filename):
        data = {
            "school_name":self.school_name,
            "students":[s.to_dict() for s in self.__students]
        }
        with open(filename,"w") as f:
            json.dump(data,f,indent=4)
        print(f"Data saved into {filename}")
    def load_from_file(self,filename):
        try:
            with open(filename,'r') as f:
                data = json.load(f)
                for student_data in data['students']:
                    student = Student.from_dict(student_data)
                    self.__students.append(student)
                print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print(f"❌ File not found - Fresh start1")
    def student_grades(self):
        for student in self.__students:
            yield f"{student.name}:{student.grade()}"
    def passing_students(self):
        for student in self.__students:
            if student.average() >= 50:
                yield student