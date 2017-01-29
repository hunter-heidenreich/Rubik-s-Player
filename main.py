import os
import time
import math
from PIL import Image
import pyaudio


# Turns on the webcam to live stream at http://localhost:8080
def init_camera_stream():
    print('Initializing camera preview')
    os.system('sudo service motion start')


# Makes the webcam take a picture
def take_picture():
    # Shuts down live stream of webcam to free up device
    print('Shutting down camera preview')
    os.system('sudo service motion stop')
    time.sleep(2)

    # Takes the picture
    print('Taking picture')
    os.system('fswebcam -r 640x480 --no-banner -d /dev/video0 -i 0 -D 1 rubiks.jpg')
    time.sleep(1)

    # Turns the lives stream back on
    init_camera_stream()


# Converts RGB to a hue value
def rgb_to_hue(rgb):
    # Normalizes RGB from 0 to 1
    primes = []
    primes.append(rgb[0])
    primes.append(rgb[1])
    primes.append(rgb[2])
    for i in range(len(primes)):
        primes[i] = primes[i] / 255

    # Identifies the max of RGB and the difference between max and min
    mx = max(primes)
    delta = mx - min(primes)

    # Calculates the hue value
    if delta == 0:
        return 0
    elif primes.index(mx) == 0:
        return 60 * (((primes[1] - primes[2]) / delta) % 6)
    elif primes.index(mx) == 1:
        return 60 * (((primes[2] - primes[0]) / delta) + 2)
    else:
        return 60 * (((primes[0] - primes[2]) / delta) + 4)


# Analyzes the cubes colors
def analyze_cube():
    # Constant cube settings
    pix_x = [110, 300, 480] # The x pixel locations
    pix_y = [80, 280, 440]  # The y pixel locations
    WHT_BD = 15             # The maximum difference between RGB for a white color

    # Loads the images into the program
    img = Image.open('rubiks.jpg')
    pixels = img.load()

    # Creates cube
    cube = []

    # Loops over cube values
    for x in pix_x:
        for y in pix_y:

            pixel_sampling = 5
            avg_c = [0, 0, 0]

            for i in range(pixel_sampling):
                avg_c[0] += pixels[x - i - (pixel_sampling // 2), y - i - (pixel_sampling // 2)][0]
                avg_c[1] += pixels[x - i - (pixel_sampling // 2), y - i - (pixel_sampling // 2)][1]
                avg_c[2] += pixels[x - i - (pixel_sampling // 2), y - i - (pixel_sampling // 2)][2]

            avg_c[0] /= pixel_sampling
            avg_c[1] /= pixel_sampling
            avg_c[2] /= pixel_sampling

            avg_pix = (avg_c[0], avg_c[1], avg_c[2])

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
    init_camera_stream()
    run = True
    while run:
        i = input('Take picutre? [y/n] ')
        if i == 'y':
            take_picture()
            play_cube(analyze_cube())
        else:
            run = False
