import pygame

screen = colors = None
X_SCALE = Y_SCALE = TILE_WIDTH = TILE_HEIGHT = 0


def init(buffer, cols, scale, tile_size):
    global screen, colors, X_SCALE, Y_SCALE, TILE_WIDTH, TILE_HEIGHT
    screen = buffer
    colors = cols
    X_SCALE, Y_SCALE = scale
    TILE_WIDTH, TILE_HEIGHT = tile_size


def hal_pset(point, arg_color):
    hal_fill_rect(point, (point[0] + 1, point[1] + 1), arg_color)


def hal_draw_line(point_1, point_2, arg_color):
    point_1 = (point_1[0] * X_SCALE, point_1[1] * Y_SCALE)
    point_2 = (point_2[0] * X_SCALE, point_2[1] * Y_SCALE)
    pygame.draw.line(screen, arg_color, point_1, point_2)


def hal_draw_rect(point_1, point_2, arg_color):
    point_1 = (point_1[0] * X_SCALE, point_1[1] * Y_SCALE)
    point_2 = (point_2[0] * X_SCALE, point_2[1] * Y_SCALE)
    pygame.draw.line(screen, arg_color, (point_1[0], point_1[1]), (point_1[0], point_2[1]))
    pygame.draw.line(screen, arg_color, (point_1[0], point_2[1]), (point_2[0], point_2[1]))
    pygame.draw.line(screen, arg_color, (point_2[0], point_2[1]), (point_2[0], point_1[1]))
    pygame.draw.line(screen, arg_color, (point_2[0], point_1[1]), (point_1[0], point_1[1]))


def hal_fill_rect(point_1, point_2, arg_color):
    point_1 = (point_1[0] * X_SCALE, point_1[1] * Y_SCALE)
    point_2 = (point_2[0] * X_SCALE, point_2[1] * Y_SCALE)
    pygame.draw.rect(screen, arg_color, (point_1[0], point_1[1], point_2[0] - point_1[0], point_2[1] - point_1[1]))


def create_box():
    hal_fill_rect((10, 11), (26, 27), colors[12])
    hal_draw_line((10, 11), (26, 27), colors[11])
    hal_draw_line((10, 26), (25, 11), colors[11])
    hal_draw_rect((11, 12), (24, 25), colors[11])
    hal_draw_rect((14, 15), (21, 22), colors[11])
    # blit to block image
    tmp = screen.subsurface((10, 11, 26, 27))
    box = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    box.blit(tmp, (0, 0))
    return box


def create_floor():
    hal_fill_rect((10, 11), (26, 27), colors[10])
    hal_draw_line((10, 11), (16, 17), colors[9])
    hal_draw_line((12, 11), (16, 15), colors[9])
    hal_draw_line((14, 11), (16, 13), colors[9])
    hal_draw_line((10, 13), (15, 18), colors[9])
    hal_draw_line((10, 15), (13, 18), colors[9])
    hal_draw_line((10, 17), (11, 18), colors[9])
    hal_pset((16, 11), colors[9])
    hal_draw_line((19, 20), (25, 26), colors[9])
    hal_draw_line((21, 20), (25, 24), colors[9])
    hal_draw_line((23, 20), (25, 22), colors[9])
    hal_draw_line((19, 22), (23, 26), colors[9])
    hal_draw_line((19, 24), (21, 26), colors[9])
    hal_draw_line((19, 26), (25, 20), colors[9])
    hal_draw_line((10, 20), (16, 26), colors[9])
    hal_draw_line((10, 23), (16, 23), colors[9])
    hal_draw_line((10, 26), (16, 20), colors[9])
    hal_draw_line((13, 20), (13, 26), colors[9])
    hal_draw_line((19, 11), (25, 17), colors[9])
    hal_draw_line((19, 14), (25, 14), colors[9])
    hal_draw_line((19, 17), (25, 11), colors[9])
    hal_draw_line((22, 11), (22, 17), colors[9])
    # blit to bottom image
    tmp = screen.subsurface((10, 11, 26, 27))
    bottom = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    bottom.blit(tmp, (0, 0))
    return bottom


def create_exit():
    hal_fill_rect((10, 11), (26, 27), colors[8])
    hal_fill_rect((10, 11), (26, 19), colors[7])
    hal_draw_line((17, 18), (18, 18), colors[8])
    hal_draw_line((17, 19), (18, 19), colors[7])
    hal_draw_line((11, 12), (15, 12), colors[8])  # E
    hal_draw_line((11, 12), (11, 17), colors[8])
    hal_draw_line((11, 17), (15, 17), colors[8])
    hal_draw_line((11, 14), (13, 14), colors[8])
    hal_draw_line((20, 12), (25, 17), colors[8])  # x
    hal_draw_line((20, 17), (25, 12), colors[8])
    hal_pset((13, 20), colors[7])  # i
    hal_draw_line((13, 22), (13, 25), colors[7])
    hal_draw_line((20, 20), (24, 20), colors[7])  # t
    hal_draw_line((22, 20), (22, 25), colors[7])
    # blit to exit image
    tmp = screen.subsurface((10, 11, 26, 27))
    exit = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    exit.blit(tmp, (0, 0))
    return exit


def create_wall():
    hal_fill_rect((10, 11), (26, 27), colors[6])
    hal_draw_rect((13, 14), (22, 23), colors[5])
    hal_draw_line((10, 11), (25, 11), colors[5])
    hal_draw_line((10, 11), (10, 26), colors[5])
    hal_draw_line((25, 11), (10, 26), colors[5])
    hal_fill_rect((10, 11), (24, 14), colors[5])
    hal_fill_rect((10, 11), (13, 25), colors[5])
    hal_fill_rect((17, 18), (22, 23), colors[5])
    hal_fill_rect((20, 16), (22, 23), colors[5])
    hal_fill_rect((15, 21), (22, 23), colors[5])
    hal_draw_line((25, 26), (10, 11), colors[5])
    # blit to wall image
    tmp = screen.subsurface((10, 11, 26, 27))
    wall = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    wall.blit(tmp, (0, 0))
    return wall


def create_destination():
    hal_fill_rect((10, 11), (26, 27), colors[4])
    hal_draw_rect((10, 11), (25, 26), colors[3])
    hal_draw_line((10, 19), (25, 19), colors[3])
    hal_draw_line((10, 18), (25, 18), colors[3])
    hal_draw_line((18, 11), (18, 26), colors[3])
    hal_draw_line((17, 11), (17, 26), colors[3])
    hal_draw_line((10, 11), (25, 26), colors[3])
    hal_draw_line((10, 26), (25, 11), colors[3])
    hal_draw_rect((13, 14), (22, 23), colors[3])
    # blit to dest image
    tmp = screen.subsurface((10, 11, 26, 27))
    dest = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    dest.blit(tmp, (0, 0))
    return dest


def create_hero():
    hal_fill_rect((20, 20), (36, 36), colors[10])
    hal_draw_line((26, 20), (29, 20), colors[7])
    hal_draw_line((24, 23), (24, 22), colors[7])
    hal_draw_line((31, 23), (31, 22), colors[7])
    hal_pset((25, 21), colors[7])
    hal_pset((30, 21), colors[7])
    hal_draw_line((26, 21), (29, 21), colors[6])
    hal_fill_rect((25, 22), (31, 26), colors[6])
    hal_draw_line((21, 31), (22, 31), colors[6])
    hal_pset((21, 32), colors[6])
    hal_draw_line((33, 31), (34, 31), colors[6])
    hal_pset((34, 32), colors[6])
    hal_draw_line((26, 30), (29, 30), colors[6])
    hal_pset((25, 25), colors[0])
    hal_pset((30, 25), colors[0])
    hal_pset((26, 22), colors[8])
    hal_pset((29, 22), colors[8])
    hal_draw_line((26, 24), (27, 25), colors[15])
    hal_draw_line((29, 24), (28, 25), colors[15])
    hal_draw_line((27, 30), (28, 30), colors[15])
    hal_draw_line((25, 31), (24, 32), colors[15])
    hal_pset((24, 33), colors[15])
    hal_pset((29, 33), colors[15])
    hal_pset((25, 30), colors[5])
    hal_pset((30, 30), colors[5])
    hal_fill_rect((25, 26), (29, 30), colors[3])
    hal_fill_rect((29, 26), (31, 30), colors[4])
    hal_pset((28, 26), colors[4])
    hal_pset((27, 27), colors[4])
    hal_pset((28, 28), colors[4])
    hal_pset((27, 29), colors[4])
    hal_draw_line((23, 35), (24, 35), colors[12])
    hal_draw_line((30, 35), (31, 35), colors[12])
    hal_fill_rect((23, 26), (25, 28), colors[11])
    hal_fill_rect((31, 26), (33, 28), colors[11])
    hal_fill_rect((22, 28), (24, 30), colors[11])
    hal_fill_rect((32, 28), (34, 30), colors[11])
    hal_draw_line((21, 30), (22, 30), colors[11])
    hal_draw_line((33, 30), (34, 30), colors[11])
    hal_pset((25, 35), colors[11])
    hal_pset((32, 35), colors[11])
    hal_pset((26, 31), colors[14])
    hal_pset((24, 34), colors[14])
    hal_draw_line((25, 32), (25, 33), colors[14])
    hal_draw_line((29, 31), (29, 32), colors[14])
    hal_draw_line((30, 32), (30, 34), colors[14])
    hal_draw_line((27, 31), (28, 31), colors[13])
    hal_pset((30, 31), colors[13])
    hal_pset((26, 32), colors[13])
    hal_pset((25, 34), colors[13])
    hal_draw_line((31, 32), (31, 34), colors[13])
    # blit to hero image
    tmp = screen.subsurface((20, 20, 36, 36))
    hero = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    hero.blit(tmp, (0, 0))
    hero.set_colorkey(colors[10])
    return hero
