"""
0 = floor(" ") ; 1 = dest(".") 2 = wall("#");
3 = start("@") ; 4 = box("$") ; 5 = box on dest("*")
"""
import os
import levelmaps

int_to_char = {0: " ", 1: ".", 2: "#", 3: "@", 4: "$", 5: "*"}
all_levels = [levelmaps.level_set01, levelmaps.level_set02, levelmaps.level_set03,
              levelmaps.level_set04, levelmaps.level_set05]


def load_file_content(filename):
    with open(filename, "r") as f:
        tmp_lst = f.readlines()
    return tmp_lst


class Playfield:
    def __init__(self):
        self._data = []
        self._start_pos = (-1, -1)

    @property
    def data(self):
        return self._data

    @property
    def start_position(self):
        return self._start_pos

    def is_complete(self):
        retval = True
        for line in self._data:
            for char in line:
                if char == "$":
                    retval = False
        return retval

    def is_occupied(self, point):
        retval = True
        if point[1] < len(self._data) and point[0] < len(self._data[point[1]]):
            if self._data[point[1]][point[0]] in [" ", ".", "@"]:
                retval = False
        return retval

    def is_block(self, point):
        retval = False
        if point[1] < len(self._data) and point[0] < len(self._data[point[1]]):
            if self._data[point[1]][point[0]] in ["$", "*"]:
                retval = True
        return retval

    def is_move_possible(self, player_pos, stone_pos):
        retval = False
        offset = [stone_pos[0] - player_pos[0], stone_pos[1] - player_pos[1]]
        stone_target = [stone_pos[0] + offset[0], stone_pos[1] + offset[1]]
        return (not self.is_occupied(stone_target)) and self.is_block(stone_pos)

    def perform_move(self, player_pos, stone_pos):
        offset = [stone_pos[0] - player_pos[0], stone_pos[1] - player_pos[1]]
        stone_target = [stone_pos[0] + offset[0], stone_pos[1] + offset[1]]
        src_tile = " "
        if self._data[stone_pos[1]][stone_pos[0]] == "*":
            src_tile = "."
        self._data[stone_pos[1]][stone_pos[0]] = src_tile
        dst_tile = "$"
        if self._data[stone_target[1]][stone_target[0]] == ".":
            dst_tile = "*"
        self._data[stone_target[1]][stone_target[0]] = dst_tile

    def load_level(self, level, set_indicator=-1):
        if set_indicator == -1:
            filename = "levels/l%d.asc" % level
            if os.path.isfile(filename):
                self.load_standard_level(load_file_content(filename))
            filename = "levels/l%d.lev" % level
            if os.path.isfile(filename):
                self.load_legacy_level(load_file_content(filename))
        else:
            self.load_standard_level(all_levels[set_indicator][level])

    def load_standard_level(self, level_content):
        retval = [[]]
        counter = [0, 0]
        for line in level_content:
            retval.append([])
            counter[1] += 1
            counter[0] = 0
            for char in line:
                if char != "\n":
                    if char == "@":
                        self._start_pos = list(counter)
                    counter[0] += 1
                    retval[-1].append(char)
        self._data = retval

    def load_legacy_level(self, level_content):
        retval = []
        for y in range(0, 16):
            retval.append([])
            for x in range(0, 20):
                val = 2
                if x < 18 and y < 14:
                    count = (y - 1) * 17 + x - 1
                    if count < len(level_content):
                        val = level_content[count]
                if int(val) == 3:
                    self._start_pos = (x, y)
                retval[y].append(int_to_char[int(val)])
        self._data = retval
