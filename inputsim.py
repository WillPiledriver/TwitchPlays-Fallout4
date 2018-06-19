import autopy
import math
import random
import time


def click(lmb=True):
	if lmb:
		autopy.mouse.toggle(True, autopy.mouse.LEFT_BUTTON)
		time.sleep(0.1)
		autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
	else:
		autopy.mouse.toggle(True, autopy.mouse.RIGHT_BUTTON)
		time.sleep(0.1)
		autopy.mouse.toggle(False, autopy.mouse.RIGHT_BUTTON)


def pressKey(t, key=None):
	autopy.key.toggle(key, True)
	time.sleep(t)
	autopy.key.toggle(key, False)
	
def moveMouse(x, y):
	(xx, yy) = autopy.mouse.get_pos()
	autopy.mouse.move(xx+x, yy+y)
	
# The autopy.mouse.smooth_move() function implemented in Python instead of C.
def smoothly_move_mouse(dst_x, dst_y):
    '''
    Smoothly moves the cursor to the given (x, y) coordinate in a
    straight line.
    '''
    if not autopy.screen.point_visible(dst_x, dst_y):
        raise ValueError("Point out of bounds")
        return

    x, y = autopy.mouse.get_pos()
    velo_x = velo_y = 0.0

    while True:
        distance = math.hypot(x - dst_x, y - dst_y)
        if distance <= 1.0:
            break

        gravity = random.uniform(5.0, 500.0)
        velo_x += (gravity * (dst_x - x)) / distance
        velo_y += (gravity * (dst_y - y)) / distance

        # Normalize velocity to get a unit vector of length 1.
        velo_distance = math.hypot(velo_x, velo_y)
        velo_x /= velo_distance
        velo_y /= velo_distance

        x += int(round(velo_x))
        y += int(round(velo_y))

        autopy.mouse.move(x, y) # Automatically raises an exception if point
                                # is out of bounds.

        time.sleep(random.uniform(0.001, 0.003))
		
