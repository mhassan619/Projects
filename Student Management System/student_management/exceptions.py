class InvalidMarksError(Exception):
    def __init__(self, marks):
        super().__init__(f" ❌ Marks {marks} invalid! Marks should be between 1 to 100.")

class DuplicateSubjectError(Exception):
    def __init__(self, subject):
        super().__init__(f"❌ {subject} already exists!")

class StudentNotFoundError(Exception):
    def __init__(self, roll_no):
        super().__init__(f"❌ Student with Roll No {roll_no} is not found.")