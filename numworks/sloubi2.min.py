_R='Score : '
_Q='base_speed'
_P='base_fps'
_O='first_tick'
_N='base_dt'
_M='base_dif'
_L='base_obstacles'
_K='base_player_color'
_J='base_player_size'
_I='base_player_speed'
_H='base_player_y_pos'
_G='base_player_x_pos'
_F='gray'
_E='Retour'
_D=True
_C='white'
_B=False
_A=None
from math import acos,asin,cos,pi,sin
from random import randint
from time import sleep
import kandinsky as k
from ion import*
BASE_PLAYER_X_POS=16e1
BASE_PLAYER_Y_POS=12e1
BASE_PLAYER_SPEED=2.
BASE_PLAYER_SIZE=10
BASE_PLAYER_COLOR=29,98,181
BASE_OBSTACLES=[]
BASE_DIFFICULTY=1
FIRST_TICK=0
BASE_FPS=6e1
BASE_DT=1/BASE_FPS
BASE_SPEED=1.
DEFAULT_OPTIONS={_G:BASE_PLAYER_X_POS,_H:BASE_PLAYER_Y_POS,_I:BASE_PLAYER_SPEED,_J:BASE_PLAYER_SIZE,_K:BASE_PLAYER_COLOR,_L:BASE_OBSTACLES,_M:BASE_DIFFICULTY,_N:BASE_DT,_O:FIRST_TICK,_P:BASE_FPS,_Q:BASE_SPEED}
SCREEN_WIDTH=320
SCREEN_HEIGHT=222
DEFAULT_BUTTON_WIDTH=220
DEFAULT_BUTTON_HEIGHT=36
DEFAULT_BUTTON_CENTER=round((SCREEN_WIDTH-DEFAULT_BUTTON_WIDTH)/2)
BORDER_THICKNESS=2
DEFAULT_SLIDER_HANDLE_WIDTH=6
DEFAULT_SLIDER_HANDLE_HEIGHT=20
DEFAULT_SLIDER_HEIGHT=10
DEFAULT_SLIDER_SIDE_MARGIN=10
OBJECT_SPEED_MULTIPLIER=15e1
COLOR_SELECTED=29,98,181
COLOR_ENABLED=26,189,12
LETTER_WIDTH=10
global is_running,current_screen_index,current_selection_index,global_game,is_collision_detected
class GraphicalNode:
    def __init__(self,x,y):self.x=x;self.y=y
class SelectableNode(GraphicalNode):
    def __init__(self,x,y,index,left_node_index=_A,right_node_index=_A,above_node_index=_A,below_node_index=_A):super().__init__(x,y);self.index=index;self.left_node_index=left_node_index;self.right_node_index=right_node_index;self.above_node_index=above_node_index;self.below_node_index=below_node_index
class Button(SelectableNode):
    def __init__(self,x,y,width,height,label,target,index,left_node_index=_A,right_node_index=_A,above_node_index=_A,below_node_index=_A):super().__init__(x,y,index,left_node_index,right_node_index,above_node_index,below_node_index);self.width=width;self.height=height;self.label=label;self.target=target
    def draw(self):
        if current_selection_index==self.index:k.fill_rect(self.x-BORDER_THICKNESS,self.y-BORDER_THICKNESS,self.width+2*BORDER_THICKNESS,self.height+2*BORDER_THICKNESS,(29,98,181))
        color=_F
        def is_target_bool():return type(self.target)==bool
        if is_target_bool()and self.target:color=29,181,103
        k.fill_rect(self.x,self.y,self.width,self.height,color);k.draw_string(self.label,round(self.x+.5*self.width-5*len(self.label)),round(self.y+.5*self.height-9),_C,_F)
    def press(self):
        type_of_target=type(self.target)
        if type_of_target==int:return _D
        elif type_of_target==bool:self.target=not self.target
        else:self.target()
        return _B
class Slider(SelectableNode):
    def __init__(self,x,y,width,size,state,index,left_node_index=_A,right_node_index=_A,above_node_index=_A,below_node_index=_A):super().__init__(x,y,index,left_node_index,right_node_index,above_node_index,below_node_index);self.width=width;self.size=size;self.state=state
    def draw(self,handle_color=COLOR_SELECTED):
        k.fill_rect(self.x,self.y-round(DEFAULT_SLIDER_HEIGHT/2),self.width,DEFAULT_SLIDER_HEIGHT,_F)
        if current_selection_index==self.index:k.fill_rect(DEFAULT_SLIDER_SIDE_MARGIN+self.x+round(self.state*(self.width-2*DEFAULT_SLIDER_SIDE_MARGIN)/(self.size-1))-round(DEFAULT_SLIDER_HANDLE_WIDTH/2)-BORDER_THICKNESS,self.y-BORDER_THICKNESS-round(DEFAULT_SLIDER_HANDLE_HEIGHT/2),DEFAULT_SLIDER_HANDLE_WIDTH+2*BORDER_THICKNESS,DEFAULT_SLIDER_HANDLE_HEIGHT+2*BORDER_THICKNESS,handle_color)
        k.fill_rect(DEFAULT_SLIDER_SIDE_MARGIN+self.x+round(self.state*(self.width-2*DEFAULT_SLIDER_SIDE_MARGIN)/(self.size-1))-round(DEFAULT_SLIDER_HANDLE_WIDTH/2),self.y-round(DEFAULT_SLIDER_HANDLE_HEIGHT/2),DEFAULT_SLIDER_HANDLE_WIDTH,DEFAULT_SLIDER_HANDLE_HEIGHT,(127,127,127))
    def refresh(self,handle_color):k.fill_rect(self.x,self.y-BORDER_THICKNESS-round(DEFAULT_SLIDER_HANDLE_HEIGHT/2),self.width,DEFAULT_SLIDER_HANDLE_HEIGHT+2*BORDER_THICKNESS,_C);self.draw(handle_color)
    def press(self):
        self.refresh(COLOR_ENABLED)
        while keydown(KEY_OK):0
        while not keydown(KEY_OK):
            if keydown(KEY_LEFT)and self.state>0:self.state-=1;self.refresh(COLOR_ENABLED);wait_key_basic(KEY_LEFT)
            if keydown(KEY_RIGHT)and self.state<self.size-1:self.state+=1;self.refresh(COLOR_ENABLED);wait_key_basic(KEY_RIGHT)
        while keydown(KEY_OK):0
class Label(GraphicalNode):
    def __init__(self,x,y,length,content,format_source=_A,color='black',background=_C):super().__init__(x,y);self.length=length;self.content=content;self.format_source=format_source;self.color=color;self.background=background
    def draw(self):
        if type(self.content)==str:buffer=self.content
        else:buffer=self.content(self.format_source)
        y=self.y
        while len(buffer)*LETTER_WIDTH>self.length:
            index=round(self.length/LETTER_WIDTH)
            while buffer[index]!=' ':index-=1
            k.draw_string(buffer[0:index],self.x,y,self.color,self.background);buffer=buffer[index+1:];y+=18
        k.draw_string(buffer,self.x,y,self.color,self.background)
class GameElement:
    def __init__(self,x,y):self.x=x;self.y=y
class Player(GameElement):
    def __init__(self,x,y,speed,size,color):super().__init__(x,y);self.speed=speed;self.size=size;self.color=color
    def edge_bounce_player(self):
        if self.x+self.size>SCREEN_WIDTH:self.x=SCREEN_WIDTH-self.size
        if self.x<0:self.x=0
        if self.y+self.size>SCREEN_HEIGHT:self.y=SCREEN_HEIGHT-self.size
        if self.y<0:self.y=0
class Obstacle(GameElement):
    def __init__(self,x,y,direction,speed,size,color):super().__init__(x,y);self.direction=direction;self.speed=speed;self.size=size;self.color=color
    def edge(self):
        if self.x+self.size>=SCREEN_WIDTH or self.x<=0:
            self.direction=oppose_lat(self.direction)
            if self.x<0:self.x=0
            elif self.x+self.size>SCREEN_WIDTH:self.x=SCREEN_WIDTH-self.size
        elif self.y+self.size>=SCREEN_HEIGHT or self.y<=0:
            self.direction=-self.direction
            if self.y<0:self.y=0
            elif self.y+self.size>SCREEN_HEIGHT:self.y=SCREEN_HEIGHT-self.size
class Game:
    def __init__(self,player,obstacles,difficulty,fps,dt,speed,score):self.player=player;self.obstacles=obstacles;self.difficulty=difficulty;self.base_difficulty=difficulty;self.fps=fps;self.dt=dt;self.speed=speed;self.score=score
    def move_game(self):
        for obstacle in self.obstacles:move_generic(obstacle,obstacle.direction,self.dt,self.speed)
        key_x=int(keydown(KEY_RIGHT))-int(keydown(KEY_LEFT));key_y=int(keydown(KEY_DOWN))-int(keydown(KEY_UP))
        if not(key_x==0 and key_y==0):
            if key_x==0:move_generic(self.player,deg(asin(key_y)),self.dt,self.speed)
            elif key_y==0:move_generic(self.player,deg(acos(key_x)),self.dt,self.speed)
            elif key_y==1:move_generic(self.player,(deg(asin(key_y))+deg(acos(key_x)))/2,self.dt,self.speed)
            else:move_generic(self.player,(deg(asin(key_y))-deg(acos(key_x)))/2,self.dt,self.speed)
        self.player.edge_bounce_player()
    def print_game(self):
        k.draw_string(_R+str(round(self.score)),0,0)
        for obstacle in self.obstacles:print_generic_square(obstacle)
        print_generic_square(self.player)
    def edge_bounce_game(self):
        for obstacle in self.obstacles:obstacle.edge()
    def is_colliding(self):
        for obstacle in self.obstacles:
            for coin in[(0,0),(0,1),(1,0),(1,1)]:
                if obstacle.x<=self.player.x+coin[0]*self.player.size<=obstacle.x+obstacle.size and obstacle.y<=self.player.y+coin[1]*self.player.size<=obstacle.y+obstacle.size:return _D
        return _B
    def next(self):
        self.edge_bounce_game();self.move_game();self.score+=self.dt*30
        if self.score/self.difficulty>240:self.difficulty+=1;self.obstacles.append(new_obstacle(self.difficulty+1))
        sleep(self.dt)
    def next_image(self):
        refresh();self.print_game()
        try:k.wait_vblank()
        except ModuleNotFoundError:sleep(1/self.fps)
        except NameError:sleep(1/self.fps)
        except AttributeError:sleep(1/self.fps)
    def game_over(self):refresh();k.draw_string('GAME OVER',112,70);k.draw_string(_R+str(round(self.score)),105,90);k.draw_string('Difficulté initiale : '+str(self.base_difficulty),45,110);wait_key(KEY_OK)
def main():
    global current_selection_index,is_running,current_screen_index;is_running=_D;current_selection_index=0;current_screen_index=0
    while is_running:
        layout_behaviour(MENUS[current_screen_index])
        if keydown(37):is_running=_B
    try:k.quit()
    except Exception:pass
def game_loop():
    global global_game,is_collision_detected;is_collision_detected=_B
    while not global_game.is_colliding():global_game.next();global_game.next_image()
    is_collision_detected=_D
def stop():global is_running;is_running=_B
def game(**kwargs):
    global global_game,is_collision_detected
    if len(kwargs)==0:global_game=game_setup()
    else:global_game=game_setup(**kwargs)
    game_loop();global_game.game_over();thanos(global_game)
def custom_game():game(base_player_x_pos=BASE_PLAYER_X_POS,base_player_y_pos=BASE_PLAYER_Y_POS,base_player_speed=BASE_PLAYER_SPEED*speed_slider(CUSTOM_GAME_MENU[2]),base_player_size=ps_slider(CUSTOM_GAME_MENU[3]),base_player_color=BASE_PLAYER_COLOR,base_obstacles=BASE_OBSTACLES,base_dif=bd_slider(CUSTOM_GAME_MENU[0]),base_dt=BASE_DT,base_speed=speed_slider(CUSTOM_GAME_MENU[1]),first_tick=FIRST_TICK,base_fps=BASE_FPS)
def create_game(**options):return Game(player=Player(x=options[_G],y=options[_H],speed=options[_I],size=options[_J],color=options[_K]),obstacles=options[_L],difficulty=options[_M],dt=options[_N],speed=options[_Q],score=options[_O],fps=options[_P])
def game_setup(**options):
    if len(options)==0:created_game=create_game(**DEFAULT_OPTIONS)
    else:created_game=create_game(**options)
    dif=[0,0];dif.extend(range(created_game.difficulty))
    for elt in dif:created_game.obstacles.append(new_obstacle(elt+1))
    return created_game
def print_layout(layout):
    refresh()
    for elt in layout:elt.draw()
def layout_behaviour(layout):
    global current_selection_index,current_screen_index;print_layout(layout)
    while not keydown(KEY_OK):
        if keydown(KEY_UP)and layout[current_selection_index].above_node_index is not _A:current_selection_index=layout[current_selection_index].above_node_index;print_layout(layout);wait_key_basic(KEY_UP)
        if keydown(KEY_DOWN)and layout[current_selection_index].below_node_index is not _A:current_selection_index=layout[current_selection_index].below_node_index;print_layout(layout);wait_key_basic(KEY_DOWN)
        if keydown(KEY_LEFT)and layout[current_selection_index].left_node_index is not _A:current_selection_index=layout[current_selection_index].left_node_index;print_layout(layout);wait_key_basic(KEY_LEFT)
        if keydown(KEY_RIGHT)and layout[current_selection_index].right_node_index is not _A:current_selection_index=layout[current_selection_index].right_node_index;print_layout(layout);wait_key_basic(KEY_RIGHT)
    if layout[current_selection_index].press():current_screen_index=layout[current_selection_index].target;current_selection_index=0
    while keydown(KEY_OK):0
def bd_slider(slider):return slider.state+1
def speed_slider(slider):return(slider.state+2)/6.
def ps_slider(slider):return(slider.state+1)*2
def bd_slider_preview(slider):return str(bd_slider(slider))
def speed_slider_preview(slider):return('x'+str(speed_slider(slider)))[:5]
def ps_slider_preview(slider):return str(ps_slider(slider))+'px'
def print_generic_square(obj):k.fill_rect(int(obj.x),int(obj.y),int(obj.size),int(obj.size),obj.color)
def move_generic(obj,direction,dt,global_speed):obj.x+=cos(rad(direction))*obj.speed*dt*global_speed*OBJECT_SPEED_MULTIPLIER;obj.y+=sin(rad(direction))*obj.speed*dt*global_speed*OBJECT_SPEED_MULTIPLIER
def wait_key(key):
    while keydown(key):0
    while not keydown(key):0
def wait_key_basic(key):
    while keydown(key):0
def refresh():k.fill_rect(0,0,320,240,_C)
def limite_plancher(nombre,limite=0):
    if nombre<limite:return limite
    return nombre
def limite_plafond(nombre,limite):
    if nombre>limite:return limite
    return nombre
def rad(ang):return ang*pi/180
def deg(ang):return ang*180/pi
def oppose_lat(ang):
    if ang<0:return-ang-180
    else:return 180-ang
def new_obstacle(dif):
    if dif>=20:temp_size=randint(1,40)
    else:temp_size=randint(21-dif,19+dif)
    return Obstacle(float(randint(0,320-temp_size)),.0,randint(1,179),.2+40/temp_size,temp_size,(222,int(126.5+15*(temp_size-20)),31))
def thanos(spider_man):
    if type(spider_man)==list:
        while len(spider_man)>0:del spider_man[0]
    else:del spider_man.player.x;del spider_man.player.y;del spider_man.player.speed;del spider_man.player.size;del spider_man.player;thanos(spider_man.obstacles);del spider_man.obstacles;del spider_man.difficulty;del spider_man.base_difficulty;del spider_man.fps;del spider_man.dt;del spider_man.score;del spider_man
MAIN_MENU=[Button(DEFAULT_BUTTON_CENTER,80,DEFAULT_BUTTON_WIDTH,DEFAULT_BUTTON_HEIGHT,'Jouer',game,0,below_node_index=1),Button(DEFAULT_BUTTON_CENTER,125,DEFAULT_BUTTON_WIDTH,DEFAULT_BUTTON_HEIGHT,'Partie personnalisée',1,1,above_node_index=0,below_node_index=2),Button(DEFAULT_BUTTON_CENTER,170,round(DEFAULT_BUTTON_WIDTH/2-5),DEFAULT_BUTTON_HEIGHT,'Quitter',stop,2,right_node_index=3,above_node_index=1),Button(round(SCREEN_WIDTH/2+5),170,round(DEFAULT_BUTTON_WIDTH/2-5),DEFAULT_BUTTON_HEIGHT,'Infos',2,3,2,above_node_index=1),Label(120,30,320,'SLOUBI 2')]
CUSTOM_GAME_MENU=[Slider(round(SCREEN_WIDTH/2)+4,20,100,10,0,0,below_node_index=1),Slider(round(SCREEN_WIDTH/2)+4,60,100,11,4,1,above_node_index=0,below_node_index=2),Slider(round(SCREEN_WIDTH/2)+4,100,100,11,4,2,above_node_index=1,below_node_index=3),Slider(round(SCREEN_WIDTH/2)+4,140,100,15,4,3,above_node_index=2,below_node_index=5),Button(4,SCREEN_HEIGHT-DEFAULT_BUTTON_HEIGHT-4,70,DEFAULT_BUTTON_HEIGHT,_E,0,4,above_node_index=3,right_node_index=5),Button(245,SCREEN_HEIGHT-DEFAULT_BUTTON_HEIGHT-4,70,DEFAULT_BUTTON_HEIGHT,'Jouer',custom_game,5,above_node_index=3,left_node_index=4),Label(0,10,SCREEN_WIDTH,'Diff. de base :'),Label(0,50,SCREEN_WIDTH,'Vit. du jeu :'),Label(0,90,SCREEN_WIDTH,'Vit. du joueur :'),Label(0,130,SCREEN_WIDTH,'Taille joueur :')]
CUSTOM_GAME_MENU.extend([Label(round(SCREEN_WIDTH/2)+108,10,50,bd_slider_preview,CUSTOM_GAME_MENU[0]),Label(round(SCREEN_WIDTH/2)+108,50,50,speed_slider_preview,CUSTOM_GAME_MENU[1]),Label(round(SCREEN_WIDTH/2)+108,90,50,speed_slider_preview,CUSTOM_GAME_MENU[2]),Label(round(SCREEN_WIDTH/2)+108,130,50,ps_slider_preview,CUSTOM_GAME_MENU[3])])
INFO_MENU=[Button(DEFAULT_BUTTON_CENTER,48,DEFAULT_BUTTON_WIDTH,DEFAULT_BUTTON_HEIGHT,'Comment jouer',3,0,below_node_index=1),Button(DEFAULT_BUTTON_CENTER,93,DEFAULT_BUTTON_WIDTH,DEFAULT_BUTTON_HEIGHT,'Crédits',4,1,above_node_index=0,below_node_index=2),Button(DEFAULT_BUTTON_CENTER,138,DEFAULT_BUTTON_WIDTH,DEFAULT_BUTTON_HEIGHT,_E,0,2,above_node_index=1)]
HOW_TO_PLAY=[Button(4,SCREEN_HEIGHT-DEFAULT_BUTTON_HEIGHT-4,70,DEFAULT_BUTTON_HEIGHT,_E,2,0),Label(4,4,312,"Vous dirigez un petit carré. Le but est d'éviter les autres carrés (oranges, rouges et jaunes) qui bougent sur l'écran. Les seules commandes sont les flèches directionnelles avec lesquelles vous déplacez le carré.")]
CREDITS=[Button(4,SCREEN_HEIGHT-DEFAULT_BUTTON_HEIGHT-4,70,DEFAULT_BUTTON_HEIGHT,_E,2,0),Label(4,4,312,'Jeu créé par Eddy F. et inspiré par la documentation de Godot'),Label(4,76,312,"Merci à Lucas P. pour l'idée d'avoir des carrés de taille et vitesse différentes")]
MENUS=[MAIN_MENU,CUSTOM_GAME_MENU,INFO_MENU,HOW_TO_PLAY,CREDITS]
main()