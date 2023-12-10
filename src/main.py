import gc
from math import cos, sin, asin, acos, pi
from random import randint
from time import sleep

from ion import *

from kandinsky import *


class Main:
    @staticmethod
    def main(**kwargs) -> None:
        Main.global_container(**kwargs)

    @staticmethod
    def global_container(**kwargs) -> None:
        gc.enable()
        running = True
        while running:
            # Layout.print_layout(Layout.MAIN_MENU)
            # Util.wait_key(4)
            if keydown(37): # 37 correspond à la touche 5 sur la numworks
                running = False
    
    @staticmethod
    def menu() -> None:
        pass
    
    @staticmethod
    def game(**kwargs) -> None:
        """
        Déroulement d'une unique partie
        """
        global _game
        # Instanciation de tous les objets
        _game = Game(
            player=Player(x=kwargs["base_player_x_pos"],
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

        for i in range(2):
            _game.obstacles.append(Util.new_obstacle(1))
        for dif in range(_game.difficulty):
            _game.obstacles.append(Util.new_obstacle(dif + 1))
        # Boucle de jeu principale
        while not _game.is_colliding():
            Main.frame()

        Util.refresh()
        draw_string("GAME OVER", 112, 70)
        draw_string("Score : " + str(_game.tick), 105, 90)
        draw_string("Difficulté initiale : " + str(_game.base_difficulty), 45, 110)
        Util.wait_key(KEY_OK)

        Util.thanos(_game)

    @staticmethod
    def frame() -> None:
        # Déroulement d'une frame :
        _game.edge_bounce_game()  # Rebondir sur les murs
        _game.move_game()  # Déplacer tous les objets
        _game.tick += 1
        if _game.tick % 240 == 0:  # Augmentation de la difficulté
            _game.difficulty += 1
            _game.obstacles.append(Util.new_obstacle(_game.difficulty + 1))
        Util.refresh()  # Rafraîchir l'écran
        _game.print_game()  # Afficher tous les objets
        sleep(_game.tick_delay)

class Button:
    """
    Bouton simple accessible par la navigation
    """
    def __init__(self, x: int, y: int, width: int, length: int, label: str, command=None, sub_layout=None, is_selected: bool=False, is_flag: bool=False, is_active: bool=False, border_thickness: int=2) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.label = label
        self.command = command
        self.sub_layout = sub_layout
        self.is_selected = is_selected
        self.is_flag = is_flag
        self.is_active = is_active
        self.border_thickness = border_thickness

    def print_button(self) -> None:
        """
        Afficher le bouton sur l'écran
        """
        if self.is_selected:
            fill_rect(self.x - self.border_thickness,
                      self.y - self.border_thickness,
                      self.width + 2 * self.border_thickness,
                      self.length + 2 * self.border_thickness,
                      (29, 98, 181))
        if self.is_active:
            color = (29, 181, 103)
        else:
            color = "gray"
        fill_rect(self.x,
                  self.y,
                  self.width,
                  self.length,
                  color)
        draw_string(self.label,
                    round(self.x + 0.5 * self.width - 5 * len(self.label)),
                    round(self.y + 0.5 * self.length - 9),
                    "white",
                    "gray")

class Layout:

    DEFAULT_WIDTH = 160
    DEFAULT_LENGTH = 36

    MAIN_MENU = [
        [
            Button(
                80, 80, DEFAULT_WIDTH, DEFAULT_LENGTH,
                "Jouer",
                is_selected=True
            )
        ],
        [
            Button(
                80, 125, DEFAULT_WIDTH, DEFAULT_LENGTH,
                "Partie rapide"
            )
        ],
        [
            Button(
                80, 170, DEFAULT_WIDTH, DEFAULT_LENGTH,
                "Options"
            )
        ],
    ]

    @staticmethod
    def print_layout(layout: list) -> None:
        """
        Affichage de la grille de boutons donnée en argument. C'est un affichage seulement, pas de comportement
        """
        for ligne in layout:
            for element in ligne:
                element.print_button()

    @staticmethod
    def layout_behaviour() -> None:
        """
        Comportement d'une grille de boutons (= écran)
        """
        pass


class Player:
    """
    Le joueur
    """

    def __init__(self, x, y, speed, size, color) -> None:
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

    def __init__(self, x, y, direction, speed, size, color) -> None:
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
            self.direction = Util.oppose_lat(self.direction)
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

    def __init__(self, player: Player, obstacles: list, difficulty, speed, fps, tick):
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
            Util.move_generic(obstacle, obstacle.direction)

        # Puis on déplace le joueur selon les touches sur lesquelles il appuie
        key_x = int(keydown(KEY_RIGHT)) - int(keydown(KEY_LEFT))  # Petite astuce pour gagner du temps, merci griffpatch :)
        key_y = int(keydown(KEY_DOWN)) - int(keydown(KEY_UP))  # Idem
        if not (key_x == 0 and key_y == 0):
            if key_x == 0:
                Util.move_generic(self.player, Util.deg(asin(key_y)))
            elif key_y == 0:
                Util.move_generic(self.player, Util.deg(acos(key_x)))
            elif key_y == 1:
                Util.move_generic(self.player, (Util.deg(asin(key_y)) + Util.deg(acos(key_x))) / 2)
            else:
                Util.move_generic(self.player, (Util.deg(asin(key_y)) - Util.deg(acos(key_x))) / 2)
        self.player.edge_bounce_player()

    def print_game(self):
        draw_string("Score : " + str(self.tick), 0, 0)
        for obstacle in self.obstacles:
            Util.print_generic_square(obstacle)
        Util.print_generic_square(self.player)

    def edge_bounce_game(self):
        for obstacle in self.obstacles:
            obstacle.edge_bounce_obstacle()

    def is_colliding(self):
        for obstacle in self.obstacles:
            for coin in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if obstacle.x <= self.player.x + coin[0] * self.player.size <= obstacle.x + obstacle.size \
                        and obstacle.y <= self.player.y + coin[1] * self.player.size <= obstacle.y + obstacle.size:
                    return True
        return False


class Util:
    """
    Fonctions et procédures utilitaires
    """

    @staticmethod
    def limite_sol(nombre, limite=0):
        if nombre < limite:
            return limite
        return nombre

    @staticmethod
    def limite_plafond(nombre, limite):
        if nombre > limite:
            return limite
        return nombre

    @staticmethod
    def wait_key(key):
        while keydown(key):
            pass
        while not keydown(key):
            pass

    @staticmethod
    def refresh():
        fill_rect(0, 0, 320, 240, "white")

    @staticmethod
    def rad(ang):
        return (ang * pi) / 180

    @staticmethod
    def deg(ang):
        return (ang * 180) / pi

    @staticmethod
    def new_obstacle(dif):
        if dif >= 1:
            temp_size = randint(21 - dif, 19 + dif)
        else:
            temp_size = randint(1, 40)
        return Obstacle(float(randint(0, 320 - temp_size)), 0.0,
                        randint(1, 179), 0.2 + (20 / temp_size), temp_size,
                        (222, int(126.5 + 15 * (temp_size - 20)), 31)
                        )

    @staticmethod
    def print_generic_square(obj):
        fill_rect(int(obj.x), int(obj.y), int(obj.size), int(obj.size), obj.color)

    @staticmethod
    def move_generic(obj, direction):
        obj.x += cos(Util.rad(direction)) * obj.speed * 3
        obj.y += sin(Util.rad(direction)) * obj.speed * 3

    @staticmethod
    def oppose_lat(ang):
        if ang < 0:
            return -ang - 180
        else:
            return 180 - ang

    @staticmethod
    def thanos(what_to_thanos):  # Pas trouvé un meilleur moyen de faire ça et ça prend trop de place, rip
        if type(what_to_thanos) == list:
            while len(what_to_thanos) > 0:
                del what_to_thanos[0]
        else:
            del what_to_thanos.player.x
            del what_to_thanos.player.y
            del what_to_thanos.player.speed
            del what_to_thanos.player.size
            del what_to_thanos.player
            while len(what_to_thanos.obstacles) > 0:
                del what_to_thanos.obstacles[0]
            del what_to_thanos.obstacles
            del what_to_thanos.difficulty
            del what_to_thanos.base_difficulty
            del what_to_thanos.speed
            del what_to_thanos.fps
            del what_to_thanos.tick
            del what_to_thanos.tick_delay
            del what_to_thanos
        gc.collect()


Main.main(base_player_x_pos=160.0, base_player_y_pos=120.0, 
          base_player_speed=1.0, base_player_size=10.0,
          base_player_color=(0, 0, 0), base_obstacles=[], base_dif=1, base_speed=1.0, first_tick=0, base_fps=40.0)
