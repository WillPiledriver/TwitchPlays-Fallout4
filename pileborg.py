#!/usr/bin/env python2.7

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


from bot import bot as b
import functions as fun
import time, re, socket, autopy


ph = b()
data = ""
data_split = []
tprev = time.time()
npprev = fun.now_playing()

while True:

## Now playing
	np = fun.now_playing()
	t = time.time()
	if(t-tprev)>15.0:
		if np:
			if not np == npprev:
				ph.send_message("Now Playing: " + fun.removeNonAscii(np))
				npprev = np
		tprev = time.time()
	
	if ph.isdelaycomplete():
		ph.executequeue()
	
##RCV data and process commands
	data = ph.rcv()
	if data:
		data_split = re.split(r"[~\r\n]+", data)
	
	for line in data_split:
		line = line.encode('utf8')
		line = str.rstrip(line)
		line = str.split(line)

		if len(line) >= 1:
			if line[0] == 'PING':
				ph.send_pong(line[1])
			if len(line)>= 2 and line[1] == 'PRIVMSG':
				sender = ph.get_sender(line[0])
				message = ph.get_message(line)
				
				ph.parse_message(sender, message)

#				print(sender + ": " + message)
	data_split = []