'''
train data
	+/tot for each user for math
	+/tot for each user for eng
	+/tot for each tag
	+/tot for each game
	+/tot for each question_type
	+/tot for each subtrack
'''

from time import gmtime, strftime
from collections import  defaultdict
from sklearn import linear_model as lm
from math import exp
import csv

def prob(pos,neg):
	if( (pos+neg) == 0):
		return -1
	else : return (pos*1.0)/(pos+neg)

def sigmoid(num):
	return exp(num)/(1+exp(num))
#'''
train = csv.reader(open(sys.argv[1],'r'))
test = csv.reader(open(sys.argv[2],'r'))


'''
train = csv.reader(open('dummy_data/tr.csv','r'))
test = csv.reader(open('dummy_data/ts.csv','r'))
'''

'''
track_name,ACT English,0
track_name,ACT Math,1
track_name,ACT Reading,2
track_name,ACT Science,3


track_name,GMAT Quantitative,4
track_name,GMAT Verbal,5

track_name,SAT Math,6
track_name,SAT Reading,7
track_name,SAT Writing,8
'''

eng_math={}
eng_math[0]=1
eng_math[1]=0
eng_math[2]=1
eng_math[3]=0

eng_math[4]=0
eng_math[5]=1

eng_math[6]=0
eng_math[7]=1
eng_math[8]=1


ques_ind = 4
track_ind = 6
subtrack_ind = 7
game_ind = 13


X = []
y = []

user_tot = defaultdict(lambda:0)
user_pos = defaultdict(lambda:0)
for line in train:
	if(line[0]=='correct' or line[1] == '3' or line[1] == '4' ): continue
	res = int(line[0])
	user = int(line[2])
	t = int(line[track_ind])

	pres = [user,user,user,user,0,0]
	pres[4]=eng_math[t]
	pres[5]=int(line[ques_ind])
	X.append(pres)
	y.append(res)
	user_tot[user,eng_math[t]]+=1
	user_pos[user,eng_math[t]]+=res


for i in xrange(len(X)):
	user = X[i][0]
	if((user_tot[user,0])==0 or (user_tot[user,1])==0):
		X[i][0] = (user_pos[user,0]*1.0+user_pos[user,1])/(user_tot[user,0]+user_tot[user,1])
		X[i][1] = X[i][0]
	else:
		X[i][0] = (user_pos[user,0]*1.0)/(user_tot[user,0])
		X[i][1] = (user_pos[user,1]*1.0)/(user_tot[user,1])
	X[i][2]=X[i][0]*X[i][0]
	X[i][3]=X[i][1]*X[i][1]
print "data ready"
clf = lm.LinearRegression()
clf = clf.fit(X,y)
print "training done"


ques_ind = 2
track_ind = 4
subtrack_ind = 5
game_ind = 11

final = open('result','w')
for line in test:
	if(line[0]=='user_id' ): continue
	user = int(line[0])	
	t = int(line[track_ind])
	pres = [0,0,0,0,0,0]
	if((user_tot[user,0])==0 or (user_tot[user,1])==0):
		pres[0] = (user_pos[user,0]*1.0+user_pos[user,1])/(user_tot[user,0]+user_tot[user,1])
		pres[1] = pres[0]
	else:
		pres[0] = (user_pos[user,0]*1.0)/(user_tot[user,0])
		pres[1] = (user_pos[user,1]*1.0)/(user_tot[user,1])
	
	pres[2]=pres[0]*pres[0]
	pres[3]=pres[1]*pres[1]
	pres[4]=eng_math[t]
	pres[5]=int(line[ques_ind])
	final.write(str(user)+","+str(sigmoid(clf.predict(pres)))+"\n")

final.close()
print "end"
