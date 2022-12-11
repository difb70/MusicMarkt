import psycopg2
import psycopg2.extras

DB_HOST = "127.0.0.1"
DB_USER = "tommy"
DB_PASSWORD = "tommy123"
DB_DATABASE = "musicmarkt"
DB_CONNECTION_STRING = f"host={DB_HOST} dbname={DB_DATABASE} user={DB_USER} password={DB_PASSWORD}"

#   CONNECTION
# -------------- #
# connect with db
def connect():
	try:
		db_connection = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	except:
		print("Error : Unable to connect to the database")
		exit()

	return db_connection, cursor

# close db connection
def close(connection, cursor):
	connection.close()
	cursor.close()



#    TABLES
# ------------ #
USERS = "users"
USER_ID = "id"
USER_NAME = "name"
USER_NUMBER = "number"



#    A P I
# ------------ #
# create user
def create_user(id, name, number):
	global connection, cursor
	query = f"INSERT INTO {USERS} VALUES (%s, %s, %s);"

	# execute and save changes made to the database
	cursor.execute(query, (id, name, number))
	connection.commit()


# delete user
def delete_user(id):
	global connection, cursor
	query = f"DELETE FROM {USERS} WHERE {USER_ID} = %s"

	# execute and save changes made to the database
	cursor.execute(query, (id, ))
	connection.commit()


# get users
def get_users():
	global connection, cursor
	query = f"SELECT * FROM {USERS};"
	cursor.execute(query)

	print("========================")
	for record in cursor:
		print(record)

	print("========================\n")



if __name__ == '__main__':
	connection, cursor = connect()

	get_users()
	create_user(2, "nes", "123456789")
	get_users()
	delete_user(2)
	get_users()

	close(connection, cursor)

