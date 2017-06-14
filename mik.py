#!flask/bin/python
from flask import Flask, jsonify, abort, request, url_for, make_response, json
from flask.ext.httpauth import HTTPBasicAuth
import os, iproute, csv, json, subprocess, re

mikrotik = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'weilun':
		return 'python'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'Error':'Unauthorized Access'}), 401)


@mikrotik.route('/route/print', methods=['GET'])
@auth.login_required
def printRoute():
	subprocess.call(['./iproute.sh', 'print'])
	with open('route.txt') as f:
		output = f.read()
		#line = re.sub('[<>,"=]', '', output)
		output2 = re.split('\n', output)
		#nice=re.split('\n', output)
		
	return jsonify({'Route': output2})

@mikrotik.route('/route/create', methods=['POST'])
@auth.login_required
def createRoute():
	dst = request.json['dst']
	src = request.json['src']
	gateway = request.json['gateway']
	subprocess.call(['./iproute.sh', 'create', dst, src, gateway])
	with open('route.txt') as f:
		output = f.read()
	return jsonify({'dst-address': dst, 'pref-src':src, 'gateway': gateway})

@mikrotik.route('/route/update=<numbers>', methods=['PUT'])
@auth.login_required
def updateRoute(numbers):
	dst = request.json['dst']
	src = request.json['src']
	gateway = request.json['gateway']
	subprocess.call(['./iproute.sh', 'update', numbers, dst, src, gateway])
	with open('route.txt') as f:
		output = f.read()
	return jsonify({'Updated Route': output})

@mikrotik.route('/route/delete=<numbers>', methods=['DELETE'])
@auth.login_required
def deleteRoute(numbers):
	subprocess.call(['./iproute.sh', 'delete', numbers])
	with open('route.txt') as f:
		output = f.read()
	return jsonify({'Route': output, 'delete':True})


'''@mik.route('/deleteRoute=<int:number>', methods=['GET'])
def deleteRoute(number):

	return jsonify({'result': True}, routePrint.deleteR('10.10.10.1', str(number)))

@mik.route('/createRoute', methods=['POST'])
def addRoute():
	function = {
		'Dst-Address': request.json['dst-addr'],
		'Pref-Src': request.json['pref-src'],
		'Gateway': request.json['gateway']
	}
	
	functions.append(function)
	#return jsonify({'function': function}), 201
	return jsonify(routePrint.createR('10.10.10.1', function['Dst-Address'], function['Pref-Src'], function['Gateway']))

#@mik.route('/updateRoute=<int:number>', methods=['PUT'])
#def addRoute(number):
'''	

if __name__ == '__main__':
	mikrotik.run(debug=True)
