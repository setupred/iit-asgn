import rst
from numpy import *
import numpy.linalg as la
from sklearn import svm
import utils

def Test(Data,a,res):
   return utils.TestLinear(Data,a,res)

def Learn(Data,res,iterCnt):
   Data,res = matrix(Data),matrix(res)
   Data,res = Data.tolist(),res.tolist()[0]
   Y = matrix(utils.ComputeY(Data,res))
   Yp = ((la.inv((Y.T)*Y))*(Y.T))

   res = matrix(res)

   b = matrix(ones((len(Data),1)))
   a = Yp*b

   for i in xrange(iterCnt):
      dJ = -2*(Y*a - b)
      dJneg =  (dJ-abs(dJ))/2
      b = b - dJneg
      a = Yp*b
   pred = matrix(ones(res.shape))
   pp,_np,pn,nn = 0,0,0,0
   fin = (Y*a)
   for i in xrange(Y.shape[0]):
      if(fin[i,0]>0): pred[0,i] =  res[0,i]
      else: pred[0,i] = -res[0,i]
      if(res[0,i] == pred[0,i] == 1 ): pp+=1
      elif(res[0,i] == 1 and  pred[0,i] == -1 ): pn+=1
      elif(res[0,i] == -1 and pred[0,i] == 1 ): _np+=1
      elif(res[0,i] == pred[0,i] == -1 ): nn+=1

   print pp,pn
   print _np,nn
   acc = (pp+nn*1.0)/(_np+pn+pp+nn)
   return a.tolist(),round(acc,4)


lst = [i for i in xrange(11)]
app = [i for i in xrange(20,101,10)]
lst.extend(app)
best = 0,-1
train,train_l = rst.Load('trainRST-norm.data')
test, test_l =rst.Load('testRST-norm.data')
for i in lst:
   a,accTr = Learn(list(train),list(train_l),i)
   accTs = Test(test,a,list(test_l))
   print int(i),":",accTr,accTs
   if(best[0]<accTs): best = (accTs,i)

#line sep
print ""
a,accTr = Learn(train,train_l,best[1])
print accTr,accTs

W = matrix(a[:-1])
w0 = a[-1]
d = matrix(train)
print d.shape,W.shape
pred = (d*W+w0)
print W.shape,d.shape,w0,pred.shape
pred = (pred.T).tolist()[0]
print pred
for i in xrange(len(pred)):
   if(pred[i]>=0): pred[i]=1
   else: pred[i] = -1

pr = zip(pred,train_l)
print len(pr),pr[0]
pos,neg=[],[]
D = list(train)

for i in xrange(len(pr)):
   if(pr[i] == (-1,-1)): neg.append(D[i])
   elif(pr[i] == (1,1)): pos.append(D[i])
print len(pos),len(neg),len(train_l)

p = [1 for i in xrange(len(pos))]
n = [0 for i in xrange(len(neg))]
y =  p+n
X = pos+neg
print "hello"
Learn(pos+neg,map(lambda x:2*(x-0.5),p+n),10)
clf = svm.LinearSVC()
clf.fit(X,y)
print y
#print (map(lambda x:clf.predict(x).tolist()[0],clf.support_vectors_))
#print len(clf.support_vectors_),len(y)
p = clf.predict(X).tolist()
#ts = ts.tolist()[0]
ts=list(y)

print p.count(1),p.count(0),len(p),len(ts)

z = zip(ts,p)
print p
print z.count((1,1)),z.count((1,-1)),z.count((0,1)),z.count((0,-1))
correct =  len(ts) - utils.diff(ts,p)
print "SVM",correct*1.0/len(ts)
