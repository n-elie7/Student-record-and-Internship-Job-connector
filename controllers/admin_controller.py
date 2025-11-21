import csv

class AdminController:
    """Controller for admin operations"""
    
    def __init__(self, student_model, internship_model, application_model, view):
        self.student = student_model
        self.internship = internship_model
        self.application = application_model
        self.view = view

    def run(self):
        """Run the admin menu loop"""
        while True:
            self.view.display_admin_menu()
            choice = input("\nEnter choice: ").strip()
            try:
                if choice == "1":
                    self._add_student()
                elif choice == "2":
                    self._view_all_students()
                elif choice == "3":
                    self._search_student()
                elif choice == "4":
                    self._update_student()
                elif choice == "5":
                    self._delete_student()
                elif choice == "6":
                    self._add_internship()
                elif choice == "7":
                    self._view_internships()
                elif choice == "8":
                    self._view_applications()
                elif choice == "9":
                    self._change_application_status()
                elif choice == "10":
                    self._export_table()
                elif choice == "11":
                    break
                else:
                    print("Invalid choice.")
            except Exception as e:
                print("Error:", e)

    def _add_student(self):
        name = self.view.input_nonempty("\nName: ")
        reg_no = self.view.input_nonempty("Reg no: ")
        age = input("Age (optional): ").strip() or None
        age = int(age) if age else None
        course = input("Course (optional): ").strip() or None
        gpa = input("GPA (optional): ").strip() or None
        gpa = float(gpa) if gpa else None

        self.student.add_student(name, reg_no, age, course, gpa)

        print("\nStudent added successfully.")
    
    def _view_all_students(self):
        students = self.student.get_all_students()
        if not students:
            print("\nNo students available.")
        else:
            print(f"\n{self.view.format_table(students)}")
    
    def _search_student(self):
        answer = self.view.input_nonempty("Enter reg_no or name substring: ")
        by_reg_no = self.student.find_student_by_reg_no(answer)
        if by_reg_no:
            print(f"\n{self.view.format_table([by_reg_no])}")
        else:
            lst = self.student.search_students_by_name(answer)
            if not lst:
                print("No student matches found.")
            else:
                print(f"\n{self.view.format_table(lst)}")
    
    def _update_student(self):
        reg_no = self.view.input_nonempty("Reg no to update: ")
        name = input("New name (blank to skip): ").strip() or None
        age = input("New age (blank to skip): ").strip() or None
        age = int(age) if age else None
        course = input("New course (blank to skip): ").strip() or None
        gpa = input("New gpa (blank to skip): ").strip() or None
        gpa = float(gpa) if gpa else None

        self.student.update_student(reg_no, name=name, age=age, course=course, gpa=gpa)

        print("\nUpdated student successfully.")
    
    def _delete_student(self):
        reg_no = self.view.input_nonempty("Reg no to delete: ")

        is_exist = self.student.find_student_by_reg_no(reg_no)

        if not is_exist:
            print("\nReg_no not found.")
            
        confirm = input(f"\nType YES to confirm deletion of {reg_no}: ").strip()
        if confirm.lower() == "yes":
            self.student.delete_student(reg_no)
            print(f"\nDeleted {reg_no} successfully.")
        else:
            print("\nCancelled deletion.")
    
    def _add_internship(self):
        title = self.view.input_nonempty("\nTitle: ")
        company = input("Company: ").strip() or None
        location = input("Location: ").strip() or None
        duration = input("Duration: ").strip() or None
        stipend = input("Stipend: ").strip() or None
        description = input("Description: ").strip() or None
        deadline = input("Deadline YYYY-MM-DD: ").strip() or None

        self.internship.add_internship(title, company, location, duration, stipend, description, deadline)

        print("\nInternship added successfully.")
    
    def _view_internships(self):
        internships = self.internship.get_all_internships()
        if not internships:
            print("\nNo internships available.")
        else:
            print(f"\n{self.view.format_table(internships)}")
    
    def _view_applications(self):
        applications = self.application.get_all_applications()
        if not applications:
            print("\nNo applications available.")
        else:
            formatted_applications = []
            for app in applications:
                formatted_applications.append({
                    'App ID': app.get('id'),
                    'Student': app.get('students', {}).get('name'),
                    'Roll No': app.get('students', {}).get('reg_no'),
                    'Internship': app.get('internships', {}).get('title'),
                    'Company': app.get('internships', {}).get('company'),
                    'Status': app.get('status'),
                    'Applied At': app.get('applied_at', '')[:10] if app.get('applied_at') else '',
                    'Note': app.get('note', '')[:30] + '...' if app.get('note') and len(app.get('note', '')) > 30 else app.get('note', '')
                })
            print(f"\n{self.view.format_table(formatted_applications)}")
    
    def _change_application_status(self):
        application_id = int(self.view.input_nonempty("Application ID: "))

        applications = self.application.get_all_applications()

        app_ids = [app["id"] for app in applications]
        if application_id not in app_ids:
            print("\nApplication ID not found.")
            
        status_options = (
            "Applied",
            "Shortlisted",
            "Rejected",
            "Hired",
            "Pending",
        )

        status = self.view.input_nonempty("\nNew status (Applied/Shortlisted/Rejected/Hired/Pending): ")

        if status not in status_options:
            print("\nInvalid status option.")
        else:
            self.application.change_application_status(application_id, status)
            print(f"\nStatus changed to {status}.")
    
    def _export_table(self):
        from database import Database
        db = Database()

        table_options = ("students", "internships", "applications")
        table = self.view.input_nonempty("\nTable (students/internships/applications): ")

        if table not in table_options:
            print("\nInvalid table name.")
        else:
            filename = self.view.input_nonempty("Filename (e.g. out.csv): ")
            data = db._exec_table_select(table, "*")

            if not data:
                print("\nNo data to export.")
            else:
                keys = list(data[0].keys())
                with open(filename, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)
                print(f"Exported to {filename}")

