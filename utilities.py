#Apple Access Object
#Handles all queries to Apple's iTunes API

import requests
import mysql.connector
from mysql.connector import Error

class AppleAccessObject:
	def __init__(self):
		self.SEARCH_PREFIX = "https://itunes.apple.com/search?term="
		self.LOOKUP_PREFIX = "https://itunes.apple.com/lookup?id="

	def searchMovieByTitle(self, title):
		#print(self.SEARCH_PREFIX+title.replace(' ', '&'))

		dataString = "%s%s&media=movie" % (self.SEARCH_PREFIX, title.replace(' ', '+'))
		print(dataString)
		req = requests.get(dataString)
		if req.status_code == 200:
			return req.json()
		else:
			print("ERROR: Request returned status code %d" % req.status_code)

	def lookupById(self, trackId):
		dataString = self.SEARCH_PREFIX + str(trackId)
		req = requests.get(dataString)
		if req.status_code == 200:
			return req.json()
		else:
			print("ERROR: Request returned status code %d" % req.status_code)

class DatabaseAccessObject:
	def __init__(self):
		self.__host = 'localhost'
		self.__database='media_sales_tracker'
		self.__user = 'root'
		self.__password = 'H@ckingTheM@infr@me'
		self.__connection = None
		self.__cursor = None

	def connect(self):
		self.__connection = mysql.connector.connect(host=self.__host,
			database=self.__database,
			user=self.__user,
			password=self.__password)
		self.__cursor = self.connection.cursor(dictionary=True)

	def disconnect(self):
		if self.__connection.is_connected():
			self.__cursor.close()
			self.__connection.close()

	# def execute(self, method):
	# 	try:
	# 		self.connect()
	# 		if self.connection.is_connected():
	# 			return method()
	# 			# if mediaType == 'movie':
	# 			# 	self.insertMovie(title=data['trackName'], trackId=data['trackId'])
	# 			# elif mediaType == 'album':
	# 			# 	self.insertAlbum(title=data['trackName'], trackId=data['trackId'])
	# 	except Error as e:
	# 		print("Error while connecting to MySQL", e)
	# 	finally:
	# 		self.disconnect()

	def selectMovieById(self, trackId):
		self.__cursor.execute('SELECT * FROM Movies WHERE iTunesTrackID="%s"', trackId)
		return self.__cursor.fetchone()

	def insertMovie(self, title, trackId, price=0, moviesAnywhere=0):
		print("INSERTING MOVIE")
		dataString = 'INSERT INTO Movies (Title, Price, iTunesTrackID, MoviesAnywhereElligible) VALUES (\'%s\', %d, %d, %d)' % (title.replace("'", "\'"), trackId, price, moviesAnywhere)
		print(dataString)
		self.__cursor.execute('INSERT INTO Movies (Title, Price, iTunesTrackID, moviesAnywhereElligible) VALUES (%s, %s, %s, %s)', (title, price, trackId, moviesAnywhere))
		self.connection.commit()
		print(self.__cursor.rowcount, "record inserted.")

	def insertAlbum(self, title, trackId, price=0):
		print("INSERTING ALBUM")
		dataString = 'INSERT INTO Movies (Title, Price, iTunesTrackID, MoviesAnywhereElligible) VALUES (\'%s\', %d, %d, %d)' % (title.replace("'", "\'"), trackId, price, moviesAnywhere)
		print(dataString)
		self.__cursor.execute('INSERT INTO Movies (Title, Price, iTunesTrackID, moviesAnywhereElligible) VALUES (%s, %s, %s, %s)', (title, price, trackId, moviesAnywhere))
		self.connection.commit()
		print(self.__cursor.rowcount, "record inserted.")

	def getMovies(self):
		print("GETTING UNPURCHASED MOVIES")
		try:
			self.connect()
			if self.__connection.is_connected():
				self.__cursor.execute('SELECT * FROM Movies WHERE Purchased = "%s" AND Price = "%s"', (0,0))
				results = self.__cursor.fetchall()
				return results
		except Error as e:
			print("Error while retreiving movies from database:", e)
			return None
		finally:
			self.disconnect()

	def updatePrice(self, title, trackId, price):
		print("UPDATING PRICE FOR %s", title)
		self.__cursor.execute('UPDATE Movies SET Price = "%s" WHERE iTunesTrackID = "%s"', (price, trackId))
		self.connection.commit()

