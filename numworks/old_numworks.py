N='Score : '
M=range
K=str
D=int
from math import cos,sin,asin as H,acos as I,pi
from random import randint as F
from time import sleep
from ion import keydown as E,KEY_RIGHT as O,KEY_LEFT as P,KEY_UP as Q,KEY_DOWN as R,KEY_OK as S
from kandinsky import fill_rect as L,draw_string as G
C=staticmethod
class J:
  @C
  def m(**C):
    while True:J.g(**C);A.thanos(B)
  @C
  def g(**C):
    global B;B=T(p=U(x=C['x'],y=C['y'],s=C['bps'],i=C['bi'],c=C['bc']),o=C['bo'],d=C['d'],s=C['bs'],t=C['f'],f=C['b'])
    for E in M(2):B.o.append(A.return_obstacle(1))
    for D in M(B.d):B.o.append(A.return_obstacle(D+1))
    while not B.op():J.l()
    A.refresh();G('GAME OVER',112,70);G(N+K(B.t),105,90);G('Difficulté initiale : '+K(B.bd),45,110);A.wa(S)
  @C
  def l():
    B.eb();B.fm();B.t+=1
    if B.t%240==0:B.d+=1;B.o.append(A.return_obstacle(B.d+1))
    A.refresh();B.pr();sleep(B.td)
class T:
  def __init__(A,p,o,d,s,f,t):A.p=p;A.o=o;A.d=d;A.bd=d;A.s=s;A.f=f;A.t=t;A.td=2./(f*3.)
  def fm(B):
    for G in B.o:A.frame_move(G,G.d)
    F=D(E(O))-D(E(P));C=D(E(R))-D(E(Q))
    if not(F==0 and C==0):
      if F==0:A.frame_move(B.p,A.deg(H(C)))
      elif C==0:A.frame_move(B.p,A.deg(I(F)))
      elif C==1:A.frame_move(B.p,(A.deg(H(C))+A.deg(I(F)))/2)
      else:A.frame_move(B.p,(A.deg(H(C))-A.deg(I(F)))/2)
    B.p.edge()
  def pr(B):
    G(N+K(B.t),0,0)
    for C in B.o:A.print_square(C)
    A.print_square(B.p)
  def eb(A):
    for B in A.o:B.eb()
  def op(B):
    for A in B.o:
      for C in[(0,0),(0,1),(1,0),(1,1)]:
        if A.x<=B.p.x+C[0]*B.p.i<=A.x+A.i and A.y<=B.p.y+C[1]*B.p.i<=A.y+A.i:return True
    return False
class U:
  def __init__(A,x,y,s,i,c):A.x=x;A.y=y;A.s=s;A.i=i;A.c=c
  def edge(A):
    if A.x+A.i>320:A.x=320-A.i
    if A.x<0:A.x=0
    if A.y+3*A.i>240:A.y=240-3*A.i+2
    if A.y<0:A.y=0
class V:
  def __init__(A,x,y,d,s,i,c):A.x=x;A.y=y;A.d=d;A.s=s;A.i=i;A.c=c
  def eb(B):
    if B.x+B.i>=320 or B.x<=0:
      B.d=A.oppose_lat(B.d)
      if B.x<0:B.x=0
      elif B.x+B.i>320:B.x=320-B.i
    elif B.y+2*B.i>=240 or B.y<=0:
      B.d=-B.d
      if B.y<0:B.y=0
      elif B.y+B.i>240:B.y=240-B.i
class A:
  @C
  def wa(key):
    while E(key):0
    while not E(key):0
  @C
  def refresh():L(0,0,320,240,'white')
  @C
  def rad(ang):return ang*pi/180
  @C
  def deg(ang):return ang*180/pi
  @C
  def return_obstacle(dif):
    B=dif
    if B>=1:A=F(21-B,19+B)
    else:A=F(1,40)
    return V(float(F(0,320-A)),.0,F(1,179),.2+20/A,A,(222,D(126.5+15*(A-20)),31))
  @C
  def print_square(obj):A=obj;L(D(A.x),D(A.y),D(A.i),D(A.i),A.c)
  @C
  def frame_move(obj,direction):C=direction;B=obj;B.x+=cos(A.rad(C))*B.s*3;B.y+=sin(A.rad(C))*B.s*3
  @C
  def oppose_lat(ang):
    A=ang
    if A<0:return-A-180
    else:return 180-A
  @C
  def thanos(g):
    del g.p.x;del g.p.y;del g.p.s;del g.p.i;del g.p
    while len(g.o)>0:del g.o[0]
    del g.o;del g.d;del g.bd;del g.s;del g.f;del g.t;del g.td;del g
J.m(x=16e1,y=12e1,bps=1.,bi=1e1,bc=(0,0,0),bo=[],d=1,bs=1.,f=0,b=4e1)