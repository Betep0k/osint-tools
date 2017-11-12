import requests
from json import loads as json_decode
import datetime
from time import sleep

location = 267646263

response = requests.get('https://www.instagram.com/explore/locations/%d/?__a=1' % location)
data = json_decode(response.text)

print 'Location: %s' % data['location']['id']
print 'Name: %s' % data['location']['name']
print 'lat: %f' % data['location']['lat']
print 'long: %f' % data['location']['lng']

next_page = data['location']['media']['page_info']['end_cursor']

while True:
	response = requests.get('https://www.instagram.com/graphql/query/?query_id=17865274345132052&variables={"id":"%d","first":12,"after":"%s"}' % (location, next_page))
	data = json_decode(response.text)
	if data['data']['location']['edge_location_to_media']['page_info']['has_next_page'] == False:
		print 'There are no more pages'
		break 
	next_page = data['data']['location']['edge_location_to_media']['page_info']['end_cursor']
	for edge in data['data']['location']['edge_location_to_media']['edges']:
		timestamp = edge['node']['taken_at_timestamp']
		print datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
		print '- https://www.instagram.com/p/%s/' % edge['node']['shortcode']

