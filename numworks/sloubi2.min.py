# @formatter:off
_R='Score : '
_Q='ak'
_P='aj'
_O='ai'
_N='ah'
_M='ag'
_L='af'
_K='aa'
_J='ab'
_I='ac'
_H='ad'
_G='ae'
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
O=220
P=36
Q=round((M-O)/2)
R=2
S=6
T=20
U=10
V=10
W=15e1
X=29,98,181
Y=26,189,12
Z=10
global b,c,d,e,f
class CA:
	def __init__(self,x,y):self.x=x;self.y=y
class CB(CA):
	def __init__(self,x,y,g,i=_A,j=_A,l=_A,m=_A):super().__init__(x,y);self.g=g;self.i=i;self.j=j;self.l=l;self.m=m
class CC(CB):
	def __init__(self,x,y,n,r,s,o,g,i=_A,j=_A,l=_A,m=_A):super().__init__(x,y,g,i,j,l,m);self.n=n;self.r=r;self.s=s;self.o=o
	def draw(self):
		if d==self.g:k.fill_rect(self.x-R,self.y-R,self.n+2*R,self.r+2*R,(29,98,181))
		v=_F
		def is_target_bool():return type(self.o)==bool
		if is_target_bool()and self.o:v=29,181,103
		k.fill_rect(self.x,self.y,self.n,self.r,v);k.draw_string(self.s,round(self.x+.5*self.n-5*len(self.s)),round(self.y+.5*self.r-9),_C,_F)
	def press(self):
		type_of_target=type(self.o)
		if type_of_target==int:return _D
		elif type_of_target==bool:self.o=not self.o
		else:self.o()
		return _B
class CD(CB):
	def __init__(self,x,y,n,h,q,g,i=_A,j=_A,l=_A,m=_A):super().__init__(x,y,g,i,j,l,m);self.n=n;self.h=h;self.q=q
	def draw(self,handle_color=X):
		k.fill_rect(self.x,self.y-round(U/2),self.n,U,_F)
		if d==self.g:k.fill_rect(V+self.x+round(self.q*(self.n-2*V)/(self.h-1))-round(S/2)-R,self.y-R-round(T/2),S+2*R,T+2*R,handle_color)
		k.fill_rect(V+self.x+round(self.q*(self.n-2*V)/(self.h-1))-round(S/2),self.y-round(T/2),S,T,(127,127,127))
	def t(self,handle_color):k.fill_rect(self.x,self.y-R-round(T/2),self.n,T+2*R,_C);self.draw(handle_color)
	def press(self):
		self.t(Y)
		while keydown(KEY_OK):0
		while not keydown(KEY_OK):
			if keydown(KEY_LEFT)and self.q>0:self.q-=1;self.t(Y);wait_key_basic(KEY_LEFT)
			if keydown(KEY_RIGHT)and self.q<self.h-1:self.q+=1;self.t(Y);wait_key_basic(KEY_RIGHT)
		while keydown(KEY_OK):0
class CE(CA):
	def __init__(self,x,y,length,content,format_source=_A,v='black',background=_C):super().__init__(x,y);self.length=length;self.content=content;self.format_source=format_source;self.v=v;self.background=background
	def draw(self):
		if type(self.content)==str:buffer=self.content
		else:buffer=self.content(self.format_source)
		y=self.y
		while len(buffer)*Z>self.length:
			g=round(self.length/Z)
			while buffer[g]!=' ':g-=1
			k.draw_string(buffer[0:g],self.x,y,self.v,self.background);buffer=buffer[g+1:];y+=18
		k.draw_string(buffer,self.x,y,self.v,self.background)
class CF:
	def __init__(self,x,y):self.x=x;self.y=y
class Player(CF):
	def __init__(self,x,y,p,h,v):super().__init__(x,y);self.p=p;self.h=h;self.v=v
	def edge_bounce_player(self):
		if self.x+self.h>M:self.x=M-self.h
		if self.x<0:self.x=0
		if self.y+self.h>N:self.y=N-self.h
		if self.y<0:self.y=0
class CG(CF):
	def __init__(self,x,y,direction,p,h,v):super().__init__(x,y);self.direction=direction;self.p=p;self.h=h;self.v=v
	def edge(self):
		if self.x+self.h>=M or self.x<=0:
			self.direction=oppose_lat(self.direction)
			if self.x<0:self.x=0
			elif self.x+self.h>M:self.x=M-self.h
		elif self.y+self.h>=N or self.y<=0:
			self.direction=-self.direction
			if self.y<0:self.y=0
			elif self.y+self.h>N:self.y=N-self.h
class CH:
	def __init__(self,w,obstacles,difficulty,fps,dt,p,score):self.w=w;self.obstacles=obstacles;self.difficulty=difficulty;self.agficulty=difficulty;self.fps=fps;self.dt=dt;self.p=p;self.score=score
	def move_game(self):
		for z in self.obstacles:move_generic(z,z.direction,self.dt,self.p)
		key_x=int(keydown(KEY_RIGHT))-int(keydown(KEY_LEFT));key_y=int(keydown(KEY_DOWN))-int(keydown(KEY_UP))
		if not(key_x==0 and key_y==0):
			if key_x==0:move_generic(self.w,deg(asin(key_y)),self.dt,self.p)
			elif key_y==0:move_generic(self.w,deg(acos(key_x)),self.dt,self.p)
			elif key_y==1:move_generic(self.w,(deg(asin(key_y))+deg(acos(key_x)))/2,self.dt,self.p)
			else:move_generic(self.w,(deg(asin(key_y))-deg(acos(key_x)))/2,self.dt,self.p)
		self.w.edge_bounce_player()
	def print_game(self):
		k.draw_string(_R+str(round(self.score)),0,0)
		for z in self.obstacles:print_generic_square(z)
		print_generic_square(self.w)
	def edge_bounce_game(self):
		for z in self.obstacles:z.edge()
	def is_colliding(self):
		for z in self.obstacles:
			for coin in[(0,0),(0,1),(1,0),(1,1)]:
				if z.x<=self.w.x+coin[0]*self.w.h<=z.x+z.h and z.y<=self.w.y+coin[1]*self.w.h<=z.y+z.h:return _D
		return _B
	def next(self):
		self.edge_bounce_game();self.move_game();self.score+=self.dt*30
		if self.score/self.difficulty>240:self.difficulty+=1;self.obstacles.append(new_obstacle(self.difficulty+1))
		sleep(self.dt)
	def next_image(self):
		t();self.print_game()
		sleep(1/self.fps)
	def game_over(self):t();k.draw_string('GAME OVER',112,70);k.draw_string(_R+str(round(self.score)),105,90);k.draw_string('Difficulté initiale : '+str(self.agficulty),45,110);wait_key(KEY_OK)
def main():
	global d,b,c;b=_D;d=0;c=0
	while b:
		layout_behaviour(MZ[c])
		if keydown(37):b=_B
	try:k.quit()
	except Exception:pass
def game_loop():
	global e,f;f=_B
	while not e.is_colliding():e.next();e.next_image()
	f=_D
def stop():global b;b=_B
def game(**kwargs):
	global e,f
	if len(kwargs)==0:e=game_setup()
	else:e=game_setup(**kwargs)
	game_loop();e.game_over();thanos(e)
def custom_game():game(ae=A,ad=B,ac=C*speed_slider(MB[2]),ab=ps_slider(MB[3]),aa=E,af=F,ag=bd_slider(MB[0]),ah=J,ak=speed_slider(MB[1]),ai=H,aj=I)
def create_game(**u):return CH(w=Player(x=u[_G],y=u[_H],p=u[_I],
	h=u[_J],v=u[_K]),obstacles=u[_L],difficulty=u[_M],dt=u[_N],
	p=u[_Q],score=u[_O],fps=u[_P])
def game_setup(**u):
	if len(u)==0:created_game=create_game(**L)
	else:created_game=create_game(**u)
	dif=[0,0];dif.extend(range(created_game.difficulty))
	for elt in dif:created_game.obstacles.append(new_obstacle(elt+1))
	return created_game
def print_layout(layout):
	t()
	for elt in layout:elt.draw()
def layout_behaviour(layout):
	global d,c;print_layout(layout)
	while not keydown(KEY_OK):
		if keydown(KEY_UP)and layout[d].l is not _A:d=layout[d].l;print_layout(layout);wait_key_basic(KEY_UP)
		if keydown(KEY_DOWN)and layout[d].m is not _A:d=layout[d].m;print_layout(layout);wait_key_basic(KEY_DOWN)
		if keydown(KEY_LEFT)and layout[d].i is not _A:d=layout[d].i;print_layout(layout);wait_key_basic(KEY_LEFT)
		if keydown(KEY_RIGHT)and layout[d].j is not _A:d=layout[d].j;print_layout(layout);wait_key_basic(KEY_RIGHT)
	if layout[d].press():c=layout[d].o;d=0
	while keydown(KEY_OK):0
def bd_slider(slider):return slider.q+1
def speed_slider(slider):return(slider.q+2)/6.
def ps_slider(slider):return(slider.q+1)*2
def bd_slider_preview(slider):return str(bd_slider(slider))
def speed_slider_preview(slider):return('x'+str(speed_slider(slider)))[:5]
def ps_slider_preview(slider):return str(ps_slider(slider))+'px'
def print_generic_square(obj):k.fill_rect(int(obj.x),int(obj.y),int(obj.h),int(obj.h),obj.v)
def move_generic(obj,direction,dt,global_speed):obj.x+=cos(rad(direction))*obj.p*dt*global_speed*W;obj.y+=sin(rad(direction))*obj.p*dt*global_speed*W
def wait_key(key):
	while keydown(key):0
	while not keydown(key):0
def wait_key_basic(key):
	while keydown(key):0
def t():k.fill_rect(0,0,320,240,_C)
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
	return CG(float(randint(0,320-temp_size)),.0,randint(1,179),.2+40/temp_size,temp_size,(222,int(126.5+15*(temp_size-20)),31))
def thanos(a):
	if type(a)==list:
		while len(a)>0:del a[0]
	else:del a.w.x;del a.w.y;del a.w.p;del a.w.h;del a.w;thanos(a.obstacles);del a.obstacles;del a.difficulty;del a.agficulty;del a.fps;del a.dt;del a.score;del a
MA=[CC(Q,80,O,P,'Jouer',game,0,m=1),CC(Q,125,O,P,'Partie personnalisée',1,1,l=0,m=2),CC(Q,170,round(O/2-5),P,'Quitter',stop,2,
	j=3,l=1),CC(round(M/2+5),170,round(O/2-5),P,'Infos',2,3,2,l=1),CE(120,30,320,'SLOUBI 2')]
MB=[CD(round(M/2)+4,20,100,10,0,0,m=1),CD(round(M/2)+4,60,100,11,4,1,l=0,m=2),CD(round(M/2)+4,100,100,11,4,2,
	l=1,m=3),CD(round(M/2)+4,140,100,15,4,3,l=2,m=5),CC(4,N-P-4,70,P,_E,0,4,
	l=3,
	j=5),CC(245,N-P-4,70,P,'Jouer',custom_game,5,l=3,
	i=4),CE(0,10,M,'Diff. de base :'),CE(0,50,M,'Vit. du jeu :'),CE(0,90,M,'Vit. du joueur :'),CE(0,130,M,'Taille joueur :')]
MB.extend([CE(round(M/2)+108,10,50,bd_slider_preview,MB[0]),CE(round(M/2)+108,50,50,speed_slider_preview,MB[1]),CE(round(M/2)+108,90,50,speed_slider_preview,MB[2]),CE(round(M/2)+108,130,50,ps_slider_preview,MB[3])])
MC=[CC(Q,48,O,P,'Comment jouer',3,0,m=1),CC(Q,93,O,P,'Crédits',4,1,l=0,m=2),CC(Q,138,O,P,_E,0,2,
	l=1)]
MD=[CC(4,N-P-4,70,P,_E,2,0),CE(4,4,312,"Vous dirigez un petit carré. Le but est d'éviter les autres carrés (oranges, rouges et jaunes) qui bougent sur l'écran. Les seules commandes sont les flèches directionnelles avec lesquelles vous déplacez le carré.")]
ME=[CC(4,N-P-4,70,P,_E,2,0),CE(4,4,312,'Jeu créé par Eddy F. et inspiré par la documentation de Godot'),CE(4,76,312,"Merci à Lucas P. pour l'idée d'avoir des carrés de taille et vitesse différentes")]
MZ=[MA,MB,MC,MD,ME]
main()