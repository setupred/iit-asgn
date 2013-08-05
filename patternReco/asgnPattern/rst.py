from sklearn.decomposition import PCA
import numpy as np
import numpy.linalg as la
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
   if(p+q<2): return 0
   upq = U(p,q,image,xMean,yMean)
   u00 = U(0,0,image,xMean,yMean)
   
   #print p,q,":",upq,u00,M(0,0,image)
   return (upq/(u00**(1+(p+q)/2.0)))

def RST(image):
   m10,m01,m00 = M(1,0,image),M(0,1,image),M(0,0,image)
   xMean,yMean = m10/m00,m01/m00
   #print "Means:",xMean,yMean
   I = [0 for i in xrange(7)]
   n = [[0 for i in xrange(4)] for j in xrange(4)]
   for i in xrange(4):
      for j in xrange(4):
         n[i][j] = round(N(i,j,image,xMean,yMean),10)
         #print i,j,n[i][j]
   #print n
   
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

def normalize(data):
   data =  np.matrix(data)
   mean = map(np.mean,data.T)
   var = map(np.var,data.T)
   return ((data-mean)/var).tolist(),mean,var

def normalizemv(data,mean,var):
   data =  np.matrix(data)
   return ((data-mean)/var).tolist()
classes = (4,6)

def conv(num):
   if(num==classes[0]): return 1
   else: return -1

def varF(m1,m2):
   print m1.shape,m2.shape
   num,den=0.0,0.0
   for i in xrange(len(m1)):
      num+= np.dot(m1[i].tolist()[0],m1[i].tolist()[0])
      den+= np.dot(m2[i].tolist()[0],m2[i].tolist()[0])
   return num/den


def lst2str(lst):
   return str(lst).replace(',','')[1:-1]
   
def convertToRST(inp,out):
   res = []
   cnt = 0
   base = []
   wrFile = open(out,'w')
   for line in open(inp,'r'):
      img = map(int,line.split(','))
      
      if(img[-1]!=classes[1] and img[-1]!=classes[0]): continue

      imgt = RST(img[:-1])
      wrFile.write(lst2str(imgt)+":"+str(conv(img[-1]))+"\n")
   wrFile.close()

def normalizeTrain(inp,out,mv):
   data = []
   val =  []
   for line in open(inp):
      split = line.split(':')
      data.append(map(float,split[0].split(' ')))
      val.append(int(split[1]))
      
   data,me,va = normalize(data)
   mvf = open(mv,'w')
   mvf.write(lst2str(me)+"\n")
   mvf.write(lst2str(va)+"\n")
   mvf.close()
   outf = open(out,'w')
   for i in xrange(len(data)):
      outf.write(lst2str(data[i])+":"+str(val[i])+"\n")
   
def normalizeTest(mv,inp,out):
   data = []
   val =  []
   for line in open(inp):
      split = line.split(':')
      data.append(map(float,split[0].split(' ')))
      val.append(int(split[1]))
   mvf = open(mv,'r')
   me = map(float,mvf.readline().split(' '))
   va = map(float,mvf.readline().split(' '))
   mvf.close()
   data = normalizemv(data,me,va)
   
   
   outf = open(out,'w')
   for i in xrange(len(data)):
      outf.write(lst2str(data[i])+":"+str(val[i])+"\n")


def Load(inp):
   retX,rety = [],[]
   for line in open(inp):
      split = line.split(':')
      retX.append(map(float,split[0].split(' ')))
      rety.append(int(split[1]))
   return retX,rety

convertToRST('optdigits.tra','trainRST.data')
convertToRST('optdigits.tes','testRST.data')

normalizeTrain('testRST.data','testRST-norm.data','mv.data')
normalizeTest('mv.data','trainRST.data','trainRST-norm.data')




         

