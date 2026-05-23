from student_management.student import Student
from student_management.school import School
from student_management.exceptions import (InvalidMarksError,StudentNotFoundError,DuplicateSubjectError)
school = School("Al-Hassan Academy")
s1 = Student("Hassan",21,"CS-01")
s2 = Student("Mohsan",23,"ENG-01")
s3 = Student("Faisal",24,"ZOO-01")
s1.add_marks("Programming Fundamentals",90)
s1.add_marks("OOP",80)
s1.add_marks("DSA",78)
s2.add_marks("Literature",87)
s2.add_marks("POETRY",70)
s2.add_marks("Linguistics",99)
s3.add_marks("Medicine",45)
s3.add_marks("Fermentation",49)
s3.add_marks("Medicine_2",37)
school.add_student(s1)
school.add_student(s2)
school.add_student(s3)
## Use Generators
print("\n✅ Passing Students:")
for student in school.passing_students():
    print(f" -> {student.name} - {student.average():.1f}%")
print("\n All Grades:")
for grade_info in school.student_grades():
    print(f"-> {grade_info}")