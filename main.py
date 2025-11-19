from listener import start_realtime_listener
from menus import admin_menu, student_menu
from setup_env import supabase as sb


def main():
    print("Connecting to Supabase...", end=" ")
    # simple ping to validate keys
    try:
        # run an innocuous request
        sb.table("students").select("id").limit(1).execute()
    except Exception as e:
        print("\n[ERROR] Could not connect to Supabase:", e)
        return
    print("OK.")
    # Start realtime listener on background thread
    start_realtime_listener()
    # CLI
    while True:
        print("\n=== SRIC (Supabase) ===")
        print("1) Admin")
        print("2) Student")
        print("3) Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            admin_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
