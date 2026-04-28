from enum import Enum


class Scenes(Enum):
    MENU_SCENE = 1
    GAME_SCENE = 2
    DIFFICULTY_SCENE = 3
    RANKING_SCENE = 4


class Difficulties(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
