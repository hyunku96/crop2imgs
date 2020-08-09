from tkinter import filedialog
from tkinter import *
import pygame, sys

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


def setup(path, scale_factor=3):
    px = pygame.image.load(path)
    px = pygame.transform.scale(px, ((int)(width / scale_factor), (int)(height / scale_factor)))
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

    scale_factor = 3  # original img size will be downscaled by this scale

    n_files = 0
    files = []
    print('press a to add file')
    print('press any key to stop selecting')
    while input() == 'a':
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg"), ("png files", "*.png")))

        if root.filename in files:
            print('same file selected!')
            sys.exit()

        files.append(root.filename)
        n_files += 1

    output_locs = []
    imgs = []
    for i in range(n_files):
        output_locs.append(files[i] + "_croped.png")
        imgs.append(cv.imread(files[i], -1))

    #scale cropping region
    height, width, channel = imgs[0].shape

    screen, px = setup(files[0])
    left, upper, right, lower = mainLoop(screen, px)

    pygame.display.quit()

    # ensure output rect always has positive width, height
    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower

    left = left * scale_factor
    right = right * scale_factor
    upper = upper * scale_factor
    lower = lower * scale_factor

    for i in range(n_files):
        img = imgs[i][upper:lower+1, left:right+1, :]
        cv.imwrite(output_locs[i], img)
