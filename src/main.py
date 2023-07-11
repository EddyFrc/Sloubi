import gc
from math import cos, sin, asin, acos, pi
from random import randint
from time import sleep

from kandinsky import fill_rect, draw_string

from ion import keydown, KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, KEY_OK


class Main:
    @staticmethod
    def game(**kwargs):
        global _game
        # Instanciation de tous les objets
        _game = Game(
            player=Player(x=kwargs["base_player_x_pos"], y=kwargs["base_player_y_pos"],
                          speed=kwargs["base_player_speed"], size=kwargs["base_player_size"],
                          color=kwargs["base_player_color"]),
            obstacles=kwargs["base_obstacles"],
            difficulty=kwargs["base_dif"],
            speed=kwargs["base_speed"],
            tick=kwargs["first_tick"],
            fps=kwargs["base_fps"]
        )
        for i in range(2):
            _game.obstacles.append(Util.return_obstacle(1))
        for dif in range(_game.difficulty):
            _game.obstacles.append(Util.return_obstacle(dif + 1))
        # Boucle de jeu principale
        while not _game.obstacle_player():
            Main.game_loop()
        Util.refresh()
        draw_string("GAME OVER", 112, 70)
        draw_string("Score : " + str(_game.tick), 105, 90)
        draw_string("Difficulté initiale : " + str(_game.base_difficulty), 45, 110)
        Util.wait_key(KEY_OK)

    @staticmethod
    def game_loop():
        # Déroulement d'une frame :
        _game.edge_bounce()  # Rebondir sur les murs
        _game.frame_move()  # Déplacer tous les objets
        Util.refresh()  # Rafraîchir l'écran
        _game.show()  # Afficher tous les objets
        _game.tick += 1
        if _game.tick % 240 == 0:  # Augmentation de la difficulté
            _game.difficulty += 1
            _game.obstacles.append(Util.return_obstacle(_game.difficulty + 1))
        sleep(_game.tick_delay)

    @staticmethod
    def main(**kwargs):
        while True:
            Main.game(**kwargs)
            Util.thanos(_game)


class Game:
    def __init__(self, player, obstacles, difficulty, speed, fps, tick):
        self.player = player
        self.obstacles = obstacles
        self.difficulty = difficulty
        self.base_difficulty = difficulty
        self.speed = speed
        self.fps = fps
        self.tick = tick
        self.tick_delay = 2.0 / (fps * 3.0)

    def frame_move(self):
        for obstacle in self.obstacles:
            Util.frame_move(obstacle, obstacle.direction)
        key_x = int(keydown(KEY_RIGHT)) - int(keydown(KEY_LEFT))
        key_y = int(keydown(KEY_DOWN)) - int(keydown(KEY_UP))
        if not (key_x == 0 and key_y == 0):
            if key_x == 0:
                Util.frame_move(self.player, Util.deg(asin(key_y)))
            elif key_y == 0:
                Util.frame_move(self.player, Util.deg(acos(key_x)))
            elif key_y == 1:
                Util.frame_move(self.player, (Util.deg(asin(key_y)) + Util.deg(acos(key_x))) / 2)
            else:
                Util.frame_move(self.player, (Util.deg(asin(key_y)) - Util.deg(acos(key_x))) / 2)
        self.player.edge()

    def show(self):
        draw_string("Score : " + str(self.tick), 0, 0)
        for obstacle in self.obstacles:
            Util.show(obstacle)
        Util.show(self.player)

    def edge_bounce(self):
        for obstacle in self.obstacles:
            obstacle.edge_bounce()

    def obstacle_player(self):
        for obstacle in self.obstacles:
            for coin in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if obstacle.x <= self.player.x + coin[0] * self.player.size <= obstacle.x + obstacle.size \
                        and obstacle.y <= self.player.y + coin[1] * self.player.size <= obstacle.y + obstacle.size:
                    return True
        return False


class Player:
    def __init__(self, x, y, speed, size, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color

    def edge(self):
        if self.x + self.size > 320:
            self.x = 320 - self.size
        if self.x < 0:
            self.x = 0
        if self.y + 3 * self.size > 240:
            self.y = 240 - 3 * self.size + 2
        if self.y < 0:
            self.y = 0


class Obstacle:
    def __init__(self, x, y, direction, speed, size, color):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.size = size
        self.color = color

    def edge_bounce(self):
        if self.x + self.size >= 320 or self.x <= 0:
            self.direction = Util.oppose_lat(self.direction)
            if self.x < 0:
                self.x = 0
            elif self.x + self.size > 320:
                self.x = 320 - self.size
        elif self.y + 2 * self.size >= 240 or self.y <= 0:
            self.direction = -self.direction
            if self.y < 0:
                self.y = 0
            elif self.y + self.size > 240:
                self.y = 240 - self.size


class Util:
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
    def return_obstacle(dif):
        if dif >= 1:
            temp_size = randint(21 - dif, 19 + dif)
        else:
            temp_size = randint(1, 40)
        return Obstacle(randint(0, 320 - temp_size), 0,
                        randint(1, 179), 0.2 + (20 / temp_size), temp_size,
                        (222, int(126.5 + 15 * (temp_size - 20)), 31)
                        )

    @staticmethod
    def show(obj):
        fill_rect(int(obj.x), int(obj.y), int(obj.size), int(obj.size), obj.color)

    @staticmethod
    def frame_move(obj, direction):
        obj.x += cos(Util.rad(direction)) * obj.speed * 3
        obj.y += sin(Util.rad(direction)) * obj.speed * 3

    @staticmethod
    def oppose_lat(ang):
        if ang < 0:
            return -ang - 180
        else:
            return 180 - ang

    @staticmethod
    def thanos(game):  # Pas trouvé une meilleure façon de faire ça
        del game.player.x
        del game.player.y
        del game.player.speed
        del game.player.size
        del game.player
        for obstacle in game.obstacles:
            del obstacle.x
            del obstacle.y
            del obstacle.direction
            del obstacle.speed
            del obstacle.size
        del game.difficulty
        del game.base_difficulty
        del game.speed
        del game.fps
        del game.tick
        del game.tick_delay
        del game
        gc.collect()


Main.main(base_player_x_pos=160.0, base_player_y_pos=120.0, base_player_speed=1.0, base_player_size=10.0,
          base_player_color=(0, 0, 0), base_obstacles=[], base_dif=1, base_speed=1.0, first_tick=0, base_fps=40.0)
