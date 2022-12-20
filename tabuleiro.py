import pygame as pg

WIDTH = 680
HEIGHT = 680

pg.init()
clock = pg.time.Clock()
running = True
window = pg.display.set_mode((WIDTH, HEIGHT))

bg_color = (0, 204, 153)


def draw_board(win):
    for x in range(5):
        pg.draw.line(win, "black", (WIDTH * x / 5, 0), (WIDTH * x / 5, HEIGHT))
        pg.draw.line(win, "black", (0, HEIGHT * x / 5), (WIDTH, HEIGHT * x / 5))


def draw_rect(win, x, y, percent_size):
    size = WIDTH / 5 * percent_size
    coord_x = x * WIDTH / 5 + WIDTH / 5 * ((1 - percent_size) / 2)
    coord_y = y * HEIGHT / 5 + HEIGHT / 5 * ((1 - percent_size) / 2)
    pg.draw.rect(win, "white", (coord_x, coord_y, size, size))
    pg.draw.rect(win, "black", (coord_x, coord_y, size, size), width=int(size/20))


def draw_circle(win, x, y, color, percent_size):
    center_x = x * WIDTH / 5 + WIDTH / 10
    center_y = y * HEIGHT / 5 + HEIGHT / 10
    radius = percent_size / 2 * (WIDTH / 5)

    pg.draw.circle(win, color, (center_x, center_y), radius)
    pg.draw.circle(win, "black", (center_x, center_y), radius, width=int(radius/10))


def draw_block(win, x, y, h):
    if h == 1:
        draw_rect(win, x, y, 0.95)
    elif h == 2:
        draw_rect(win, x, y, 0.75)
    elif h == 3:
        draw_circle(win, x, y, "white", 0.65)
    elif h == 4:
        draw_circle(win, x, y, "blue", 0.55)
    else:
        print(f"Altura inválida ({h})")
        exit(1)


def draw_player(win, x, y, p):
    if p == 0:
        draw_circle(win, x, y, (128, 128, 128), 0.5)
    elif p == 1:
        draw_circle(win, x, y, (200, 200, 200), 0.5)
    elif p == 2:
        draw_circle(win, x, y, (153, 153, 255), 0.5)
    else:
        print(f"Jogador inválido ({p})")


def draw_all(win):
    window.fill(bg_color)
    draw_board(win)

    draw_block(win, 2, 2, 1)
    draw_block(win, 2, 2, 2)

    draw_player(win, 2, 2, 1)
    draw_player(win, 1, 2, 0)
    draw_player(win, 3, 2, 2)

    pg.display.update()


while running:
    clock.tick(60)
    draw_all(window)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
# end main loop
pg.quit()
