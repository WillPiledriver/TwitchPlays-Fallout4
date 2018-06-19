try:
	import config
except:
	print("You didnt include a config file")
	exit()
	
import re, socket, time, autopy, json, math
import functions as fun
	
class bot:
	def __init__(self):
		self.host = config.HOST
		self.port = config.PORT
		self.chan = config.CHAN
		self.nick = config.NICK
		self.oauth = config.PASS

		self.options = {"w": fun.w, "a": fun.a, "d": fun.d, "s": fun.s, "sprint": fun.sprint,
		"vats" : fun.vats, "up": fun.up, "left": fun.left, "right": fun.right, "down": fun.down, "e":fun.activate, "jump":fun.jump,
		"map": fun.map, "inv": fun.inv, "pip": fun.pip, "radio": fun.radio, "data": fun.data,
		"tl45": fun.tl45, "tl90": fun.tl90, "tr45": fun.tr45, "tr90": fun.tr90, "180": fun.turn180,
		"qs": fun.quicksave, "ql": fun.quickload,
		"ml": fun.mouseleft, "mu": fun.mouseup, "mr": fun.mouseright, "md": fun.mousedown, "click": fun.click, "q": fun.vats, "tab":fun.tab,
		"mlf": fun.mouseleftfine, "muf": fun.mouseupfine, "mrf": fun.mouserightfine, "mdf": fun.mousedownfine,
		"melee": fun.melee, "grenade":fun.grenade, "r":fun.r, "holster":fun.holster, "sneak": fun.sneak, "light": fun.light,
		"1": fun.one, "2": fun.two, "3": fun.three, "4": fun.four, "5": fun.five, "6": fun.six, "7": fun.seven, "8": fun.eight, "9": fun.nine, "0":fun.zero,
		"t": fun.presst, "holde": fun.holde, "enter":fun.pressenter, "crit":fun.crit,
		"delayup":self.delayup, "delaydn":self.delaydn, "chaos": self.orderdn, "order": self.orderup, "tp": fun.tp,
		"banpip": self.pipup, "unbanpip": self.pipdn, "pause": self.pauseup, "nopause": self.pausedn}
		
		
		self.legal = ["a", "w", "s", "d", "sprint", "jump", "t", "holde", "enter",
		"qs", "ql", "crit",
		"tl45", "tl90", "tr45", "tr90", "180", "ml", "mr", "mu", "md", "click", "mlf", "muf", "mdf", "mrf", 
		"vats", "e", "up", "down", "left", "right", 
		"pip", "map", "inv", "radio", "data", "light", "sneak", "r", "holster", "melee", "grenade", "tab", "q", "tp",
		"delayup", "delaydn", "chaos", "order", "banpip", "unbanpip", "pause", "nopause"]
		
		self.movement = ["w", "a", "s", "d"]
		self.pipcommands = ["pip", "map", "inv", "radio", "data"]
		self.iterated = ["sprint", "click", "left", "right", "up", "down", "mu", "md", "ml", "mr",
		"muf", "mlf", "mrf", "mdf", "q", "e", "w", "a", "s", "d"]
		self.tugowar = ["banpip", "unbanpip", "chaos", "order", "pause", "nopause", "delayup", "delaydn"]
		
#		for k in "wasd":
#			kk = k
#			for i in range(0,2):
#				kk = kk + k
#				self.legal.append(kk)
		
		for k in "0123456789":
			self.legal.append(k)
			self.iterated.append(k)
		
		##weirdstuff
		self.basedelay = 10
		self.lastcommandt = time.time()
		self.t = time.time()
		self.names = []
		self.queue = {}
		

		self.delayoffset = 0
		self.delaynum = 1500
		self.delaylast = 1500
		self.delaynummax = 3000
		self.delaystep = 50
		
		self.ordernum = 750
		self.orderlast = 750
		self.ordernummax = 1000
		self.chaospoint = self.ordernummax // 2
		self.orderstep = 100
		self.order = True

		self.banpip = False
		self.banpipnummax = 500
		self.banpipnum = self.banpipnummax // 2
		self.banpiplast = self.banpipnum
		self.banpippoint = 400
		self.banpipstep = 50
		
		self.pause = True
		self.pausenummax = 500
		self.pausenum = int(self.pausenummax * 0.75)
		self.pauselast = self.pausenum
		self.pausepoint = self.pausenummax // 2
		self.pausestep = 50
		
		
		
		self.pushtugs()

		
		
		for it in self.iterated:
			for i in range(2, 6):
				self.legal.append(it + "x" + str(i))
		
		self._login();
		
	
	def _login(self):
		self.con = socket.socket()
		self.con.connect((self.host, self.port))
		self.con.settimeout(0.1)
		self.send_pass()
		self.send_nick()
		self.join_channel()

		
		
##=-=-=-=-=-=-=-=-=-=-=-=-=-=Tugowar Stuff=-=-=-=-=-=-=-=-=-=-=-=-=-=##
	def delayup(self):
		if ((self.delaynum + self.delaystep) >= self.delaynummax) and (self.delaynum != self.delaynummax):
			self.delaynum = self.delaynummax
			self.pushtugs()
		elif (self.delaynum + self.delaystep) < self.delaynummax:
			self.delaynum += self.delaystep
			self.updatedelay()
		else:
			print("Delay Reached Max")
			
	def delaydn(self):
		if ((self.delaynum - self.delaystep) <= 0)  and (self.delaynum != 0):
			self.delaynum = 0
			self.pushtugs()
		elif(self.delaynum - self.delaystep) > 0:
			self.delaynum -= self.delaystep	
			self.updatedelay()	
		else:
			print("Delay reached 0")
		
	def updatedelay(self):
		self.delayoffset = self.delaynum / 100
		if(abs(self.delaynum - self.delaylast) > (self.delaynummax*0.05)):
			self.delaylast = self.delaynum
			self.pushtugs()

	def pushtugs(self):
		tuglist = {"delay": [self.delaynum, self.delaynummax],
		"order": [self.ordernum, self.ordernummax],
		"banpip": [self.banpipnum, self.banpipnummax],
		"pause": [self.pausenum, self.pausenummax]}
		for k in tuglist.keys():
			print(k + " : " + str(tuglist[k]))
		with open("./html/tugs.dat", 'wb') as outfile:
			json.dump(tuglist, outfile)
		
		
	def orderup(self):
		if ((self.ordernum + self.orderstep) >= self.ordernummax) and (self.ordernum != self.ordernummax):
			self.ordernum = self.ordernummax
			self.pushtugs()
		elif (self.ordernum + self.orderstep) < self.ordernummax:
			self.ordernum += self.orderstep
			self.updateorder()
		else:
			print("Order Reached Max")

	def orderdn(self):
		if ((self.ordernum - self.orderstep) <= 0) and (self.ordernum != 0):
			self.ordernum = 0
			self.pushtugs()
		elif (self.ordernum - self.orderstep) > 0:
			self.ordernum -= self.orderstep
			self.updateorder()
		else:
			print("Order Reached Zero")
			
	
	def updateorder(self):
		if(self.ordernum <= self.chaospoint) and self.order:
			self.order = False
			print("Chaos activated")
			self.send_message("**********CHAOS HAS BEEN ACTIVATED**********")
			self.pushtugs()
		elif(self.ordernum > self.chaospoint) and not self.order:
			self.order = True
			print("Order activated")
			self.send_message("**********ORDER HAS BEEN RETURNED**********")
			self.pushtugs()
			
		if(abs(self.ordernum - self.orderlast) > (self.ordernummax*0.05)):
			self.orderlast = self.ordernum
			self.pushtugs()
			

	def pipup(self):
		if ((self.banpipnum + self.banpipstep) >= self.banpipnummax) and (self.banpipnum != self.banpipnummax):
			self.banpipnum = self.banpipnummax
			self.pushtugs()
		elif (self.banpipnum + self.banpipstep) < self.banpipnummax:
			self.banpipnum += self.banpipstep
			self.updatebanpip()
		else:
			print("Banpip Reached Max")

	def pipdn(self):
		if ((self.banpipnum - self.banpipstep) <= 0) and (self.banpipnum != 0):
			self.banpipnum = 0
			self.pushtugs()
		elif (self.banpipnum - self.banpipstep) > 0:
			self.banpipnum -= self.banpipstep
			self.updatebanpip()
		else:
			print("Banpip Reached Zero")
	
	def updatebanpip(self):
		if(self.banpipnum >= self.banpippoint) and not self.banpip:
			self.banpip = True
			print("Pipboy Banned")
			self.send_message("**********PIPBOY HAS BEEN BANNED**********")
			self.pushtugs()
		elif(self.banpipnum < self.banpippoint) and self.banpip:
			self.banpip = False
			print("Pipboy unbanned")
			self.send_message("**********PIPBOY HAS BEEN UNBANNED**********")
			self.pushtugs()
			
		if(abs(self.banpipnum - self.banpiplast) > (self.banpipnummax*0.05)):
			self.banpiplast = self.banpipnum
			self.pushtugs()
			
	def pauseup(self):
		if ((self.pausenum + self.pausestep) >= self.pausenummax) and (self.pausenum != self.pausenummax):
			self.pausenum = self.pausenummax
			self.pushtugs()
		elif (self.pausenum + self.pausestep) < self.pausenummax:
			self.pausenum += self.pausestep
			self.updatepause()
		else:
			print("Pause Reached Max")

	def pausedn(self):
		if ((self.pausenum - self.pausestep) <= 0) and (self.pausenum != 0):
			self.pausenum = 0
			self.pushtugs()
		elif (self.pausenum - self.pausestep) > 0:
			self.pausenum -= self.pausestep
			self.updatepause()
		else:
			print("Pause Reached Zero")

	def updatepause(self):
		if(self.pausenum >= self.pausepoint) and not self.pause:
			self.pause = True
			print("Pause Activated")
			self.send_message("**********PAUSE HAS BEEN ACTIVATED**********")
			fun.togglepause()
			self.pushtugs()
		elif(self.pausenum < self.pausepoint) and self.pause:
			self.pause = False
			print("Pause Deactivated")
			self.send_message("**********PAUSE HAS BEEN DEACTIVATED**********")
			fun.togglepause()
			self.pushtugs()
			
		if(abs(self.pausenum - self.pauselast) > (self.pausenummax*0.05)):
			self.pauselast = self.pausenum
			self.pushtugs()			
	
	
##=-=-=-=-=-=-=-=-=-=-=-=IRC STUFF=-=-=-=-=-=-=-=-=-=-=-=##		

	
	def send_pong(self, msg):
		self.con.send(bytes('PONG %s\r\n' % msg))


	def send_message(self, msg):
		self.con.send(bytes('PRIVMSG %s :%s\r\n' % (self.chan, msg)))


	def send_nick(self):
		self.con.send(bytes('NICK %s\r\n' % self.nick))


	def send_pass(self):
		self.con.send(bytes('PASS %s\r\n' % self.oauth))


	def join_channel(self):
		self.con.send(bytes('JOIN %s\r\n' % self.chan))


	def part_channel(self):
		self.con.send(bytes('PART %s\r\n' % self.chan))
		
			
		
	def get_sender(self, msg):
		result = ""
		for char in msg:
			if char == "!":
				break
			if char != ":":
				result += char
		return result

	def get_message(self, msg):
		result = ""
		i = 3
		length = len(msg)
		while i < length:
			result += msg[i] + " "
			i += 1
		result = result.lstrip(':')
		return result

	def addtoqueue(self, s, m):
		if(m in self.pipcommands) and self.banpip: return False
		if s not in self.names:
			self.names.append(s)
			if m not in self.queue.keys():
				self.queue[m] = 1
				with open("./html/queue.dat", 'wb') as outfile:
					json.dump(self.queue, outfile)
				return True
			else:
				self.queue[m] += 1
				with open("./html/queue.dat", 'wb') as outfile:
					json.dump(self.queue, outfile)
				return True
		else:
			return False

	def isdelaycomplete(self):
		self.t = time.time()
		if(self.t-self.lastcommandt)>=(self.basedelay + self.delayoffset):
			return True
		else:
			return False
	
	def executequeue(self):
		if len(self.queue) > 0:
			s = max(self.queue, key=self.queue.get)
			print(s + " chosen as the command with" + str(self.queue[s]) + " votes")
			self.send_message(s + " chosen as the command with " + str(self.queue[s]) + " votes")
#			if s[0] in self.movement and len(s) > 1 and s[1] is s[0]: #WASD
#				for ii in range(0, len(s)):
#					self.options[s[ii]]()
#			else:
			if(self.pause): fun.togglepause()
			itsplit = s.split("x")
			if itsplit[0] in self.iterated:
				
				if len(itsplit)>1:
					it = int(itsplit[1])
					for i in range(0,it):
						self.options[itsplit[0]]()
				else:
					self.options[s]()
			else:
				if(s in self.pipcommands) and not self.banpip:
					self.options[s]()
				else:
					self.options[s]()
			if(self.pause): fun.togglepause()
		self.names = []
		self.queue = {}
		self.lastcommandt = time.time()

	def parse_message(self, sender, msg):
		if len(msg) >= 1:
			s = msg.split(" ")[0].lower()
			if s in self.legal:
				if(s in self.tugowar) or (not self.order):
					itsplit = s.split("x")
					if itsplit[0] in self.iterated:
						
						if len(itsplit)>1:
							it = int(itsplit[1])
							if(self.pause): fun.togglepause()
							for i in range(0,it):
								self.options[itsplit[0]]()
							if(self.pause): fun.togglepause()
						else:
							if(self.pause): fun.togglepause()
							self.options[s]()
							if(self.pause): fun.togglepause()
					else:
						if(s in self.pipcommands):
							if not self.banpip:
								if(self.pause): fun.togglepause()
								self.options[s]()
								if(self.pause): fun.togglepause()
						else:
							if(self.pause)and(s not in self.tugowar): fun.togglepause()
							self.options[s]()
							if(self.pause)and(s not in self.tugowar): fun.togglepause()
				elif self.addtoqueue(sender, s):
					print(sender + " has added " + s + " to the queue")
					
#				if s[0] in self.movement and len(s) > 1 and s[1] is s[0]: #WASD
#					for ii in range(0, len(s)):
#						self.options[s[ii]]()
#				else:
#					itsplit = s.split("x")
#					if itsplit[0] in self.iterated:
#						
#						if len(itsplit)>1:
#							it = int(itsplit[1])
#							for i in range(0,it):
#								self.options[itsplit[0]]()
#						else:
#							self.options[s]()
#					else:
#						self.addtoqueue(sender, s)
#						self.options[s]()
		
	def rcv(self):
		try:
			return self.con.recv(1024).decode('ascii', 'ignore')
		except socket.timeout:
			pass
			
