from tabulate import tabulate


class MenuView:
    """View class for rendering menus and displaying data"""
    @staticmethod
    def input_nonempty(prompt):
        """Get non-empty input from user"""
        while True:
            v = input(prompt).strip()
            if v:
                return v
    
    @staticmethod
    def format_table(data, headers="keys", tablefmt="fancy_grid"):
        """Format data as a beautiful table"""
        if not data:
            return "No data to display."
        return tabulate(data, headers=headers, tablefmt=tablefmt)
    
    @staticmethod
    def display_admin_menu():
        """Display admin menu options"""
        print("\n-- ADMIN MENU --")
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
    
    @staticmethod
    def display_student_menu():
        """Display student menu options"""
        print("\n-- STUDENT MENU --")
        print("\n1. View Profile")
        print("2. List Open Internships")
        print("3. Apply to Internship")
        print("4. View My Applications")
        print("5. Back")
    
    @staticmethod
    def display_main_menu():
        """Display main menu"""
        print("\n=== Student Record & Internship System ===")
        print("\n1) Admin")
        print("2) Student")
        print("3) Exit")
