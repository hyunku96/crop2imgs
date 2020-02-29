from tkinter import filedialog
from tkinter import *
import pygame, sys

#from PIL import Image
import cv2 as cv

pygame.init()

def displayImage(screen, px, topleft, prior):
    # ensure that the rect always has positive width, height
    x, y = topleft
    width = pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height

    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)


def setup(path):
    px = pygame.image.load(path)
    px = pygame.transform.scale(px, ((int)(width / 5), (int)(height / 5)))
    screen = pygame.display.set_mode(px.get_rect()[2:])
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px


def mainLoop(screen, px):
    topleft = bottomright = prior = None
    n = 0
    while n != 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = event.pos
                else:
                    bottomright = event.pos
                    n = 1
        if topleft:
            prior = displayImage(screen, px, topleft, prior)
    return (topleft + bottomright)


if __name__ == "__main__":
    root = Tk()
    root.filename1 = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg")))
    input1_loc = root.filename1

    root.filename2 = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg")))
    input2_loc = root.filename2

    if root.filename1 == root.filename2:
        sys.exit()

    output1_loc = root.filename1
    output2_loc = root.filename2

    #im1 = Image.open(input1_loc)
    im1 = cv.imread(input1_loc, -1)
    #im2 = Image.open(input2_loc)
    im2 = cv.imread(input2_loc, -1)

    #scale cropping region
    height, width, channel = im1.shape

    screen, px = setup(input1_loc)
    left, upper, right, lower = mainLoop(screen, px)

    # ensure output rect always has positive width, height
    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower
    #left = left * im1.width / 500
    #right = right * im1.width / 500
    #upper = upper * im1.height / 500
    #lower = lower * im1.height / 500
    left = left * 5
    right = right * 5
    upper = upper * 5
    lower = lower * 5
    #im1 = im1.crop((left, upper, right, lower))
    im1 = im1[upper:lower+1, left:right+1,:]
    #im2 = im2.crop((left, upper, right, lower))
    im2 = im2[upper:lower+1, left:right+1,:]
    pygame.display.quit()
    #im1.save(output1_loc)
    cv.imwrite(output1_loc, im1)
    #im2.save(output2_loc)
    cv.imwrite(output2_loc, im2)
'''
def post_processing(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    h = clahe.apply(h)
    out = cv.merge([h, s, v])
    out = cv.cvtColor(out, cv.COLOR_HSV2BGR)
    return out

img = cv.imread('ship.png', cv.IMREAD_COLOR)
cv.imshow('ex', img)
res = post_processing(img)
cv.imshow('ex', img)
cv.waitKey(0)
'''