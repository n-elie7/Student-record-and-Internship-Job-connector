from applications import (
    apply_to_internship,
    change_application_status,
    get_all_applications,
    get_applications_for_student,
)
from helper_wrappers import _exec_table_select
from internships import add_internship, get_all_internships, get_open_internships
from students import (
    add_student,
    delete_student,
    find_student_by_reg_no,
    get_all_students,
    search_students_by_name,
    update_student,
)


def input_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v


def admin_menu():
    while True:
        print("\n-- ADMIN MENU --")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Add Internship")
        print("7. View Internships")
        print("8. View Applications")
        print("9. Change Application Status")
        print("10. Export Table (CSV)")
        print("11. Back")
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                name = input_nonempty("Name: ")
                roll = input_nonempty("Roll no: ")
                age = input("Age (optional): ").strip() or None
                age = int(age) if age else None
                course = input("Course (optional): ").strip() or None
                gpa = input("GPA (optional): ").strip() or None
                gpa = float(gpa) if gpa else None
                add_student(name, roll, age, course, gpa)
                print("Student added.")
            elif choice == "2":
                s = get_all_students()
                if not s:
                    print("No students.")
                for r in s:
                    print(r)
            elif choice == "3":
                q = input_nonempty("Enter roll or name substring: ")
                by_roll = find_student_by_reg_no(q)
                if by_roll:
                    print(by_roll)
                else:
                    lst = search_students_by_name(q)
                    if not lst:
                        print("No matches.")
                    for r in lst:
                        print(r)
            elif choice == "4":
                roll = input_nonempty("Roll no to update: ")
                name = input("New name (blank to skip): ").strip() or None
                age = input("New age (blank to skip): ").strip() or None
                age = int(age) if age else None
                course = input("New course (blank to skip): ").strip() or None
                gpa = input("New gpa (blank to skip): ").strip() or None
                gpa = float(gpa) if gpa else None
                update_student(roll, name=name, age=age, course=course, gpa=gpa)
                print("Update attempted.")
            elif choice == "5":
                roll = input_nonempty("Roll no to delete: ")
                confirm = input(f"Type YES to confirm deletion of {roll}: ").strip()
                if confirm == "YES":
                    delete_student(roll)
                    print("Deleted (if existed).")
                else:
                    print("Cancelled.")
            elif choice == "6":
                title = input_nonempty("Title: ")
                company = input("Company: ").strip() or None
                location = input("Location: ").strip() or None
                duration = input("Duration: ").strip() or None
                stipend = input("Stipend: ").strip() or None
                description = input("Description: ").strip() or None
                deadline = (
                    input("Deadline YYYY-MM-DD (blank if none): ").strip() or None
                )
                add_internship(
                    title, company, location, duration, stipend, description, deadline
                )
                print("Internship added.")
            elif choice == "7":
                it = get_all_internships()
                if not it:
                    print("No internships.")
                for r in it:
                    print(r)
            elif choice == "8":
                apps = get_all_applications()
                if not apps:
                    print("No applications.")
                for a in apps:
                    print(a)
            elif choice == "9":
                aid = int(input_nonempty("Application ID: "))
                st = input_nonempty(
                    "New status (Applied/Shortlisted/Rejected/Hired/Pending): "
                )
                change_application_status(aid, st)
                print("Status changed (if application exists).")
            elif choice == "10":
                import csv

                tbl = input_nonempty("Table (students/internships/applications): ")
                fname = input_nonempty("Filename to save (e.g. out.csv): ")
                data = _exec_table_select(tbl, "*")
                if not data:
                    print("No rows to export.")
                else:
                    keys = list(data[0].keys())
                    with open(fname, "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=keys)
                        writer.writeheader()
                        writer.writerows(data)
                    print("Exported to", fname)
            elif choice == "11":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)


def student_menu():
    while True:
        print("\n-- STUDENT MENU --")
        print("1. View Profile")
        print("2. List Open Internships")
        print("3. Apply to Internship")
        print("4. View My Applications")
        print("5. Back")
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                roll = input_nonempty("Enter your roll no: ")
                s = find_student_by_reg_no(roll)
                print(s if s else "Not found")
            elif choice == "2":
                lst = get_open_internships()
                if not lst:
                    print("No open internships.")
                for r in lst:
                    print(r)
            elif choice == "3":
                roll = input_nonempty("Your roll no: ")
                iid = int(input_nonempty("Internship ID: "))
                note = input("Note (optional): ").strip() or None
                apply_to_internship(roll, iid, note)
                print("Applied (or error thrown).")
            elif choice == "4":
                roll = input_nonempty("Your roll no: ")
                apps = get_applications_for_student(roll)
                if not apps:
                    print("No applications.")
                for a in apps:
                    print(a)
            elif choice == "5":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)
