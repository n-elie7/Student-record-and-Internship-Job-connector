from database import DEFAULT_DB, init_db

def main(db_path=DEFAULT_DB):
    init_db(db_path)
    print("\n=== STUDENT RECORD & INTERNSHIP CONNECTOR ===\n")
    while True:
        print("Select role:")
        print("1) Admin")
        print("2) Student")
        print("3) Exit")
        role = input("Enter choice: ").strip()
        if role == '3':
            print('\nGoodbye.')
            break
        if role == '1':
            pass
        elif role == '2':
            pass
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
    except Exception as e:
        print("Unhandled error:", e)
