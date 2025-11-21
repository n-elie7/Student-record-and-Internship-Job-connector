class StudentController:
    """Controller for student operations"""
    
    def __init__(self, student_model, internship_model, application_model, view):
        self.student = student_model
        self.internship = internship_model
        self.application = application_model
        self.view = view
    
    def run(self):
        """Run the student menu loop"""
        while True:
            self.view.display_student_menu()
            choice = input("\nEnter choice: ").strip()
            try:
                if choice == "1":
                    self._view_profile()
                elif choice == "2":
                    self._list_open_internships()
                elif choice == "3":
                    self._apply_to_internship()
                elif choice == "4":
                    self._view_my_applications()
                elif choice == "5":
                    break
                else:
                    print("Invalid choice.")
            except Exception as e:
                print("Error:", e)
    
    def _view_profile(self):
        reg_no = self.view.input_nonempty("\nEnter your reg_no: ")
        student = self.student.find_student_by_reg_no(reg_no)

        if student:
            print("\n" + self.view.format_table([student]))
        else:
            print("\nReg_no not found")
    
    def _list_open_internships(self):
        lst = self.internship.get_open_internships()
        if not lst:
            print("\nNo open internships.")
        else:
            print(f"\n{self.view.format_table(lst)}")
    
    def _apply_to_internship(self):
        reg_no = self.view.input_nonempty("\nYour reg_no: ")
        internship_id = int(self.view.input_nonempty("Internship ID: "))
        note = input("Note (optional): ").strip() or None

        self.application.apply_to_internship(reg_no, internship_id, note)

        print(f"\nApplied to internship {internship_id}.")
    
    def _view_my_applications(self):
        reg_no = self.view.input_nonempty("\nYour reg_no: ")
        apps = self.application.get_applications_for_student(reg_no)

        if not apps:
            print("\nNo applications available.")
        else:
            formatted_apps = []
            for app in apps:
                formatted_apps.append({
                    'App ID': app.get('id'),
                    'Internship': app.get('internships', {}).get('title'),
                    'Company': app.get('internships', {}).get('company'),
                    'Status': app.get('status'),
                    'Applied At': app.get('applied_at', '')[:10] if app.get('applied_at') else '',
                    'Note': app.get('note', '')[:50] + '...' if app.get('note') and len(app.get('note', '')) > 50 else app.get('note', '')
                })
            print(f"\n{self.view.format_table(formatted_apps)}")
