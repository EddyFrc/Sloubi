import gc
from math import cos, sin, asin, acos, pi
from random import randint
from time import sleep

from ion import *
from kandinsky import *

# Pour modifier les options par défaut en partie rapide, modifier ces paramètres :
BASE_PLAYER_X_POS = 160.0
BASE_PLAYER_Y_POS = 120.0
BASE_PLAYER_SPEED = 1.0
BASE_PLAYER_SIZE = 10.0
BASE_PLAYER_COLOR = (0, 0, 0)
BASE_OBSTACLES = []
BASE_DIFFICULTY = 1
BASE_SPEED = 1.0
FIRST_TICK = 0
BASE_FPS = 40.0

DEFAULT_OPTIONS = {"base_player_x_pos": BASE_PLAYER_X_POS,
                   "base_player_y_pos": BASE_PLAYER_Y_POS,
                   "base_player_speed": BASE_SPEED,
                   "base_player_size": BASE_PLAYER_SIZE,
                   "base_player_color": BASE_PLAYER_COLOR,
                   "base_obstacles": BASE_OBSTACLES,
                   "base_dif": BASE_DIFFICULTY,
                   "base_speed": BASE_SPEED,
                   "first_tick": FIRST_TICK,
                   "base_fps": BASE_FPS}

SCREEN_WIDTH = 320
SCREEN_LENGTH = 222

DEFAULT_BUTTON_WIDTH = 220
DEFAULT_BUTTON_LENGTH = 36

DEFAULT_BUTTON_CENTER = round((SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2)

GAME = None

RUNNING = None


class Button:
    """
    Bouton simple accessible par la navigation
    """

    def __init__(self, x: int, y: int, width: int, length: int, label: str, command=None, sub_layout=None, is_selected: bool = False, is_flag: bool = False, is_active: bool = False, left: tuple = None, right: tuple = None, up: tuple = None, down: tuple = None, border_thickness: int = 2) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.label = label
        self.command = command
        self.sub_layout = sub_layout
        self.is_selected = is_selected
        self.is_flag = is_flag
        self.is_flag_active = is_active
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.border_thickness = border_thickness

    def print_button(self) -> None:
        """
        Afficher le bouton sur l'écran
        """
        if self.is_selected:
            fill_rect(round(self.x - self.border_thickness),
                      round(self.y - self.border_thickness),
                      round(self.width + 2 * self.border_thickness),
                      round(self.length + 2 * self.border_thickness),
                      (29, 98, 181))
        if self.is_flag_active:
            color = (29, 181, 103)
        else:
            color = "gray"
        fill_rect(round(self.x),
                  round(self.y),
                  round(self.width),
                  round(self.length),
                  color)
        draw_string(self.label,
                    round(self.x + 0.5 * self.width - 5 * len(self.label)),
                    round(self.y + 0.5 * self.length - 9),
                    "white",
                    "gray")

    def press_button(self) -> None:
        """Appuie sur le bouton et renvoie True s'il correspond à un sous-menu

        Returns:
            bool: True si un sous-menu est rattaché au bouton
        """
        if self.is_flag:
            self.is_flag_active = not self.is_flag_active
        if self.command is not None:
            self.command()
        if self.sub_layout is not None:
            return True
        return False


class Player:
    """
    Le joueur
    """

    def __init__(self, x: float, y: float, speed: float, size: int, color: tuple) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color

    def edge_bounce_player(self) -> None:
        if self.x + self.size > 320:
            self.x = 320 - self.size
        if self.x < 0:
            self.x = 0
        if self.y + 3 * self.size > 240:
            self.y = 240 - 3 * self.size + 2
        if self.y < 0:
            self.y = 0


class Obstacle:
    """
    Chaque objet de cette classe est un ennemi avec son propre comportement
    """

    def __init__(self, x: float, y: float, direction: int | float, speed: float, size: int, color: tuple) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.size = size
        self.color = color

    def edge_bounce_obstacle(self) -> None:
        """
        Fait rebondir l'obstacle s'il touche un rebord de l'écran, en modifiant la direction de celui-ci
        """
        # Deux cas principaux :
        if self.x + self.size >= 320 or self.x <= 0:
            # Changement de direction
            self.direction = oppose_lat(self.direction)
            # Si l'obstacle est au delà du rebord, le décaler pour éviter qu'il se coince
            if self.x < 0:
                self.x = 0
            elif self.x + self.size > 320:
                self.x = 320 - self.size
        elif self.y + 2 * self.size >= 240 or self.y <= 0:
            # Changement de direction
            self.direction = -self.direction
            # Si l'obstacle est au delà du rebord, le décaler pour éviter qu'il se coince
            if self.y < 0:
                self.y = 0
            elif self.y + self.size > 240:
                self.y = 240 - self.size


class Game:
    """
    Conteneur d'une partie
    """

    def __init__(self, player: Player, obstacles: list, difficulty: int, speed: int | float, fps: int | float, tick: int) -> None:
        self.player = player
        self.obstacles = obstacles
        self.difficulty = difficulty
        self.base_difficulty = difficulty
        self.speed = speed
        self.fps = fps
        self.tick = tick
        self.tick_delay = 2.0 / (fps * 3.0)

    def move_game(self) -> None:
        # On commence par déplacer tous les obstacles
        for obstacle in self.obstacles:
            move_generic(obstacle, obstacle.direction)

        # Puis on déplace le joueur selon les touches sur lesquelles il appuie
        # Petite astuce pour gagner du temps, merci griffpatch :)
        key_x = int(keydown(KEY_RIGHT)) - int(keydown(KEY_LEFT))
        key_y = int(keydown(KEY_DOWN)) - int(keydown(KEY_UP))  # Idem
        if not (key_x == 0 and key_y == 0):
            if key_x == 0:
                move_generic(self.player, deg(asin(key_y)))
            elif key_y == 0:
                move_generic(self.player, deg(acos(key_x)))
            elif key_y == 1:
                move_generic(
                    self.player, (deg(asin(key_y)) + deg(acos(key_x))) / 2)
            else:
                move_generic(
                    self.player, (deg(asin(key_y)) - deg(acos(key_x))) / 2)
        self.player.edge_bounce_player()

    def print_game(self) -> None:
        draw_string("Score : " + str(self.tick), 0, 0)
        for obstacle in self.obstacles:
            print_generic_square(obstacle)
        print_generic_square(self.player)

    def edge_bounce_game(self) -> None:
        for obstacle in self.obstacles:
            obstacle.edge_bounce_obstacle()

    def is_colliding(self) -> bool:
        for obstacle in self.obstacles:
            for coin in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if obstacle.x <= self.player.x + coin[0] * self.player.size <= obstacle.x + obstacle.size \
                        and obstacle.y <= self.player.y + coin[1] * self.player.size <= obstacle.y + obstacle.size:
                    return True
        return False


def main() -> None:
    gc.enable()
    RUNNING = True
    while RUNNING:
        layout_behaviour(MAIN_MENU)
        if keydown(37):  # 37 correspond à la touche 5 sur la numworks
            RUNNING = False


def menu() -> None:
    layout_behaviour(MAIN_MENU)


def game(game: Game = None, **kwargs) -> None:
    """
    Déroulement d'une unique partie
    """
    if kwargs is None:
        game_setup(game)
    else:
        game_setup(game, **kwargs)

    # Boucle de jeu principale
    while not game.is_colliding():
        frame(game)

    game_over(game)
    # thanos(game)


CUSTOM_GAME_MENU = []

MAIN_MENU = [
    [
        Button(
            DEFAULT_BUTTON_CENTER, 80, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_LENGTH,
            "Jouer", game,
            down=(1, 0),
            is_selected=True
        )
    ],
    [
        Button(
            DEFAULT_BUTTON_CENTER, 125, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_LENGTH,
            "Partie personnalisée",
            up=(0, 0), down=(2, 0)
        )
    ],
    [
        Button(
            DEFAULT_BUTTON_CENTER, 170, DEFAULT_BUTTON_WIDTH / 2 - 6, DEFAULT_BUTTON_LENGTH,
            "Infos",
            up=(1, 0), right=(2, 1)
        ),
        Button(
            SCREEN_WIDTH / 2 + 6, 170, DEFAULT_BUTTON_WIDTH / 2 - 6, DEFAULT_BUTTON_LENGTH,
            "Quitter",
            up=(1, 0), left=(2, 0)
        )
    ]
]


def create_game(**kwargs):
    """Retourne un objet Game correspondant aux paramètres en entrée

    Returns:
        Game: l'objet Game correspondant aux paramètres en entrée
    """
    # Instanciation de tous les objets
    return Game(
        player=Player(
            x=kwargs["base_player_x_pos"],
            y=kwargs["base_player_y_pos"],
            speed=kwargs["base_player_speed"],
            size=kwargs["base_player_size"],
            color=kwargs["base_player_color"]
        ),
        obstacles=kwargs["base_obstacles"],
        difficulty=kwargs["base_dif"],
        speed=kwargs["base_speed"],
        tick=kwargs["first_tick"],
        fps=kwargs["base_fps"]
    )


def game_setup(game: Game, **kwargs) -> None:
    if game is None:
        game = create_game(kwargs=DEFAULT_OPTIONS)
    else:
        game = create_game(**kwargs)

    dif = [0, 0].extend(range(game.difficulty))
    for elt in dif:
        game.obstacles.append(new_obstacle(elt + 1))


def frame(game: Game) -> None:
    """Fait dérouler une frame du jeu en argument

    Args:
        game (Game): le jeu à faire tourner
    """
    # Déroulement d'une frame :
    game.edge_bounce_game()  # Rebondir sur les murs
    game.move_game()  # Déplacer tous les objets
    game.tick += 1
    if game.tick % 240 == 0:  # Augmentation de la difficulté
        game.difficulty += 1
        game.obstacles.append(new_obstacle(game.difficulty + 1))
    refresh()  # Rafraîchir l'écran
    game.print_game()  # Afficher tous les objets
    sleep(game.tick_delay)


def game_over(game: Game) -> None:
    refresh()
    draw_string("GAME OVER", 112, 70)
    draw_string("Score : " + str(game.tick), 105, 90)
    draw_string("Difficulté initiale : " + str(game.base_difficulty), 45, 110)
    wait_key(KEY_OK)


def print_layout(layout: list) -> tuple:
    """
    Affichage de la grille de boutons donnée en argument. C'est un affichage seulement, pas de comportement.
    Retourne un tuple correspondant à la position sur la grille du bouton sélectionné.
    """
    output = ()
    for ligne in range(len(layout)):
        for colonne in range(len(layout[ligne])):
            current_elt = layout[ligne][colonne]
            current_elt.print_button()
            if current_elt.is_selected:
                output = (ligne, colonne)
    return output


def layout_behaviour(layout: list) -> None:
    """
    Comportement d'une grille de boutons (= écran)
    

    Oui. Je sais. C'est dégueulasse.
    """
    pos = print_layout(layout)
    current_elt = layout[pos[0]][pos[1]]
    ok = keydown(KEY_OK)
    down = keydown(KEY_DOWN)
    up = keydown(KEY_DOWN)
    left = keydown(KEY_LEFT)
    right = keydown(KEY_RIGHT)

    while not (ok or down or up or left or right):
        ok = keydown(KEY_OK)
        down = keydown(KEY_DOWN)
        up = keydown(KEY_DOWN)
        left = keydown(KEY_LEFT)
        right = keydown(KEY_RIGHT)
    if down and (current_elt.down is not None):
        current_elt.is_selected = not current_elt.is_selected
        layout[current_elt.down[0]][current_elt.down[1]].is_selected = not layout[current_elt.down[0]][current_elt.down[1]].is_selected
    if up and (current_elt.up is not None):
        current_elt.is_selected = current_elt.is_selected
        layout[current_elt.up[0]][current_elt.up[1]].is_selected = not layout[current_elt.up[0]][current_elt.up[1]].is_selected
    if left and (current_elt.left is not None):
        current_elt.is_selected = not current_elt.is_selected
        layout[current_elt.left[0]][current_elt.left[1]].is_selected = not layout[current_elt.left[0]][current_elt.left[1]].is_selected
    if right and (current_elt.right is not None):
        current_elt.is_selected = not current_elt.is_selected
        layout[current_elt.right[0]][current_elt.right[1]].is_selected = not layout[current_elt.right[0]][current_elt.right[1]].is_selected
    if ok:
        for row in layout:
            for column in row:
                if column.is_selected:
                    column.press_button()
    while ok or down or up or left or right:
        ok = keydown(KEY_OK)
        down = keydown(KEY_DOWN)
        up = keydown(KEY_DOWN)
        left = keydown(KEY_LEFT)
        right = keydown(KEY_RIGHT)

def limite_sol(nombre: int, limite: int = 0) -> int:
    if nombre < limite:
        return limite
    return nombre


def limite_plafond(nombre: int, limite: int) -> int:
    if nombre > limite:
        return limite
    return nombre


def wait_key(key: int) -> None:
    while keydown(key):
        pass
    while not keydown(key):
        pass


def refresh() -> None:
    fill_rect(0, 0, 320, 240, "white")


def rad(ang: int | float) -> float:
    return (ang * pi) / 180


def deg(ang: int | float) -> float:
    return (ang * 180) / pi


def new_obstacle(dif: int) -> Obstacle:
    if dif >= 1:
        temp_size = randint(21 - dif, 19 + dif)
    else:
        temp_size = randint(1, 40)
    return Obstacle(float(randint(0, 320 - temp_size)), 0.0,
                    randint(1, 179), 0.2 + (20 / temp_size), temp_size,
                    (222, int(126.5 + 15 * (temp_size - 20)), 31)
                    )


def print_generic_square(obj: Obstacle | Player) -> None:
    fill_rect(int(obj.x), int(obj.y), int(obj.size), int(obj.size), obj.color)


def move_generic(obj: Player | Obstacle, direction: int | float) -> None:
    obj.x += cos(rad(direction)) * obj.speed * 3
    obj.y += sin(rad(direction)) * obj.speed * 3


def oppose_lat(ang: int | float) -> int | float:
    if ang < 0:
        return -ang - 180
    else:
        return 180 - ang


# Pas trouvé un meilleur moyen de faire ça et ça prend trop de place, rip
def thanos(object: list | Game) -> None:
    if type(object) == list:
        while len(object) > 0:
            del object[0]
    else:
        del object.player.x
        del object.player.y
        del object.player.speed
        del object.player.size
        del object.player
        while len(object.obstacles) > 0:
            del object.obstacles[0]
        del object.obstacles
        del object.difficulty
        del object.base_difficulty
        del object.speed
        del object.fps
        del object.tick
        del object.tick_delay
        del object
    gc.collect()


main()
