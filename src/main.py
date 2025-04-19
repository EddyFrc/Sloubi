#!/bin/env python

from math import acos, asin, cos, pi, sin
from random import randint
from threading import Thread
from time import sleep
from typing import Callable, List, Tuple, Union

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
global global_game, is_game_running, current_selection_index, current_screen_index, is_collision_detected
global_game = None
is_game_running = None
current_selection_index = None
current_screen_index = None
is_collision_detected = None


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
        self,
        x: int,
        y: int,
        index: int,
        left_node_index: int = None,
        right_node_index: int = None,
        above_node_index: int = None,
        below_node_index: int = None
    ) -> None:
        super().__init__(x, y)
        self.index = index
        self.left_node_index = left_node_index
        self.right_node_index = right_node_index
        self.above_node_index = above_node_index
        self.below_node_index = below_node_index


class Button(SelectableNode):
    """
    Bouton simple accessible par la navigation
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        target: Union[int, bool, Callable[[], None]],
        index,
        left_node_index: int = None,
        right_node_index: int = None,
        above_node_index: int = None,
        below_node_index: int = None
    ) -> None:
        super().__init__(x, y, index, left_node_index, right_node_index, above_node_index, below_node_index)
        self.width = width
        self.height = height
        self.label = label
        self.target = target

    def draw(self) -> None:
        """
        Afficher le bouton sur l'écran
        """
        if current_selection_index == self.index:
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

        type_of_target = type(self.target)

        if type_of_target == int:
            return True
        elif type_of_target == bool:
            self.target = not self.target
        else:
            self.target()

        return False


class Slider(SelectableNode):
    """
    Barre de défilement accessible par la navigation (utilisée pour choisir la difficulté par exemple)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        size: int,
        state: int,
        index,
        left_node_index: int = None,
        right_node_index: int = None,
        above_node_index: int = None,
        below_node_index: int = None
    ) -> None:
        super().__init__(x, y, index, left_node_index, right_node_index, above_node_index, below_node_index)
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
        if current_selection_index == self.index:
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
        self,
        x: int,
        y: int,
        length: int,
        content: Union[str, Callable[[Slider], str]],
        format_source: Slider = None,
        color: Union[str, tuple] = "black",
        background: Union[str, tuple] = "white"
    ) -> None:
        super().__init__(x, y)
        self.length = length
        self.content = content
        self.format_source = format_source
        self.color = color
        self.background = background

    def draw(self) -> None:
        if type(self.content) == str:
            buffer = self.content
        else:
            buffer = self.content(self.format_source)

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

    def __init__(
        self, x: float, y: float, direction: Union[int, float], speed: float, size: int, color: Tuple[int, int, int]
    ) -> None:
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
        self,
        player: Player,
        obstacles: list,
        difficulty: int,
        fps: Union[int, float],
        dt: float,
        speed: float,
        score: int
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
    global current_selection_index, is_game_running, current_screen_index
    is_game_running = True
    current_selection_index = 0
    current_screen_index = 0

    while is_game_running:
        layout_behaviour(MENUS[current_screen_index])
        if keydown(37):  # 37 correspond à la touche 5 sur la numworks
            is_game_running = False

    try:
        k.quit()
    except Exception:
        pass


def engine_thread() -> None:
    global global_game, is_collision_detected
    is_collision_detected = False
    while not global_game.is_colliding():
        global_game.next()
    is_collision_detected = True


def graphic_thread() -> None:
    global global_game, is_collision_detected
    while not is_collision_detected:
        global_game.next_image()


def stop() -> None:
    """
    Définit le flag _running à False
    """
    global is_game_running
    is_game_running = False


# PARTIE
def game(**kwargs) -> None:
    """
    Déroulement d'une unique partie
    """
    global global_game, is_collision_detected

    if len(kwargs) == 0:
        global_game = game_setup()
    else:
        global_game = game_setup(**kwargs)

    # Boucle de jeu principale
    processing = Thread(target=engine_thread, name="EngineThread")
    processing.start()

    graphic_thread()

    global_game.game_over()
    thanos(global_game)


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
        created_game = create_game(**DEFAULT_OPTIONS)
    else:
        created_game = create_game(**options)

    dif = [0, 0]
    dif.extend(range(created_game.difficulty))
    for elt in dif:
        created_game.obstacles.append(new_obstacle(elt + 1))

    return created_game


# UTILITAIRE
def print_layout(layout: List[Union[Button, Slider, Label]]) -> None:
    """Affichage de l'écran de boutons donné en argument. C'est un affichage seulement, pas de comportement.

    Args:
        layout (list): Ecran de boutons à afficher
    """
    refresh()
    for elt in layout:
        elt.draw()


def layout_behaviour(layout: List[Button]) -> None:
    """Comportement de l'écran de boutons donné en argument

    Args:
        layout (list): Ecran de boutons à "faire fonctionner"
    """
    global current_selection_index, current_screen_index
    print_layout(layout)

    while not keydown(KEY_OK):
        if keydown(KEY_UP) and (layout[current_selection_index].above_node_index is not None):
            current_selection_index = layout[current_selection_index].above_node_index
            print_layout(layout)
            wait_key_basic(KEY_UP)
        if keydown(KEY_DOWN) and (layout[current_selection_index].below_node_index is not None):
            current_selection_index = layout[current_selection_index].below_node_index
            print_layout(layout)
            wait_key_basic(KEY_DOWN)
        if keydown(KEY_LEFT) and (layout[current_selection_index].left_node_index is not None):
            current_selection_index = layout[current_selection_index].left_node_index
            print_layout(layout)
            wait_key_basic(KEY_LEFT)
        if keydown(KEY_RIGHT) and (layout[current_selection_index].right_node_index is not None):
            current_selection_index = layout[current_selection_index].right_node_index
            print_layout(layout)
            wait_key_basic(KEY_RIGHT)

    if layout[current_selection_index].press:
        current_screen_index = layout[current_selection_index].target
        current_selection_index = 0
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


def print_generic_square(obj: Union[Obstacle, Player]) -> None:
    """Affiche l'élément (obstacle ou joueur) en argument

    Args:
        obj (Obstacle | Player): Element à afficher
    """
    k.fill_rect(
        int(obj.x), int(obj.y), int(obj.size), int(obj.size), obj.color
    )


def move_generic(obj: Union[Player, Obstacle], direction: Union[int, float], dt: float, global_speed: float) -> None:
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


def rad(ang: Union[int, float]) -> float:
    """Retourne l'équivalent en radians de l'angle en argument

    Args:
        ang (int | float): Angle en degrés à convertir

    Returns:
        float: Angle converti en radians
    """
    return (ang * pi) / 180


def deg(ang: Union[int, float]) -> float:
    """Retourne l'équivalent en degrés de l'angle en argument

    Args:
        ang (int | float): Angle en radians à convertir

    Returns:
        float: Angle converti en degrés
    """
    return (ang * 180) / pi


def oppose_lat(ang: Union[int, float]) -> Union[int, float]:
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


def thanos(spider_man: Union[list, Game]) -> None:
    """L'une des plus grosses énigmes ici c'est comment ça se fait que la variable _game (ou plus généralement la
    variable qui contient l'objet Game) semble référencer toujours le même objet (même en l'assignant à autre chose,
    rien à faire). C'est à cause de ce comportement que je suis semble-t-il obligé de faire cette procédure affreuse
    qui prend beaucoup trop de place dans le stockage de la calculatrice (sachant que chaque caractère compte).
    Pourtant le garbage collector est supposé jouer son rôle, mais non. Ça me les casse :/

    Args:
        spider_man (list | Game): L'élément à supprimer
    """
    if type(spider_man) == list:
        while len(spider_man) > 0:
            del spider_man[0]
    else:
        del spider_man.player.x
        del spider_man.player.y
        del spider_man.player.speed
        del spider_man.player.size
        del spider_man.player
        thanos(spider_man.obstacles)
        del spider_man.obstacles
        del spider_man.difficulty
        del spider_man.base_difficulty
        del spider_man.fps
        del spider_man.dt
        del spider_man.score
        del spider_man


# MENUS
MAIN_MENU = [
    Button(
        DEFAULT_BUTTON_CENTER, 80,
        DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Jouer", game,
        0, below_node_index=1
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 125,
        DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Partie personnalisée", 1,
        1, above_node_index=0, below_node_index=2
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 170,
        round(DEFAULT_BUTTON_WIDTH / 2 - 5), DEFAULT_BUTTON_HEIGHT,
        "Quitter", stop,
        2, right_node_index=3, above_node_index=1
    ),
    Button(
        round(SCREEN_WIDTH / 2 + 5), 170,
        round(DEFAULT_BUTTON_WIDTH / 2 - 5), DEFAULT_BUTTON_HEIGHT,
        "Infos", 2,
        3, 2, above_node_index=1
    ),
    Label(120, 30, 320, "SLOUBI 2")
]

CUSTOM_GAME_MENU = [
    # Slider difficulté de base
    Slider(
        round(SCREEN_WIDTH / 2) + 4, 20, 100,
        10, 0,
        0, below_node_index=1
    ),

    # Slider vitesse du jeu
    Slider(
        round(SCREEN_WIDTH / 2) + 4, 60, 100,
        11, 4,
        1, above_node_index=0, below_node_index=2
    ),

    # Slider vitesse du joueur
    Slider(
        round(SCREEN_WIDTH / 2) + 4, 100, 100,
        11, 4,
        2, above_node_index=1, below_node_index=3
    ),

    # Slider taille du joueur
    Slider(
        round(SCREEN_WIDTH / 2) + 4, 140, 100,
        15, 4,
        3, above_node_index=2, below_node_index=5
    ),

    Button(
        4, SCREEN_HEIGHT - DEFAULT_BUTTON_HEIGHT - 4, 70, DEFAULT_BUTTON_HEIGHT,
        "Retour", 0,
        4, above_node_index=3, right_node_index=5
    ),
    Button(
        245, SCREEN_HEIGHT - DEFAULT_BUTTON_HEIGHT - 4, 70, DEFAULT_BUTTON_HEIGHT,
        "Jouer", custom_game,
        5, above_node_index=3, left_node_index=4
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
        0, below_node_index=1
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 93, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Crédits", 4,
        1, above_node_index=0, below_node_index=2
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 138, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT,
        "Retour", 0,
        2, above_node_index=1
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
