#!/bin/env python
od=round
oM=None
og=int
oY=super
oF=str
ou=len
ao=type
ah=bool
aB=True
aP=False
aO=float
am=tuple
aE=list
aq=NameError
ae=AttributeError
aQ=range
al=isinstance
aV=object
from math import cos,sin,asin,acos,pi
from random import randint
from time import sleep
from threading import Thread
from ion import*
import kandinsky as k
oR=k.quit
try:
 oz=k.wait_vblank
except:
 pass
ox=k.fill_rect
oL=k.draw_string
o=160.0
a=120.0
h=2.0
B=10
P=(29,98,181)
O=[]
m=1
E=0
q=60.0
e=1/q
Q={"base_player_x_pos":o,"base_player_y_pos":a,"base_player_speed":h,"base_player_size":B,"base_player_color":P,"base_obstacles":O,"base_dif":m,"base_dt":e,"first_tick":E,"base_fps":q}
l=320
V=222
D=220
f=36
s=od((l-D)/2)
U=2
j=6
r=20
b=10
v=10
k=50.0
global T,J,H,S,W
J=oM
T=oM
H=oM
S=oM
W=oM
class F:
 def __init__(G,x:og,y:og)->oM:
  G.x=x
  G.y=y
class u(F):
 def __init__(G,x:og,y:og,S:og,_left:og=oM,_right:og=oM,_up:og=oM,_down:og=oM)->oM:
  oY().__init__(x,y)
  G._index=S
  G._left=_left
  G._right=_right
  G._up=_up
  G._down=_down
class i(F):
 def __init__(G,x:og,y:og,length:og,content:oF,A:oF|am="black",background:oF|am="white")->oM:
  oY().__init__(x,y)
  G.length=length
  G.content=content
  G.color=A
  G.background=background
 def oE(G)->oM:
  buffer=G.content
  y=G.y
  while ou(buffer)*10>G.length:
   y=od(G.length/10)
   while buffer[y]!=" ":
    y-=1
   oL(buffer[0:y],G.x,y,G.color,G.background)
   buffer=buffer[y+1:]
   y+=18
  oL(buffer,G.x,y,G.color,G.background)
class oa(u):
 def __init__(G,x:og,y:og,width:og,height:og,label:oF,target,S,_left:og=oM,_right:og=oM,_up:og=oM,_down:og=oM)->oM:
  oY().__init__(x,y,S,_left,_right,_up,_down)
  G.width=width
  G.height=height
  G.label=label
  G.target=target
 def oE(G)->oM:
  if H==G._index:
   ox(G.x-U,G.y-U,G.width+2*U,G.height+2*U,(29,98,181))
  A="gray"
  def oq():
   return ao(G.target)==ah
  if oq()and G.target:
   A=(29,181,103)
  ox(G.x,G.y,G.width,G.height,A)
  oL(G.label,od(G.x+0.5*G.width-5*ou(G.label)),od(G.y+0.5*G.height-9),"white","gray")
 def oe(G)->ah:
  match G.target:
   case og():
    return aB
   case ah():
    G.target=not G.target
   case _:
    G.target()
  return aP
class oh(u):
 def __init__(G,x:og,y:og,width:og,size:og,state:og,S,_left:og=oM,_right:og=oM,_up:og=oM,_down:og=oM)->oM:
  oY().__init__(x,y,S,_left,_right,_up,_down)
  G.width=width
  G.size=size
  G.state=state
 def oE(G)->oM:
  ox(G.x,G.y-od(b/2),G.width,b,"gray")
  if H==G._index:
   ox(v+G.x+od(G.state*(G.width-2*v)/(G.size-1))-od(j/2)-U,G.y-U-od(r/2),j+2*U,r+2*U,(29,98,181))
  ox(v+G.x+od(G.state*(G.width-2*v)/(G.size-1))-od(j/2),G.y-od(r/2),j,r,(127,127,127))
 def oe(G)->oM:
  pass
class oB:
 def __init__(G,x:aO,y:aO)->oM:
  G.x=x
  G.y=y
class oP(oB):
 def __init__(G,x:aO,y:aO,speed:aO,size:og,A:am)->oM:
  oY().__init__(x,y)
  G.speed=speed
  G.size=size
  G.color=A
 def oQ(G)->oM:
  if G.x+G.size>l:
   G.x=l-G.size
  if G.x<0:
   G.x=0
  if G.y+G.size>V:
   G.y=V-G.size
  if G.y<0:
   G.y=0
class oO(oB):
 def __init__(G,x:aO,y:aO,direction:og|aO,speed:aO,size:og,A:am)->oM:
  oY().__init__(x,y)
  G.direction=direction
  G.speed=speed
  G.size=size
  G.color=A
 def ol(G)->oM:
  if G.x+G.size>=l or G.x<=0:
   G.direction=oK(G.direction)
   if G.x<0:
    G.x=0
   elif G.x+G.size>l:
    G.x=l-G.size
  elif G.y+G.size>=V or G.y<=0:
   G.direction=-G.direction
   if G.y<0:
    G.y=0
   elif G.y+G.size>V:
    G.y=V-G.size
class om:
 def __init__(G,player:oP,obstacles:aE,difficulty:og,fps:og|aO,dt:aO,score:og)->oM:
  G.player=player
  G.obstacles=obstacles
  G.difficulty=difficulty
  G.base_difficulty=difficulty
  G.fps=fps
  G.dt=dt
  G.score=score
 def oV(G)->oM:
  for p in G.obstacles:
   ot(p,p.direction,G.dt)
  X=og(keydown(KEY_RIGHT))-og(keydown(KEY_LEFT))
  C=og(keydown(KEY_DOWN))-og(keydown(KEY_UP))
  if not(X==0 and C==0):
   if X==0:
    ot(G.player,on(asin(C)),G.dt)
   elif C==0:
    ot(G.player,on(acos(X)),G.dt)
   elif C==1:
    ot(G.player,(on(asin(C))+on(acos(X)))/2,G.dt)
   else:
    ot(G.player,(on(asin(C))-on(acos(X)))/2,G.dt)
  G.player.oQ()
 def oD(G)->oM:
  oL("Score : "+oF(od(G.score)),0,0)
  for p in G.obstacles:
   oA(p)
  oA(G.player)
 def of(G)->oM:
  for p in G.obstacles:
   p.ol()
 def os(G)->ah:
  for p in G.obstacles:
   for c in[(0,0),(0,1),(1,0),(1,1)]:
    if p.x<=G.player.x+c[0]*G.player.size<=p.x+p.size and p.y<=G.player.y+c[1]*G.player.size<=p.y+p.size:
     return aB
  return aP
 def oU(G)->oM:
  G.of()
  G.oV()
  G.score+=G.dt*30
  if G.score/G.difficulty>240:
   G.difficulty+=1
   G.obstacles.append(oN(G.difficulty+1))
  n(G.dt)
 def oj(G)->oM:
  op()
  G.oD()
  try:
   oz()
  except ModuleNotFoundError:
   n(1/G.fps)
  except aq:
   n(1/G.fps)
  except ae:
   n(1/G.fps)
 def ob(G)->oM:
  op()
  oL("GAME OVER",112,70)
  oL("Score : "+oF(od(G.score)),105,90)
  oL("Difficulté initiale : "+oF(G.base_difficulty),45,110)
  ow(KEY_OK)
def ov()->oM:
 global H,T,S
 T=aB
 H=0
 S=0
 while T:
  oy(Y[S])
  if keydown(37):
   T=aP
 try:
  oR()
 except ModuleNotFoundError:
  pass
 except aq:
  pass
 except ae:
  pass
def ok()->oM:
 global J,W
 W=aP
 while not J.os():
  J.oU()
 W=aB
def oJ()->oM:
 global J,W
 while not W:
  J.oj()
def oT()->oM:
 global T
 T=aP
def oH(**kwargs)->oM:
 global J,W
 if ou(kwargs)==0:
  J=oW()
 else:
  J=oW(**kwargs)
 K=Thread(target=ok,name="EngineThread")
 K.start()
 oJ()
 J.ob()
 oI(J)
def oS(**options)->om:
 return om(player=oP(x=options["base_player_x_pos"],y=options["base_player_y_pos"],speed=options["base_player_speed"],size=options["base_player_size"],color=options["base_player_color"]),obstacles=options["base_obstacles"],difficulty=options["base_dif"],dt=options["base_dt"],score=options["first_tick"],fps=options["base_fps"])
def oW(**options)->om:
 if ou(options)==0:
  oH=oS(**Q)
 else:
  oH=oS(**options)
 N=[0,0]
 N.extend(aQ(oH.difficulty))
 for I in N:
  oH.obstacles.append(oN(I+1))
 return oH
def oG(layout:aE)->oM:
 op()
 for I in layout:
  if al(I,F):
   I.oE()
def oy(layout:aE)->oM:
 global H,S
 oG(layout)
 while not keydown(KEY_OK):
  if keydown(KEY_UP)and(layout[H]._up is not oM):
   H=layout[H]._up
   oG(layout)
   while keydown(KEY_UP):
    pass
  if keydown(KEY_DOWN)and(layout[H]._down is not oM):
   H=layout[H]._down
   oG(layout)
   while keydown(KEY_DOWN):
    pass
  if keydown(KEY_LEFT)and(layout[H]._left is not oM):
   H=layout[H]._left
   oG(layout)
   while keydown(KEY_LEFT):
    pass
  if keydown(KEY_RIGHT)and(layout[H]._right is not oM):
   H=layout[H]._right
   oG(layout)
   while keydown(KEY_RIGHT):
    pass
 if layout[H].press():
  S=layout[H].target
  H=0
 while keydown(KEY_OK):
  pass
def oA(L:oO|oP)->oM:
 ox(og(L.x),og(L.y),og(L.size),og(L.size),L.color)
def ot(L:oP|oO,direction:og|aO,dt:aO)->oM:
 L.x+=cos(oc(direction))*L.speed*dt*k
 L.y+=sin(oc(direction))*L.speed*dt*k
def ow(key:og)->oM:
 while keydown(key):
  pass
 while not keydown(key):
  pass
def op()->oM:
 ox(0,0,320,240,"white")
def oX(nombre:og,limite:og=0)->og:
 if nombre<limite:
  return limite
 return nombre
def oC(nombre:og,limite:og)->og:
 if nombre>limite:
  return limite
 return nombre
def oc(ang:og|aO)->aO:
 return(ang*pi)/180
def on(ang:og|aO)->aO:
 return(ang*180)/pi
def oK(ang:og|aO)->og|aO:
 if ang<0:
  return-ang-180
 else:
  return 180-ang
def oN(N:og)->oO:
 if N>=20:
  x=randint(1,40)
 else:
  x=randint(21-N,19+N)
 return oO(aO(randint(0,320-x)),0.0,randint(1,179),0.2+(40/x),x,(222,og(126.5+15*(x-20)),31))
def oI(aV:aE|om)->oM:
 if ao(aV)==aE:
  while ou(aV)>0:
   del aV[0]
 else:
  del aV.player.x
  del aV.player.y
  del aV.player.speed
  del aV.player.size
  del aV.player
  oI(aV.obstacles)
  del aV.obstacles
  del aV.difficulty
  del aV.base_difficulty
  del aV.fps
  del aV.dt
  del aV.score
  del aV
z=[oa(s,80,D,f,"Jouer",oH,0,_down=1),oa(s,125,D,f,"Partie personnalisée",1,1,_up=0,_down=2),oa(s,170,od(D/2-5),f,"Infos",2,2,_right=3,_up=1),oa(od(l/2+5),170,od(D/2-5),f,"Quitter",oT,3,2,_up=1),i(120,30,320,"SLOUBI 2","black","white")]
R=[oh(20,20,100,4,0,0,_down=1),oh(20,60,100,4,1,1,_up=0,_down=2),oh(20,100,100,4,2,2,_up=1,_down=3),oh(20,140,100,4,3,3,_up=2,_down=4),oa(246,V-f-4,70,f,"Retour",0,4,_up=3)]
d=[oa(s,48,D,f,"Comment jouer",3,0,_down=1),oa(s,93,D,f,"Crédits",4,1,_up=0,_down=2),oa(s,138,D,f,"Retour",0,2,_up=1)]
M=[oa(246,V-f-4,70,f,"Retour",2,0),i(4,4,312,"Vous dirigez un petit carré. Le but est d'éviter les autres carrés (oranges, rouges et jaunes) qui bougent sur l'écran. Les seules commandes sont les flèches directionnelles avec lesquelles vous déplacez le carré.")]
g=[oa(246,V-f-4,70,f,"Retour",2,0),i(4,4,312,"Jeu créé par Eddy F. Inspiré à l'origine par la documentation de Godot"),i(4,76,312,"Merci à Lucas P. pour l'idée d'avoir des carrés de taille et vitesse différentes")]
Y=[z,R,d,M,g]
ov()
# Created by pyminifier (https://github.com/dzhuang/pyminifier3)

