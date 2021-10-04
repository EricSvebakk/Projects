
import sqlite3

# Connects to database
connect = sqlite3.connect("mydatabase42.db")

# Creates cursor
c = connect.cursor()

# NULL
# INTEGER
# REAL
# TEXT
# BLOB

# =======================================================================
# Creates table
# c.execute("""UPDATE TABLE customers (
#     first_name text,
#     last_name text,
#     email text
# );""")


# =======================================================================
# Inserts single value into database
# connect.execute("INSERT INTO customers VALUES('heyo', 'test123',  '456');")


# =======================================================================
# List of values for database
# many_customers = [
# 	("Tom", "Andre", "111"),
# 	("Tayna", "lemos", "222"),
# 	("Victoria", "Andersen", "333")
# ]

# # Inserts several values into table
# c.executemany("INSERT INTO customers VALUES (?,?,?);", many_customers)


# =======================================================================
# Fetches values from table
# c.execute("SELECT rowid, * FROM customers;")

# header = ("rowId", "FirstName", "LastName", "Email")
# myList = [header] + c.fetchall()

# pad = 20
# for row in range(len(myList)):
# 	tempRow = ""
# 	for item in range(len(myList[row])):
# 		tempRow += f"{myList[row][item]:<{pad}}"
		
# 	print(tempRow)


# =======================================================================
# Query database for specific rows
# c.execute("SELECT rowid, * FROM customers WHERE email LIKE '1%';")
# print(c.fetchall())

# Commits table to database
connect.commit()

# Closes connects
connect.close()
