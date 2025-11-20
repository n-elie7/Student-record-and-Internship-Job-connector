from database.listener import start_realtime_listener
from menu.menus import admin_menu, student_menu
from setup_env import supabase as sb


def main():
    # simple ping to validate keys
    try:
        # run an innocuous request
        sb.table("students").select("id").limit(1).execute()
    except Exception as e:
        print("\n[ERROR] Could not connect to Supabase:", e)
        return
    # Start realtime listener on background thread
    start_realtime_listener()
    # CLI
    while True:
        print("\n=== Student Record & Internships Connector ===")
        print("\n1) Admin")
        print("2) Student")
        print("3) Exit")
        choice = input("\nEnter choice: ").strip()
        if choice == "1":
            admin_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            print("\nGoodbye.")
            print("")
            break
        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()
