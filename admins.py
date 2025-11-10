#!/usr/bin/python3
from database import get_connection:
students = []
def add_student(name, reg_no, age, course, gpa):
    name = input("Enter the names of the student: ")
    reg_no = int(input("Enter the registration number of the student: "))
    age = int(input("Enter the age: "))
    course = input("Enter the enrollment course: ")
    gpa = int(input("Enter the GPA: "))
    students.append(name, reg_no, age, course, gpa)
    if students is None:
        return f"THE STUDENT HAS BEEN ADDED SUCCESSFULY"
    return f"ERROR HAS OCCURED"
