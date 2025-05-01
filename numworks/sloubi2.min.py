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
from random import randint as ma
from time import sleep
from kandinsky import fill_rect as mb, draw_string as mc
from ion import keydown as k
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
	def __init__(_,x,y):_.x=x;_.y=y
class CB(CA):
	def __init__(_,x,y,g,i=_A,j=_A,l=_A,m=_A):super().__init__(x,y);_.g=g;_.i=i;_.j=j;_.l=l;_.m=m
class CC(CB):
	def __init__(_,x,y,n,r,s,o,g,i=_A,j=_A,l=_A,m=_A):super().__init__(x,y,g,i,j,l,m);_.n=n;_.r=r;_.s=s;_.o=o
	def fa(_):
		if d==_.g:mb(_.x-R,_.y-R,_.n+2*R,_.r+2*R,(29,98,181))
		v=_F
		def fb():return type(_.o)==bool
		if fb()and _.o:v=29,181,103
		mb(_.x,_.y,_.n,_.r,v);mc(_.s,round(_.x+.5*_.n-5*len(_.s)),round(_.y+.5*_.r-9),_C,_F)
	def fc(_):
		ba=type(_.o)
		if ba==int:return _D
		elif ba==bool:_.o=not _.o
		else:_.o()
		return _B
class CD(CB):
	def __init__(_,x,y,n,h,q,g,i=_A,j=_A,l=_A,m=_A):super().__init__(x,y,g,i,j,l,m);_.n=n;_.h=h;_.q=q
	def fa(_,bb=X):
		mb(_.x,_.y-round(U/2),_.n,U,_F)
		if d==_.g:mb(V+_.x+round(_.q*(_.n-2*V)/(_.h-1))-round(S/2)-R,_.y-R-round(T/2),S+2*R,T+2*R,bb)
		mb(V+_.x+round(_.q*(_.n-2*V)/(_.h-1))-round(S/2),_.y-round(T/2),S,T,(127,127,127))
	def t(_,bb):mb(_.x,_.y-R-round(T/2),_.n,T+2*R,_C);_.fa(bb)
	def fc(_):
		_.t(Y)
		while k(4):0
		while not k(4):
			if k(0)and _.q>0:_.q-=1;_.t(Y);ge(0)
			if k(3)and _.q<_.h-1:_.q+=1;_.t(Y);ge(3)
		while k(4):0
class CE(CA):
	def __init__(_,x,y,bc,bd,be=_A,v='black',bf=_C):super().__init__(x,y);_.bc=bc;_.bd=bd;_.be=be;_.v=v;_.bf=bf
	def fa(_):
		if type(_.bd)==str:bg=_.bd
		else:bg=_.bd(_.be)
		y=_.y
		while len(bg)*Z>_.bc:
			g=round(_.bc/Z)
			while bg[g]!=' ':g-=1
			mc(bg[0:g],_.x,y,_.v,_.bf);bg=bg[g+1:];y+=18
		mc(bg,_.x,y,_.v,_.bf)
class CF:
	def __init__(_,x,y):_.x=x;_.y=y
class CI(CF):
	def __init__(_,x,y,p,h,v):super().__init__(x,y);_.p=p;_.h=h;_.v=v
	def fd(_):
		if _.x+_.h>M:_.x=M-_.h
		if _.x<0:_.x=0
		if _.y+_.h>N:_.y=N-_.h
		if _.y<0:_.y=0
class CG(CF):
	def __init__(_,x,y,bh,p,h,v):super().__init__(x,y);_.bh=bh;_.p=p;_.h=h;_.v=v
	def fe(_):
		if _.x+_.h>=M or _.x<=0:
			_.bh=gj(_.bh)
			if _.x<0:_.x=0
			elif _.x+_.h>M:_.x=M-_.h
		elif _.y+_.h>=N or _.y<=0:
			_.bh=-_.bh
			if _.y<0:_.y=0
			elif _.y+_.h>N:_.y=N-_.h
class CH:
	def __init__(_,w,bi,bj,bk,dt,p,bl):_.w=w;_.bi=bi;_.bj=bj;_.ma=bj;_.bk=bk;_.dt=dt;_.p=p;_.bl=bl
	def ff(_):
		for z in _.bi:gc(z,z.bh,_.dt,_.p)
		bm=int(k(3))-int(k(0));bn=int(k(2))-int(k(1))
		if not(bm==0 and bn==0):
			if bm==0:gc(_.w,gi(asin(bn)),_.dt,_.p)
			elif bn==0:gc(_.w,gi(acos(bm)),_.dt,_.p)
			elif bn==1:gc(_.w,(gi(asin(bn))+gi(acos(bm)))/2,_.dt,_.p)
			else:gc(_.w,(gi(asin(bn))-gi(acos(bm)))/2,_.dt,_.p)
		_.w.fd()
	def fg(_):
		mc(_R+str(round(_.bl)),0,0)
		for z in _.bi:gb(z)
		gb(_.w)
	def fh(_):
		for z in _.bi:z.fe()
	def fi(_):
		for z in _.bi:
			for bo in[(0,0),(0,1),(1,0),(1,1)]:
				if z.x<=_.w.x+bo[0]*_.w.h<=z.x+z.h and z.y<=_.w.y+bo[1]*_.w.h<=z.y+z.h:return _D
		return _B
	def fj(_):
		_.fh();_.ff();_.bl+=_.dt*30
		if _.bl/_.bj>240:_.bj+=1;_.bi.append(gk(_.bj+1))
		sleep(_.dt)
	def fk(_):
		t();_.fg()
		sleep(1/_.bk)
	def fl(_):t();mc('GAME OVER',112,70);mc(_R+str(round(_.bl)),105,90);mc('Difficulté initiale : '+str(_.ma),45,110);gd(4)
def fm():
	global d,b,c;b=_D;d=0;c=0
	while b:
		fu(MZ[c])
		if k(37):b=_B
	quit()
def fn():
	global e,f;f=_B
	while not e.fi():e.fj();e.fk()
	f=_D
def fo():global b;b=_B
def fp(**u):
	global e,f
	if len(u)==0:e=fs()
	else:e=fs(**u)
	fn();e.fl();gl(e)
def fq():fp(ae=A,ad=B,ac=C*fw(MB[2]),ab=fx(MB[3]),aa=E,af=F,ag=fv(MB[0]),ah=J,ak=fw(MB[1]),ai=H,aj=I)
def fr(**u):return CH(w=CI(x=u[_G],y=u[_H],p=u[_I],
	h=u[_J],v=u[_K]),bi=u[_L],bj=u[_M],dt=u[_N],
	p=u[_Q],bl=u[_O],bk=u[_P])
def fs(**u):
	if len(u)==0:bp=fr(**L)
	else:bp=fr(**u)
	dif=[0,0];dif.extend(range(bp.bj))
	for elt in dif:bp.bi.append(gk(elt+1))
	return bp
def ft(bq):
	t()
	for br in bq:br.fa()
def fu(a):
	global d,c;ft(a)
	while not k(4):
		if k(1)and a[d].l is not _A:d=a[d].l;ft(a);ge(1)
		if k(2)and a[d].m is not _A:d=a[d].m;ft(a);ge(2)
		if k(0)and a[d].i is not _A:d=a[d].i;ft(a);ge(0)
		if k(3)and a[d].j is not _A:d=a[d].j;ft(a);ge(3)
	if a[d].fc():c=a[d].o;d=0
	while k(4):0
def fv(a):return a.q+1
def fw(a):return(a.q+2)/6.
def fx(a):return(a.q+1)*2
def fy(a):return str(fv(a))
def fz(a):return('x'+str(fw(a)))[:5]
def ga(a):return str(fx(a))+'px'
def gb(a):mb(int(a.x),int(a.y),int(a.h),int(a.h),a.v)
def gc(a,b,dt,bs):a.x+=cos(gh(b))*a.p*dt*bs*W;a.y+=sin(gh(b))*a.p*dt*bs*W
def gd(a):
	while k(a):0
	while not k(a):0
def ge(a):
	while k(a):0
def t():mb(0,0,320,240,_C)
def gf(a,b=0):
	if a<b:return b
	return a
def gg(a,b):
	if a>b:return b
	return a
def gh(a):return a*pi/180
def gi(a):return a*180/pi
def gj(a):
	if a<0:return-a-180
	else:return 180-a
def gk(a):
	if a>=20:bt=ma(1,40)
	else:bt=ma(21-a,19+a)
	return CG(float(ma(0,320-bt)),.0,ma(1,179),.2+40/bt,bt,(222,int(126.5+15*(bt-20)),31))
def gl(a):
	if type(a)==list:
		while len(a)>0:del a[0]
	else:del a.w.x;del a.w.y;del a.w.p;del a.w.h;del a.w;gl(a.bi);del a.bi;del a.bj;del a.ma;del a.bk;del a.dt;del a.bl;del a
MA=[CC(Q,80,O,P,'Jouer',fp,0,m=1),CC(Q,125,O,P,'Partie personnalisée',1,1,l=0,m=2),CC(Q,170,round(O/2-5),P,'Quitter',fo,2,
	j=3,l=1),CC(round(M/2+5),170,round(O/2-5),P,'Infos',2,3,2,l=1),CE(120,30,320,'SLOUBI 2')]
MB=[CD(round(M/2)+4,20,100,10,0,0,m=1),CD(round(M/2)+4,60,100,11,4,1,l=0,m=2),CD(round(M/2)+4,100,100,11,4,2,
	l=1,m=3),CD(round(M/2)+4,140,100,15,4,3,l=2,m=5),CC(4,N-P-4,70,P,_E,0,4,
	l=3,
	j=5),CC(245,N-P-4,70,P,'Jouer',fq,5,l=3,
	i=4),CE(0,10,M,'Diff. de base :'),CE(0,50,M,'Vit. du jeu :'),CE(0,90,M,'Vit. du joueur :'),CE(0,130,M,'Taille joueur :')]
MB.extend([CE(round(M/2)+108,10,50,fy,MB[0]),CE(round(M/2)+108,50,50,fz,MB[1]),CE(round(M/2)+108,90,50,fz,MB[2]),CE(round(M/2)+108,130,50,ga,MB[3])])
MC=[CC(Q,48,O,P,'Comment jouer',3,0,m=1),CC(Q,93,O,P,'Crédits',4,1,l=0,m=2),CC(Q,138,O,P,_E,0,2,
	l=1)]
MD=[CC(4,N-P-4,70,P,_E,2,0),CE(4,4,312,"Vous dirigez un petit carré. Le but est d'éviter les autres carrés (oranges, rouges et jaunes) qui bougent sur l'écran. Les seules commandes sont les flèches directionnelles avec lesquelles vous déplacez le carré.")]
ME=[CC(4,N-P-4,70,P,_E,2,0),CE(4,4,312,'Jeu créé par Eddy F. et inspiré par la documentation de Godot'),CE(4,76,312,"Merci à Lucas P. pour l'idée d'avoir des carrés de taille et vitesse différentes")]
MZ=[MA,MB,MC,MD,ME]
fm()