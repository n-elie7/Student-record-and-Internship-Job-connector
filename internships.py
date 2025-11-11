import sqlite3


def add_internship(title, company, location, duration, stipend, description, deadline):
    conn = sqlite3.connect("student_internship.db")
cur = sqlite3.connect.cursor()
