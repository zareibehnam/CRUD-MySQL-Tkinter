# CRUD-MySQL-Tkinter

This is a Python application built with Tkinter and MySQL Connector for creating, reading, updating, and deleting (CRUD) data in a MySQL database. The application provides a graphical user interface (GUI) for interacting with the database tables.

## Features

- Connects to a MySQL database.
- Dynamically generates tabs for each table in the database.
- Allows CRUD operations on the tables.
- Utilizes stored procedures for data manipulation.
- Provides logging functionality to track application events.

## Prerequisites

- Python 3.x
- Tkinter (usually included in Python standard library)
- MySQL Connector for Python

## Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/your-username/database-form-app.git
```

2. Install the required dependencies:

```
pip install mysql-connector-python
```

3. Update the MySQL connection details in the `DatabaseForm` class constructor (`__init__`) in `main.py`:

```python
self.mydb = mysql.connector.connect(
    host="localhost",
    user="your-username",
    password="your-password",
    database="your-database"
)
```

4. Run the application:

```
python main.py
```

## Usage

1. Launch the application by running `main.py`.
2. Enter your MySQL database credentials.
3. Navigate through the tabs to view and manipulate data in different tables.
4. Use the provided buttons for CRUD operations: Create, Read (Select), Update, Delete.
5. Data changes are logged to `app.log` in the project directory.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Make sure to replace placeholders like `your-username`, `your-password`, and `your-database` with your actual database credentials and details. Also, ensure that the file paths and dependencies mentioned in the README are accurate based on your project structure and setup.
