#!/usr/bin/python3

import cv2
import numpy as np

FRMX=200
FRMY=200

frate=15.0
codec=cv2.VideoWriter_fourcc(*'mp4v')
ofile='./line.mp4'
wt=cv2.VideoWriter(ofile,codec,frate,(FRMX,FRMY))

X=0
Y=1
Z=2

BX=40
BY=40
BZ=40
LX=50
LY=50
LZ=50

COLOR=(128,0,100)

p = np.array(
    [[BX+LX, BY+LY, BZ+LZ],
    [BX, BY+LY, BZ+LZ],
    [BX, BY, BZ+LZ],
    [BX+LX, BY, BZ+LZ],
    [BX+LX, BY+LY, BZ],
    [BX, BY+LY, BZ],
    [BX, BY, BZ],
    [BX+LX, BY, BZ]])

s = np.array([150,150,300])


def calc_line(p, s):
    b=np.zeros((8,2),np.int)
    b[:,X]=p[:,X]+(s[X]-p[:,X])*(100-p[:,Z])/(s[Z]-p[:,Z])
    b[:,Y]=200-(p[:,Y]+(s[Y]-p[:,Y])*(100-p[:,Z])/(s[Z]-p[:,Z]))
    return b


#img=np.zeros((200,200,3), np.uint8)

def dispBox(lp):
    img=np.zeros((FRMX,FRMY,3), np.uint8)
    for i in range(4):
        cv2.line(img,(lp[i,X],lp[i,Y]),(lp[((i+1) % 4),X],lp[((i+1) % 4),Y]),COLOR,2)
        cv2.line(img,(lp[(i+4),X],lp[(i+4),Y]),(lp[(((i+1) % 4)+4),X],lp[(((i+1) % 4)+4),Y]),COLOR,2)
        cv2.line(img,(lp[i][X],lp[i][Y]),(lp[i+4][X],lp[i+4][Y]),COLOR,2)
    return img

R=20

for i in np.arange(0.0,4*np.pi,0.05):
    dx=R+R*np.sin(i)
    dz=R+R*np.cos(i)
    pn=p+[dx, 0, dz]
    lp=calc_line(pn,s)
    img=dispBox(lp)
    wt.write(img)
    cv2.imshow('Test img',img)
    cv2.waitKey(100)

wt.release()
#cv2.imshow('Test img',img)
#cv2.waitKey()
cv2.destroyAllWindows()

