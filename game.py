import math
import pygame
import playfield
import gfx_creator

TILE_WIDTH = 16
TILE_HEIGHT = 16

MAX_TILES_HOR = 40
MAX_TILES_VER = 29

GAME_RUN = "run"
GAME_SOLVED = "solved"


class Painter:
    def __init__(self, screen):
        colors = [(0, 0, 0), (0, 1, 0), (1, 1, 1), (0, 1, .4),
                  (0, .9, .5), (1, 1, 0), (1, .7, 0), (1, 1, 1),
                  (.3, .3, .3), (.6, .3, .6), (.6, 0, 0), (0, .6, .6),
                  (0, 1, 1), (.3, .0, .0), (.6, 0, 0), (1, 0, 0)]
        colors = [[c * 255 for c in col] for col in colors]
        self.screen = screen
        self.X_SCALE, self.Y_SCALE = 1, 1
        gfx_creator.init(screen, colors, (1, 1), (TILE_WIDTH, TILE_HEIGHT))
        self.hero = gfx_creator.create_hero()
        self.dest = gfx_creator.create_destination()
        self.wall = gfx_creator.create_wall()
        self.start = gfx_creator.create_exit()
        self.floor = gfx_creator.create_floor()
        self.box = gfx_creator.create_box()
        self.char_to_tile = {"'": self.floor, " ": self.floor, ".": self.dest, "#": self.wall,
                             "@": self.start, "+": self.start, "$": self.box, "*": self.box}

    def hal_blt(self, img, coords):
        self.screen.blit(img, (coords[0] * self.X_SCALE, coords[1] * self.Y_SCALE))

    def paint(self, frame_counter, playfield_data, player, game_status):
        for y in range(0, MAX_TILES_VER):
            for x in range(0, MAX_TILES_HOR):
                tile = self.floor
                if y < len(playfield_data) and x < len(playfield_data[y]):
                    char = playfield_data[y][x]
                    tile = self.char_to_tile[char]
                    # flashing blocks on solved board
                    if game_status == GAME_SOLVED and frame_counter % 60 > 30 and char in ["$", "*"]:
                        tile = self.dest
                if x == 0 or y == 0 or x == MAX_TILES_HOR - 1 or y == MAX_TILES_VER - 1:
                    tile = self.wall
                self.hal_blt(tile, (x * TILE_WIDTH, y * TILE_HEIGHT))
        if game_status == GAME_RUN:
            self.hal_blt(self.hero, player._position)


class Player:
    HALT = "halt"
    PUSH = "push"
    MOVE = "move"

    def __init__(self, game_map):
        self._game_map = game_map
        self._position = [-1, -1]
        self._target = [0, 0]
        self._status = 0  # 0 = stop; 1,2,3,4 = moving(up,right, down, left) 5,6,7,8 = pushing

    def set_target(self, direction):
        retval = Player.HALT
        xs = self._position[0] // TILE_WIDTH
        ys = self._position[1] // TILE_HEIGHT
        xco = int(xs + direction[0])
        yco = int(ys + direction[1])
        if not self._game_map.is_occupied((xco, yco)):
            self._target[0] = xco * TILE_WIDTH
            self._target[1] = yco * TILE_HEIGHT
            self.set_position((xco, yco))
            retval = Player.MOVE
        elif self._game_map.is_move_possible((xs, ys), (xco, yco)):
            self._game_map.perform_move((xs, ys), (xco, yco))
            self.set_position((xco, yco))
            self._target = list(self._position)
            retval = Player.PUSH
        return retval

    def move(self):
        offset = [0, 0]
        offset[0] = self._target[0] - self._position[0]
        offset[1] = self._target[1] - self._position[1]
        if offset[0] != 0:
            self._position[0] = self._position[0] + math.copysign(1, offset[0])
        if offset[1] != 0:
            self._position[1] = self._position[1] + math.copysign(1, offset[1])

    def set_position(self, new_position):
        self._position = [new_position[0] * TILE_WIDTH, new_position[1] * TILE_HEIGHT]


class Game:
    def __init__(self, screen):
        self.up = self.down = self.left = self.right = self.fire = False
        self._playfield = playfield.Playfield()
        self._painter = Painter(screen)
        self._player = Player(self._playfield)
        self._move = self._push = 0
        self._level_collection = 0  # valida values are 0-5 (0 means loading files from disk)
        self._level = 1
        self._status = GAME_RUN
        self.set_level(self._level)
        self._font = pygame.font.Font("topaz.ttf", 16)

    def handle_key(self, key, is_pressed):
        if is_pressed:
            if self._status == GAME_RUN:
                action = Player.HALT
                if key == pygame.K_LEFT:
                    action = self._player.set_target((-1, 0))
                if key == pygame.K_RIGHT:
                    action = self._player.set_target((1, 0))
                if key == pygame.K_UP:
                    action = self._player.set_target((0, -1))
                if key == pygame.K_DOWN:
                    action = self._player.set_target((0, 1))
                if key == pygame.K_SPACE:
                    self.fire = is_pressed
                if action == Player.MOVE:
                    self._move += 1
                if action == Player.PUSH:
                    self._push += 1
            if key == pygame.K_HOME:  # increment level collection
                self._level_collection = (self._level_collection + 1) % (len(playfield.all_levels) + 1)
                self.set_level(self._level)
            if key == pygame.K_END:  # reset level
                self.set_level(self._level)
            if key == pygame.K_PAGEUP:  # next level
                self._level = (self._level + 1) % playfield.get_max_levels(self._level_collection - 1)
                self.set_level(self._level)
            if key == pygame.K_PAGEDOWN:  # previous level
                self._level = (self._level - 1) % playfield.get_max_levels(self._level_collection - 1)
                self.set_level(self._level)

    def handle_event(self, frame_counter):
        if self._status == GAME_RUN:
            self._player.move()
        if self._playfield.is_complete():
            self._status = GAME_SOLVED

    def paint(self, frame_counter):
        self._painter.paint(frame_counter, self._playfield.data, self._player, self._status)
        text = self._font.render(
            "Moves:{:d} Pushs:{:d} Col:{:d} Lev:{:d}/{:d}"
                .format(self._move, self._push, self._level_collection,
                        self._level, playfield.get_max_levels(self._level_collection - 1)),
            False, (255, 255, 255))
        self._painter.hal_blt(text, (0, 465))

    def set_level(self, level):
        self._level = level
        self._status = GAME_RUN
        self._move = self._push = 0
        self._playfield.load_level(self._level - 1, self._level_collection - 1)
        self._player.set_position(self._playfield.start_position)
        self._player.set_target((0, 0))
