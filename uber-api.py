import requests
import json

CLIENT_ID = '8eEU2A1t1gQywuP4wfGOgMgmJ_aKYByf'
SERVER_TOKEN = 'XHaNMremvtZcDJAFs1nhgDyTb2MVQeKboQKQo3sT'
BASE_URL_PRICES = 'https://api.uber.com/v1/estimates/price'



class tripData:
	def __init__(self, start_latitude, start_longitude, end_latitude, end_longitude):
		self.start_latitude = start_latitude
		self.start_longitude = start_longitude
		self.end_latitude = end_latitude
		self.end_longitude = end_longitude

	def getPriceEstimate(self):
		parameters = {
			'server_token': SERVER_TOKEN,
			'start_latitude': self.start_latitude,
			'start_longitude': self.start_longitude,
			'end_latitude': self.end_latitude,
			'end_longitude': self.end_longitude
		}
		response = requests.get(BASE_URL_PRICES, params=parameters)
		data = response.json()
		# print out prices individually
		for price in data['prices']:
			print price
		print data['prices']
		# return data['prices']

x  = tripData("42.275133", "-71.785472", "42.173582", "-71.426239")

x.getPriceEstimate()


'''
0: pickup date time
1: trip distance
2: pickup long
3: pickup lat
4: dropoff long
5: dropoff lat
6: fare amount
7: total amount
'''
