#!/bin/env python
WR=round
Wb=int
Wd=None
Wx=super
Wi=str
WA=bool
WJ=type
Wv=len
Wa=True
Wg=False
Wr=tuple
Wk=buffer
WL=float
WB=list
WY=NameError
Wm=AttributeError
WU=Exception
Wy=range
from math import acos,asin,cos,pi,sin
from random import randint
from time import sleep
from typing import Callable,List,Tuple,Union
import kandinsky as k
WI=k.quit
We=k.wait_vblank
Wu=k.draw_string
uG=k.fill_rect
from ion import*
u=160.0
W=120.0
e=2.0
I=10
R=(29,98,181)
b=[]
d=1
x=0
i=60.0
A=1/i
J=1.0
v={"base_player_x_pos":u,"base_player_y_pos":W,"base_player_speed":e,"base_player_size":I,"base_player_color":R,"base_obstacles":b,"base_dif":d,"base_dt":A,"first_tick":x,"base_fps":i,"base_speed":J}
a=320
g=222
r=220
k=36
L=WR((a-r)/2)
B=2
Y=6
m=20
U=10
y=10
n=150.0
S=(29,98,181)
l=(26,189,12)
O=10
global z,X,N,Q,T
class ue:
 def __init__(M,x:Wb,y:Wb)->Wd:
  M.x=x
  M.y=y
class uI(ue):
 def __init__(M,x:Wb,y:Wb,K:Wb,left_node_index:Wb=Wd,right_node_index:Wb=Wd,above_node_index:Wb=Wd,below_node_index:Wb=Wd)->Wd:
  Wx().__init__(x,y)
  M.index=K
  M.left_node_index=left_node_index
  M.right_node_index=right_node_index
  M.above_node_index=above_node_index
  M.below_node_index=below_node_index
class uR(uI):
 def __init__(M,x:Wb,y:Wb,width:Wb,height:Wb,label:Wi,target:Union[Wb,WA,Callable[[],Wd]],K,left_node_index:Wb=Wd,right_node_index:Wb=Wd,above_node_index:Wb=Wd,below_node_index:Wb=Wd)->Wd:
  Wx().__init__(x,y,K,left_node_index,right_node_index,above_node_index,below_node_index)
  M.width=width
  M.height=height
  M.label=label
  M.target=target
 def uv(M)->Wd:
  if N==M.index:
   uG(M.x-B,M.y-B,M.width+2*B,M.height+2*B,(29,98,181))
  D="gray"
  def ua():
   return WJ(M.target)==WA
  if ua()and M.target:
   D=(29,181,103)
  uG(M.x,M.y,M.width,M.height,D)
  Wu(M.label,WR(M.x+0.5*M.width-5*Wv(M.label)),WR(M.y+0.5*M.height-9),"white","gray")
 def ug(M)->WA:
  j=WJ(M.target)
  if j==Wb:
   return Wa
  elif j==WA:
   M.target=not M.target
  else:
   M.target()
  return Wg
class ub(uI):
 def __init__(M,x:Wb,y:Wb,width:Wb,size:Wb,state:Wb,K,left_node_index:Wb=Wd,right_node_index:Wb=Wd,above_node_index:Wb=Wd,below_node_index:Wb=Wd)->Wd:
  Wx().__init__(x,y,K,left_node_index,right_node_index,above_node_index,below_node_index)
  M.width=width
  M.size=size
  M.state=state
 def uv(M,handle_color=S)->Wd:
  uG(M.x,M.y-WR(U/2),M.width,U,"gray")
  if N==M.index:
   uG(y+M.x+WR(M.state*(M.width-2*y)/(M.size-1))-WR(Y/2)-B,M.y-B-WR(m/2),Y+2*B,m+2*B,handle_color)
  uG(y+M.x+WR(M.state*(M.width-2*y)/(M.size-1))-WR(Y/2),M.y-WR(m/2),Y,m,(127,127,127))
 def ur(M,handle_color)->Wd:
  uG(M.x,M.y-B-WR(m/2),M.width,m+2*B,"white")
  M.uv(handle_color)
 def ug(M)->Wd:
  M.ur(l)
  while keydown(KEY_OK):
   pass
  while not keydown(KEY_OK):
   if keydown(KEY_LEFT)and M.state>0:
    M.state-=1
    M.ur(l)
    uq(KEY_LEFT)
   if keydown(KEY_RIGHT)and M.state<M.size-1:
    M.state+=1
    M.ur(l)
    uq(KEY_RIGHT)
  while keydown(KEY_OK):
   pass
class ud(ue):
 def __init__(M,x:Wb,y:Wb,length:Wb,content:Union[Wi,Callable[[ub],Wi]],format_source:ub=Wd,D:Union[Wi,Wr]="black",background:Union[Wi,Wr]="white")->Wd:
  Wx().__init__(x,y)
  M.length=length
  M.content=content
  M.format_source=format_source
  M.color=D
  M.background=background
 def uv(M)->Wd:
  if WJ(M.content)==Wi:
   Wk=M.content
  else:
   Wk=M.content(M.format_source)
  y=M.y
  while Wv(Wk)*O>M.length:
   K=WR(M.length/O)
   while Wk[K]!=" ":
    K-=1
   Wu(Wk[0:K],M.x,y,M.color,M.background)
   Wk=Wk[K+1:]
   y+=18
  Wu(Wk,M.x,y,M.color,M.background)
class ux:
 def __init__(M,x:WL,y:WL)->Wd:
  M.x=x
  M.y=y
class ui(ux):
 def __init__(M,x:WL,y:WL,speed:WL,size:Wb,D:Wr)->Wd:
  Wx().__init__(x,y)
  M.speed=speed
  M.size=size
  M.color=D
 def uk(M)->Wd:
  if M.x+M.size>a:
   M.x=a-M.size
  if M.x<0:
   M.x=0
  if M.y+M.size>g:
   M.y=g-M.size
  if M.y<0:
   M.y=0
class uA(ux):
 def __init__(M,x:WL,y:WL,direction:Union[Wb,WL],speed:WL,size:Wb,D:Tuple[Wb,Wb,Wb])->Wd:
  Wx().__init__(x,y)
  M.direction=direction
  M.speed=speed
  M.size=size
  M.color=D
 def uL(M)->Wd:
  if M.x+M.size>=a or M.x<=0:
   M.direction=uw(M.direction)
   if M.x<0:
    M.x=0
   elif M.x+M.size>a:
    M.x=a-M.size
  elif M.y+M.size>=g or M.y<=0:
   M.direction=-M.direction
   if M.y<0:
    M.y=0
   elif M.y+M.size>g:
    M.y=g-M.size
class uJ:
 def __init__(M,player:ui,obstacles:WB,difficulty:Wb,fps:Union[Wb,WL],dt:WL,speed:WL,score:Wb)->Wd:
  M.player=player
  M.obstacles=obstacles
  M.difficulty=difficulty
  M.base_difficulty=difficulty
  M.fps=fps
  M.dt=dt
  M.speed=speed
  M.score=score
 def uB(M)->Wd:
  for V in M.obstacles:
   uo(V,V.direction,M.dt,M.speed)
  C=Wb(keydown(KEY_RIGHT))-Wb(keydown(KEY_LEFT))
  c=Wb(keydown(KEY_DOWN))-Wb(keydown(KEY_UP))
  if not(C==0 and c==0):
   if C==0:
    uo(M.player,ut(asin(c)),M.dt,M.speed)
   elif c==0:
    uo(M.player,ut(acos(C)),M.dt,M.speed)
   elif c==1:
    uo(M.player,(ut(asin(c))+ut(acos(C)))/2,M.dt,M.speed)
   else:
    uo(M.player,(ut(asin(c))-ut(acos(C)))/2,M.dt,M.speed)
  M.player.uk()
 def uY(M)->Wd:
  Wu("Score : "+Wi(WR(M.score)),0,0)
  for V in M.obstacles:
   uQ(V)
  uQ(M.player)
 def um(M)->Wd:
  for V in M.obstacles:
   V.uL()
 def uU(M)->WA:
  for V in M.obstacles:
   for p in[(0,0),(0,1),(1,0),(1,1)]:
    if V.x<=M.player.x+p[0]*M.player.size<=V.x+V.size and V.y<=M.player.y+p[1]*M.player.size<=V.y+V.size:
     return Wa
  return Wg
 def uy(M)->Wd:
  M.um()
  M.uB()
  M.score+=M.dt*30
  if M.score/M.difficulty>240:
   M.difficulty+=1
   M.obstacles.append(uF(M.difficulty+1))
  f(M.dt)
 def un(M)->Wd:
  ur()
  M.uY()
  try:
   We()
  except ModuleNotFoundError:
   f(1/M.fps)
  except WY:
   f(1/M.fps)
  except Wm:
   f(1/M.fps)
 def uS(M)->Wd:
  ur()
  Wu("GAME OVER",112,70)
  Wu("Score : "+Wi(WR(M.score)),105,90)
  Wu("Difficult� initiale : "+Wi(M.base_difficulty),45,110)
  uh(KEY_OK)
def ul()->Wd:
 global N,z,X
 z=Wa
 N=0
 X=0
 while z:
  uc(uW[X])
  if keydown(37):
   z=Wg
 try:
  WI()
 except WU:
  pass
def uO()->Wd:
 global Q,T
 T=Wg
 while not Q.uU():
  Q.uy()
  Q.un()
 T=Wa
def uM()->Wd:
 global z
 z=Wg
def uD(**kwargs)->Wd:
 global Q,T
 if Wv(kwargs)==0:
  Q=uV()
 else:
  Q=uV(**kwargs)
 uO()
 Q.uS()
 us(Q)
def uj()->Wd:
 uD(base_player_x_pos=u,base_player_y_pos=W,base_player_speed=e*uf(w[2]),base_player_size=uz(w[3]),base_player_color=R,base_obstacles=b,base_dif=up(w[0]),base_dt=A,base_speed=uf(w[1]),first_tick=x,base_fps=i)
def uK(**options)->uJ:
 return uJ(player=ui(x=options["base_player_x_pos"],y=options["base_player_y_pos"],speed=options["base_player_speed"],size=options["base_player_size"],color=options["base_player_color"]),obstacles=options["base_obstacles"],difficulty=options["base_dif"],dt=options["base_dt"],speed=options["base_speed"],score=options["first_tick"],fps=options["base_fps"])
def uV(**options)->uJ:
 if Wv(options)==0:
  h=uK(**v)
 else:
  h=uK(**options)
 q=[0,0]
 q.extend(Wy(h.difficulty))
 for H in q:
  h.obstacles.append(uF(H+1))
 return h
def uC(layout:List[Union[uR,ub,ud]])->Wd:
 ur()
 for H in layout:
  H.uv()
def uc(layout:List[uR])->Wd:
 global N,X
 uC(layout)
 while not keydown(KEY_OK):
  if keydown(KEY_UP)and(layout[N].above_node_index is not Wd):
   N=layout[N].above_node_index
   uC(layout)
   uq(KEY_UP)
  if keydown(KEY_DOWN)and(layout[N].below_node_index is not Wd):
   N=layout[N].below_node_index
   uC(layout)
   uq(KEY_DOWN)
  if keydown(KEY_LEFT)and(layout[N].left_node_index is not Wd):
   N=layout[N].left_node_index
   uC(layout)
   uq(KEY_LEFT)
  if keydown(KEY_RIGHT)and(layout[N].right_node_index is not Wd):
   N=layout[N].right_node_index
   uC(layout)
   uq(KEY_RIGHT)
 if layout[N].press():
  X=layout[N].target
  N=0
 while keydown(KEY_OK):
  pass
def up(slider:ub)->Wb:
 return slider.state+1
def uf(slider:ub)->WL:
 return(slider.state+2)/6.0
def uz(slider:ub)->Wb:
 return(slider.state+1)*2
def uN(slider:ub)->Wi:
 return Wi(up(slider))
def uX(slider:ub)->Wi:
 return('x'+Wi(uf(slider)))[:5]
def uT(slider:ub)->Wi:
 return Wi(uz(slider))+'px'
def uQ(E:Union[uA,ui])->Wd:
 uG(Wb(E.x),Wb(E.y),Wb(E.size),Wb(E.size),E.color)
def uo(E:Union[ui,uA],direction:Union[Wb,WL],dt:WL,global_speed:WL)->Wd:
 E.x+=cos(uP(direction))*E.speed*dt*global_speed*n
 E.y+=sin(uP(direction))*E.speed*dt*global_speed*n
def uh(key:Wb)->Wd:
 while keydown(key):
  pass
 while not keydown(key):
  pass
def uq(key:Wb)->Wd:
 while keydown(key):
  pass
def ur()->Wd:
 uG(0,0,320,240,"white")
def uH(nombre:Wb,limite:Wb=0)->Wb:
 if nombre<limite:
  return limite
 return nombre
def uE(nombre:Wb,limite:Wb)->Wb:
 if nombre>limite:
  return limite
 return nombre
def uP(ang:Union[Wb,WL])->WL:
 return(ang*pi)/180
def ut(ang:Union[Wb,WL])->WL:
 return(ang*180)/pi
def uw(ang:Union[Wb,WL])->Union[Wb,WL]:
 if ang<0:
  return-ang-180
 else:
  return 180-ang
def uF(q:Wb)->uA:
 if q>=20:
  P=randint(1,40)
 else:
  P=randint(21-q,19+q)
 return uA(WL(randint(0,320-P)),0.0,randint(1,179),0.2+(40/P),P,(222,Wb(126.5+15*(P-20)),31))
def us(spider_man:Union[WB,uJ])->Wd:
 if WJ(spider_man)==WB:
  while Wv(spider_man)>0:
   del spider_man[0]
 else:
  del spider_man.player.x
  del spider_man.player.y
  del spider_man.player.speed
  del spider_man.player.size
  del spider_man.player
  us(spider_man.obstacles)
  del spider_man.obstacles
  del spider_man.difficulty
  del spider_man.base_difficulty
  del spider_man.fps
  del spider_man.dt
  del spider_man.score
  del spider_man
t=[uR(L,80,r,k,"Jouer",uD,0,below_node_index=1),uR(L,125,r,k,"Partie personnalis�e",1,1,above_node_index=0,below_node_index=2),uR(L,170,WR(r/2-5),k,"Quitter",uM,2,right_node_index=3,above_node_index=1),uR(WR(a/2+5),170,WR(r/2-5),k,"Infos",2,3,2,above_node_index=1),ud(120,30,320,"SLOUBI 2")]
w=[ub(WR(a/2)+4,20,100,10,0,0,below_node_index=1),ub(WR(a/2)+4,60,100,11,4,1,above_node_index=0,below_node_index=2),ub(WR(a/2)+4,100,100,11,4,2,above_node_index=1,below_node_index=3),ub(WR(a/2)+4,140,100,15,4,3,above_node_index=2,below_node_index=5),uR(4,g-k-4,70,k,"Retour",0,4,above_node_index=3,right_node_index=5),uR(245,g-k-4,70,k,"Jouer",uj,5,above_node_index=3,left_node_index=4),ud(0,10,a,"Diff. de base :"),ud(0,50,a,"Vit. du jeu :"),ud(0,90,a,"Vit. du joueur :"),ud(0,130,a,"Taille joueur :")]
w.extend([ud(WR(a/2)+108,10,50,uN,w[0]),ud(WR(a/2)+108,50,50,uX,w[1]),ud(WR(a/2)+108,90,50,uX,w[2]),ud(WR(a/2)+108,130,50,uT,w[3])])
F=[uR(L,48,r,k,"Comment jouer",3,0,below_node_index=1),uR(L,93,r,k,"Cr�dits",4,1,above_node_index=0,below_node_index=2),uR(L,138,r,k,"Retour",0,2,above_node_index=1)]
s=[uR(4,g-k-4,70,k,"Retour",2,0),ud(4,4,312,'''Vous dirigez un petit carr�. Le but est d'�viter les autres carr�s (oranges, rouges et jaunes) qui bougent sur l'�cran. Les seules commandes sont les fl�ches directionnelles avec lesquelles vous d�placez le carr�.''')]
G=[uR(4,g-k-4,70,k,"Retour",2,0),ud(4,4,312,"Jeu cr�� par Eddy F. et inspir� par la documentation de Godot"),ud(4,76,312,"Merci � Lucas P. pour l'id�e d'avoir des carr�s de taille et vitesse diff�rentes")]
uW=[t,w,F,s,G]
ul()

