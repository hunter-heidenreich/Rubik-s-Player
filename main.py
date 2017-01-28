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
    os.system('fswebcam -r 600x600 --no-banner -d /dev/video0 -D 1 image-test2.jpg')
    time.sleep(1)
    init()
    

def analyze_cube():

    RED = (180, 30, 10)
    img = Image.open('image-test2.jpg')
    pixels = img.load()

    dim = 100
    
    for ix in range(img.size[1]):
        for i in range(img.size[0]):
            if pixels[i, ix][0] >= 180 and pixels[i, ix][1] < 30 and pixels[i, ix][2] < 10:
               # i += dim // 2
               # ix += dim // 2
                print(pixels[i, ix])
                print(i, ix)
                for x in range(3):
                    for y in range(3):
                        print(pixels[i + dim * x + dim // 2, ix + dim * y + dim // 2])
                img.crop((i, ix, i + dim * 3, ix + dim * 3)).save('sight2.jpg', 'JPEG')
                #img.crop((0, 0, 100, 300)).save('sight2.jpg', 'JPEG')
                return None
            #print(pixels[i, ix])


if __name__ == '__main__':
    '''
    init()
    while True:
        i = input('Take picutre? [y/n] ')
        if i == 'y':
            take_picture()
    '''
    analyze_cube()

