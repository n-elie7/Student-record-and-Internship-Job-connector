# SRIC - Student Record Internship System

A collaborative CLI-based application for managing student records, internships, and applications with **real-time updates** across multiple users using Supabase.

## Features

- **Real-time Collaboration**: Changes made by any user are instantly reflected across all running instances
- **Student Management**: Add, view, search, update, and delete student records
- **Internship Management**: Create and manage internship opportunities
- **Application Tracking**: Students can apply to internships and track their application status
- **Admin Controls**: Manage applications, change statuses, and export data to CSV
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Prerequisites

- Python 3.10 or higher
- Supabase account (free tier works)
- Internet connection

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/n-elie7/Student-record-and-Internship-Job-connector.git
cd Student-record-and-Internship-Job-connector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
supabase>=2.0.0
python-dotenv>=1.0.0
certifi>=2023.0.0
psycopg2-binary>=2.9.0
```

### 3. Set Up Supabase

#### Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign up/login
2. Click **"New Project"**
3. Fill in project details and click **"Create new project"**
4. Wait for the project to be provisioned (~2 minutes)

#### Get Your Credentials

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **Anon/Public Key** (long string starting with `eyJ...`)

#### Create Database Tables

1. In Supabase dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Paste and run this SQL:

```sql
-- Create students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    reg_no TEXT UNIQUE NOT NULL,
    age INTEGER,
    course TEXT,
    gpa DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create internships table
CREATE TABLE internships (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    duration TEXT,
    stipend TEXT,
    description TEXT,
    application_deadline DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create applications table
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    internship_id INTEGER REFERENCES internships(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'Pending',
    note TEXT,
    applied_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(student_id, internship_id)
);

-- Enable Row Level Security (RLS)
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE internships ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;

-- Enable Realtime
ALTER PUBLICATION supabase_realtime ADD TABLE students;
ALTER PUBLICATION supabase_realtime ADD TABLE internships;
ALTER PUBLICATION supabase_realtime ADD TABLE applications;
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# .env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
```

**Important:** Replace the values with your actual Supabase credentials!

### 5. Fix SSL Certificates (macOS Only)

If you're on macOS, run this once:

```bash
# Option 1: Use the installer
/Applications/Python\ 3.13/Install\ Certificates.command

# Option 2: Or set environment variable
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
```

Windows and Linux users can skip this step.

## Running the Application

```bash
python3 main.py
```

You should see:
```
🚀 Connecting to Supabase... ✓ Connected!
👂 [Realtime] Listening for changes...

========================================
SRIC - Student Record Internship System
========================================
1) Admin
2) Student
3) Exit
Enter choice:
```

## Multi-User Collaboration

To test real-time collaboration:

1. **Terminal 1** (You):
   ```bash
   python3 main.py
   ```

2. **Terminal 2** (Teammate):
   ```bash
   python3 main.py
   ```

When your teammate adds/updates/deletes a record, you'll see:
```
🔔 [Realtime] students - INSERT
   → {'id': 1, 'name': 'John Doe', 'reg_no': 'S001', ...}
```

## Usage Guide

### Admin Functions

1. **Add Student**: Register new students with reg_no number, name, age, course, and GPA
2. **View All Students**: Display complete list of registered students
3. **Search Student**: Find students by reg_no number or name
4. **Update Student**: Modify existing student information
5. **Delete Student**: Remove student records
6. **Add Internship**: Create new internship opportunities
7. **View Internships**: List all available internships
8. **View Applications**: See all student applications
9. **Change Application Status**: Update status (Pending/Shortlisted/Rejected/Hired)
10. **Export Table (CSV)**: Export students, internships, or applications data

### Student Functions

1. **View Profile**: Look up your student profile by reg_no number
2. **List Open Internships**: View internships that haven't passed their deadline
3. **Apply to Internship**: Submit an application with optional note
4. **View My Applications**: Track your application status

## Project Structure

```
student-record-internship-system/
├── main.py                 # Entry point
├── setup_env.py           # Supabase configuration
├── listener.py            # Real-time listener
├── helper_wrappers.py     # Database helper functions
├── students.py            # Student CRUD operations
├── internships.py         # Internship CRUD operations
├── applications.py        # Application CRUD operations
├── menus.py               # CLI menu interfaces
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
├── seed.py                # initiates database with some data
└── README.md             # This file
```

## Troubleshooting

### "Connection failed" Error

**Problem:** Cannot connect to Supabase

**Solutions:**
- Check your `.env` file has correct `SUPABASE_URL` and `SUPABASE_ANON_KEY`
- Ensure you have internet connection
- Verify your Supabase project is active

### SSL Certificate Error (macOS)

**Problem:** `[SSL: CERTIFICATE_VERIFY_FAILED]`

**Solution:**
```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

### "Table does not exist" Error

**Problem:** Database tables not created

**Solution:**
- Go to Supabase dashboard → SQL Editor
- Run the SQL script from the setup section above

### Realtime Updates Not Working

**Problem:** Changes from other users don't appear

**Solutions:**
- Verify Realtime is enabled on tables (see SQL setup)
- Check Supabase dashboard → Database → Replication
- Restart the application

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'supabase'`

**Solution:**
```bash
pip install -r requirements.txt
```

## Security Notes

- The current setup uses RLS policies with public access for simplicity
- For production, implement proper authentication and authorization
- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore`:
  ```
  .env
  __pycache__/
  *.pyc
  ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


## Authors

**Team 404**

---

**Happy Coding! 🎉**
