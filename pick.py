from pynput.mouse import Button, Controller
import random
import time
import math

mouse = Controller()

totalTime = 20

time.sleep(1)

size = 220
width = 1920
height = 1080

_width = int(math.ceil(float(width) / size))
_height = int(math.ceil(float(height) / size))

def index2coord(i):
    quotient, rem = divmod(i, _width)
    return ((rem % _width) * size, (quotient % _height) * size) 

index = 0
start = time.time()
end = start
while end - start < totalTime:
   
    x, y = index2coord(index)
    x += random.randint(-20, 20)
    y += random.randint(-20, 20)
    f = lambda z: max(0, min(width, z))

    # move mouse
    mouse.position = (f(x), f(y))

    mouse.press(Button.left)
    mouse.release(Button.left)

    end = time.time()
    index += 1
