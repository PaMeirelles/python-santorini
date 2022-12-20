import pygame as pg

WIDTH = 680
HEIGHT = 680


class GameInfo:
    def __init__(self, name):
        with open(name, "r") as f:
            linhas = [[int(y) for y in x.split()] for x in f.read().split("\n")]
            print(linhas)
            self.cores = linhas[0]
            self.players = linhas[1]
            self.linhas = linhas
            self.turn = 0
            self.blocks = [0 for _ in range(25)]

    def make_move(self):
        who, to, block = self.linhas[self.turn + 2]
        self.turn += 1
        self.players[who] = to
        self.blocks[block] += 1

    def draw_players(self, win):
        for i in range(4):
            coord = convert_to_coord(self.players[i])
            if i > 1:
                cor = self.cores[1]
            else:
                cor = self.cores[0]
            draw_player(win, coord[0], coord[1], cor)

    def draw_blocks(self, win):
        for n, b in enumerate(self.blocks):
            coord = convert_to_coord(n)
            draw_block(win, coord[0], coord[1], b)

    def draw_all(self, win):
        self.draw_blocks(win)
        self.draw_players(win)


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
    pg.draw.rect(win, "black", (coord_x, coord_y, size, size), width=int(size / 20))


def draw_circle(win, x, y, color, percent_size):
    center_x = x * WIDTH / 5 + WIDTH / 10
    center_y = y * HEIGHT / 5 + HEIGHT / 10
    radius = percent_size / 2 * (WIDTH / 5)

    pg.draw.circle(win, color, (center_x, center_y), radius)
    pg.draw.circle(win, "black", (center_x, center_y), radius, width=int(radius / 10))


def draw_block(win, x, y, h):
    if h == 0:
        return
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


def convert_to_coord(n):
    return n % 5, n // 5


def draw_all(win):
    window.fill(bg_color)
    draw_board(win)
    info.draw_all(win)
    pg.display.update()


info = GameInfo("test")
while running:
    clock.tick(60)
    draw_all(window)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            info.make_move()
# end main loop
pg.quit()
