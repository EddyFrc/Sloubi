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
from math import cos,sin,asin,acos,pi
from random import randint
from time import sleep
from threading import Thread
from ion import*
import kandinsky as k
A=16e1
B=12e1
C=2.
D=10
E=29,98,181
F=[]
G=1
H=0
I=6e1
J=1/I
K=1.
L={_G:A,_H:B,_I:C,_J:D,_K:E,_L:F,_M:G,_N:J,_O:H,_P:I,_Q:K}
M=320
N=222
N=220
O=36
P=round((M-N)/2)
Q=2
R=6
S=20
T=10
U=10
V=5e1
W=29,98,181
X=26,189,12
Y=10
global _running,_game,_cursor,_index,_collision
_game=_A
_running=_A
_cursor=_A
_index=_A
_collision=_A
class AF:
	def __init__(self,x,y):self.x=x;self.y=y
class AH(AF):
	def __init__(self,x,y,_index,_left=_A,_right=_A,_up=_A,_down=_A):super().__init__(x,y);self._index=_index;self._left=_left;self._right=_right;self._up=_up;self._down=_down
class AG(AH):
	def __init__(self,x,y,width,height,label,target,_index,_left=_A,_right=_A,_up=_A,_down=_A):super().__init__(x,y,_index,_left,_right,_up,_down);self.width=width;self.height=height;self.label=label;self.target=target
	def draw(self):
		if _cursor==self._index:k.fill_rect(self.x-Q,self.y-Q,self.width+2*Q,self.height+2*Q,(29,98,181))
		color=_F
		def is_target_bool():return type(self.target)==bool
		if is_target_bool()and self.target:color=29,181,103
		k.fill_rect(self.x,self.y,self.width,self.height,color);k.draw_string(self.label,round(self.x+.5*self.width-5*len(self.label)),round(self.y+.5*self.height-9),_C,_F)
	def press(self):
		match self.target:
			case int():return _D
			case bool():self.target=not self.target
			case _:self.target()
		return _B
class AI(AH):
	def __init__(self,x,y,width,size,state,_index,_left=_A,_right=_A,_up=_A,_down=_A):super().__init__(x,y,_index,_left,_right,_up,_down);self.width=width;self.size=size;self.state=state
	def draw(self,handle_color=W):
		k.fill_rect(self.x,self.y-round(T/2),self.width,T,_F)
		if _cursor==self._index:k.fill_rect(U+self.x+round(self.state*(self.width-2*U)/(self.size-1))-round(R/2)-Q,self.y-Q-round(S/2),R+2*Q,S+2*Q,handle_color)
		k.fill_rect(U+self.x+round(self.state*(self.width-2*U)/(self.size-1))-round(R/2),self.y-round(S/2),R,S,(127,127,127))
	def refresh(self,handle_color):k.fill_rect(self.x,self.y-Q-round(S/2),self.width,S+2*Q,_C);self.draw(handle_color)
	def press(self):
		self.refresh(X)
		while keydown(KEY_OK):0
		while not keydown(KEY_OK):
			if keydown(KEY_LEFT)and self.state>0:self.state-=1;self.refresh(X);j(KEY_LEFT)
			if keydown(KEY_RIGHT)and self.state<self.size-1:self.state+=1;self.refresh(X);j(KEY_RIGHT)
		while keydown(KEY_OK):0
class AJ(AF):
	def __init__(self,x,y,length,content,input=_A,color='black',background=_C):super().__init__(x,y);self.length=length;self.content=content;self.input=input;self.color=color;self.background=background
	def draw(self):
		if type(self.content)==str:buffer=self.content
		else:buffer=self.content(self.input)
		y=self.y
		while len(buffer)*Y>self.length:
			index=round(self.length/Y)
			while buffer[index]!=' ':index-=1
			k.draw_string(buffer[0:index],self.x,y,self.color,self.background);buffer=buffer[index+1:];y+=18
		k.draw_string(buffer,self.x,y,self.color,self.background)
class AK:
	def __init__(self,x,y):self.x=x;self.y=y
class AL(AK):
	def __init__(self,x,y,speed,size,color):super().__init__(x,y);self.speed=speed;self.size=size;self.color=color
	def edge_bounce_player(self):
		if self.x+self.size>M:self.x=M-self.size
		if self.x<0:self.x=0
		if self.y+self.size>N:self.y=N-self.size
		if self.y<0:self.y=0
class AM(AK):
	def __init__(self,x,y,direction,speed,size,color):super().__init__(x,y);self.direction=direction;self.speed=speed;self.size=size;self.color=color
	def edge(self):
		if self.x+self.size>=M or self.x<=0:
			self.direction=q(self.direction)
			if self.x<0:self.x=0
			elif self.x+self.size>M:self.x=M-self.size
		elif self.y+self.size>=N or self.y<=0:
			self.direction=-self.direction
			if self.y<0:self.y=0
			elif self.y+self.size>N:self.y=N-self.size
class AN:
	def __init__(self,player,obstacles,difficulty,fps,dt,speed,score):self.player=player;self.obstacles=obstacles;self.difficulty=difficulty;self.base_difficulty=difficulty;self.fps=fps;self.dt=dt;self.speed=speed;self.score=score
	def move_game(self):
		for obstacle in self.obstacles:h(obstacle,obstacle.direction,self.dt,self.speed)
		key_x=int(keydown(KEY_RIGHT))-int(keydown(KEY_LEFT));key_y=int(keydown(KEY_DOWN))-int(keydown(KEY_UP))
		if not(key_x==0 and key_y==0):
			if key_x==0:h(self.player,p(asin(key_y)),self.dt,self.speed)
			elif key_y==0:h(self.player,p(acos(key_x)),self.dt,self.speed)
			elif key_y==1:h(self.player,(p(asin(key_y))+p(acos(key_x)))/2,self.dt,self.speed)
			else:h(self.player,(p(asin(key_y))-p(acos(key_x)))/2,self.dt,self.speed)
		self.player.edge_bounce_player()
	def print_game(self):
		k.draw_string(_R+str(round(self.score)),0,0)
		for obstacle in self.obstacles:g(obstacle)
		g(self.player)
	def edge_bounce_game(self):
		for obstacle in self.obstacles:obstacle.edge()
	def is_colliding(self):
		for obstacle in self.obstacles:
			for coin in[(0,0),(0,1),(1,0),(1,1)]:
				if obstacle.x<=self.player.x+coin[0]*self.player.size<=obstacle.x+obstacle.size and obstacle.y<=self.player.y+coin[1]*self.player.size<=obstacle.y+obstacle.size:return _D
		return _B
	def next(self):
		self.edge_bounce_game();self.move_game();self.score+=self.dt*30
		if self.score/self.difficulty>240:self.difficulty+=1;self.obstacles.append(r(self.difficulty+1))
		sleep(self.dt)
	def next_image(self):
		l();self.print_game()
		try:k.wait_vblank()
		except ModuleNotFoundError:sleep(1/self.fps)
		except NameError:sleep(1/self.fps)
		except AttributeError:sleep(1/self.fps)
	def game_over(self):l();k.draw_string('GAME OVER',112,70);k.draw_string(_R+str(round(self.score)),105,90);k.draw_string('Difficulté initiale : '+str(self.base_difficulty),45,110);i(KEY_OK)
def main():
	global _cursor,_running,_index;_running=_D;_cursor=0;_index=0
	while _running:
		layout_behaviour(AE[_index])
		if keydown(37):_running=_B
def engine_thread():
	global _game,_collision;_collision=_B
	while not _game.is_colliding():_game.next()
	_collision=_D
def graphic_thread():
	global _game,_collision
	while not _collision:_game.next_image()
def stop():global _running;_running=_B
def game(**kwargs):
	global _game,_collision
	if len(kwargs)==0:_game=game_setup()
	else:_game=game_setup(**kwargs)
	processing=Thread(target=engine_thread,name='EngineThread');processing.start();graphic_thread();_game.game_over();s(_game)
def custom_game():game(base_player_x_pos=A,base_player_y_pos=B,base_player_speed=C*b(Z[2]),base_player_size=c(Z[3]),base_player_color=E,base_obstacles=F,base_dif=a(Z[0]),base_dt=J,base_speed=b(Z[1]),first_tick=H,base_fps=I)
def create_game(**options):return AN(player=AL(x=options[_G],y=options[_H],speed=options[_I],size=options[_J],color=options[_K]),obstacles=options[_L],difficulty=options[_M],dt=options[_N],speed=options[_Q],score=options[_O],fps=options[_P])
def game_setup(**options):
	if len(options)==0:game=create_game(**L)
	else:game=create_game(**options)
	dif=[0,0];dif.extend(range(game.difficulty))
	for elt in dif:game.obstacles.append(r(elt+1))
	return game
def print_layout(layout):
	l()
	for elt in layout:
		if isinstance(elt,AF):elt.draw()
def layout_behaviour(layout):
	global _cursor,_index;print_layout(layout)
	while not keydown(KEY_OK):
		if keydown(KEY_UP)and layout[_cursor]._up is not _A:_cursor=layout[_cursor]._up;print_layout(layout);j(KEY_UP)
		if keydown(KEY_DOWN)and layout[_cursor]._down is not _A:_cursor=layout[_cursor]._down;print_layout(layout);j(KEY_DOWN)
		if keydown(KEY_LEFT)and layout[_cursor]._left is not _A:_cursor=layout[_cursor]._left;print_layout(layout);j(KEY_LEFT)
		if keydown(KEY_RIGHT)and layout[_cursor]._right is not _A:_cursor=layout[_cursor]._right;print_layout(layout);j(KEY_RIGHT)
	if layout[_cursor].press():_index=layout[_cursor].target;_cursor=0
	while keydown(KEY_OK):0
def a(sl):return sl.state+1
def b(sl):return(sl.state+2)/6.
def c(sl):return(sl.state+1)*2
def d(sl):return str(a(sl))
def e(sl):return('x'+str(b(sl)))[:5]
def f(sl):return str(c(sl))+'px'
def g(obj):k.fill_rect(int(obj.x),int(obj.y),int(obj.size),int(obj.size),obj.color)
def h(obj,direction,dt,global_speed):obj.x+=cos(o(direction))*obj.speed*dt*global_speed*V;obj.y+=sin(o(direction))*obj.speed*dt*global_speed*V
def i(key):
	while keydown(key):0
	while not keydown(key):0
def j(key):
	while keydown(key):0
def l():k.fill_rect(0,0,320,240,_C)
def m(a,b=0):
	if a<b:return b
	return a
def n(a,b):
	if a>b:return b
	return a
def o(a):return a*pi/180
def p(a):return a*180/pi
def q(a):
	if a<0:return-a-180
	else:return 180-a
def r(a):
	if a>=20:b=randint(1,40)
	else:b=randint(21-a,19+a)
	return AM(float(randint(0,320-b)),.0,randint(1,179),.2+40/b,b,(222,int(126.5+15*(b-20)),31))
def s(a):
	if type(a)==list:
		while len(a)>0:del a[0]
	else:del a.player.x;del a.player.y;del a.player.speed;del a.player.size;del a.player;s(a.obstacles);del a.obstacles;del a.difficulty;del a.base_difficulty;del a.fps;del a.dt;del a.score;del a
AA=[AG(P,80,N,O,'Jouer',game,0,_down=1),AG(P,125,N,O,'Partie personnalisée',1,1,_up=0,_down=2),AG(P,170,round(N/2-5),O,'Quitter',stop,2,_right=3,_up=1),AG(round(M/2+5),170,round(N/2-5),O,'Infos',2,3,2,_up=1),AJ(120,30,320,'SLOUBI 2')]
Z=[AI(round(M/2)+4,20,100,10,0,0,_down=1),AI(round(M/2)+4,60,100,11,4,1,_up=0,_down=2),AI(round(M/2)+4,100,100,11,4,2,_up=1,_down=3),AI(round(M/2)+4,140,100,15,4,3,_up=2,_down=5),AG(4,N-O-4,70,O,_E,0,4,_up=3,_right=5),AG(245,N-O-4,70,O,'Jouer',custom_game,5,_up=3,_left=4),AJ(0,10,M,'Diff. de base :'),AJ(0,50,M,'Vit. du jeu :'),AJ(0,90,M,'Vit. du joueur :'),AJ(0,130,M,'Taille joueur :')]
Z.extend([AJ(round(M/2)+108,10,50,d,Z[0]),AJ(round(M/2)+108,50,50,e,Z[1]),AJ(round(M/2)+108,90,50,e,Z[2]),AJ(round(M/2)+108,130,50,f,Z[3])])
AC=[AG(P,48,N,O,'Comment jouer',3,0,_down=1),AG(P,93,N,O,'Crédits',4,1,_up=0,_down=2),AG(P,138,N,O,_E,0,2,_up=1)]
AB=[AG(4,N-O-4,70,O,_E,2,0),AJ(4,4,312,"Vous dirigez un petit carré. Le but est d'éviter les autres carrés (oranges, rouges et jaunes) qui bougent sur l'écran. Les seules commandes sont les flèches directionnelles avec lesquelles vous déplacez le carré.")]
AD=[AG(4,N-O-4,70,O,_E,2,0),AJ(4,4,312,"Jeu créé par Eddy F. Inspiré à l'origine par la documentation de Godot"),AJ(4,76,312,"Merci à Lucas P. pour l'idée d'avoir des carrés de taille et vitesse différentes")]
AE=[AA,Z,AC,AB,AD]
main()