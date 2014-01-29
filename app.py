from flask import Flask, request, jsonify, abort, make_response
import smtplib
import random, datetime, threading
import pystache


app = Flask(__name__, static_folder='static', static_url_path='')
username = 'your gmail username'
password = 'your gmail password'
message_template = 'You have {{pair}} for secret santa{{#group-name}} with {{group-name}}{{/group-name}}! {{#date}}The exchange will take place on {{date}}{{#limit}} and t{{/limit}}{{^limit}}.{{/limit}}{{/date}}{{#limit}}{{^date}}T{{/date}}he limit is ${{limit}}.{{/limit}}'

@app.route('/', methods=['GET'])
def index():
	return app.send_static_file('index.html')

@app.route('/', methods=['POST'])
def post():

	if not request.json:
		return 'request must be json', 400

	# error checking
	names = set()
	emails = set()
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
		if person['email'] in emails:
			return make_response(jsonify({'email-repeat': person['email']}), 400)

		names.add(person['name'])
		emails.add(person['email'])

		person['date'] = date
		person['group-name'] = group
		person['limit'] = limit

		people.append(person)

	# set up random pairings
	pairings = range(len(people))
	random.shuffle(pairings)

	for index in xrange(len(pairings)):
		people[pairings[index]]['pair'] = people[pairings[index-1]]['name']


	# launch text message thread
	t = threading.Thread(target=send_emails, args=(people,))
	t.daemon = True
	t.start()

	return 'success'

def send_emails(people):
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username, password)
	for person in people:
		text = pystache.render(message_template, person)
		subject = 'Secret Santa'
		if person['group-name']:
			subject +=  'with ' + person['group-name']
		message = 'Subject: %s\n\n%s' % (subject, text)
		server.sendmail(username+'@gmail.com', person['email'], message)
		server.ehlo()
	server.quit()



if __name__ == '__main__':
	app.run()
