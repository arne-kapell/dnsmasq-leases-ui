#!/usr/bin/env python
# This tool provides a web based ui for leases file of the famous DNS/DHCP daemon dnsmasq.
#
# 
# See https://github.com/fschlag/dnsmasq-leases-ui
# by Florian Schlag (https://github.com/fschlag)
#
from flask import Flask, render_template, jsonify, send_from_directory
import datetime
import os
import socket
import speedtest

DNSMASQ_LEASES_FILE = "/var/lib/misc/dnsmasq.leases"
# !!! dev only !!!
#DNSMASQ_LEASES_FILE = "./dnsmasq.leases"

app = Flask(__name__)

class LeaseEntry:
	def __init__(self, leasetime, macAddress, ipAddress, name):
		if (leasetime == '0'):
			self.staticIP = True
		else:
			self.staticIP = False
		self.leasetime = datetime.datetime.fromtimestamp(
			int(leasetime)
			).strftime('%Y-%m-%d %H:%M:%S')
		self.macAddress = macAddress.upper()
		self.ipAddress = ipAddress
		self.name = name

	def serialize(self):
		return {
			'staticIP': self.staticIP,
			'leasetime': self.leasetime,
			'macAddress': self.macAddress,
			'ipAddress': self.ipAddress,
			'name': self.name
		}

def leaseSort(arg):
	# Fixed IPs first
	if arg.staticIP == True:
		return '0' + arg.ipAddress
	else:
		return arg.ipAddress

class OnlineStatus:
	def __init__(self, online, ip):
		self.online = online
		self.ip = ip

def getOnlineStatus():
	ownIP=socket.gethostbyname(socket.gethostname())
	if ownIP=="127.0.0.1":
		return OnlineStatus(False,ownIP)
	else:
		return OnlineStatus(True,ownIP)

class SpeedResult:
	def __init__(self, down, up, ping):
		self.download = down
		self.upload = up
		self.ping = ping

def getSpeed():
	st = speedtest.Speedtest()
	down = st.download()
	up = st.upload()
	servernames =[]   
	st.get_servers(servernames)
	ping = st.results.ping
	return SpeedResult(down, up, ping)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/api")
def getInfo():
	online = getOnlineStatus()
	leases = list()
	with open(DNSMASQ_LEASES_FILE) as f:
		for line in f:
			elements = line.split()
			if len(elements) == 5:
				entry = LeaseEntry(elements[0],
						   elements[1],
						   elements[2],
						   elements[3])
				leases.append(entry)

	leases.sort(key = leaseSort)
	return jsonify(status={'online': online.online, 'ip': online.ip}, leases=[lease.serialize() for lease in leases])

@app.route("/api/speed")
def showSpeed():
	speed = getSpeed()
	return jsonify(speed={'download': round(speed.download*0.000001, 3), 'upload': round(speed.upload*0.000001, 3), 'ping': round(speed.ping, 0)})


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'img'), 'cropped-raspberrry_pi_logo-32x32.png')

if __name__ == "__main__":
	app.run("0.0.0.0")
