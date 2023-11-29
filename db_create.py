import mysql.connector

dataBase = mysql.connector.connect(
	host = 'localhost',
	user =
	passwd =
	)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE qr")


print("All Done!")