import gc
from math import cos, sin, asin, acos, pi
from random import randint
from time import sleep
from threading import Thread

from ion import *
# from kandinsky import *
import kandinsky as k

### CONSTANTES
# Pour modifier les options par défaut en partie rapide, modifier ces constantes :
BASE_PLAYER_X_POS = 160.0
BASE_PLAYER_Y_POS = 120.0
BASE_PLAYER_SPEED = 2.0
BASE_PLAYER_SIZE = 10
BASE_PLAYER_COLOR = "blue"
BASE_OBSTACLES = []
BASE_DIFFICULTY = 1
FIRST_TICK = 0
BASE_FPS = 60.0
BASE_DT = 1 / BASE_FPS

DEFAULT_OPTIONS = {"base_player_x_pos": BASE_PLAYER_X_POS,
                   "base_player_y_pos": BASE_PLAYER_Y_POS,
                   "base_player_speed": BASE_PLAYER_SPEED,
                   "base_player_size": BASE_PLAYER_SIZE,
                   "base_player_color": BASE_PLAYER_COLOR,
                   "base_obstacles": BASE_OBSTACLES,
                   "base_dif": BASE_DIFFICULTY,
                   "base_dt": BASE_DT,
                   "first_tick": FIRST_TICK,
                   "base_fps": BASE_FPS}

SCREEN_WIDTH = 320
SCREEN_LENGTH = 222

DEFAULT_BUTTON_WIDTH = 220
DEFAULT_BUTTON_LENGTH = 36
DEFAULT_BUTTON_CENTER = round((SCREEN_WIDTH - DEFAULT_BUTTON_WIDTH) / 2)
BORDER_THICKNESS = 2

OBJECT_SPEED_MULTIPLIER = 50.0

### VARIABLES GLOBALES CRITIQUES
global _running, _game, _cursor, _index, _collision
_game = None
_running = None
_cursor = None
_index = None
_collision = None

### CLASSES
# MENUS
class Label:
    """
    Texte simple qui peut être affiché sur l'écran
    """

    def __init__(self, x: int, y: int, length: int, content: str, color: str | tuple = "black", background: str | tuple = "white") -> None:
        self.x = x
        self.y = y
        self.length = length
        self.content = content
        self.color = color
        self.background = background

    def print_label(self) -> None:
        buffer = self.content
        y = self.y
        while len(buffer) * 10 > self.length:
            index = round(self.length / 10)
            while buffer[index] != " ":
                index -= 1
            k.draw_string(buffer[0:index], self.x, y,
                          self.color, self.background)
            buffer = buffer[index + 1:]
            y += 18
        k.draw_string(buffer, self.x, y, self.color, self.background)


class Button:
    """
    Bouton simple accessible par la navigation
    """

    def __init__(self, x: int, y: int, width: int, length: int, label: str, target, _index, _left: int = None, _right: int = None, _up: int = None, _down: int = None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.label = label
        self.target = target
        self._index = _index
        self._left = _left
        self._right = _right
        self._up = _up
        self._down = _down

    def print_button(self) -> None:
        """
        Afficher le bouton sur l'écran
        """
        if _cursor == self._index:
            k.fill_rect(
                self.x - BORDER_THICKNESS,
                self.y - BORDER_THICKNESS,
                self.width + 2 * BORDER_THICKNESS,
                self.length + 2 * BORDER_THICKNESS,
                (29, 98, 181)
            )

        color = "gray"
        if type(self.target) == bool:
            if self.target:
                color = (29, 181, 103)

        k.fill_rect(
            self.x,
            self.y,
            self.width,
            self.length,
            color
        )
        k.draw_string(
            self.label,
            round(self.x + 0.5 * self.width - 5 * len(self.label)),
            round(self.y + 0.5 * self.length - 9),
            "white",
            "gray"
        )

    def press_button(self) -> bool:
        """Appuyer sur le bouton

        Returns:
            bool: True si le bouton renvoie vers un autre menu (int), False sinon
        """
        if type(self.target) == int:
            return True
        elif type(self.target) == bool:
            self.target = not self.target
        else:
            self.target()
        return False


class Slider:
    """
    Barre de défilement accessible par la navigation (utilisée pour choisir la difficulté par exemple)
    """

    def __init__(self, x: int, y: int, length: int, size: int, state: int, _index, _left: int = None, _right: int = None, _up: int = None, _down: int = None) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.size = size
        self.state = state
        self._index = _index
        self._left = _left
        self._right = _right
        self._up = _up
        self._down = _down


# PARTIE
class Player:
    """
    Classe réprésentant le joueur (carré)
    """

    def __init__(self, x: float, y: float, speed: float, size: int, color: tuple) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color

    def edge_bounce_player(self) -> None:
        """
        S'assure que le joueur ne puisse pas sortir des limites de l'écran
        """
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
    Chaque objet de cette classe est un ennemi (= carré rouge)
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

    def __init__(self, player: Player, obstacles: list, difficulty: int, fps: int | float, dt: float, score: int) -> None:
        # fps = rendus par secondes du thread graphique
        # dt = facteur de vitesse du jeu (moteur)
        self.player = player
        self.obstacles = obstacles
        self.difficulty = difficulty
        self.base_difficulty = difficulty
        self.fps = fps
        self.dt = dt
        self.score = score

    def move_game(self) -> None:
        """
        Déplacer tous les objets contenus dans cette partie (obstacles et joueur)
        """
        # On commence par déplacer tous les obstacles
        for obstacle in self.obstacles:
            move_generic(obstacle, obstacle.direction, self.dt)

        # Puis on déplace le joueur selon les touches sur lesquelles il appuie
        # Petite astuce pour gagner du temps, merci griffpatch :)
        key_x = int(keydown(KEY_RIGHT)) - int(keydown(KEY_LEFT))
        key_y = int(keydown(KEY_DOWN)) - int(keydown(KEY_UP))  # Idem
        if not (key_x == 0 and key_y == 0):
            if key_x == 0:
                move_generic(self.player, deg(asin(key_y)), self.dt)
            elif key_y == 0:
                move_generic(self.player, deg(acos(key_x)), self.dt)
            elif key_y == 1:
                move_generic(
                    self.player, (deg(asin(key_y)) + deg(acos(key_x))) / 2, self.dt)
            else:
                move_generic(
                    self.player, (deg(asin(key_y)) - deg(acos(key_x))) / 2, self.dt)
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
        Appelle edge_bounce_obstacle pour chaque obstacle du jeu
        """
        for obstacle in self.obstacles:
            obstacle.edge_bounce_obstacle()

    def is_colliding(self) -> bool:
        """Détermine si le joueur touche un obstacle

        Returns:
            bool: True si le joueur se superpose avec un obstacle
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
        self.score += self.dt * 10  # Plus dt est grand, plus le laps de temps est grand et par conséquent plus le score doit augmenter
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
        k.draw_string("Difficulté initiale : " +
                      str(self.base_difficulty), 45, 110)
        wait_key(KEY_OK)


### FONCTIONS & PROCÉDURES
# CONTAINER
def main() -> None:
    gc.enable()
    global _cursor, _running, _index, _collision
    _running = True
    _cursor = 0
    _index = 0
    _collision = False

    while _running:
        layout_behaviour(MENUS[_index])
        if keydown(37):  # 37 correspond à la touche 5 sur la numworks
            _running = False

    try:
        k.quit()
    except ModuleNotFoundError:
        pass
    except NameError:
        pass
    except AttributeError:
        pass


def engine_thread() -> None:
    global _game, _collision
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
        score=options["first_tick"],
        fps=options["base_fps"]
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
        if type(elt) == Button:
            elt.print_button()
        elif type(elt) == Label:
            elt.print_label()


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
            while keydown(KEY_UP):
                pass
        if keydown(KEY_DOWN) and (layout[_cursor]._down is not None):
            _cursor = layout[_cursor]._down
            print_layout(layout)
            while keydown(KEY_DOWN):
                pass
        if keydown(KEY_LEFT) and (layout[_cursor]._left is not None):
            _cursor = layout[_cursor]._left
            print_layout(layout)
            while keydown(KEY_LEFT):
                pass
        if keydown(KEY_RIGHT) and (layout[_cursor]._right is not None):
            _cursor = layout[_cursor]._right
            print_layout(layout)
            while keydown(KEY_RIGHT):
                pass

    if layout[_cursor].press_button():
        _index = layout[_cursor].target
        _cursor = 0
    while keydown(KEY_OK):
        pass


def print_generic_square(obj: Obstacle | Player) -> None:
    """Affiche l'élément (obstacle ou joueur) en argument

    Args:
        obj (Obstacle | Player): Element à afficher
    """
    k.fill_rect(int(obj.x), int(obj.y), int(
        obj.size), int(obj.size), obj.color)


def move_generic(obj: Player | Obstacle, direction: int | float, dt: float) -> None:
    """Déplace l'élement en argument (obstacle ou joueur) selon sa vitesse et la direction donnée en argument

    Args:
        obj (Player | Obstacle): Elément à déplacer
        direction (int | float): Direction dans laquelle déplacer l'objet
    """
    obj.x += cos(rad(direction)) * obj.speed * dt * OBJECT_SPEED_MULTIPLIER
    obj.y += sin(rad(direction)) * obj.speed * dt * OBJECT_SPEED_MULTIPLIER


def wait_key(key: int) -> None:
    """Attendre l'appui d'une touche en particulier (relâchée au préalable)

    Args:
        key (int): Touche (numworks) à détecter
    """
    while keydown(key):
        pass
    while not keydown(key):
        pass


def refresh() -> None:
    """
    Efface l'écran (remplit tout par du blanc)
    """
    k.fill_rect(0, 0, 320, 240, "white")


def limite_sol(nombre: int, limite: int = 0) -> int:
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
        dif (int): Difficulté à laquelle se rattacher

    Returns:
        Obstacle: Obstacle correspondant à la difficulté
    """
    if dif >= 20:
        temp_size = randint(1, 40)
    else:
        temp_size = randint(21 - dif, 19 + dif)
    return Obstacle(float(randint(0, 320 - temp_size)),
                    0.0,
                    randint(1, 179),
                    0.2 + (40 / temp_size),
                    temp_size,
                    (222, int(126.5 + 15 * (temp_size - 20)), 31)
                    )


def thanos(object: list | Game) -> None:
    """L'une des plus grosses énigmes ici c'est comment ça se fait que la variable _game (ou plus généralement la variable qui contient l'objet Game) semble référencer toujours le même objet (même en l'assignant à autre chose, rien à faire). C'est à cause de ce comportement que je suis semble-t-il obligé de faire cette procédure affreuse qui prend beaucoup trop de place dans le stockage de la calculatrice (sachant que chaque caractère compte). Pourtant le garbage collector est supposé jouer son rôle, mais non. Ça pète les couilles :/

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


### MENUS
MAIN_MENU = [
    Button(
        DEFAULT_BUTTON_CENTER, 80, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_LENGTH,
        "Jouer", game,
        0, _down=1
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 125, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_LENGTH,
        "Partie personnalisée", 1,
        1, _up=0, _down=2
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 170, round(
            DEFAULT_BUTTON_WIDTH / 2 - 5), DEFAULT_BUTTON_LENGTH,
        "Infos", 2,
        2, _right=3, _up=1
    ),
    Button(
        round(SCREEN_WIDTH / 2 + 5), 170, round(DEFAULT_BUTTON_WIDTH /
                                                2 - 5), DEFAULT_BUTTON_LENGTH,
        "Quitter", stop,
        3, 2, _up=1
    ),
    Label(
        120, 30, 320, "SLOUBI 2", "black", "white"
    )
]

CUSTOM_GAME_MENU = [
    # - Slider difficulté de base
    # - Slider vitesse du jeu
    # - Slider vitesse du joueur
    # - Slider taille du joueur
    Button(
        246, SCREEN_LENGTH - DEFAULT_BUTTON_LENGTH - 4, 70, DEFAULT_BUTTON_LENGTH,
        "Retour", 0,
        0
    )
]

INFO_MENU = [
    Button(
        DEFAULT_BUTTON_CENTER, 48, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_LENGTH,
        "Comment jouer", 3,
        0, _down=1
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 93, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_LENGTH,
        "Crédits", 4,
        1, _up=0, _down=2
    ),
    Button(
        DEFAULT_BUTTON_CENTER, 138, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_LENGTH,
        "Retour", 0,
        2, _up=1
    )
]

HOW_TO_PLAY = [
    Button(
        246, SCREEN_LENGTH - DEFAULT_BUTTON_LENGTH - 4, 70, DEFAULT_BUTTON_LENGTH,
        "Retour", 2,
        0
    ),
    Label(
        4, 4, 312,
        "Vous dirigez un petit carré. Le but est d'éviter les autres carrés (oranges, rouges et jaunes) qui bougent sur l'écran. Les seules commandes sont les flèches directionnelles avec lesquelles vous déplacez le carré."
    )
]

CREDITS = [
    Button(
        246, SCREEN_LENGTH - DEFAULT_BUTTON_LENGTH - 4, 70, DEFAULT_BUTTON_LENGTH,
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
