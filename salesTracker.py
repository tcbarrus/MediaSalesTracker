# GET MOVIES
# CHECK PRICE
# UPDATE DB
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
			for m in movies:
				price = m['Price']
				trackId = data['iTunesTrackID']
				results = self.__AAO.lookupById(trackId)
				media = results['results'][0]
				applePrice = media['trackHdPrice'] if 'trackHdPrice' in media else media['trackPrice']
				if price != applePrice:
					self.__DAO.updatePrice(media['trackName'], media['trackId'], applePrice)
				if applePrice < price:
					m['Price'] = applePrice
					self.sales.append(m)
				#wait four seconds to avoid Apple API call limits
				time.sleep(4)