import urllib2, json
apikey = 'ab5c827e4a90cf97' #apikey, won't change
city = 'Charlottesville' #city, state comes from post
state = 'VA'
url = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/' + state + '/'+ city + '.json'
r = urllib2.urlopen(url)

json_string = r.read()
parsed_json = json.loads(json_string)
weather = parsed_json['current_observation']['weather']
temp_f = parsed_json['current_observation']['temp_f']
relative_humidity = parsed_json['current_observation']['relative_humidity']
precip_today_in = parsed_json['current_observation']['precip_today_in']

r.close();
