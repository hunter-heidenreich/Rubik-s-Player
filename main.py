import os
import time
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

    img = Image.open('image-test2.jpg')
    pixels = img.load()

    pix_x = [110, 300, 480]
    pix_y = [80, 280, 440]

    WHT_BD = 15

    cube = []

    for x in pix_x:
        for y in pix_y:
            if abs(pixels[x, y][0] - pixels[x, y][1]) < WHT_BD and abs(pixels[x, y][1] - pixels[x, y][2]) < WHT_BD and abs(pixels[x, y][0] - pixels[x, y][2]) < WHT_BD:
                print('(', x, ', ', y, ')', ':', pixels[x, y], 'WHITE')
                cube.append(2)
            else:
                hue = rgb_to_hue(pixels[x, y])
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
                print('(', x, ', ', y, ')', ':', pixels[x, y], rgb_to_hue(pixels[x, y]))

    print(cube)
    return cube


def play_cube(cube):
    root = cube[4]

    PyAudio = pyaudio.PyAudio
    BITRATE = 16000
    FREQUENCY = 261.63
    LENGTH = 1.2232

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''    

    for x in xrange(NUMBEROFFRAMES):
        WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    

    #fill remainder of frameset with silence
    for x in xrange(RESTFRAMES): 
        WAVEDATA = WAVEDATA+chr(128)

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
    while True:
        i = input('Take picutre? [y/n] ')
        if i == 'y':
            take_picture()
        else:
            play_cube(analyze_cube())

