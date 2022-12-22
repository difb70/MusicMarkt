import psycopg2
import psycopg2.extras
import hashlib
from random import randint
from time import time
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
TWO_FA = "factor_authentication" 

#   COLUMNS
# ------------ #
CID = "cid"
CNAME = "name"
CPASS = "pass"
CSALT = "salt"

AID = "aid"
ANAME = "name"

AMOUNT = "amount"

PID = "pid"
PNAME = "name"
PTYPE = "type"
PSTATE = "state"
PRICE = "price"

CODE = "code"
ATTEMPT_TS = "attempt_ts"
BAN_TS = "ban_ts"
ATTEMPTS = "attempts"


#    A P I
# ------------ #
# create user
def create_user(username, password):
	global connection, cursor

	salt = randint(0, 2**15)
	password = str.encode(password + str(salt))
	digest = hashlib.sha256(password).hexdigest()

	# create user entry in the 2fa table
	query = f"INSERT INTO {TWO_FA} ({CNAME}, {ATTEMPT_TS}, {BAN_TS}, {ATTEMPTS}) VALUES (%s, %s, %s, %s);"
	cursor.execute(query, (username, 0, 0, 0))

	# create user the actual user
	query = f"INSERT INTO {CLIENT} ({CNAME}, {CPASS}, {CSALT}) VALUES (%s, %s, %s);"

	cursor.execute(query, (username, digest, salt))
	connection.commit()

def get_cid (username):
	global connection, cursor
	
	query = f"SELECT {CID} FROM {CLIENT} WHERE {CNAME} = %s;"
	cursor.execute(query, (username, ))
	
	# check if the username exists
	if (cursor.rowcount == 0):
		return None

	cid = cursor.fetchone()[0]
	return cid

def check_password(username, password):
	global connection, cursor

	query = f"SELECT {CPASS}, {CSALT} FROM {CLIENT} WHERE {CNAME} = %s;"
	cursor.execute(query, (username, ))

	# user doesnt exist
	if (cursor.rowcount == 0):
		return False

	response = cursor.fetchone()
	user_digest = response[0]
	salt = response[1]

	password = str.encode(password + str(salt))
	digest = hashlib.sha256(password).hexdigest()

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

def get_products():
	global connection, cursor

	query = f"SELECT {PID}, {PNAME}, {PSTATE}, {PRICE} FROM {PRODUCT}"
	cursor.execute(query)

	products = copyRecords(cursor)
	return products

def get_artists():
	global connection, cursor

	query = f"SELECT {AID}, {ANAME} FROM {ARTIST}"
	cursor.execute(query)

	artists = copyRecords(cursor)
	return artists


def get_scoreboard (aid):
	global connection, cursor

	query = f"SELECT {AMOUNT}, {CID} FROM {SCOREBOARD} WHERE {AID} = %s ORDER BY {AMOUNT} DESC;"
	cursor.execute(query, (aid, ))

	scoreboard = copyRecords(cursor)
	return scoreboard

# two factor authentication funcions 
def generate_code(cid, valid_period):
	global connection, cursor

	query = f"UPDATE {TWO_FA} SET {CODE} = %s, {ATTEMPT_TS} = %s WHERE {CID} = %s"

	# generate code
	code = ""
	for _ in range(4):
		code += str(randint(0, 9))

	# calculate end time of attempt (aka attempt_ts)
	attempt_ts = time() + valid_period
	cursor.execute(query, (code, attempt_ts, cid))
	
	connection.commit()

def check_code():
	return



def copyRecords (cursor):
	records = []
	for record in cursor:
		records.append(record)

	return records
