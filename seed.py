#!/usr/bin/python3
"""
Seed Supabase DB with dummy data for SRIC.
Uses SUPABASE_SERVICE_ROLE_KEY (set as env var).
"""

from datetime import date, timedelta
from setup_env import supabase as sb

def seed_students():
    students = [
        {"name":"Niyubwayo Irakoze Elie","reg_no":"S001","age":21,"course":"Computer Science","gpa":3.8},
        {"name":"Ngabo Denzel","reg_no":"S002","age":22,"course":"Information Systems","gpa":3.6},
        {"name":"Iradukunda Suwafa","reg_no":"S003","age":20,"course":"Software Engineering","gpa":3.9},
        {"name":"Gathungu Collins","reg_no":"S004","age":23,"course":"AI and Data Science","gpa":3.7},
        {"name":"Kaliza Sabrina","reg_no":"S005","age":21,"course":"Cybersecurity","gpa":3.5},
    ]
    for s in students:
        try:
            sb.table("students").insert(s).execute()
        except Exception as e:
            print("Skip student (maybe exists):", s["reg_no"], e)
    print("Seeded students.")

def seed_internships():
    today = date.today()
    internships = [
        {"title":"Frontend Developer Intern","company":"TechNure Ltd","location":"Kigali","duration":"3 months","stipend":"RWF 150,000","description":"React/Next.js work","application_deadline":(today + timedelta(days=30)).isoformat()},
        {"title":"Data Analyst Intern","company":"DataSense","location":"Remote","duration":"2 months","stipend":"RWF 120,000","description":"Data cleaning & analysis","application_deadline":(today + timedelta(days=20)).isoformat()},
        {"title":"Mobile App Intern","company":"VoltSol","location":"Kigali","duration":"4 months","stipend":"RWF 200,000","description":"Flutter apps","application_deadline":(today + timedelta(days=45)).isoformat()},
        {"title":"Cybersecurity Assistant","company":"SafeNet Africa","location":"Remote","duration":"3 months","stipend":"RWF 130,000","description":"Security audits","application_deadline":(today + timedelta(days=25)).isoformat()},
    ]
    for i in internships:
        try:
            sb.table("internships").insert(i).execute()
        except Exception as e:
            print("Skip internship:", i["title"], e)
    print("Seeded internships.")

def seed_applications():
    applications = [
        {"student_id":1,"internship_id":1,"note":"Interested in frontend"},
        {"student_id":2,"internship_id":2,"note":"Data enthusiast"},
        {"student_id":3,"internship_id":1,"note":"UI passion"},
        {"student_id":4,"internship_id":3,"note":"Mobile apps experience"},
        {"student_id":5,"internship_id":4,"note":"Security background"},
    ]
    for a in applications:
        try:
            sb.table("applications").insert(a).execute()
        except Exception as e:
            print("Skip application:", a, e)
    print("Seeded applications.")

def main():
    print("Seeding database...")
    seed_students()
    seed_internships()
    seed_applications()
    print("Done.")

if __name__ == "__main__":
    main()
