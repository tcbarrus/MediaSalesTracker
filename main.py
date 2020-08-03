import mysql.connector
from mysql.connector import Error
import requests
import sys
import pprint
from utilities import AppleAccessObject, DatabaseAccessObject
from salesTracker import SalesTracker
import time

def test():
	req = requests.get('https://itunes.apple.com/lookup?id=192846080')
	# req = requests.get('https://itunes.apple.com/search?term=casablanca&media=movie')
	# req = requests.get('https://itunes.apple.com/search?term=restless+heart&media=music&entity=musicArtist')
	# req = requests.get('https://itunes.apple.com/lookup?amgArtistId=1788&entity=song&limit=500')
	results = req.json()
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(results)
	# songs = []
	# for song in results['results']:
	# 	# pp.pprint(song)
	# 	# print(song['artistId'])
	# 	if 'trackName' in song:
	# 		songs.append(song['trackName'])
	# print (req.status_code)
	# # print (req.content)
	# songs.sort()
	# print(len(songs))
	# for s in songs:
	# 	print(s)
	# pp.pprint(req.json())

def updatePrice(DAO, AAO, data):
	try:
		print('Looking up %s' % data['Title'])
		price = data['Price']
		trackId = data['iTunesTrackID']
		results = AAO.lookupById(trackId)
		media = results['results'][0]
		print(media)
		applePrice = media['trackHdPrice'] if 'trackHdPrice' in media else media['trackPrice']
		if price != applePrice:
			DAO.updatePrice(media['trackName'], media['trackId'], applePrice)
		return data if applePrice < price else None
	except Error as e:
		print("Error while updating price for %s:" % data['Title'], e)
		return None


if __name__ == '__main__':
	# test()

	tracker = SalesTracker()
	tracker.updatePrices()

	if tracker.sales:
		#send email or text
		pass

	# if movies is not None:
	# 	for m in movies:
	# 		updatePrice(DAO, AAO, m)

# print "Hello World"