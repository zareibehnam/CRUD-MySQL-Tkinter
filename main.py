import tkinter as tk
from tkinter import ttk
import mysql.connector
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Bicycle_Shop")

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your pass",
            database="your_db"
        )

        if self.mydb.is_connected():
            db_Info = self.mydb.get_server_info()
            print("Connected to MySQL Server version ", db_Info, "\n#################################################")
            logging.info(f"Connected to MySQL Server version {db_Info}")

        self.cursor = self.mydb.cursor()
        self.tables = self.get_table_names()
        self.create_widgets()

    def get_table_names(self):
        try:
            # Execute a query to retrieve table names
            self.cursor.execute("SHOW TABLES")
            tables = [table[0] for table in self.cursor.fetchall()]
            return tables
        except Exception as e:
            logging.error(f"Error retrieving table names: {str(e)}")

    def create_widgets(self):
        # Create a notebook with tabs for each table
        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10)

        # Create tabs for each table dynamically
        for table in self.tables:
            if table == 'customers_factor':
                continue
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=table)

            # Fetch column names for the current table
            columns = self.get_column_names(table)

            # Create table form and CRUD buttons
            self.create_table_form(tab, table, columns)
            self.create_crud_buttons(tab, table, [columns[0]])  # Assuming the first column is a primary key

        # Close connection when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        try:
            # Close the database connection when the window is closed
            self.cursor.close()
            self.mydb.close()
            self.root.destroy()
            logging.info("Database connection closed.")
        except Exception as e:
            logging.error(f"Error closing database connection: {str(e)}")

    def create_table_form(self, parent, table_name, columns):
        frame = ttk.Frame(parent)
        frame.pack(padx=100, pady=50)

        # Label and entry/dropdown widgets for each column
        for col in columns:
            ttk.Label(frame, text=f"{col.capitalize()}:").grid(row=columns.index(col), column=0, padx=5, pady=15)
            setattr(self, f"{table_name}_{col}_entry", ttk.Entry(frame))
            getattr(self, f"{table_name}_{col}_entry").grid(row=columns.index(col), column=1, padx=10, pady=10)

    def create_crud_buttons(self, parent, table_name, key_columns):
        frame = ttk.Frame(parent)
        frame.pack(pady=15)

        # Create CSUD buttons
        ttk.Button(frame, text="Create", command=lambda: self.insert_data(table_name)).grid(row=0, column=0, padx=8)
        ttk.Button(frame, text="Select", command=lambda: self.select_data(table_name)).grid(row=0, column=1, padx=8)
        ttk.Button(frame, text="Update", command=lambda: self.update_data(table_name, key_columns)).grid(row=0, column=2, padx=8)
        ttk.Button(frame, text="Delete", command=lambda: self.delete_data(table_name, key_columns)).grid(row=0, column=3, padx=8)

    def get_column_names(self, table_name):
        # Execute a query to retrieve column names for a specific table
        self.cursor.execute(f"DESCRIBE {table_name}")
        columns = [column[0] for column in self.cursor.fetchall()]
        return columns

    def insert_data(self, table_name):
        try:
            # Extract values from entry/dropdown widgets
            columns = self.get_column_names(table_name)
            values = []

            for col in columns:
                value = getattr(self, f"{table_name}_{col}_entry").get()
                values.append(value)

            # Execute the stored procedure
            self.cursor.callproc(f"create_{table_name}", values)
            logging.info(f"Inserting data into {table_name}")
            self.mydb.commit()

            # Clear entry/dropdown widgets after submission
            for col in columns:
                # if col in ['P_code', 'Body_code']:
                #     getattr(self, f"{table_name}_{col}_var").set(self.get_foreign_key_values(col)[0])
                # else:
                getattr(self, f"{table_name}_{col}_entry").delete(0, 'end')

            logging.info("Data inserted successfully.")
        except Exception as e:
            logging.error(f"Error inserting data into {table_name}: {str(e)}")


    def select_data(self, table_name):

        cursor = self.cursor
        columns = self.get_column_names(table_name)
        id = [getattr(self, f"{table_name}_{col}_entry").get() for col in columns][0]

        # Execute the stored procedure
        
        sql = f"CALL read_{table_name}(%s);"
        val = [id]
        #excute
        self.cursor.execute(sql,val)

        result = cursor.fetchall()
        logging.info(f"Selected data from {table_name}")
        # Display the result in a new window
        result_window = tk.Toplevel(self.root)
        result_window.title(f"{table_name} Data")

        tree = ttk.Treeview(result_window)
        tree["columns"] = tuple(self.cursor.column_names)
        tree["show"] = "headings"

        for col in self.cursor.column_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in result:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill="both")
        self.cursor.nextset()

    def update_data(self, table_name, key_columns):
        cursor = self.cursor

        # Extract values from entry widgets
        columns = self.get_column_names(table_name)
        values = [getattr(self, f"{table_name}_{col}_entry").get() for col in columns]

        # Execute the stored procedure
        cursor.callproc(f"update_{table_name}", values)
        logging.info(f"Updating data in {table_name}")
        self.mydb.commit()

    def delete_data(self, table_name, key_columns):
        cursor = self.cursor

        # Extract key values
        key_values = [getattr(self, f"{table_name}_{col}_entry").get() for col in key_columns]

      
        # Execute the stored procedure
        cursor.callproc(f"delete_{table_name}", key_values)
        logging.info(f"Deleting data from {table_name}")
        self.mydb.commit()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseForm(root)
    root.mainloop()

