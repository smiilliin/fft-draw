import pygame as pg
import numpy as np
import sys


pg.init()
width = 400
height = 400
screen = pg.display.set_mode((width, height))
pg.display.set_caption("fft-draw")

drawing = False
last_mouse_pos = None
ratio = max(width / 2, height / 2) / 20


def z_to_position(z):
    z = z.conjugate() * ratio + (width / 2 + 1j * height / 2)
    return (z.real, z.imag)


def position_to_z(z):
    z = z[0] + 1j * z[1]
    z = (z - (width / 2 + 1j * height / 2)) / ratio
    return z.conjugate()


def draw_circle_vector(start, z):
    end = start + z
    scale = round(abs(z), 2)

    pg.draw.line(screen, (255, 255, 255), z_to_position(start), z_to_position(end), 3)
    pg.draw.line(
        screen,
        (255, 255, 255),
        z_to_position(end),
        z_to_position(end + z * np.exp(1j * np.radians(-180 + 45)) / 2),
        3,
    )
    pg.draw.line(
        screen,
        (255, 255, 255),
        z_to_position(end),
        z_to_position(end + z * np.exp(1j * np.radians(-180 - 45)) / 2),
        3,
    )
    pg.draw.circle(screen, (100, 100, 100), z_to_position(start), scale * ratio, 2)


clock = pg.time.Clock()

fs = 0.03

started = False
drawing = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing_zs = []
                drawing = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                started = True
                drawing = False
                last_mouse_pos = None
                lastn = 0
                ss = []
                N = len(drawing_zs)
                yfft = np.fft.fft(drawing_zs, N)
                start_tick = pg.time.get_ticks()

    screen.fill((0, 0, 0))

    if drawing:
        mouse_pos = pg.mouse.get_pos()

        drawing_zs.append(position_to_z(mouse_pos))

        if len(drawing_zs) > 1:
            pg.draw.lines(
                screen,
                (100, 100, 200),
                False,
                [z_to_position(s) for s in drawing_zs],
                3,
            )
    elif started:
        ms = pg.time.get_ticks() - start_tick
        n = ((ms / 1000) // fs) % N

        if lastn > n:
            ss = []
        lastn = n

        zs = np.array(
            [1 / N * X * np.exp(1j * 2 * np.pi * k * n / N) for k, X in enumerate(yfft)]
        )

        zsum = zs[0]
        zs = zs[1:]

        for z in zs:
            draw_circle_vector(zsum, z)
            zsum += z

        ss.append(zsum)

        if len(ss) > 1:
            pg.draw.lines(
                screen, (100, 100, 200), False, [z_to_position(s) for s in ss], 3
            )

    pg.display.flip()
    clock.tick(60)
