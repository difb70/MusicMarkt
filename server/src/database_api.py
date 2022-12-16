import psycopg2
import psycopg2.extras
import hashlib
from cfg.database_cfg import DB_CONNECTION_STRING

connection, cursor = (None, None)

#   CONNECTION
# -------------- #
# connect with db
def connect():
	global connection, cursor
	try:
		connection = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	except:
		print("Error : Unable to connect to the database")
		exit()

# close db connection
def close():
	global connection, cursor
	connection.close()
	cursor.close()



#    TABLES
# ------------ #
CLIENT = "client"
PRODUCT = "product"
ARTIST = "artist"
SCOREBOARD = "scoreboard"

#   COLUMNS
# ------------ #
CID = "cid"
CNAME = "name"
CPASS = "pass"

AID = "aid"
ANAME = "name"

AMOUNT = "amount"

PID = "pid"
PNAME = "name"
PTYPE = "type"
PRICE = "price"


#    A P I
# ------------ #
# create user
def create_client(name, password):
	global connection, cursor

	password = str.encode(password)
	digest = hashlib.sha256(password).hexdigest()

	query = f"INSERT INTO {CLIENT} ({CNAME}, {CPASS}) VALUES (%s, %s);"

	cursor.execute(query, (name, digest))
	connection.commit()


def check_password(cid, password):
	global connection, cursor

	password = str.encode(password)
	digest = hashlib.sha256(password).hexdigest()

	query = f"SELECT {CPASS} FROM {CLIENT} WHERE {CID} = %s;"
	cursor.execute(query, (cid, ))

	# cid doesnt exist
	if (cursor.rowcount == 0):
		return False

	user_digest = cursor.fetchone()[0]
	return user_digest == digest

# this needs to be a session created when 
# the user logs in the website (in this case this funcion only takes 
# pid as argument)

# @login_required
def buy_item (cid, pid):
	global connection, cursor

	# get product information
	query = f"SELECT {AID}, {PRICE} FROM {PRODUCT} WHERE {PID} = %s"
	cursor.execute(query, (pid, ))

	# pid doesnt exist
	if (cursor.rowcount == 0):
		return False

	aid, price = cursor.fetchone()
	query = f"INSERT INTO {SCOREBOARD} VALUES (%s, %s, %s) ON CONFLICT ON CONSTRAINT pk_scoreboard DO UPDATE SET {AMOUNT} = {SCOREBOARD}.{AMOUNT} + money(%s);"
	
	cursor.execute(query, (aid, price, cid, price))
	connection.commit()

	return True


def get_scoreboard (aid):
	global connection, cursor

	query = f"SELECT {AMOUNT}, {CID} FROM {SCOREBOARD} WHERE {AID} = %s ORDER BY {AMOUNT} DESC;"
	cursor.execute(query, (aid, ))

	print(f"aid : {aid}")
	i = 1
	for record in cursor:
		print(f"{i} - user : {record[1]}    amount : {record[0]}")
		i += 1

	print("==================")




if __name__ == '__main__':
	connect()

	print(check_password(1, "tommy123"))
	get_scoreboard(1)
	get_scoreboard(2)
	get_scoreboard(3)
	get_scoreboard(4)

	close()
