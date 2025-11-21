from crud.applications import Application
from database.helper_wrappers import Database
from crud.internships import Internship
from crud.students import Student

from tabulate import tabulate


def input_nonempty(prompt):
    while True:
        response = input(prompt).strip()
        if response:
            return response


def admin_menu():
    while True:
        print("\n=== ADMIN MENU ===")
        print("\n1. Add Student")
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
        choice = input("\nEnter choice: ").strip()
        try:
            if choice == "1":
                name = input_nonempty("\nName: ")
                reg_no = input_nonempty("Reg no: ")
                age = input("Age (optional): ").strip() or None
                age = int(age) if age else None
                course = input("Course (optional): ").strip() or None
                gpa = input("GPA (optional): ").strip() or None
                gpa = float(gpa) if gpa else None

                Student.add_student(name, reg_no, age, course, gpa)

                print("\nStudent added.")
            elif choice == "2":
                students = Student.get_all_students()

                data = []
                if not students:
                    print("\nNo students.")
                for student in students:
                    data.append(student)
                print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
            elif choice == "3":
                answer = input_nonempty("\nEnter reg_no or name substring: ")
                by_reg_no = Student.find_student_by_reg_no(answer)

                data = []
                if by_reg_no:
                    data.append(by_reg_no)
                    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
                else:
                    students = Student.search_students_by_name(answer)
                    data = []
                    if not students:
                        print("\nNo student matches.")
                    for student in students:
                        data.append(student)
                    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
            elif choice == "4":
                reg_no = input_nonempty("\nReg no to update: ")
                name = input("New name (blank to skip): ").strip() or None
                age = input("New age (blank to skip): ").strip() or None
                age = int(age) if age else None
                course = input("New course (blank to skip): ").strip() or None
                gpa = input("New gpa (blank to skip): ").strip() or None
                gpa = float(gpa) if gpa else None

                Student.update_student(reg_no, name=name, age=age, course=course, gpa=gpa)

                print("\nUpdate attempted.")
            elif choice == "5":
                reg_no = input_nonempty("\nReg no to delete: ")

                is_exist = Student.find_student_by_reg_no(reg_no)

                if not is_exist:
                    print("\nReg_no not found.")
                    continue

                confirm = input(f"\nType YES to confirm deletion of {reg_no}: ").strip()

                if confirm.lower() == "yes":
                    Student.delete_student(reg_no)
                    print(f"\nDeleted {reg_no} successfully.")
                else:
                    print("\nCancelled deletion.")
            elif choice == "6":
                title = input_nonempty("\nTitle: ")
                company = input("Company: ").strip() or None
                location = input("Location: ").strip() or None
                duration = input("Duration: ").strip() or None
                stipend = input("Stipend: ").strip() or None
                description = input("Description: ").strip() or None
                deadline = (
                    input("Deadline YYYY-MM-DD (blank if none): ").strip() or None
                )

                Internship.add_internship(
                    title, company, location, duration, stipend, description, deadline
                )

                print("\nInternship added successfully.")
            elif choice == "7":
                internships = Internship.get_all_internships()

                data = []

                if not internships:
                    print("\nNo internships found.")
                for internship in internships:
                    data.append(internship)

                print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
            elif choice == "8":
                applications = Application.get_all_applications()

                data = []

                if not applications:
                    print("\nNo applications found.")
                for application in applications:
                    data.append(application)

                print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
            elif choice == "9":
                application_id = int(input_nonempty("\nApplication ID: "))

                applications = Application.get_all_applications()

                app_ids = [app["id"] for app in applications]
                if application_id not in app_ids:
                    print("\nApplication ID not found.")
                    continue

                status_options = (
                    "Applied",
                    "Shortlisted",
                    "Rejected",
                    "Hired",
                    "Pending",
                )

                status = input_nonempty(
                    "New status (Applied/Shortlisted/Rejected/Hired/Pending): "
                )

                if status not in status_options:
                    print("\nInvalid status option.")
                    continue

                Application.change_application_status(application_id, status)
                print(f"\nStatus changed to {status}.")
            elif choice == "10":
                import csv

                table_options = ("students", "internships", "applications")
                table = input_nonempty("\nTable (students/internships/applications): ")

                if table not in table_options:
                    print("\nInvalid table name.")
                    continue

                filename = input_nonempty("Filename to save (e.g. filename.csv): ")
                data = Database._exec_table_select(table, "*")
                if not data:
                    print("\nNo data to export.")
                else:
                    keys = list(data[0].keys())
                    with open(filename, "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=keys)
                        writer.writeheader()
                        writer.writerows(data)
                    print("Exported to", filename)
            elif choice == "11":
                break
            else:
                print("\nPlease enter correct number(1-11)")
        except Exception as e:
            print("Error:", e)


def student_menu():
    while True:
        print("\n=== STUDENT MENU ===")
        print("\n1. View Profile")
        print("2. List Open Internships")
        print("3. Apply to Internship")
        print("4. View My Applications")
        print("5. Back")
        choice = input("\nEnter choice: ").strip()
        try:
            if choice == "1":
                reg_no = input_nonempty("\nEnter your reg_no: ")
                student = Student.find_student_by_reg_no(reg_no)

                data = []
                if student:
                    data.append(student)
                else:
                    print("\nReg_no not found")
                print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
            elif choice == "2":
                open_internships = Internship.get_open_internships()

                data = []

                if not open_internships:
                    print("\nNo open internships.")
                for internship in open_internships:
                    data.append(internship)
                print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
            elif choice == "3":
                reg_no = input_nonempty("\nYour reg_no: ")
                internship_id = int(input_nonempty("Internship ID: "))
                note = input("Note (optional): ").strip() or None

                Application.apply_to_internship(reg_no, internship_id, note)

                print(f"\nApplied to internship {internship_id}.")
            elif choice == "4":
                reg_no = input_nonempty("\nYour reg_no: ")
                applications = Application.get_applications_for_student(reg_no)

                data = []

                if not applications:
                    print("\nNo applications yet.")
                for application in applications:
                    data.append(application)
                print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
            elif choice == "5":
                break
            else:
                print("Please enter correct number(1-5)")
        except Exception as e:
            print("Error:", e)
