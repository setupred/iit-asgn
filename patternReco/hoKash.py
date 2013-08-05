import rst
from numpy import *
import numpy.linalg as la

def Learn(Data,res,iterCnt):
   Y = ComputeY(Data,res)
   Yp = ((la.inv((Y.T)*Y))*(Y.T))
   #print Yp
   
   b = matrix(ones((len(Data),1)))
   a = Yp*b
   
   for i in xrange(iterCnt):
      dJ = -2*(Y*a - b)
      dJneg =  (dJ-abs(dJ))/2
      b = b - dJneg
      a = Yp*b
   pred = matrix(ones(res.shape))
   pp,np,pn,nn = 0,0,0,0
   fin = (Y*a)
   for i in xrange(Y.shape[0]):
      if(fin[i,0]>0): pred[0,i] =  res[0,i]
      else: pred[0,i] = -res[0,i]
      if(res[0,i] == pred[0,i] == 1 ): pp+=1
      elif(res[0,i] == 1 and  pred[0,i] == -1 ): pn+=1
      elif(res[0,i] == -1 and pred[0,i] == 1 ): np+=1
      elif(res[0,i] == pred[0,i] == -1 ): nn+=1   
   
   
   #print pp,pn
   #print np,nn
   acc = (pp+nn*1.0)/(np+pn+pp+nn)
   return a,round(acc,4)
def ComputeY(Data,res):
   ret = Data.tolist()
   for i in xrange(len(ret)):
      ret[i].append(1)
   ret = matrix(ret)
   for i in xrange(len(ret)):
      ret[i] = res[0,i]*ret[i] 
   #print ret
   #
   return ret


def Test(Data,a,res):
   W = a[:-1,:]
   w0 = a[-1,0]
   #print Data.shape
   #print W.shape,a.shape
   Pred = (Data*W) + w0
   delta = 0.00001
   for i in xrange(len(Pred)):
      if(Pred[i,0]>=0): Pred[i,0]=1
      else: Pred[i,0] = -1

   Pred = (Pred.T).tolist()[0]
   res = res.tolist()[0]
   pr = zip(Pred,res)
   #print Pred
   #print res
   
   pp,np,pn,nn = 0,0,0,0
   for i in pr:
      if(i==(1,1)): pp+=1
      elif(i==(1,-1)): pn+=1
      elif(i==(-1,1)): np+=1
      elif(i==(-1,-1)): nn+=1
   
   #print pp,pn
   #print np,nn
   acc = (pp+nn*1.0)/(np+pn+pp+nn)
   return round(acc,4)

d,r = rst.DataMatrix()
td,ts = rst.TestData()
lst = [i for i in xrange(11)]
app = [i for i in xrange(20,101,10)]
lst.extend(app)
for i in lst:
   a,accTr = Learn(d,r,i)
   accTs = Test(td,a,ts)
   print int(i),":",accTr,accTs
