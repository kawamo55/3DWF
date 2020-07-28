#!/usr/bin/python3
# in Debian Linux Buster
# 3 dimension wire frame write program
# With mp4 video
# Programed by M.kawase 
# Embed AI Laboratory Inc.

import cv2
import numpy as np

# frame rate
frate=10.0
codec=cv2.VideoWriter_fourcc(*'mp4v')
ofile='./line.mp4'

# 軸の定義
X=0
Y=1
Z=2

# 視点から見た箱の左下座標
BX=10
BY=50
BZ=10

# 箱の軸方向長さ
LX=50
LY=50
LZ=50

# image size
IMX = 200
IMY = 200
wt=cv2.VideoWriter(ofile,codec,frate,(IMX,IMY))

# Screen Position (Z軸位置)
SCP=100

# 箱の３Dデータ
p = np.array(
    [[BX+LX, BY+LY, BZ+LZ],
    [BX, BY+LY, BZ+LZ],
    [BX, BY, BZ+LZ],
    [BX+LX, BY, BZ+LZ],
    [BX+LX, BY+LY, BZ],
    [BX, BY+LY, BZ],
    [BX, BY, BZ],
    [BX+LX, BY, BZ]])


# ワイヤーフレームの頂点計算関数
def calc_line(p, s):
    b=np.zeros((8,2),np.int)
    b[:,X]=p[:,X]+(s[X]-p[:,X])*(SCP-p[:,Z])/(s[Z]-p[:,Z])
    b[:,Y]=IMY-(p[:,Y]+(s[Y]-p[:,Y])*(SCP-p[:,Z])/(s[Z]-p[:,Z]))
    return b

# 描画
def dispLines(lp,color):
    img=np.zeros((IMX,IMY,3), np.uint8)
    for i in range(4):
        cv2.line(img,(lp[i,X],lp[i,Y]),
            (lp[((i+1) % 4),X],lp[((i+1) % 4),Y]),color,2)
        cv2.line(img,(lp[(i+4),X],lp[(i+4),Y]),
            (lp[(((i+1) % 4)+4),X],lp[(((i+1) % 4)+4),Y]),color,2)
        cv2.line(img,(lp[i][X],lp[i][Y]),
            (lp[i+4][X],lp[i+4][Y]),color,2)
    return img

# この部分で物体の位置や視点を変えると
# いろんな画像を作れます。
# 視点の位置を変える(xを200->260 step3)
for x in range(200,261,3):
    #             x   y   z
    s = np.array([x  ,130,200]) # 視点
    lp=calc_line(p,s)           # 結果を得る
    #   COLOR 0-255   B   G   R
    img=dispLines(lp,(255,  0,128))
    cv2.imshow('Test img',img)
    wt.write(img)
    cv2.waitKey(100)
cv2.destroyAllWindows()

