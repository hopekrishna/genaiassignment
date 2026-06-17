# Student Grade System

name = input("Enter student name: ")
marks = float(input("Enter student marks (0-100): "))

if marks < 0 or marks > 100:
    print("Invalid marks! Please enter marks between 0 and 100.")
elif marks >= 90:
    grade = "A+"
elif marks >= 80:
    grade = "A"
elif marks >= 70:
    grade = "B"
elif marks >= 60:
    grade = "C"
elif marks >= 50:
    grade = "D"
else:
    grade = "F"

if 0 <= marks <= 100:
    print("\n----- Result -----")
    print("Student Name:", name)
    print("Marks:", marks)
    print("Grade:", grade)
