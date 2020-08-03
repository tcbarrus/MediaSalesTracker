import mysql.connector
from mysql.connector import Error
import argparse
from utilities import AppleAccessObject, DatabaseAccessObject
import pprint

def insertMedia(DAO, data, mediaType):
	try:
		DAO.connect()
		if DAO.connection.is_connected():
			if mediaType == 'movie':
				DAO.insertMovie(title=data['trackName'], trackId=data['trackId'])
			elif mediaType == 'album':
				DAO.insertAlbum(title=data['trackName'], trackId=data['trackId'])
	except Error as e:
		print("Error while connecting to MySQL", e)
	finally:
		DAO.disconnect()

def addMovie(AAO, titles = None, trackId = None):
	#Query DB through DAO.
	moviesNotAdded = []
	DAO = DatabaseAccessObject()
	pp = pprint.PrettyPrinter(indent=4)

	if trackId is not None:
		results = AAO.lookupById(trackId)
		data = results['results'][0]
		insertMedia(DAO, data, mediaType='movie')
		return

	for t in titles:
		results = AAO.searchMovieByTitle(t)
		print("SEARCHING FOR ", t)
		pp.pprint(results)
		if results['resultCount'] is not 1:
			moviesNotAdded.append(t)
			print("More than one result for %s" % t)
		else:
			#Query DB by id to prevent duplicates
			data = results['results'][0]
			insertMedia(DAO, data, mediaType='movie')
		
	if moviesNotAdded:
		print("Movies not added: ", moviesNotAdded)

def addAlbum(AAO, albums = None, albumId = None):
	albumsNotAdded = []
	DAO = DatabaseAccessObject()
	pp = pprint.PrettyPrinter(indent=4)

	if albumId is not None:
		results = AAO.lookupById(albumId)
		data = results['results'][0]
		insertMedia(DAO, data, mediaType='album')

def readFile(AAO, fileName):
	#Parse text file 
	#Call addMovie() for each title in file
	titles = []
	with open(fileName, 'r') as file:
		for line in file:
			titles.append(line.strip())

	addMovie(AAO, titles)

#Support a title or a document to parse
if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('-m', '--movies', nargs = '+', help="A list of titles of the movies you wish to add")
	parser.add_argument('-f', '--file', help="A file containing a list of movies to add")
	parser.add_argument('-i', '--id', help="iTunes track id")

	args = parser.parse_args()

	AAO = AppleAccessObject()

	if args.movies:
		addMovie(AAO, titles = args.movies)
	elif args.id:
		addMovie(AAO, trackId = args.id)
	elif args.file:
		readFile(AAO, args.file)
	else:
		print("Invalid input. Must supply movie or file.")
