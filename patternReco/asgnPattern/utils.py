from numpy import matrix,array

def diff(m1,m2):
   return (array(m1) != array(m2)).sum()

def ComputeY(Data,res):
   Data =  list(Data)
   res = list(res)
   for i in xrange(len(Data)):
      Data[i].append(1)
   ret = matrix(Data)
   for i in xrange(len(ret)):
      ret[i] = res[i]*ret[i]
   return ret.tolist()


def TestLinear(Data,a,res):
   Data = matrix(Data)
   a = matrix(a)
   res = matrix(res)

   W = a[:-1,:]
   w0 = a[-1,0]
   #print Data.shape
   #print W.shape,a.shape
   Pred = (Data*W) + w0

   for i in xrange(len(Pred)):
      if(Pred[i,0]>0): Pred[i,0]=1
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
   return [[pp,pn],[np,nn]]


def pca(Train,Test,acc):
   Train = np.matrix(Train)
   Test = np.matrix(Test)
   S = np.cov(Train.T)
   Z = la.eig(S)
   E = Z[0]
   b = sum(E)
   su,i,x =0,0,0
   while su <= acc:
      su = su+(E[x]/b)
      i+=1
      x+=1
   print Z
   print S
   return (Train*(np.matrix(E[0][:i]).T)).tolist(),(Test*(np.matrix(E[0][:i]).T)).tolist()
