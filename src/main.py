#!/bin/env python

from math import acos, asin, cos, pi, sin
from random import randint
from threading import Thread
from time import sleep
from typing import Callable

# from kandinsky import *
import kandinsky as k

from ion import *

# CONSTANTES
# Pour modifier les options par défaut en partie rapide, modifier ces constantes :
BASE_PLAYER_X_POS = 160.0
BASE_PLAYER_Y_POS = 120.0
BASE_PLAYER_SPEED = 2.0
BASE_PLAYER_SIZE = 10
BASE_PLAYER_COLOR = (29, 98, 181)
BASE_OBSTACLES = []
BASE_DIFFICULTY = 1
FIRST_TICK = 0
BASE_FPS = 60.0
BASE_DT = 1 / BASE_FPS
BASE_SPEED = 1.0

DEFAULT_OPTIONS = {
    "base_player_x_pos": BASE_PLAYER_X_POS,
    "base_player_y_pos": BASE_PLAYER_Y_POS,
    "base_player_speed": BASE_PLAYER_SPEED,
    "base_player_size": BASE_PLAYER_SIZE,
    "base_player_color": BASE_PLAYER_COLOR,
    "base_obstacles": BASE_OBSTACLES,
    "base_dif": BASE_DIFFICULTY,
    "base_dt": BASE_DT,
    "first_tick": FIRST_TICK,
    "base_fps": BASE_FPS,
    "base_speed": BASE_SPEED
}

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 222

DEFAULT_BUTTON_WIDTH = 220
DEFAULT_BUTTON_HEIGHT = 36
DEFAULT_BUTTON_CENTER = round((SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2)
BORDER_THICKNESS = 2

DEFAULT_SLIDER_HANDLE_WIDTH = 6
DEFAULT_SLIDER_HANDLE_HEIGHT = 20
DEFAULT_SLIDER_HEIGHT = 10
DEFAULT_SLIDER_SIDE_MARGIN = 10

OBJECT_SPEED_MULTIPLIER = 50.0

COLOR_SELECTED = (29, 98, 181)
COLOR_ENABLED = (26, 189, 12)

LETTER_WIDTH = 10

# VARIABLES GLOBALES CRITIQUES
global _running, _game, _cursor, _index, _collision
_game = None
_running = None
_cursor = None
_index = None
_collision = None


# MENUS
class GraphicalNode:
    """
    Element de menu générique
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class SelectableNode(GraphicalNode):
    """
    Element de menu qu'on sélectionne au curseur
    """

    def __init__(
        self, x: int, y: int, _index: int,
        _left: int = None, _right: int = None, _up: int = None, _down: int = None
    ) -> None:
        super().__init__(x, y)
        self._index = _index
        self._left = _left
        self._right = _right
        self._up = _up
        self._down = _down


class Button(SelectableNode):
    """
    Bouton simple accessible par la navigation
    """

    def __init__(
        self, x: int, y: int, width: int, height: int, label: str, target, _index,
        _left: int = None, _right: int = None, _up: int = None, _down: int = None
    ) -> None:
        super().__init__(x, y, _index, _left, _right, _up, _down)
        self.width = width
        self.height = height
        self.label = label
        self.target = target

    def draw(self) -> None:
        """
        Afficher le bouton sur l'écran
        """
        if _cursor == self._index:
            # Si le curseur est positionné sur ce bouton, on affiche un contour bleu
            # supplémentaire (rectangle bleu en arrière plan)
            k.fill_rect(
                self.x - BORDER_THICKNESS,
                self.y - BORDER_THICKNESS,
                self.width + 2 * BORDER_THICKNESS,
                self.height + 2 * BORDER_THICKNESS,
                (29, 98, 181)
            )

        # Couleur principale
        color = "gray"

        def is_target_bool():  # C'est soit ça soit deux if imbriqués au lieu d'un "and"...
            return type(self.target) == bool

        # And "court-circuité"
        if is_target_bool() and self.target:
            color = (29, 181, 103)

        k.fill_rect(
            self.x,
            self.y,
            self.width,
            self.height,
            color
        )

        k.draw_string(
            self.label,
            round(self.x + 0.5 * self.width - 5 * len(self.label)),
            round(self.y + 0.5 * self.height - 9),
            "white",
            "gray"
        )

    def press(self) -> bool:
        """Appuyer sur le bouton"""
        match self.target:
            case int():
                return True
            case bool():
                self.target = not self.target
            case _:
                self.target()
        return False


class Slider(SelectableNode):
    """
    Barre de défilement accessible par la navigation (utilisée pour choisir la difficulté par exemple)
    """

    def __init__(
        self, x: int, y: int, width: int, size: int, state: int, _index,
        _left: int = None, _right: int = None, _up: int = None, _down: int = None
    ) -> None:
        super().__init__(x, y, _index, _left, _right, _up, _down)
        self.width = width  # attention length est la longueur en pixels utilisée à l'affichage
        self.size = size  # ceci est le nombre de valeurs que peut prendre la barre
        # ceci est la valeur de la barre à l'instant t (0 <= state < size)
        self.state = state

    def draw(self, handle_color=COLOR_SELECTED) -> None:
        k.fill_rect(
            self.x,
            self.y - round(DEFAULT_SLIDER_HEIGHT / 2),
            self.width,
            DEFAULT_SLIDER_HEIGHT,
            "gray"
        )

        # Si le curseur est positionné sur ce bouton, on affiche un contour supplémentaire
        # (rectangle de couleur en arrière plan)
        if _cursor == self._index:
            k.fill_rect(
                DEFAULT_SLIDER_SIDE_MARGIN + self.x + round(
                    self.state * (self.width - 2 * DEFAULT_SLIDER_SIDE_MARGIN) / (self.size - 1)
                ) - round(DEFAULT_SLIDER_HANDLE_WIDTH / 2) - BORDER_THICKNESS,
                self.y - BORDER_THICKNESS -
                round(DEFAULT_SLIDER_HANDLE_HEIGHT / 2),
                DEFAULT_SLIDER_HANDLE_WIDTH + 2 * BORDER_THICKNESS,
                DEFAULT_SLIDER_HANDLE_HEIGHT + 2 * BORDER_THICKNESS,
                handle_color
            )

        k.fill_rect(
            DEFAULT_SLIDER_SIDE_MARGIN + self.x + round(
                self.state * (self.width - 2 * DEFAULT_SLIDER_SIDE_MARGIN) / (self.size - 1)
            ) - round(DEFAULT_SLIDER_HANDLE_WIDTH / 2),
            self.y - round(DEFAULT_SLIDER_HANDLE_HEIGHT / 2),
            DEFAULT_SLIDER_HANDLE_WIDTH,
            DEFAULT_SLIDER_HANDLE_HEIGHT,
            (127, 127, 127)
        )

    def refresh(self, handle_color) -> None:
        k.fill_rect(
            self.x,
            self.y - BORDER_THICKNESS -
            round(DEFAULT_SLIDER_HANDLE_HEIGHT / 2),
            self.width,
            DEFAULT_SLIDER_HANDLE_HEIGHT + 2 * BORDER_THICKNESS,
            "white"
        )
        self.draw(handle_color)

    def press(self) -> None:
        self.refresh(COLOR_ENABLED)
        while keydown(KEY_OK):
            pass

        while not keydown(KEY_OK):
            if keydown(KEY_LEFT) and self.state > 0:
                self.state -= 1
                self.refresh(COLOR_ENABLED)
                wait_key_basic(KEY_LEFT)
            if keydown(KEY_RIGHT) and self.state < self.size - 1:
                self.state += 1
                self.refresh(COLOR_ENABLED)
                wait_key_basic(KEY_RIGHT)

        while keydown(KEY_OK):
            pass


class Label(GraphicalNode):
    """
    Texte simple qui peut être affiché sur l'écran
    """

    def __init__(
        self, x: int, y: int, length: int, content: str | Callable[[Slider], str], input: object = None,
        color: str | tuple = "black", background: str | tuple = "white"
    ) -> None:
        super().__init__(x, y)
        self.length = length
        self.content = content
        self.input = input
        self.color = color
        self.background = background

    def draw(self) -> None:
        if type(self.content) == str:
            buffer = self.content
        else:
            buffer = self.content(self.input)

        y = self.y
        while len(buffer) * LETTER_WIDTH > self.length:
            index = round(self.length / LETTER_WIDTH)
            while buffer[index] != " ":
                index -= 1
            k.draw_string(
                buffer[0:index], self.x, y,
                self.color, self.background
            )
            buffer = buffer[index + 1:]
            y += 18

        k.draw_string(buffer, self.x, y, self.color, self.background)


# PARTIE
class GameElement:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Player(GameElement):
    """
    Classe réprésentant le joueur (carré)
    """

    def __init__(self, x: float, y: float, speed: float, size: int, color: tuple) -> None:
        super().__init__(x, y)
        self.speed = speed
        self.size = size
        self.color = color

    def edge_bounce_player(self) -> None:
        """
        S'assure que le joueur ne puisse pas sortir des limites de l'écran
        """
        if self.x + self.size > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.size
        if self.x < 0:
            self.x = 0
        if self.y + self.size > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.size
        if self.y < 0:
            self.y = 0


class Obstacle(GameElement):
    """
    Chaque objet de cette classe est un ennemi (= carré rouge)
    """

    def __init__(self, x: float, y: float, direction: int | float, speed: float, size: int, color: tuple) -> None:
        super().__init__(x, y)
        self.direction = direction
        self.speed = speed
        self.size = size
        self.color = color

    def edge(self) -> None:
        """
        Fait rebondir l'obstacle s'il touche un rebord de l'écran, en modifiant la direction de celui-ci
        """
        # Deux cas principaux :
        if self.x + self.size >= SCREEN_WIDTH or self.x <= 0:
            # Changement de direction
            self.direction = oppose_lat(self.direction)
            # Si l'obstacle est au delà du rebord, le décaler pour éviter qu'il se coince
            if self.x < 0:
                self.x = 0
            elif self.x + self.size > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.size
        elif self.y + self.size >= SCREEN_HEIGHT or self.y <= 0:
            # Changement de direction
            self.direction = -self.direction
            # Si l'obstacle est au delà du rebord, le décaler pour éviter qu'il se coince
            if self.y < 0:
                self.y = 0
            elif self.y + self.size > SCREEN_HEIGHT:
                self.y = SCREEN_HEIGHT - self.size


class Game:
    """
    Conteneur d'une partie
    """

    def __init__(
        self, player: Player, obstacles: list, difficulty: int, fps: int | float, dt: float, speed: float, score: int
    ) -> None:
        # fps = rendus par secondes du thread graphique
        # dt = facteur de vitesse du jeu (moteur) : normalement inversement proportionnel au nombre d'ips
        self.player = player
        self.obstacles = obstacles
        self.difficulty = difficulty
        self.base_difficulty = difficulty
        self.fps = fps
        self.dt = dt
        self.speed = speed
        self.score = score

    def move_game(self) -> None:
        """
        Déplacer tous les objets contenus dans cette partie (obstacles et joueur)
        """
        # On commence par déplacer tous les obstacles
        for obstacle in self.obstacles:
            move_generic(obstacle, obstacle.direction, self.dt, self.speed)

        # Puis on déplace le joueur selon les touches sur lesquelles il appuie
        key_x = int(keydown(KEY_RIGHT)) - int(keydown(KEY_LEFT))
        key_y = int(keydown(KEY_DOWN)) - int(keydown(KEY_UP))  # Idem
        if not (key_x == 0 and key_y == 0):
            if key_x == 0:
                move_generic(self.player, deg(asin(key_y)), self.dt, self.speed)
            elif key_y == 0:
                move_generic(self.player, deg(acos(key_x)), self.dt, self.speed)
            elif key_y == 1:
                move_generic(self.player, (deg(asin(key_y)) + deg(acos(key_x))) / 2, self.dt, self.speed)
            else:
                move_generic(self.player, (deg(asin(key_y)) - deg(acos(key_x))) / 2, self.dt, self.speed)
        self.player.edge_bounce_player()

    def print_game(self) -> None:
        """
        Afficher tous les éléments de la partie
        """
        k.draw_string("Score : " + str(round(self.score)), 0, 0)
        for obstacle in self.obstacles:
            print_generic_square(obstacle)
        print_generic_square(self.player)

    def edge_bounce_game(self) -> None:
        """
        Appelle edge() pour chaque obstacle du jeu
        """
        for obstacle in self.obstacles:
            obstacle.edge()

    def is_colliding(self) -> bool:
        """Détermine si le joueur touche un obstacle

        Returns:
            bool: True si le joueur est superposé avec un obstacle
        """
        for obstacle in self.obstacles:
            for coin in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if obstacle.x <= self.player.x + coin[0] * self.player.size <= obstacle.x + obstacle.size \
                    and obstacle.y <= self.player.y + coin[1] * self.player.size <= obstacle.y + obstacle.size:
                    return True
        return False

    def next(self) -> None:
        """
        Fait dérouler un "moment" du jeu : une itération de boucle
        """
        self.edge_bounce_game()  # Faire rebondir les obstacles sur les murs si besoin
        self.move_game()  # Déplacer tous les objets
        # Plus dt est grand, plus le laps de temps est grand et par conséquent plus le score doit augmenter
        self.score += self.dt * 30
        if self.score / self.difficulty > 240:  # Augmentation de la difficulté
            self.difficulty += 1
            self.obstacles.append(new_obstacle(self.difficulty + 1))
        sleep(self.dt)

    def next_image(self) -> None:
        refresh()  # Rafraîchir l'écran
        self.print_game()  # Afficher tous les objets
        try:
            k.wait_vblank()
        except ModuleNotFoundError:
            sleep(1 / self.fps)
        except NameError:
            sleep(1 / self.fps)
        except AttributeError:
            sleep(1 / self.fps)

    def game_over(self) -> None:
        """
        Affiche l'écran de game over
        """
        refresh()
        k.draw_string("GAME OVER", 112, 70)
        k.draw_string("Score : " + str(round(self.score)), 105, 90)
        k.draw_string(
            "Difficulté initiale : " + str(self.base_difficulty),
            45, 110
        )
        wait_key(KEY_OK)


# FONCTIONS & PROCÉDURES
# CONTAINER
def main() -> None:
    global _cursor, _running, _index
    _running = True
    _cursor = 0
    _index = 0

    while _running:
        layout_behaviour(MENUS[_index])
        if keydown(37):  # 37 correspond à la touche 5 sur la numworks
            _running = False

    try:
        k.quit()
    except Exception:
        pass


def engine_thread() -> None:
    global _game, _collision
    _collision = False
    while not _game.is_colliding():
        _game.next()
    _collision = True


def graphic_thread() -> None:
    global _game, _collision
    while not _collision:
        _game.next_image()


def stop() -> None:
    """
    Définit le flag _running à False
    """
    global _running
    _running = False


# PARTIE
def game(**kwargs) -> None:
    """
    Déroulement d'une unique partie
    """
    global _game, _collision

    if len(kwargs) == 0:
        _game = game_setup()
    else:
        _game = game_setup(**kwargs)

    # Boucle de jeu principale
    processing = Thread(target=engine_thread, name="EngineThread")
    processing.start()

    graphic_thread()

    _game.game_over()
    thanos(_game)


def custom_game() -> None:
    game(
        base_player_x_pos=BASE_PLAYER_X_POS,
        base_player_y_pos=BASE_PLAYER_Y_POS,
        base_player_speed=BASE_PLAYER_SPEED * speed_slider(CUSTOM_GAME_MENU[2]),
        base_player_size=ps_slider(CUSTOM_GAME_MENU[3]),
        base_player_color=BASE_PLAYER_COLOR,
        base_obstacles=BASE_OBSTACLES,
        base_dif=bd_slider(CUSTOM_GAME_MENU[0]),
        base_dt=BASE_DT,
        base_speed=speed_slider(CUSTOM_GAME_MENU[1]),
        first_tick=FIRST_TICK,
        base_fps=BASE_FPS
    )


def create_game(**options) -> Game:
    """Retourne un objet Game correspondant aux paramètres en entrée

    Returns:
        Game: l'objet Game correspondant aux paramètres en entrée
    """
    # Instanciation de tous les objets
    return Game(
        player=Player(
            x=options["base_player_x_pos"],
            y=options["base_player_y_pos"],
            speed=options["base_player_speed"],
            size=options["base_player_size"],
            color=options["base_player_color"]
        ),
        obstacles=options["base_obstacles"],
        difficulty=options["base_dif"],
        dt=options["base_dt"],
        speed=options["base_speed"],
        score=options["first_tick"],
        fps=options["base_fps"],
    )


def game_setup(**options) -> Game:
    """Effectue les opérations nécessaires à un début de partie classique et valide

    Returns:
        Game: Un objet jeu correspondant aux options si elles sont précisées, sinon les options par défaut
    """
    if len(options) == 0:
        game = create_game(**DEFAULT_OPTIONS)
    else:
        game = create_game(**options)

    dif = [0, 0]
    dif.extend(range(game.difficulty))
    for elt in dif:
        game.obstacles.append(new_obstacle(elt + 1))

    return game


# UTILITAIRE
def print_layout(layout: list) -> None:
    """Affichage de l'écran de boutons donné en argument. C'est un affichage seulement, pas de comportement.

    Args:
        layout (list): Ecran de boutons à afficher
    """
    refresh()
    for elt in layout:
        if isinstance(elt, GraphicalNode):
            elt.draw()


def layout_behaviour(layout: list) -> None:
    """Comportement de l'écran de boutons donné en argument

    Args:
        layout (list): Ecran de boutons à "faire fonctionner"
    """
    global _cursor, _index
    print_layout(layout)

    while not keydown(KEY_OK):
        if keydown(KEY_UP) and (layout[_cursor]._up is not None):
            _cursor = layout[_cursor]._up
            print_layout(layout)
            wait_key_basic(KEY_UP)
        if keydown(KEY_DOWN) and (layout[_cursor]._down is not None):
            _cursor = layout[_cursor]._down
            print_layout(layout)
            wait_key_basic(KEY_DOWN)
        if keydown(KEY_LEFT) and (layout[_cursor]._left is not None):
            _cursor = layout[_cursor]._left
            print_layout(layout)
            wait_key_basic(KEY_LEFT)
        if keydown(KEY_RIGHT) and (layout[_cursor]._right is not None):
            _cursor = layout[_cursor]._right
            print_layout(layout)
            wait_key_basic(KEY_RIGHT)

    if layout[_cursor].press():
        _index = layout[_cursor].target
        _cursor = 0
    while keydown(KEY_OK):
        pass


def bd_slider(slider: Slider) -> int:
    return slider.state + 1


def speed_slider(slider: Slider) -> float:
    return (slider.state + 2) / 6.0


def ps_slider(slider: Slider) -> int:
    return (slider.state + 1) * 2


def bd_slider_preview(slider: Slider) -> str:
    return str(bd_slider(slider))


def speed_slider_preview(slider: Slider) -> str:
    return ('x' + str(speed_slider(slider)))[:5]


def ps_slider_preview(slider: Slider) -> str:
    return str(ps_slider(slider)) + 'px'


def print_generic_square(obj: Obstacle | Player) -> None:
    """Affiche l'élément (obstacle ou joueur) en argument

    Args:
        obj (Obstacle | Player): Element à afficher
    """
    k.fill_rect(
        int(obj.x), int(obj.y), int(
            obj.size
        ), int(obj.size), obj.color
    )


def move_generic(obj: Player | Obstacle, direction: int | float, dt: float, global_speed: float) -> None:
    """Déplace l'élement en argument (obstacle ou joueur) selon sa vitesse et la direction donnée en argument

    Args:
        obj (Player | Obstacle): Elément à déplacer
        direction (int | float): Direction dans laquelle déplacer l'objet
    """
    obj.x += cos(rad(direction)) * obj.speed * dt * global_speed * OBJECT_SPEED_MULTIPLIER
    obj.y += sin(rad(direction)) * obj.speed * dt * global_speed * OBJECT_SPEED_MULTIPLIER


def wait_key(key: int) -> None:
    """Attendre l'appui et le relâchement d'une touche en particulier (relâchée au préalable)

    Args:
        key (int): Touche (numworks) à détecter
    """
    while keydown(key):
        pass
    while not keydown(key):
        pass


def wait_key_basic(key: int) -> None:
    """Attendre l'appui d'une touche en particulier (relâchée au préalable)

    Args:
        key (int): Touche (numworks) à détecter
    """
    while keydown(key):
        pass


def refresh() -> None:
    """
    Efface l'écran (remplit tout par du blanc)
    """
    k.fill_rect(0, 0, 320, 240, "white")


def limite_plancher(nombre: int, limite: int = 0) -> int:
    """Prévient une valeur trop petite (contrôle de valeur)

    Args:
        nombre (int): Valeur à contrôler
        limite (int, optional): Limite à appliquer. Defaults to 0.

    Returns:
        int: Entier >= à la limite
    """
    if nombre < limite:
        return limite
    return nombre


def limite_plafond(nombre: int, limite: int) -> int:
    """Prévient une valeur trop grande (contrôle de valeur)

    Args:
        nombre (int): Valeur à contrôler
        limite (int): Limite à appliquer

    Returns:
        int: Entier <= à la limite
    """
    if nombre > limite:
        return limite
    return nombre


def rad(ang: int | float) -> float:
    """Retourne l'équivalent en radians de l'angle en argument

    Args:
        ang (int | float): Angle en degrés à convertir

    Returns:
        float: Angle converti en radians
    """
    return (ang * pi) / 180


def deg(ang: int | float) -> float:
    """Retourne l'équivalent en degrés de l'angle en argument

    Args:
        ang (int | float): Angle en radians à convertir

    Returns:
        float: Angle converti en degrés
    """
    return (ang * 180) / pi


def oppose_lat(ang: int | float) -> int | float:
    """Retourne l'opposé latéral de l'angle en argument

    Args:
        ang (int | float): Angle à inverser

    Returns:
        int | float: Angle inversé latéralement (axe vertical)
    """
    if ang < 0:
        return -ang - 180
    else:
        return 180 - ang


def new_obstacle(dif: int) -> Obstacle:
    """Retourne un nouvel obstacle en fonction de la difficulté spécifiée en argument

    Args:
        dif (int): Difficulté de l'obstacle

    Returns:
        Obstacle: Obstacle correspondant à la difficulté
    """
    if dif >= 20:
        temp_size = randint(1, 40)
    else:
        temp_size = randint(21 - dif, 19 + dif)
    return Obstacle(
        float(randint(0, 320 - temp_size)),
        0.0,
        randint(1, 179),
        0.2 + (40 / temp_size),
        temp_size,
        (222, int(126.5 + 15 * (temp_size - 20)), 31)
    )


def thanos(object: list | Game) -> None:
    """L'une des plus grosses énigmes ici c'est comment ça se fait que la variable _game (ou plus généralement la
    variable qui contient l'objet Game) semble référencer toujours le même objet (même en l'assignant à autre chose,
    rien à faire). C'est à cause de ce comportement que je suis semble-t-il obligé de faire cette procédure affreuse
    qui prend beaucoup trop de place dans le stockage de la calculatrice (sachant que chaque caractère compte).
    Pourtant le garbage collector est supposé jouer son rôle, mais non. Ça me les casse :/

    Args:
        object (list | Game): L'élément à supprimer
    """
    if type(object) == list:
        while len(object) > 0:
            del object[0]
    else:
        del object.player.x
        del object.player.y
        del object.player.speed
        del object.player.size
        del object.player
        thanos(object.obstacles)
        del object.obstacles
        del object.difficulty
        del object.base_difficulty
        del object.fps
        del object.dt
        del object.score
        del object


# MENUS
MAIN_MENU = [
    Button(
        DEFAULT_BUTTON_CENTER, 80,
        DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Jouer", game,
        0, _down=1
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 125,
        DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Partie personnalisée", 1,
        1, _up=0, _down=2
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 170,
        round(DEFAULT_BUTTON_WIDTH / 2 - 5), DEFAULT_BUTTON_HEIGHT,
        "Quitter", stop,
        2, _right=3, _up=1
    ),
    Button(
        round(SCREEN_WIDTH / 2 + 5), 170,
        round(DEFAULT_BUTTON_WIDTH / 2 - 5), DEFAULT_BUTTON_HEIGHT,
        "Infos", 2,
        3, 2, _up=1
    ),
    Label(120, 30, 320, "SLOUBI 2")
]

CUSTOM_GAME_MENU = [
    # Slider difficulté de base
    Slider(
        round(SCREEN_WIDTH / 2) + 4, 20, 100,
        10, 0,
        0, _down=1
    ),

    # Slider vitesse du jeu
    Slider(
        round(SCREEN_WIDTH / 2) + 4, 60, 100,
        11, 4,
        1, _up=0, _down=2
    ),

    # Slider vitesse du joueur
    Slider(
        round(SCREEN_WIDTH / 2) + 4, 100, 100,
        11, 4,
        2, _up=1, _down=3
    ),

    # Slider taille du joueur
    Slider(
        round(SCREEN_WIDTH / 2) + 4, 140, 100,
        15, 4,
        3, _up=2, _down=5
    ),

    Button(
        4, SCREEN_HEIGHT - DEFAULT_BUTTON_HEIGHT - 4, 70, DEFAULT_BUTTON_HEIGHT,
        "Retour", 0,
        4, _up=3, _right=5
    ),
    Button(
        245, SCREEN_HEIGHT - DEFAULT_BUTTON_HEIGHT - 4, 70, DEFAULT_BUTTON_HEIGHT,
        "Jouer", custom_game,
        5, _up=3, _left=4
    ),

    Label(
        0, 10, SCREEN_WIDTH,
        "Diff. de base :"
    ),
    Label(
        0, 50, SCREEN_WIDTH,
        "Vit. du jeu :"
    ),
    Label(
        0, 90, SCREEN_WIDTH,
        "Vit. du joueur :"
    ),
    Label(
        0, 130, SCREEN_WIDTH,
        "Taille joueur :"
    )
]

CUSTOM_GAME_MENU.extend(
    [
        Label(
            round(SCREEN_WIDTH / 2) + 108, 10, 50,
            bd_slider_preview, CUSTOM_GAME_MENU[0]
        ),
        Label(
            round(SCREEN_WIDTH / 2) + 108, 50, 50,
            speed_slider_preview, CUSTOM_GAME_MENU[1]
        ),
        Label(
            round(SCREEN_WIDTH / 2) + 108, 90, 50,
            speed_slider_preview, CUSTOM_GAME_MENU[2]
        ),
        Label(
            round(SCREEN_WIDTH / 2) + 108, 130, 50,
            ps_slider_preview, CUSTOM_GAME_MENU[3]
        )
    ]
)

INFO_MENU = [
    Button(
        DEFAULT_BUTTON_CENTER, 48, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Comment jouer", 3,
        0, _down=1
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 93, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Crédits", 4,
        1, _up=0, _down=2
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 138, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Retour", 0,
        2, _up=1
    )
]

HOW_TO_PLAY = [
    Button(
        4, SCREEN_HEIGHT - DEFAULT_BUTTON_HEIGHT - 4, 70, DEFAULT_BUTTON_HEIGHT,
        "Retour", 2,
        0
    ),
    Label(
        4, 4, 312,
        "Vous dirigez un petit carré. Le but est d'éviter les autres carrés (oranges, rouges et jaunes) qui bougent "
        "sur l'écran. Les seules commandes sont les flèches directionnelles avec lesquelles vous déplacez le carré."
    )
]

CREDITS = [
    Button(
        4, SCREEN_HEIGHT - DEFAULT_BUTTON_HEIGHT - 4, 70, DEFAULT_BUTTON_HEIGHT,
        "Retour", 2,
        0
    ),
    Label(
        4, 4, 312,
        "Jeu créé par Eddy F. Inspiré à l'origine par la documentation de Godot"
    ),
    Label(
        4, 76, 312,
        "Merci à Lucas P. pour l'idée d'avoir des carrés de taille et vitesse différentes"
    )
]

MENUS = [
    MAIN_MENU,
    CUSTOM_GAME_MENU,
    INFO_MENU,
    HOW_TO_PLAY,
    CREDITS
]

main()
