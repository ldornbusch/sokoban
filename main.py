import pygame
from pygame.locals import *

import game

WINDOW_WIDTH = 512  # size of the window displayed on screen
WINDOW_HEIGHT = 512

GAME_WIDTH = 320.0  # internal game logic resolution
GAME_HEIGHT = 256.0

TPS = 60  # number of game updates per second
SKIP_TICKS = 1000 / TPS  # ms to start skipping frames
MAX_FRAMESKIP = 5  # no we calc max updates (if we are behind) before displaying
MAX_TIMESKIP = 1000  # max Time we try to catch up until we just reset counter

frame_counter = 0  # counts the frames
screen = window_surface = None
sokoban_game = None


def get_real_time():
    """ Real time of the system in ms after pygame.init"""
    return pygame.time.get_ticks()


def init():
    global window_surface, screen, sokoban_game
    pygame.init()
    window_surface = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT], pygame.RESIZABLE)
    screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    sokoban_game = game.Game(screen)


def gameloop():  # http://www.koonsolo.com/news/dewitters-gameloop/
    global frame_counter
    next_game_tick = get_real_time() - 1
    while 1:
        loops = 0
        while get_real_time() > next_game_tick and loops < MAX_FRAMESKIP:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    sokoban_game.handle_key(event.key, True)
                if event.type == KEYUP:
                    sokoban_game.handle_key(event.key, False)
                if event.type == pygame.VIDEORESIZE:
                    global WINDOW_WIDTH, WINDOW_HEIGHT
                    WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
            frame_counter += 1
            sokoban_game.handle_event()
            next_game_tick += SKIP_TICKS
            if get_real_time() > next_game_tick + MAX_TIMESKIP:
                next_game_tick = get_real_time() + SKIP_TICKS
            loops += 1

        screen.fill(0)
        sokoban_game.paint()
        window_tmp = pygame.transform.scale(screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window_surface.blit(window_tmp, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    init()
    gameloop()
