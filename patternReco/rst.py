import numpy as np
def M(p,q,image):
   ret = 0
   for x in xrange(8):
      for y in xrange(8):
         ret+=(x**p)*(y**q)*image[x*8 + y]
   return ret*1.0

def U(p,q,image,xMean,yMean):
   ret=0
   for x in xrange(8):
      for y in xrange(8):
         xd = x-xMean
         yd = y-yMean
         ret+=(xd**p)*(yd**q)*image[8*x + y]
   return ret*1.0
      
def N(p,q,image,xMean,yMean):
   upq = U(p,q,image,xMean,yMean)
   u00 = U(0,0,image,xMean,yMean)
   return (upq/(u00**(1+(p+q)/2.0)))

def RST(image):
   m10,m01,m00 = M(1,0,image),M(0,1,image),M(0,0,image)
   xMean,yMean = m10/m00,m01/m00
   #print "Means:",xMean,yMean
   I = [0 for i in xrange(7)]
   n = [[0 for i in xrange(4)] for j in xrange(4)]
   for i in xrange(4):
      for j in xrange(4):
         n[i][j] = N(i,j,image,xMean,yMean)
         #print i,j,n[i][j]
   
   I[0] = n[0][2] + n[2][0]
   I[1] = (n[0][2] - n[2][0])**2 + (2*n[1][1])**2
   I[2] = (n[0][3] - 3*n[2][1])**2 + (n[3][0] - 3*n[1][2])**2
   I[3] = (n[0][3] + n[2][1])**2 + (n[3][0] + n[1][2])**2

   t1 = (n[3][0] - 3*n[1][2])*(n[3][0] + n[1][2])
   t2 = (3*n[2][1] - n[0][3])*(n[0][3] + n[2][1])
   t3 = (n[3][0] + n[1][2])**2 - 3*((n[0][3] + n[2][1])**2)
   t4 = 3*((n[3][0] + n[1][2])**2) - (n[0][3] + n[2][1])**2
   I[4] = t1*t3 + t2*t4

   t1 = (n[3][0] + n[1][2])**2 - (n[0][3] + n[2][1])**2 
   t2 =  4*n[1][1]*(n[3][0] + n[1][2])*(n[0][3] + n[2][1])
   I[5] = (n[2][0] - n[0][2])*(t1+t2)

   t1 = (-n[0][3] + 3*n[2][1])*(n[3][0] + n[1][2])
   t2 = (-3*n[1][2] + n[0][3])*(n[0][3] + n[2][1])
   t3 = (n[3][0] + n[1][2])**2 - 3*((n[0][3] + n[2][1])**2)
   t4 = 3*((n[3][0] + n[1][2])**2) - (n[0][3] + n[2][1])**2
   I[6] = t1*t3 + t2*t4
   
   return I

def run():
   sumArr = np.array([0.0 for i in xrange(7)])
   cnt = 0
   for line in open('optdigits.tra'):
      img = RST(map(int,line.split(','))[:-1])
      sumArr+= np.array(img)
      cnt+=1 
   avg = sumArr/cnt
   print avg

def conv(num):
   if(num==1): return 1
   else: return -1
def DataMatrix():
   ret  = []
   res = []
   cnt = 0
   for line in open('optdigits.tra'):
      img = map(int,line.split(','))
      if(img[-1]!=1 and img[-1]!=7): continue
      res.append(conv(img[-1]))
      img = RST(img[:-1])
      ret.append(img)
   return (np.matrix(ret),np.matrix(res))

def TestData():
   ret  = []
   res = []
   cnt = 0
   for line in open('optdigits.tes'):
      img = map(int,line.split(','))
      if(img[-1]!=1 and img[-1]!=7): continue
      res.append(conv(img[-1]))
      img = RST(img[:-1])
      ret.append(img)
   return (np.matrix(ret),np.matrix(res))
