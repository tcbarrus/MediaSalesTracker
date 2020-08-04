from utilities import AppleAccessObject, DatabaseAccessObject
import time

class SalesTracker:
	def __init__(self):
		self.__AAO = AppleAccessObject()
		self.__DAO = DatabaseAccessObject()
		self.movies = self.__DAO.getMovies()
		self.sales = []

	def updatePrices(self):
		sales = []
		if self.movies is not None:
			# Crawl "deals" page on MoviesAnywhere. Parse out sales titles and keep them in a list
			# Create a crawler object. It will take in raw HTML and parse out the title name and price into a python dictionary
			for m in movies:
				storedPrice = m['Price']
				trackId = data['iTunesTrackID']
				#If MoviesAnywhere eligible, compare title to sale titles in dictionary. 
				if m['MoviesAnywhereElligible']:
					#Check deals list against elligible titles

					#if m['Title'] in dictionary:
						# Extract price, compare to DB
					pass
				else:
				#Else Get price from iTunes
					results = self.__AAO.lookupById(trackId)
					media = results['results'][0]
					applePrice = media['trackHdPrice'] if 'trackHdPrice' in media else media['trackPrice']
					if storedPrice != applePrice:
						self.__DAO.updatePrice(media['trackName'], media['trackId'], applePrice)
					if applePrice < storedPrice:
						m['Price'] = applePrice
						self.sales.append(m)
				#wait four seconds to avoid Apple API call limits
				time.sleep(4)

	def sendNotifications(self):
		#Send email or text informing user of sales
		pass