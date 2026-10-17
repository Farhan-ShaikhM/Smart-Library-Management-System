# Smart Library Management System

A Python desktop application for managing a library's books, readers and borrowing transactions, backed by a relational database. The system supports separate roles for Admins, Librarians and Readers, each with their own module and permissions.

<!-- Add screenshots of the login screen and main dashboards here -->
<!-- ![Login screen](screenshots/login.png) -->

## Features

### Login & Registration
- User registration for new readers
- Role-based login for Admin, Librarian and Reader

### Admin Module
- Manage librarian and user accounts
- Oversee library records

### Librarian Module
- Add, update and remove books
- Manage reader records
- Process book issue and return transactions

### Reader Module
- Browse available books
- Borrow books and view borrowed books

### Database
- Relational schema for books, users and transactions
- Foreign keys with cascade rules to keep related records consistent

## Tech Stack

- **Language:** Python
- **GUI:** [Tkinter / other – fill in]
- **Database:** [MySQL / SQLite – fill in]

## Project Structure

```
main.py                Application entry point
Login_Module/          Login screen and authentication
Registration_Module/   New user registration
Admin_Module/          Admin features
Librarian_Module/      Book, reader and transaction management
Reader_Module/         Reader-facing features
DB_Stuff/              Database schema and setup scripts
Synopsis Stuff/        Project synopsis and documentation
```

## Getting Started

### Prerequisites
- Python 3.x
- [Database name – fill in] installed and running

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Farhan-ShaikhM/Smart-Library-Management-System.git
   cd Smart-Library-Management-System
   ```
2. Install dependencies
   ```bash
   pip install [packages – fill in, e.g. mysql-connector-python]
   ```
3. Set up the database using the scripts in `DB_Stuff/`
4. Update the database connection details in [file name – fill in]
5. Run the application
   ```bash
   python main.py
   ```

## Future Improvements

- Fine calculation for late returns
- Search and filter for books
- Email reminders for due dates
- Password hashing for stored credentials

## Contributors

- Farhan Shaikh – [GitHub](https://github.com/Farhan-ShaikhM)
- Adiy Rahman – [GitHub](https://github.com/Adiy-Rahman)


