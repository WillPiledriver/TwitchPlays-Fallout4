import time, inputsim, autopy

lastsprint = time.time()

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def now_playing():
	try:
		f = open("np.txt", 'r')
		npp = removeNonAscii(f.read())
	except:
		return "???? shit broke d00d"
	f.close()
	return None if npp=="0" else npp

			
	
#MOVEMENT

def w():
	print("Forward")
	inputsim.pressKey(0.75, 'w')

def a():
	print("Left")
	inputsim.pressKey(0.75, 'a')

def d():
	print("Right")
	inputsim.pressKey(0.75, 'd')
	
def s():
	print("Backward")
	inputsim.pressKey(0.75, 's')
	
def jump():
	print("Jump")
	autopy.key.toggle('w', True)
	time.sleep(0.2)
	inputsim.pressKey(1, 32)
	time.sleep(0.5)
	autopy.key.toggle('w', False)
	
def sprint():
	global lastsprint
	print("Sprint")
	autopy.key.toggle('w', True)
	time.sleep(0.1)
	if(time.time() - lastsprint)>=10:
		inputsim.pressKey(1, 'z')
		lastsprint=time.time()
	else:
		time.sleep(1)
		
	autopy.key.toggle('w', False)
	
##END MOVEMENT
	
##FILE MANIPULATION	
def quicksave():
	print("quicksave")
	inputsim.pressKey(0.3, 116)

def quickload():
	print("quickload")
	inputsim.pressKey(0.3, 120)
	
##END FILE MANIPULATION

##MOUSE CONTROLS

def mouseleft():
	mouse(0)

def mouseup():
	mouse(1)

def mouseright():
	mouse(2)

def mousedown():
	mouse(3)
	
def tl45():
	mouse(4)

def tr45():
	mouse(5)
	
def tl90():
	mouse(6)

def tr90():
	mouse(7)

def turn180():
	mouse(8)

def mouseleftfine():
	mouse(9)
	
def mouseupfine():
	mouse(10)
	
def mouserightfine():
	mouse(11)
	
def mousedownfine():
	mouse(12)

def mouse(n):
	if n is 0:
		print("Mouse Left")
	elif n is 1:
		print("Mouse Up")
	elif n is 2:
		print("Mouse Right")
	elif n is 3:
		print("Mouse Down")
	elif n is 4:
		print("Turn Left 45 degrees")
	elif n is 5:
		print("Turn Right 45 degrees")
	elif n is 6:
		print("Turn Left 90 degrees")
	elif n is 7:
		print("Turn Right 90 degrees")
	elif n is 8:
		print("Turned around")
	elif n is 9:
		print("Mouse left Fine")
	elif n is 10:
		print("Mouse up Fine")
	elif n is 11:
		n+=1
		print("Mouse right Fine")
	elif n is 12:
		n+=1
		print("Mouse down Fine")		
	else:
		print("Mouse num outside bounds")
	inputsim.pressKey(0.1, 96+n)
		
def click():
	print("Click")
	inputsim.click()
	time.sleep(.3)
	


##END MOUSE CONTROLS

##KEY PRESSES

def tp():
	time.sleep(10)

def crit():
	print("Critical attack")
	inputsim.pressKey(.1, 'e')
	time.sleep(.2)
	inputsim.pressKey(.2, 32)

def pressenter():
	print("Press Enter")
	inputsim.pressKey(.1, 13)
	time.sleep(0.3)

def activate():
	print("Press E")
	inputsim.pressKey(.1, 'e')
	time.sleep(0.3)
	
	
def pip():
	print("Activate pipboy")
	inputsim.pressKey(.2, 'p')
	
def map():
	print("Opening Map")
	inputsim.pressKey(.3, 'm')
	
def inv():
	print("Opening Inv")
	inputsim.pressKey(.3, 'i')
	
def radio():
	print("Opening Radio")
	inputsim.pressKey(.3, 'o')
	
def data():
	print("Opening Data")
	inputsim.pressKey(.3, 'j')
	
	
def vats():
	print("Activate VATS")
	inputsim.pressKey(.5, 'q')
	time.sleep(.5)
	
def left():
	print("Press LEFT arrow")
	arrow(0)
	
def up():
	print("Press UP arrow")
	arrow(1)
	
def right():
	print("Press RIGHT arrow")
	arrow(2)
	
def down():
	print("Press DOWN arrow")
	arrow(3)

def melee():
	print("Melee")
	inputsim.pressKey(.1, 'f')
	
def grenade():
	print("Grenade")
	inputsim.pressKey(1, 'f')
	
def arrow(n):
	arrows = ",;/."
	inputsim.pressKey(.2, arrows[n])
	
def numbers(n):
	print("Pressed " + str(n))
	numlist = "0123456789"
	inputsim.pressKey(.2, numlist[n])

def zero():
	numbers(0)
def one():
	numbers(1)
def two():
	numbers(2)
def three():
	numbers(3)
def four():
	numbers(4)
def five():
	numbers(5)
def six():
	numbers(6)
def seven():
	numbers(7)
def eight():
	numbers(8)
def nine():
	numbers(9)

def tab():
	print("Tab Pressed")
	inputsim.pressKey(.2, 9)
	
def r():
	print("Reload")
	inputsim.pressKey(.2, 'r')
	
def holster():
	print("Holster weapon")
	inputsim.pressKey(1, 'r')
	
def sneak():
	print("Sneaky beaky")
	inputsim.pressKey(.2, 17)
	
def light():
	print("Light")
	inputsim.pressKey(1, 'p')

def presst():
	print("Press T")
	inputsim.pressKey(.2, 't')
	
def holde():
	print("Hold E")
	inputsim.pressKey(1, 'e')
	
def togglepause():
	inputsim.pressKey(.05, 192)
	time.sleep(.1)
	autopy.key.type_string("tgp", 100)
	pressenter()
	inputsim.pressKey(.05, 192)
	time.sleep(.3)
	
##END KEY PRESSES