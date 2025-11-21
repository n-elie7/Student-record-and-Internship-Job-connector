from database.helper_wrappers import Database
from database.listener import RealtimeListener
from menu.menus import MenuView
from controllers.admin_controller import AdminController
from controllers.student_controller import StudentController

class MainApplication:
    """Main application class following MVC pattern"""
    
    def __init__(self):
        # Initialize database
        self.db = Database()
        
        # Initialize models
        from crud.students import Student
        from crud.internships import Internship
        from crud.applications import Application
        
        self.student_model = Student(self.db)
        self.internship_model = Internship(self.db)
        self.application_model = Application(self.db, self.student_model, self.internship_model)
        
        # Initialize view
        self.view = MenuView()
        
        # Initialize controllers
        self.admin_controller = AdminController(
            self.student_model, self.internship_model, 
            self.application_model, self.view
        )
        self.student_controller = StudentController(
            self.student_model, self.internship_model,
            self.application_model, self.view
        )
        
        # Initialize realtime listener
        self.listener = RealtimeListener()
    
    def connect_to_database(self):
        """Test database connection"""
        try:
            self.db._exec_table_select("students", "id")
            return True
        except Exception as e:
            print(f"\n[ERROR] Could not connect to Supabase: {e}")
            return False
    
    def run(self):
        """Run the main application"""
        if not self.connect_to_database():
            return
        
        # Start realtime listener
        self.listener.start_realtime_listener()
        
        # Main menu loop
        while True:
            self.view.display_main_menu()
            choice = input("\nEnter choice: ").strip()
            
            if choice == "1":
                self.admin_controller.run()
            elif choice == "2":
                self.student_controller.run()
            elif choice == "3":
                print("\nGoodbye!")
                print("")
                break
            else:
                print("\nInvalid choice.")

def main():
    app = MainApplication()
    app.run()

if __name__ == "__main__":
    main()
