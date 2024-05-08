#!/bin/env python
from math import cos,sin,asin,acos,pi
from random import randint
from time import sleep
from ion import keydown,KEY_RIGHT,KEY_LEFT,KEY_UP,KEY_DOWN,KEY_OK
from kandinsky import fill_rect,draw_string
S=staticmethod
class M:
 @S
 def m(**kw):
  while True:
   M.g(**kw)
   U.th(_g)
 @S
 def g(**kw):
  global _g
  _g=G(p=P(x=kw["x"],y=kw["y"],s=kw["bps"],i=kw["bi"],c=kw["bc"]),o=kw["bo"],d=kw["d"],s=kw["bs"],t=kw["f"],f=kw["b"])
  for i in range(2):_g.o.append(U.ro(1))
  for dif in range(_g.d):_g.o.append(U.ro(dif + 1))
  while not _g.op():M.l()
  U.re()
  draw_string("GAME OVER",112,70)
  draw_string("Score : "+str(_g.t),105, 90)
  draw_string("Difficulté initiale : "+str(_g.bd),45,110)
  U.wa(KEY_OK)
 @S
 def l():
  _g.eb();_g.fm();_g.t+=1
  if _g.t%240==0:
   _g.d+=1
   _g.o.append(U.ro(_g.d + 1))
  U.re();_g.pr();sleep(_g.td)
class G:
 def __init__(e,p,o,d,s,f,t):
  e.p=p;e.o=o;e.d=d;e.bd=d;e.s=s;e.f=f;e.t=t;e.td=2.0/(f*3.0)
 def fm(e):
  for o in e.o: U.fmo(o, o.d)
  key_x=int(keydown(KEY_RIGHT))-int(keydown(KEY_LEFT))
  key_y=int(keydown(KEY_DOWN))-int(keydown(KEY_UP))
  if not(key_x==0 and key_y==0):
   if key_x==0:
    U.fmo(e.p, U.deg(asin(key_y)))
   elif key_y==0:
    U.fmo(e.p, U.deg(acos(key_x)))
   elif key_y==1:
    U.fmo(e.p, (U.deg(asin(key_y)) + U.deg(acos(key_x))) / 2)
   else:
    U.fmo(e.p, (U.deg(asin(key_y)) - U.deg(acos(key_x))) / 2)
  e.p.e()
 def pr(e):
  draw_string("Score : " + str(e.t), 0, 0)
  for obstacle in e.o:U.psq(obstacle)
  U.psq(e.p)
 def eb(e):
  for o in e.o:
   o.eb()
 def op(e):
  for o in e.o:
   for c in[(0,0),(0,1),(1,0),(1,1)]:
    if o.x<=e.p.x+c[0]*e.p.i<=o.x+o.i and o.y<=e.p.y+c[1]*e.p.i<=o.y+o.i:
     return True
  return False
class P:
 def __init__(e,x,y,s,i,c):
  e.x=x;e.y=y;e.s=s;e.i=i;e.c=c
 def e(e):
  if e.x+e.i>320:e.x=320-e.i
  if e.x<0:e.x=0
  if e.y+3*e.i>240:e.y=240-3*e.i+2
  if e.y<0:e.y=0
class O:
 def __init__(e,x,y,d,s,i,c):
  e.x=x;e.y=y;e.d=d;e.s=s;e.i=i;e.c=c
 def eb(e):
  if e.x+e.i>=320 or e.x<=0:
   e.d=U.ol(e.d)
   if e.x<0:e.x=0
   elif e.x+e.i>320:e.x=320-e.i
  elif e.y+2*e.i>=240 or e.y<=0:
   e.d=-e.d
   if e.y<0:e.y=0
   elif e.y+e.i>240:e.y=240-e.i
class U:
 @S
 def wa(key):
  while keydown(key):pass
  while not keydown(key):pass
 @S
 def re():fill_rect(0, 0, 320, 240, "white")
 @S
 def rad(ang):return(ang*pi)/180
 @S
 def deg(ang):return(ang*180)/pi
 @S
 def ro(dif):
  if dif>=1:ts=randint(21-dif,19+dif)
  else:ts=randint(1,40)
  return O(float(randint(0,320-ts)),0.0,randint(1, 179),0.2+(20/ts),ts,(222,int(126.5+15*(ts-20)),31))
 @S
 def psq(obj):fill_rect(int(obj.x), int(obj.y), int(obj.i), int(obj.i), obj.c)
 @S
 def fmo(obj,direction):
  obj.x+=cos(U.rad(direction))*obj.s*3
  obj.y+=sin(U.rad(direction))*obj.s*3
 @S
 def ol(ang):
  if ang<0:return-ang-180
  else:return 180-ang
 @S
 def th(g):
  del g.p.x;del g.p.y;del g.p.s;del g.p.i;del g.p
  while len(g.o)>0:del g.o[0]
  del g.o;del g.d;del g.bd;del g.s;del g.f;del g.t;del g.td;del g
M.m(x=160.0,y=120.0,bps=1.0,bi=10.0,bc=(0, 0, 0),bo=[],d=1,bs=1.0,f=0,b=40.0)
