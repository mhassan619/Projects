from abc import ABC, abstractmethod
from student_management import InvalidMarksError,DuplicateSubjectError
class Person(ABC):
    def __init__(self,name,age):
        self.name = name
        self._age = age
    @abstractmethod
    def info(self):
        pass
class Student(Person):
    def __init__(self, name, age,roll_no):
        super().__init__(name, age)
        self.roll_no = roll_no
        self.__marks = {}
    def add_marks(self,subject,marks):
        if not 0 <= marks <= 100:
            raise InvalidMarksError(marks)
        if subject in self.__marks:
            raise DuplicateSubjectError(marks)
        self.__marks[subject]=marks
        print(f"{subject}:{marks} added.")
    def get_marks(self):
        return self.__marks
    def average(self):
        if not self.__marks:
            return 0
        avg = sum(self.__marks.values()) / len(self.__marks)
        return avg
    def grade(self):
        avg = self.average()
        if avg >= 80:
            return "A"
        elif 70 <= avg <= 79:
            return "B"
        elif 60 <= avg <= 69:
            return "C"
        elif 50 <= avg <= 59:
            return "D"
        else:
            return "F"
    def info(self):
        print(f"Name:{self.name}")
        print(f"Age:{self._age}")
        print(f"Roll No:{self.roll_no}")
        print(f"Average:{self.average():.1f}%")
        print(f"Grade:{self.grade()}")
    def report_card(self):
        print(f"\n{'='*35}")
        print(f"        REPORT CARD")
        print(f"{'='*35}")
        print(f"  Name:{self.name}")
        print(f"  Roll No:{self.roll_no}")
        print(f"  Age:{self._age}")
        print(f"{'-'*35}")
        for subject,marks in self.__marks.items():
            print(f"  {subject}:{marks}/100")
        print(f"{'-'*35}")
        print(f"  Average:{self.average():.1f}%")
        print(f"  Grade:{self.grade()}")
        print(f"{'='*35}")
    def to_dict(self):
        return {
            "name":self.name,
            "age":self._age,
            "roll_no":self.roll_no,
            "marks":self.get_marks()
        }
    @classmethod
    def from_dict(cls,data):
        student = cls(data['name'],data['age'],data['roll_no'])
        for subject,marks in data['marks'].items():
            student.add_marks(subject,marks)
        return student 