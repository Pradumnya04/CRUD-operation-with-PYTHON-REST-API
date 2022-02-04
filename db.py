import sqlite3

conn = sqlite3.connect("emp_data.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE IF NOT EXISTS emps
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    First_Name TEXT ,
                    Last_Name TEXT ,
                    Company_Name TEXT,
                    Branch TEXT)"""
cursor.execute(sql_query)

