#!/usr/bin/env python3

# simpleircbot.py - A simple IRC-bot written in python
#
# Copyright (C) 2015 : Niklas Hempel - http://liq-urt.de
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import re
import socket
import time
import commands, config, irc_functions


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
	con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
	con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
	con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
	con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
	con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
	con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
	result = ""
	for char in msg:
		if char == "!":
			break
		if char != ":":
			result += char
	return result

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def get_message(msg):
	result = ""
	i = 3
	length = len(msg)
	while i < length:
		result += msg[i] + " "
		i += 1
	result = result.lstrip(':')
	return result

def now_playing():
	try:
		f = open("np.txt", 'r')
		npp = removeNonAscii(f.read())
	except:
		return "???? shit broke d00d"
	f.close()
	return None if npp=="0" else npp

def parse_message(msg):
	if len(msg) >= 1:
		msg = msg.split(' ')
		options = {'!test': command_test}
		if msg[0] in options:
			options[msg[0]]()
# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Start Command Functions --------------------------------------------
def command_test():
	send_message(CHAN, 'testing some stuff')

# --------------------------------------------- End Command Functions ----------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))
con.settimeout(0.1)
send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""
tprev = time.time()
npprev = now_playing()
while True:
	np = now_playing()
	t = time.time()
	if(t-tprev)>15.0:
		if np:
			if not np == npprev:
				send_message(CHAN, ("Now Playing: " + removeNonAscii(np)))
				npprev = np
		tprev = time.time()
	try:
		data = data+con.recv(1024).decode('ascii', 'ignore')
		data_split = re.split(r"[~\r\n]+", data)
		data = ""

			
		for line in data_split:
			line = str.rstrip(line)
			line = str.split(line)

			if len(line) >= 1:
				if line[0] == 'PING':
					send_pong(line[1])
				elif line[1] == 'PRIVMSG':
					sender = get_sender(line[0])
					message = get_message(line)
					parse_message(message)

					print(sender + ": " + message)

	except socket.error:
		pass
