from flask import Flask, request, jsonify, abort, make_response
from twilio.rest import TwilioRestClient
import random, datetime, threading
import pystache


app = Flask(__name__, static_folder='static', static_url_path='')
account_sid = 'your twilio account sid'
auth_token = 'your twilio auth token'
client = TwilioRestClient(account_sid, auth_token)
message_template = 'You have {{pair}} for secret santa{{#group-name}} with {{group-name}}{{/group-name}}! {{#date}}The exchange will take place on {{date}}{{#limit}} and t{{/limit}}{{^limit}}.{{/limit}}{{/date}}{{#limit}}{{^date}}T{{/date}}he limit is ${{limit}}.{{/limit}}'

@app.route('/', methods=['GET'])
def index():
	return app.send_static_file('index.html')

@app.route('/', methods=['POST'])
def post():

	if not request.json:
		return 'request must be json', 400

	# error checking
	names = {}
	numbers = {}
	people = []
	date = None
	group = None
	limit = None
	if 'date' in request.json and len(request.json['date']) > 0:
		date = datetime.datetime.strptime(request.json['date'], '%Y-%m-%d').strftime('%m/%d/%y')
	if 'group-name' in request.json and len(request.json['group-name']) > 0:
		group = request.json['group-name']
	if 'limit' in request.json and len(request.json['limit']) > 0:
		limit = request.json['limit']


	for person in request.json['people']:
		person = person.copy()
		if person['name'] in names or len(person['name']) == 0:
			return make_response(jsonify({'name-repeat': person['name']}), 400)
		if person['number'] in numbers:
			return make_response(jsonify({'number-repeat': person['number']}), 400)

		names[person['name']] = None
		names[person['number']] = None

		person['number'] = person['number'].replace('-', '')

		try:
			int(person['number'])
		except:
			return make_response(jsonify({'number-error': person['number']}))

		if len(person['number']) != 10:
			return make_response(jsonify({'number-error': person['number']}))

		person['date'] = date
		person['group-name'] = group
		person['limit'] = limit

		people.append(person)

	# set up random pairings
	pairings = range(len(people))
	random.shuffle(pairings)

	for index in xrange(len(pairings)):
		people[pairings[index]]['pair'] = people[pairings[index-1]]['name']


	# launch text message threads
	for person in people:
		t = threading.Thread(target=send_sms, args=(person,))
		t.daemon = True
		t.start()

	return 'success'

def send_sms(person):
	body = pystache.render(message_template, person)
	client.sms.messages.create(to=person['number'], from_='your twilio number', body=body)


@app.errorhandler(400)
def error(error):
    return 'error', 400



if __name__ == '__main__':
	app.run()
