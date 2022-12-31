import psycopg2
import psycopg2.extras
import hashlib
import os
from random import randint
from datetime import *

# TODO for the Diogo pc to run, the code below should be removed
#from cfg.database_cfg import DB_CONNECTION_STRING

import mobileApp_api as mobileApp

DB_HOST = "localhost"
DB_USER = "postgres"
DB_DATABASE = "musicmarkt"
#DB_PASSWORD = "postgres"

#TODO for the Ramalho pc to run password is sirs
DB_PASSWORD = "sirs"



# TODO for the Diogo pc to run, the code below should be uncommented
# TODO for the Ramalho pc to run, port=5432
DB_CONNECTION_STRING = "host=%s port=5432 dbname=%s user=%s password=%s" % (
    DB_HOST,
    DB_DATABASE,
    DB_USER,
    DB_PASSWORD,
)

connection, cursor = (None, None)

#   CONNECTION
# -------------- #
# connect with db
def connect():
	global connection, cursor
	try:
		connection = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	except Exception as e :
		print(e)
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
NAME = "name"

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

def get_artist_name(aid):
	global connection, cursor

	query = f"SELECT {ANAME} FROM {ARTIST} WHERE {AID} = %s"
	cursor.execute(query, (aid, ))
	
	# artist doesnt exist
	if (cursor.rowcount == 0):
		return None

	name = cursor.fetchone()[0]
	return name

def get_scoreboard (aid):
	global connection, cursor

	query = f"SELECT {AMOUNT}, {CNAME} FROM {SCOREBOARD} NATURAL JOIN {CLIENT} WHERE {AID} = %s ORDER BY {AMOUNT} DESC;"
	cursor.execute(query, (aid, ))

	scoreboard = copyRecords(cursor)
	if (scoreboard == []):
		scoreboard = [[]]

	return scoreboard

# two factor authentication funcions 
def generate_code(name):
	global connection, cursor

	query = f"UPDATE {TWO_FA} SET {CODE} = %s, {ATTEMPT_TS} = %s WHERE {NAME} = %s"

	while True:
		# generate code
		code = ""
		for _ in range(4):
			code += str(randint(0, 9))

		# calculate end time of attempt (aka attempt_ts)
		attempt_ts = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		if(mobileApp.sendCode(code)):
			break

	cursor.execute(query, (code, attempt_ts, name))
	
	connection.commit()

def check_code(name, code):

	query = f"SELECT {CODE}, {ATTEMPT_TS}, {BAN_TS}, {ATTEMPTS} FROM {TWO_FA} WHERE {NAME} = %s;"
	cursor.execute(query, (name, ))

	if (cursor.rowcount == 0):
		return False

	response = response = cursor.fetchone()

	db_code = response[0]
	print("db_code: " + db_code)
	db_attempt_ts = response[1]
	print("db_attempts_ts: " + db_attempt_ts)
	db_ban_ts = response[2]
	print("db_ban_ts:" + db_ban_ts)
	db_attempts = response[3]
	print("db_attempts: " + str(db_attempts))

	db_attempt_ts = datetime.strptime(db_attempt_ts, '%d/%m/%Y, %H:%M:%S')
	if db_ban_ts != '0':
		db_ban_ts = datetime.strptime(db_ban_ts, '%d/%m/%Y, %H:%M:%S')

	if (db_ban_ts == '0' or (db_ban_ts + timedelta(minutes=5)) < datetime.now()): # If the user is not banned or the ban time has already passed
		if ((db_attempt_ts + timedelta(hours=1)) >= datetime.now()): # It hasn't passed an hour since the code has been requested
			if (db_code == code): # The code checks
				new_attempts = 0
				query = f"UPDATE {TWO_FA} SET {ATTEMPTS} = {new_attempts}, {BAN_TS} = 0 WHERE {NAME} = %s"
				cursor.execute(query, (name, ))
				return 1
			else :
				return increaseAttempts(name, db_attempts)

			
		else: # It has passed an hour since the code has been requested
			return increaseAttempts(name, db_attempts)
	else: # User is still banned
		return -1

			



	if (code == db_code):
		return True



def copyRecords (cursor):
	records = []
	for record in cursor:
		records.append(record)

	return records

def increaseAttempts(name, db_attempts):
	new_attempts = db_attempts + 1

	if (new_attempts < 3): # User has tried less than 3 times
		query = f"UPDATE {TWO_FA} SET {ATTEMPTS} = {new_attempts} WHERE {NAME} = %s"
		cursor.execute(query, (name, ))
		generate_code(name)
		return 0
	else: # User has tried 3 times, so now will be banned for a while
		new_attempts = 0
		db_ban_ts = (datetime.now() + timedelta(minutes=5)).strftime("%d/%m/%Y, %H:%M:%S")
		query = f"UPDATE {TWO_FA} SET {BAN_TS} = %s, {ATTEMPTS} = {new_attempts} WHERE {NAME} = %s"
		cursor.execute(query, (db_ban_ts, name))
		return -1
