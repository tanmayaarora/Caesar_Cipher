import os
import logging
from flask import Flask, request, render_template


app = Flask(__name__)


# various Flask explanations available at:  https://flask.palletsprojects.com/en/1.1.x/quickstart/

		
def doRender(tname='index.htm', values={}):
	values['logo'] = "./static/wallpaper.jpg"
	return render_template(tname, **values)	 


@app.route('/hello')
# Keep a Hello World message to show that at least something is working
def hello():
	return 'Hello World!'

# Defines a POST supporting calculate route
@app.route('/result',methods=['POST'])
def caesar():

	alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	message = request.form.get('usermessage').lower()
	shift_amount = int(request.form.get('shift'))%26
	cipher_direction = request.form['encdec']
	end_text = ""
	
	if cipher_direction == "decode":
		shift_amount *= -1

	for char in message:
		if char.isalpha():
			position = alphabet.index(char)
			new_position = position + shift_amount
			end_text += alphabet[new_position]
		else:
			end_text += char
	
	return doRender('index.htm',{'output':f"Here's the {cipher_direction}d result: {end_text}"})


# catch all other page requests - doRender checks if a page is available (shows it) or not (index)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def mainPage(path):
	return doRender('index.htm')

@app.errorhandler(500)
# A small bit of error handling
def server_error(e):
	logging.exception('ERROR!')
	return """
	An  error occurred: <pre>{}</pre>
	""".format(e), 500

if __name__ == '__main__':
	# Entry point for running on the local machine
	# On GAE, endpoints (e.g. /) would be called.
	# Called as: gunicorn -b :$PORT index:app,
	# host is localhost; port is 8080; this file is index (.py)

	app.run(host='127.0.0.1', port=8080, debug=True)
