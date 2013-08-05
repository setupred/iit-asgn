from collections import  defaultdict
from sklearn import  tree
import csv

'''
An attempt to learn a decision tree regressor for each user
Resulted in run time error (may be it is consuming resources beyond what is permitted)
'''

def prob(pos,neg):
	if( (pos+neg) == 0):
		return -1
	else : return (pos*1.0)/(pos+neg)

#'''
train = csv.reader(open(sys.argv[1],'r'))
test = csv.reader(open(sys.argv[2],'r'))
final = open('result','w')

'''
train = csv.reader(open('tr.csv','r'))
test = csv.reader(open('ts.csv','r'))
final = open('result','w')
'''

ques_ind = 4
track_ind = 6
subtrack_ind = 7
game_ind = 13


X_user = defaultdict(lambda:[])
y_user = defaultdict(lambda:[])



for line in train:
	if(line[0]=='correct' or line[1] == '3' or line[1] == '4' ): continue
	res = int(line[0])
	user = int(line[2])
	st = int(line[subtrack_ind])
	t = int(line[track_ind])
	q = int(line[ques_ind])
	g= int(line[subtrack_ind])
	
	X_user[user].append([st,t,q,g])
	y_user[user].append(res)
	


classfiers = {}
print "date ready"
for user,y in y_user.iteritems():
	X = X_user[user]
	clf = tree.DecisionTreeRegressor()
	clf = clf.fit(X,y)	
	classfiers[user]=clf
	
ques_ind = 2
track_ind = 4
subtrack_ind = 5
game_ind = 11

print "training vover"

for line in test:
	if(line[0]=='user_id' ): continue
	user = int(line[0])
	
	st = int(line[subtrack_ind])
	t = int(line[track_ind])
	q = int(line[ques_ind])
	g= (line[subtrack_ind])
	final.write(str(user)+","+str(classfiers[user].predict([st,t,q,g])[0])+"\n")


final.close()

print "end"
