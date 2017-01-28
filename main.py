import os
import time
from PIL import Image


def init():
    print('Initializing camera preview')
    os.system('sudo service motion start')


def take_picture():
    print('Shutting down camera preview')
    os.system('sudo service motion stop')
    time.sleep(2)
    print('Taking screenshot')
    os.system('fswebcam -r 640x480 --no-banner -d /dev/video0 -D 1 image-test2.jpg')
    time.sleep(1)
    init()
    

def rgb_to_hue(rgb):
    primes = []
    primes.append(rgb[0])
    primes.append(rgb[1])
    primes.append(rgb[2])
    for i in range(len(primes)):
        primes[i] = primes[i] / 255
    mx = max(primes)
    delta = mx - min(primes)

    if delta == 0:
        return 0
    elif primes.index(mx) == 0:
        return 60 * (((primes[1] - primes[2]) / delta) % 6)
    elif primes.index(mx) == 1:
        return 60 * (((primes[2] - primes[0]) / delta) + 2)
    else:
        return 60 * (((primes[0] - primes[2]) / delta) + 4)


def analyze_cube():

    colors = {
        'BLUE': (0, 0, 0),      #175 - 185
        'GREEN': (0, 0, 0),     #100 - 115
        'ORANGE': (0, 0, 0),    # 24 -  35
        'RED': (180, 30, 10),   #  2 - 21
        'WHITE': (0, 0, 0),     
        'YELLOW': (0, 0, 0)     # 46 - 56
    }
    img = Image.open('image-test2.jpg')
    pixels = img.load()

    pix_x = [110, 300, 480]
    pix_y = [80, 280, 440]

    WHT_BD = 15

    for x in pix_x:
        for y in pix_y:
            if abs(pixels[x, y][0] - pixels[x, y][1]) < WHT_BD and abs(pixels[x, y][1] - pixels[x, y][2]) < WHT_BD and abs(pixels[x, y][0] - pixels[x, y][2]) < WHT_BD:
                print('WHITE')
            else:
                print('(', x, ', ', y, ')', ':', pixels[x, y], rgb_to_hue(pixels[x, y]))


if __name__ == '__main__':
    
    init()
    while True:
        i = input('Take picutre? [y/n] ')
        if i == 'y':
            take_picture()
        else:
            analyze_cube()

