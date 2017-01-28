import os
import time
import math
from PIL import Image
import pyaudio


def init():
    print('Initializing camera preview')
    os.system('sudo service motion start')


def take_picture():
    print('Shutting down camera preview')
    os.system('sudo service motion stop')
    time.sleep(2)
    print('Taking screenshot')
    os.system('fswebcam -r 640x480 --no-banner -d /dev/video0 -i 0 -D 1 image-test2.jpg')
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

    img = Image.open('image-test2.jpg')
    pixels = img.load()

    pix_x = [110, 300, 480]
    pix_y = [80, 280, 440]

    WHT_BD = 15

    cube = []

    for x in pix_x:
        for y in pix_y:
            avg_red = (pixels[x - 2, y - 2][0] + pixels[x - 1, y - 1][0] + pixels[x, y][0] + pixels[x + 1, y + 1][0] + pixels[x + 2, y + 2][0]) / 5
            avg_green = (pixels[x - 2, y - 2][1] + pixels[x - 1, y - 1][1] + pixels[x, y][1] + pixels[x + 1, y + 1][1] + pixels[x + 2, y + 2][1]) / 5
            avg_blue = (pixels[x - 2, y - 2][2] + pixels[x - 1, y - 1][2] + pixels[x, y][2] + pixels[x + 1, y + 1][2] + pixels[x + 2, y + 2][2]) / 5

            avg_pix = (avg_red, avg_green, avg_blue)
            
            if abs(avg_pix[0] - avg_pix[1]) < WHT_BD and abs(avg_pix[1] - avg_pix[2]) < WHT_BD and abs(avg_pix[0] - avg_pix[2]) < WHT_BD:
                print('(', x, ', ', y, ')', ':', avg_pix, 'WHITE')
                cube.append(2)
            else:
                hue = rgb_to_hue(avg_pix)
                if hue < 20: # RED 0 - 15
                    cube.append(1)
                elif hue < 35: # ORANGE
                    cube.append(5)
                elif hue < 60: # YELLOW
                    cube.append(3)
                elif hue < 115: # GREEN
                    cube.append(6)
                else: # BLUE
                    cube.append(4)
                print('(', x, ', ', y, ')', ':', avg_pix, rgb_to_hue(avg_pix))

    print(cube)
    return cube


def play_cube(cube):
    root = cube[4]

    tonic = 220.0
    tonic = tonic * (2 ** (-5/12))
    
    pattern = []
    
    if root == 1:
        pattern = [0, 4, 7]
    elif root == 2:
        pattern = [2, 5, 9]
    elif root == 3:
        pattern = [4, 7, 11]
    elif root == 4:
        pattern = [5, 9, 12]
    elif root == 5:
        pattern = [7, 11, 14]
    else:
        pattern = [9, 12, 16]

    melody = []
    
    for i in range(3):
        for p in range(len(pattern)):
            diff = root - cube[i * 3 + p]
            note = tonic * (2 ** (((i * 12) + pattern[p] + diff) / 12))
            melody.append(note)
            if p == 2:
                melody.append(note)

    print(melody)

    # This fixes the melody getting cut off. [DON'T TOUCH]
    
    melody.append(22)
    melody.append(22)
    melody.append(22)
    melody.append(22)
    melody.append(22)
    melody.append(22)
    melody.append(22)
    melody.append(22)

    # End of melody fix

    PyAudio = pyaudio.PyAudio
    BITRATE = 16000
    LENGTH = 0.5

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    WAVEDATA = ''    

    for f in melody:
        for x in range(NUMBEROFFRAMES):
            WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/f)/math.pi))*127+128))    

    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = BITRATE, 
                    output = True)
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()
    p.terminate()
    


if __name__ == '__main__':
    
    init()
    run = True
    while run:
        i = input('Take picutre? [y/n] ')
        if i == 'y':
            take_picture()
            play_cube(analyze_cube())
        else:
            run = False
            

