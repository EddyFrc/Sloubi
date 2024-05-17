#!/bin/env python
_Q='Score : '
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
_Z=int
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
K={_G:A,_H:B,_I:C,_J:D,_K:E,_L:F,_M:G,_N:J,_O:H,_P:I}
L=320
M=222
N=220
O=36
P=round((L-N)/2)
Q=2
R=6
S=20
T=10
U=10
V=5e1
global _r,_g,_c,_i,_l
_g=_A
_r=_A
_c=_A
_i=_A
_l=_A
class W:
	def __init__(self,x,y):self.x=x;self.y=y
class X(W):
	def __init__(self,x,y,a,b=_A,c=_A,d=_A,e=_A):super().__init__(x,y);self.a=a;self.b=b;self.c=c;self.d=d;self.e=e
class Y(W):
	def __init__(self,x,y,f,g,h='black',i=_C):super().__init__(x,y);self.f=f;self.g=g;self.h=h;self.i=i
	def m(self):
		j=self.g;y=self.y
		while len(j)*10>self.f:
			index=round(self.f/10)
			while j[index]!=' ':index-=1
			k.draw_string(j[0:index],self.x,y,self.h,self.i);j=j[index+1:];y+=18
		k.draw_string(j,self.x,y,self.h,self.i)
class Z(X):
	def __init__(self,x,y,a,b,c,d,e,f=_A,g=_A,h=_A,i=_A):super().__init__(x,y,e,f,g,h,i);self.a=a;self.b=b;self.c=c;self.d=d
	def m(self):
		if _c==self.a:k.fill_rect(self.x-Q,self.y-Q,self.a+2*Q,self.b+2*Q,(29,98,181))
		color=_F
		def oi():return type(self.d)==bool
		if oi()and self.d:color=29,181,103
		k.fill_rect(self.x,self.y,self.a,self.b,color);k.draw_string(self.c,round(self.x+.5*self.a-5*len(self.c)),round(self.y+.5*self.b-9),_C,_F)
	def n(self):
		match self.d:
			case _Z():return _D
			case bool():self.d=not self.d
			case _:self.d()
		return _B
class AA(X):
	def __init__(self,x,y,a,j,l,e,f=_A,g=_A,h=_A,i=_A):super().__init__(x,y,e,f,g,h,i);self.a=a;self.j=j;self.l=l
	def m(self):
		k.fill_rect(self.x,self.y-round(T/2),self.a,T,_F)
		if _c==self.a:k.fill_rect(U+self.x+round(self.l*(self.a-2*U)/(self.j-1))-round(R/2)-Q,self.y-Q-round(S/2),R+2*Q,S+2*Q,(29,98,181))
		k.fill_rect(U+self.x+round(self.l*(self.a-2*U)/(self.j-1))-round(R/2),self.y-round(S/2),R,S,(127,127,127))
	def n(self):0
class BA:
	def __init__(self,x,y):self.x=x;self.y=y
class CA(BA):
	def __init__(self,x,y,speed,j,color):super().__init__(x,y);self.speed=speed;self.j=j;self.color=color
	def o(self):
		if self.x+self.j>L:self.x=L-self.j
		if self.x<0:self.x=0
		if self.y+self.j>M:self.y=M-self.j
		if self.y<0:self.y=0
class DA(BA):
	def __init__(self,x,y,direction,speed,j,color):super().__init__(x,y);self.direction=direction;self.speed=speed;self.j=j;self.color=color
	def p(self):
		if self.x+self.j>=L or self.x<=0:
			self.direction=oppose_lat(self.direction)
			if self.x<0:self.x=0
			elif self.x+self.j>L:self.x=L-self.j
		elif self.y+self.j>=M or self.y<=0:
			self.direction=-self.direction
			if self.y<0:self.y=0
			elif self.y+self.j>M:self.y=M-self.j
class EA:
	def __init__(self,player,obstacles,difficulty,fps,dt,score):self.player=player;self.obstacles=obstacles;self.difficulty=difficulty;self.base_difficulty=difficulty;self.fps=fps;self.dt=dt;self.score=score
	def q(self):
		for obstacle in self.obstacles:r(obstacle,obstacle.direction,self.dt)
		key_x=_Z(keydown(KEY_RIGHT))-_Z(keydown(KEY_LEFT));key_y=_Z(keydown(KEY_DOWN))-_Z(keydown(KEY_UP))
		if not(key_x==0 and key_y==0):
			if key_x==0:r(self.player,deg(asin(key_y)),self.dt)
			elif key_y==0:r(self.player,deg(acos(key_x)),self.dt)
			elif key_y==1:r(self.player,(deg(asin(key_y))+deg(acos(key_x)))/2,self.dt)
			else:r(self.player,(deg(asin(key_y))-deg(acos(key_x)))/2,self.dt)
		self.player.o()
	def print_game(self):
		k.draw_string(_Q+str(round(self.score)),0,0)
		for obstacle in self.obstacles:print_generic_square(obstacle)
		print_generic_square(self.player)
	def s(self):
		for obstacle in self.obstacles:obstacle.p()
	def is_colliding(self):
		for obstacle in self.obstacles:
			for coin in[(0,0),(0,1),(1,0),(1,1)]:
				if obstacle.x<=self.player.x+coin[0]*self.player.j<=obstacle.x+obstacle.j and obstacle.y<=self.player.y+coin[1]*self.player.j<=obstacle.y+obstacle.j:return _D
		return _B
	def next(self):
		self.s();self.q();self.score+=self.dt*30
		if self.score/self.difficulty>240:self.difficulty+=1;self.obstacles.append(new_obstacle(self.difficulty+1))
		sleep(self.dt)
	def next_image(self):
		refresh();self.print_game()
		try:k.wait_vblank()
		except ModuleNotFoundError:sleep(1/self.fps)
		except NameError:sleep(1/self.fps)
		except AttributeError:sleep(1/self.fps)
	def game_over(self):refresh();k.draw_string('GAME OVER',112,70);k.draw_string(_Q+str(round(self.score)),105,90);k.draw_string('Difficulté initiale : '+str(self.base_difficulty),45,110);wait_key(KEY_OK)
def main():
	global _c,_r,_i;_r=_D;_c=0;_i=0
	while _r:
		layout_behaviour(KA[_i])
		if keydown(37):_r=_B
	try:k.quit()
	except ModuleNotFoundError:pass
	except NameError:pass
	except AttributeError:pass
def engine_thread():
	global _g,_l;_l=_B
	while not _g.is_colliding():_g.next()
	_l=_D
def graphic_thread():
	global _g,_l
	while not _l:_g.next_image()
def stop():global _r;_r=_B
def game(**kwargs):
	global _g,_l
	if len(kwargs)==0:_g=game_setup()
	else:_g=game_setup(**kwargs)
	processing=Thread(target=engine_thread,name='EngineThread');processing.start();graphic_thread();_g.game_over();thanos(_g)
def create_game(**options):return EA(player=CA(x=options[_G],y=options[_H],speed=options[_I],j=options[_J],color=options[_K]),obstacles=options[_L],difficulty=options[_M],dt=options[_N],score=options[_O],fps=options[_P])
def game_setup(**options):
	if len(options)==0:game=create_game(**K)
	else:game=create_game(**options)
	dif=[0,0];dif.extend(range(game.difficulty))
	for elt in dif:game.obstacles.append(new_obstacle(elt+1))
	return game
def print_layout(layout):
	refresh()
	for elt in layout:
		if isinstance(elt,W):elt.m()
def layout_behaviour(layout):
	global _c,_i;print_layout(layout)
	while not keydown(KEY_OK):
		if keydown(KEY_UP)and layout[_c].h is not _A:
			_c=layout[_c].h;print_layout(layout)
			while keydown(KEY_UP):0
		if keydown(KEY_DOWN)and layout[_c].i is not _A:
			_c=layout[_c].i;print_layout(layout)
			while keydown(KEY_DOWN):0
		if keydown(KEY_LEFT)and layout[_c].f is not _A:
			_c=layout[_c].f;print_layout(layout)
			while keydown(KEY_LEFT):0
		if keydown(KEY_RIGHT)and layout[_c].g is not _A:
			_c=layout[_c].g;print_layout(layout)
			while keydown(KEY_RIGHT):0
	if layout[_c].n():_i=layout[_c].d;_c=0
	while keydown(KEY_OK):0
def print_generic_square(obj):k.fill_rect(_Z(obj.x),_Z(obj.y),_Z(obj.j),_Z(obj.j),obj.color)
def r(obj,direction,dt):obj.x+=cos(rad(direction))*obj.speed*dt*V;obj.y+=sin(rad(direction))*obj.speed*dt*V
def wait_key(key):
	while keydown(key):0
	while not keydown(key):0
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
	return DA(float(randint(0,320-temp_size)),.0,randint(1,179),.2+40/temp_size,temp_size,(222,_Z(126.5+15*(temp_size-20)),31))
def thanos(t):
	if type(t)==list:
		while len(t)>0:del t[0]
	else:del t.player.x;del t.player.y;del t.player.speed;del t.player.j;del t.player;thanos(t.obstacles);del t.obstacles;del t.difficulty;del t.base_difficulty;del t.fps;del t.dt;del t.score;del t
FA=[Z(P,80,N,O,'Jouer',game,0,i=1),Z(P,125,N,O,'Partie personnalisée',1,1,h=0,i=2),Z(P,170,round(N/2-5),O,'Infos',2,2,_right=3,h=1),Z(round(L/2+5),170,round(N/2-5),O,'Quitter',stop,3,2,h=1),Y(120,30,320,'SLOUBI 2','black',_C)]
GA=[AA(20,20,100,4,0,0,i=1),AA(20,60,100,4,1,1,h=0,i=2),AA(20,100,100,4,2,2,h=1,i=3),AA(20,140,100,4,3,3,h=2,i=4),Z(246,M-O-4,70,O,_E,0,4,h=3)]
HA=[Z(P,48,N,O,'Comment jouer',3,0,i=1),Z(P,93,N,O,'Crédits',4,1,h=0,i=2),Z(P,138,N,O,_E,0,2,h=1)]
IA=[Z(246,M-O-4,70,O,_E,2,0),Y(4,4,312,"Vous dirigez un petit carré. Le but est d'éviter les autres carrés (oranges, rouges et jaunes) qui bougent sur l'écran. Les seules commandes sont les flèches directionnelles avec lesquelles vous déplacez le carré.")]
JA=[Z(246,M-O-4,70,O,_E,2,0),Y(4,4,312,"Jeu créé par Eddy F. Inspiré à l'origine par la documentation de Godot"),Y(4,76,312,"Merci à Lucas P. pour l'idée d'avoir des carrés de taille et vitesse différentes")]
KA=[FA,GA,HA,IA,JA]
main()